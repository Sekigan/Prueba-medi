from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import models
from datetime import datetime

class Inventory_movements:
    def create_inventory_movement(
        db: Session,
        product_id: int,
        movement_type: str,
        quantity: int,
        notes: Optional[str] = None,
        reference_id: Optional[int] = None
    ):
        product = get_product(db, product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
    
        previous_stock = product.stock
        new_stock = previous_stock + quantity
    
        if new_stock < 0:
            raise ValueError("Movement would result in negative stock")
    
        # Crear movimiento
        db_movement = models.Inventory_movement(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity,
            previous_stock=previous_stock,
            new_stock=new_stock,
            reference_id=reference_id,
            notes=notes
        )
        db.add(db_movement)
    
        # Actualizar stock del producto
        product.stock = new_stock
    
        db.commit()
        db.refresh(db_movement)
        return db_movement

    def get_product_movements(
        db: Session,
        product_id: int,
        skip: int = 0,
        limit: int = 50,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ):
        query = db.query(models.Inventory_movement).filter(
            models.Inventory_movement.product_id == product_id
        )
    
        if from_date:
            query = query.filter(models.Inventory_movement.movement_date >= from_date)
        if to_date:
            query = query.filter(models.Inventory_movement.movement_date <= to_date)
    
        return query.order_by(
            models.Inventory_movement.movement_date.desc()
        ).offset(skip).limit(limit).all()

    def get_inventory_summary(db: Session):
        products = db.query(models.Product).all()
        summary = []
    
        for product in products:
            summary.append({
                "product_id": product.product_id,
                "name": product.name,
                "current_stock": product.stock,
                "category": product.category,
                "status": "Bajo stock" if product.stock <= 5 else "Normal" if product.stock > 0 else "Agotado"
            })
    
        return summary

    def get_movements_by_type(db: Session, movement_type: str, days: int = 30):
        from datetime import timedelta
    
        cutoff_date = datetime.now() - timedelta(days=days)
    
        return db.query(models.Inventory_movement).filter(
            models.Inventory_movement.movement_type == movement_type,
            models.Inventory_movement.movement_date >= cutoff_date
        ).all()
