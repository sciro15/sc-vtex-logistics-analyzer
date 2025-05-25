from sqlalchemy.orm import Session
from app.models import Order, Product, Warehouse, OrderItem
from datetime import datetime

def get_or_create_order(db: Session, order_id: str, invoiced_date: datetime, city: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        order = Order(id=order_id, invoiced_date=invoiced_date, city=city)
        db.add(order)
        db.commit()
        db.refresh(order)
    return order

def get_or_create_product(db: Session, product_id: str):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        product = Product(id=product_id)
        db.add(product)
        db.commit()
        db.refresh(product)
    return product

def get_or_create_warehouse(db: Session, warehouse_id: str):
    warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not warehouse:
        warehouse = Warehouse(id=warehouse_id)
        db.add(warehouse)
        db.commit()
        db.refresh(warehouse)
    return warehouse

def create_order_item(db: Session, order: Order, product: Product, warehouse: Warehouse):
    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        warehouse_id=warehouse.id
    )
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item
