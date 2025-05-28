import os
import sys
import json
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.vtex_client import listar_ordenes_facturadas_enero, obtener_detalle_orden


def sincronizar_ordenes_facturadas():
    print("Obteniendo órdenes facturadas de enero...")
    ordenes_resumen = listar_ordenes_facturadas_enero()
    ordenes_detalladas = []

    for orden in ordenes_resumen:
        order_id = orden.get("orderId")
        if not order_id:
            print("Orden sin ID, se omite.")
            continue
        print(f"Obteniendo detalle de orden: {order_id}")
        try:
            detalle = obtener_detalle_orden(order_id)
            ordenes_detalladas.append(detalle)
        except Exception as e:
            print(f"Error obteniendo orden {order_id}: {e}")

    print(f"Enviando {len(ordenes_detalladas)} órdenes a la API local...")

    try:
        response = requests.post(
            "http://localhost:8000/sync-orders",
            headers={"Content-Type": "application/json"},
            data=json.dumps(ordenes_detalladas, ensure_ascii=False).encode("utf-8")
        )

        if response.status_code == 200:
            print("✅ Órdenes sincronizadas correctamente.")
        else:
            print(f"❌ Error al sincronizar órdenes: {response.status_code}")
            print(response.text)
    except requests.RequestException as e:
        print(f"❌ Error de conexión con la API local: {e}")


if __name__ == "__main__":
    sincronizar_ordenes_facturadas()
