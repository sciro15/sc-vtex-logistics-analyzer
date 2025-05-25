# models.py
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, declarative_base
from app.db import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)  
    invoiced_date = Column(DateTime)
    city = Column(String)

    items = relationship("OrderItem", back_populates="order")


class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True)

    items = relationship("OrderItem", back_populates="product")


class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(String, primary_key=True)

    items = relationship("OrderItem", back_populates="warehouse")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)

    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"))
    warehouse_id = Column(String, ForeignKey("warehouses.id"))

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")
    warehouse = relationship("Warehouse", back_populates="items")
