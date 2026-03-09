from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import models
from datetime import datetime
class Report():
    def get_sales_report(
        db: Session,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        group_by: str = "day"  # day, month, category
    ):
        from sqlalchemy import func, extract
    
        query = db.query(
            models.Order.order_date,
            models.Order.total,
            models.Order_item.product_id,
            models.Order_item.quantity,
            models.Product.category
        ).join(
            models.Order_item, models.Order.order_id == models.Order_item.order_id
        ).join(
            models.Product, models.Order_item.product_id == models.Product.product_id
        ).filter(
            models.Order.status == "delivered"
        )
    
        if from_date:
            query = query.filter(models.Order.order_date >= from_date)
        if to_date:
            query = query.filter(models.Order.order_date <= to_date)
    
        return query.all()

    def get_top_products(db: Session, limit: int = 10):
        from sqlalchemy import func
    
        return db.query(
            models.Product.name,
            models.Product.category,
            func.sum(models.Order_item.quantity).label('total_sold'),
            func.sum(models.Order_item.quantity * models.Order_item.unit_price).label('total_revenue')
        ).join(
            models.Order_item, models.Product.product_id == models.Order_item.product_id
        ).join(
            models.Order, models.Order_item.order_id == models.Order.order_id
        ).filter(
            models.Order.status == "delivered"
        ).group_by(
            models.Product.product_id
        ).order_by(
            func.sum(models.Order_item.quantity).desc()
        ).limit(limit).all()

    def get_customer_purchases(db: Session, customer_id: int):
        customer = get_customer(db, customer_id)
        if not customer:
            return None
    
        orders = get_customer_orders(db, customer_id)
    
        total_spent = sum(float(order.total) for order in orders if order.status == "delivered")
    
        return {
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email
            },
            "total_orders": len(orders),
            "total_spent": total_spent,
            "orders": [
                {
                    "order_id": o.order_id,
                    "date": o.order_date,
                    "status": o.status,
                    "total": float(o.total)
                } for o in orders
            ]
        }
