import os
from datetime import datetime
from app.db import SessionLocal
from app.models import Order, OrderItem
from app.crud import get_or_create_order, get_or_create_product, get_or_create_warehouse, create_order_item

def sincronizar_ordenes(ordenes):
    db = SessionLocal()
    try:
        for orden in ordenes:
            order_id = orden.get("orderId")
            if not order_id:
                print("orderId no encontrado en la orden:", orden)
                continue
            invoiced_date_str = orden.get("invoicedDate")
            invoiced_date = None
            if invoiced_date_str:
                try:
                    invoiced_date = datetime.fromisoformat(invoiced_date_str.replace("Z", "+00:00"))
                except ValueError as e:
                    print(f"Error parseando fecha {invoiced_date_str}: {e}")
            shipping_city = orden.get("shippingData", {}).get("address", {}).get("city")
            order = get_or_create_order(db, order_id, invoiced_date, shipping_city)

            items = orden.get("items", [])
            logistics_info = orden.get("shippingData", {}).get("logisticsInfo", [])
            
            for item in items:
                product_id = item.get("id")
                if not product_id:
                    print(f"Product ID no encontrado en item: {item}")
                    continue
                    
                product = get_or_create_product(db, product_id)

                item_logistics = None
                for logistics in logistics_info:
                    if logistics.get("itemId") == product_id:
                        item_logistics = logistics
                        break
                
                if item_logistics:
                    delivery_ids = item_logistics.get("deliveryIds", [])
                    for delivery in delivery_ids:
                        warehouse_id = delivery.get("warehouseId")
                        if warehouse_id:
                            warehouse = get_or_create_warehouse(db, warehouse_id)
                            create_order_item(db, order, product, warehouse)
                else:
                    print(f"No se encontró información logística para el item {product_id} en la orden {order_id}")

        db.commit()
        print(f"Sincronización completada exitosamente. Procesadas {len(ordenes)} órdenes.")

    except Exception as e:
        db.rollback()
        print(f"Error en sincronizar_ordenes: {e}")
        raise e
    finally:
        db.close()

def productos_por_almacen():
    db = SessionLocal()
    try:
        result = {}
        items = db.query(OrderItem).all()
        for item in items:
            if item.warehouse_id:  # Verificar que warehouse_id no sea None
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
            .filter(Order.city.isnot(None))  # Filtrar ciudades nulas
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
            .filter(OrderItem.warehouse_id.isnot(None))  
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
        ciudades = db.query(Order.city).filter(Order.city.isnot(None)).distinct().all()
        return [c[0] for c in ciudades]
    finally:
        db.close()
        
def todos_los_productos():
    db = SessionLocal()
    try:
        productos = db.query(OrderItem.product_id).filter(OrderItem.product_id.isnot(None)).distinct().all()
        return [p[0] for p in productos]
    finally:
        db.close()
