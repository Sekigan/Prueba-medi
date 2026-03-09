from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import models
from datetime import datetime
from entities.products import Product
class Order:
    def get_order(db: Session, order_id: int):
        return db.query(models.Order).filter(models.Order.order_id == order_id).first()

    def get_orders(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        customer_id: Optional[int] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ):
        query = db.query(models.Order)
    
        if status:
            query = query.filter(models.Order.status == status)
        if customer_id:
            query = query.filter(models.Order.customer_id == customer_id)
        if from_date:
            query = query.filter(models.Order.order_date >= from_date)
        if to_date:
            query = query.filter(models.Order.order_date <= to_date)
    
        return query.order_by(models.Order.order_date.desc()).offset(skip).limit(limit).all()

    def create_order(db: Session, customer_id: int, items: list):
        # Crear orden
        db_order = models.Order(
            customer_id=customer_id,
            status="pending"
        )
        db.add(db_order)
        db.flush()  # Para obtener order_id
    
        total = 0
        # Crear items y verificar stock
        for item in items:
            product = Product.get_product(db, item['product_id'])
            if not product:
                raise ValueError(f"Product {item['product_id']} not found")
            if product.stock < item['quantity']:
                raise ValueError(f"Insufficient stock for product {product.name}")
        
            # Crear order item
            db_item = models.Order_item(
                order_id=db_order.order_id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                unit_price=product.price
            )
            db.add(db_item)
            total += product.price * item['quantity']
    
        db_order.total = total
        db.commit()
        db.refresh(db_order)
        return db_order

    def update_order_status(db: Session, order_id: int, new_status: str):
        valid_statuses = ["pending", "confirmed", "rejected", "delivered"]
        if new_status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
    
        db_order = Order.get_order(db, order_id)
        if db_order:
            db_order.status = new_status
            db.commit()
            db.refresh(db_order)
        return db_order

    def get_customer_orders(db: Session, customer_id: int):
        return db.query(models.Order).filter(
            models.Order.customer_id == customer_id
        ).order_by(models.Order.order_date.desc()).all()

    def get_order_summary(db: Session):
        from sqlalchemy import func
    
        summary = db.query(
            models.Order.status,
            func.count(models.Order.order_id).label('count'),
            func.sum(models.Order.total).label('total_amount')
        ).group_by(models.Order.status).all()
    
        return [{"status": s, "count": c, "total": float(t or 0)} for s, c, t in summary]
