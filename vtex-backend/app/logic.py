import os
from datetime import datetime
from app.db import SessionLocal
from app.models import Order, OrderItem
from app.crud import get_or_create_order, get_or_create_product, get_or_create_warehouse, create_order_item

def obtener_detalle_orden(order_id, data):
    detalle = next(
        (entry["orden"] for entry in data if entry.get("orden", {}).get("orderId") == order_id),
        None
    )
    if detalle is None:
        raise ValueError(f"No se encontró detalle para orderId {order_id}")
    return detalle

def sincronizar_ordenes(ordenes):
    db = SessionLocal()
    try:
        for item in ordenes:
            orden = item.get("orden")
            if not orden:
                print("Orden no encontrada en el item:", item)
                continue

            order_id = orden.get("orderId")
            if not order_id:
                print("orderId no encontrado en la orden:", orden)
                continue

            detalle = obtener_detalle_orden(order_id, ordenes)

            invoiced_date_str = detalle.get("invoicedDate")
            invoiced_date = None
            if invoiced_date_str:
                invoiced_date = datetime.fromisoformat(invoiced_date_str.replace("Z", "+00:00"))

            shipping_city = detalle.get("shippingData", {}).get("city")

            # Crear o conseguir la orden en la DB
            order = get_or_create_order(db, order_id, invoiced_date, shipping_city)

            for item in detalle.get("items", []):
                product_id = item.get("id")
                product = get_or_create_product(db, product_id)

                for logistics in detalle.get("logisticsInfo", []):
                    warehouse_id = logistics.get("matchedWarehouseId")
                    if warehouse_id:
                        warehouse = get_or_create_warehouse(db, warehouse_id)
                        create_order_item(db, order, product, warehouse)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error en sincronizar_ordenes: {e}")
        raise e
    finally:
        db.close()

# Las demás funciones quedan igual
def productos_por_almacen():
    db = SessionLocal()
    try:
        result = {}
        items = db.query(OrderItem).all()
        for item in items:
            result.setdefault(item.warehouse_id, set()).add(item.product_id)
        return {k: list(v) for k, v in result.items()}
    finally:
        db.close()

def ciudades_por_producto(product_id: str):
    db = SessionLocal()
    try:
        ciudades_query = (
            db.query(Order.city)
            .join(OrderItem, Order.id == OrderItem.order_id)
            .filter(OrderItem.product_id == product_id)
            .distinct()
        )
        ciudades = [c[0] for c in ciudades_query.all()]
        return ciudades
    finally:
        db.close()

def almacenes_por_ciudad(ciudad: str):
    db = SessionLocal()
    try:
        almacenes_query = (
            db.query(OrderItem.warehouse_id)
            .join(Order, Order.id == OrderItem.order_id)
            .filter(Order.city == ciudad)
            .distinct()
        )
        almacenes = [a[0] for a in almacenes_query.all()]
        return almacenes
    finally:
        db.close()

def movimientos_generales(desde: str, hasta: str):
    db = SessionLocal()
    try:
        desde_dt = datetime.fromisoformat(desde)
        hasta_dt = datetime.fromisoformat(hasta)
        items = (
            db.query(OrderItem)
            .join(Order, Order.id == OrderItem.order_id)
            .filter(Order.invoiced_date >= desde_dt, Order.invoiced_date <= hasta_dt)
            .all()
        )
        return [
            {
                "producto": item.product_id,
                "almacen": item.warehouse_id,
                "ciudad_destino": item.order.city,
                "fecha": item.order.invoiced_date.isoformat() if item.order.invoiced_date else None,
            }
            for item in items
        ]
    finally:
        db.close()
        
def todas_las_ciudades():
    db = SessionLocal()
    try:
        ciudades = db.query(Order.city).distinct().all()
        return [c[0] for c in ciudades if c[0] is not None]
    finally:
        db.close()
        
def todos_los_productos():
    db = SessionLocal()
    try:
        productos = db.query(OrderItem.product_id).distinct().all()
        return [p[0] for p in productos if p[0] is not None]
    finally:
        db.close()   
