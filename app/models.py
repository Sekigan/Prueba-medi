from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    orders = relationship("Order", back_populates="customer")



class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, index=True, nullable=False)
    product_code = Column(Integer, unique=True, index=True, nullable=False)
    stock = Column(Integer, index=True)
    category = Column(String(50), index=True)
    price = Column(Numeric(10,2), nullable=False)

    order_items = relationship("Order_item", back_populates="product")
    inventory_movements = relationship("Inventory_movement", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    order_date = Column(DateTime, default=datetime.now)
    status = Column(String(25), default="pending") # Pending, Confirmed, Rejected, Delivered
    total = Column(Numeric(10, 2), default=0)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("Order_item", back_populates="order", cascade="all,delete-orphan")


class Order_item(Base):
    __tablename__ = "order_items"
    item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Inventory_movement(Base):
    __tablename__ = "inventory_movements"
    movement_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    movement_type = Column(String(20), nullable=False) #Entrada, Salida, Ajuste
    quantity = Column(Integer, nullable=False)
    previous_stock = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)

    reference_id = Column(Integer)
    movement_date = Column(DateTime, default=datetime.now)
    notes = Column(Text)

    product = relationship("Product", back_populates="inventory_movements")
