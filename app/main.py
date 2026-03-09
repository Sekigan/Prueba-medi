from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import db
import models

from entities.customers import Customer as customer_entity
from entities.products import Product as product_entity
from entities.orders import Order as order_entity
from entities.inventory_movements import Inventory_movements as inventory_entity
from datetime import datetime

app = FastAPI(title="API MEDIPIEL",
    description="API de PRUEBA MEDIPIEL",
    version="1.0.0")

models.Base.metadata.create_all(bind=db.engine)


@app.get("/")
def root():
    return {
        "message": "API de Prueba MEDIPIEL",
        "version": "1.0.0",
        "endpoints": {
            "customers": "/customers",
            "products": "/products",
            "orders": "/orders",
            "/inventory_movements": "/inventory_movements"
        }
    }

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#CREATE CUSTOMER
@app.post("/customers/")
def create_customer(name:str, email:str, city:str, db: Session = Depends(db.get_db)):
    # Verificar si email existe
    if customer_entity.get_customer_by_email(db, email):
        raise HTTPException(400, "Email ya existe")
    
    customer = customer_entity.create_customer(db, name, email, city)
    return customer

# GET CUSTOMER BY ID
@app.get("/customers/{id}")
def get_customer(id: int, db: Session = Depends(db.get_db)):
    c = customer_entity.get_customer(db, id)
    if not c:
        raise HTTPException(404, "No encontrado")
    return c
# GET ALL CUSTOMERS
@app.get("/customers/")
def get_customers(db: Session = Depends(db.get_db)):
    customers = db.query(models.Customer).all()
    return customers

#UPDATE CUSTOMERS
@app.put("/customers/{customer_id}")
def update_customer_simple(customer_id: int,name:str = None,email:str = None,city:str = None,db: Session = Depends(db.get_db)):
    # Verificar que existe
    customer = customer_entity.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(404, "Cliente no encontrado")
    # Verificar email si cambia
    if email and email != customer.email:
        if customer_entity.get_customer_by_email(db, email):
            raise HTTPException(400, "Email ya existe")
    # Actualizar
    updated = customer_entity.update_customer(
        db, customer_id, name, email, city
    )

    return {
        "id": updated.id,
        "name": updated.name,
        "email": updated.email,
        "city": updated.city
    }

# GET CUSTOMERS BY EMAIL
@app.get("/customers/email/{email}")
def get_customer_by_email(email: str, db: Session = Depends(db.get_db)):
    customer = customer_entity.get_customer_by_email(db, email)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente con email {email} no encontrado"
        )
    return customer

#GET CUSTOMERS BY CITY
@app.get("/customers/city/{city}")
def get_customers_by_city(city: str,db: Session = Depends(db.get_db)):
    customers = customer_entity.get_customers_by_city(db, city)
    if not customers:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron clientes en {city}"
        )
    return [c for c in customers]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# CREAR PRODUCT
@app.post("/products/")
def create_product(name: str, product_code: int, price: float, stock: int = 0, db: Session = Depends(db.get_db)):
    if product_entity.get_product_by_code(db, product_code):
        raise HTTPException(400, "Código ya existe")
    return product_entity.create_product(db, name, product_code, price, stock)

# LISTAR TODOS PRODCUT
@app.get("/products/")
def get_all_products(db: Session = Depends(db.get_db)):
    return product_entity.get_products(db)

# OBTENER POR ID PRODUCT
@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(db.get_db)):
    p = product_entity.get_product(db, id)
    if not p:
        raise HTTPException(404, "No encontrado")
    return p

# AGREGAR STOCK PRODUCT
@app.patch("/products/{id}/stock")
def update_stock(id: int, change: int, db: Session = Depends(db.get_db)):
    try:
        return product_entity.update_product_stock(db, id, change)
    except ValueError as e:
        raise HTTPException(400, str(e))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from pydantic import BaseModel
from typing import Optional, List  

# Modelos Pydantic
class ProductItem(BaseModel):
    product_id: int
    quantity: int

class OrderRequest(BaseModel):
    customer: int
    products: List[ProductItem]


@app.post("/orders/")
def create_order(order: OrderRequest, db: Session = Depends(db.get_db)):
    """Crear nueva orden"""
    # Verificar cliente
    customer = customer_entity.get_customer(db, order.customer)
    if not customer:
        raise HTTPException(404, f"Cliente {order.customer} no encontrado")
    
    # Verificar productos y stock
    for item in order.products:
        product = product_entity.get_product(db, item.product_id)
        if not product:
            raise HTTPException(404, f"Producto {item.product_id} no encontrado")
        if product.stock < item.quantity:
            raise HTTPException(400, f"Stock insuficiente para {product.name}")
    
    # Crear orden
    try:
        items_list = [{"product_id": p.product_id, "quantity": p.quantity} for p in order.products]
        new_order = order_entity.create_order(db, order.customer, items_list)
        
        # Preparar respuesta
        return {
            "message": "Orden creada",
            "order_id": new_order.order_id,
            "customer": customer.name,
            "total": float(new_order.total),
            "status": new_order.status
        }
    except ValueError as e:
        raise HTTPException(400, str(e))



# LISTAR TODAS LAS ORDENES
@app.get("/orders/")
def get_all_orders(db: Session = Depends(db.get_db)):
    return order_entity.get_orders(db)

# OBTENER ORDEN POR ID
@app.get("/orders/{id}")
def get_order(id: int, db: Session = Depends(db.get_db)):
    order = order_entity.get_order(db, id)
    if not order:
        raise HTTPException(404, "No encontrada")
    return order

# ACTUALIZAR ESTADO DE ORDEN
@app.patch("/orders/{id}/status")
def update_status(id: int, status: str, db: Session = Depends(db.get_db)):
    try:
        return order_entity.update_order_status(db, id, status)
    except ValueError as e:
        raise HTTPException(400, str(e))

# ORDENES POR CLIENTE
@app.get("/orders/customer/{customer_id}")
def customer_orders(customer_id: int, db: Session = Depends(db.get_db)): 
    return order_entity.get_customer_orders(db, customer_id)
