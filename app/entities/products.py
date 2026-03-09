from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import models


class Product:
    def get_product(db: Session, product_id: int):
        return db.query(models.Product).filter(models.Product.product_id == product_id).first()

    def get_product_by_code(db: Session, product_code: int):
        return db.query(models.Product).filter(models.Product.product_code == product_code).first()

    def get_products(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock_only: bool = False
    ):
        query = db.query(models.Product)
    
        if category:
            query = query.filter(models.Product.category == category)
        if min_price:
            query = query.filter(models.Product.price >= min_price)
        if max_price:
            query = query.filter(models.Product.price <= max_price)
        if in_stock_only:
            query = query.filter(models.Product.stock > 0)
    
        return query.offset(skip).limit(limit).all()

    def create_product(
        db: Session,
        name: str,
        product_code: int,
        price: float,
        stock: int = 0,
        category: Optional[str] = None
    ):
        db_product = models.Product(
            name=name,
            product_code=product_code,
            price=price,
            stock=stock,
            category=category
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update_product_stock(db: Session, product_id: int, quantity_change: int):
        db_product = Product.get_product(db, product_id)
        if db_product:
            new_stock = db_product.stock + quantity_change
            if new_stock < 0:
                raise ValueError("Insufficient stock")
            db_product.stock = new_stock
            db.commit()
            db.refresh(db_product)
        return db_product

    def get_low_stock_products(db: Session, threshold: int = 5):
        return db.query(models.Product).filter(models.Product.stock <= threshold).all()

    def get_products_by_category(db: Session, category: str):
        return db.query(models.Product).filter(models.Product.category == category).all()
