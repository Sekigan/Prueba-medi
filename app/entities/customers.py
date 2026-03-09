from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import models

class Customer:

    def get_customer(db: Session, customer_id: int):
        return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

    def get_customer_by_email(db: Session, email: str):
        return db.query(models.Customer).filter(models.Customer.email == email).first()

    def get_customers(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ):
        query = db.query(models.Customer)
    
        if search:
            query = query.filter(
                or_(
                    models.Customer.name.ilike(f"%{search}%"),
                    models.Customer.email.ilike(f"%{search}%"),
                    models.Customer.city.ilike(f"%{search}%")
                )
            )
    
        return query.offset(skip).limit(limit).all()

    def create_customer(db: Session, name: str, email: str, city: str):
        db_customer = models.Customer(
            name=name,
            email=email,
            city=city
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer

    def update_customer(
        db: Session, 
        customer_id: int, 
        name: Optional[str] = None,
        email: Optional[str] = None,
        city: Optional[str] = None
    ):
        db_customer = Customer.get_customer(db, customer_id)
        if db_customer:
            if name:
                db_customer.name = name
            if email:
                db_customer.email = email
            if city:
                db_customer.city = city
            db.commit()
            db.refresh(db_customer)
        return db_customer

    def delete_customer(db: Session, customer_id: int):
        db_customer = Customer.get_customer(db, customer_id)
        if db_customer:
            # Verificar si tiene órdenes
            if db_customer.orders:
                raise ValueError("Cannot delete customer with existing orders")
            db.delete(db_customer)
            db.commit()
            return True
        return False

    def get_customers_by_city(db: Session, city: str):
        return db.query(models.Customer).filter(models.Customer.city == city).all()
