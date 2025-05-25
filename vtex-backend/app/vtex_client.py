import os
import requests
import json
from app.config import VTEX_ACCOUNT, HEADERS
BASE_URL = f"https://{VTEX_ACCOUNT}.vtexcommercestable.com.br"
BASE_PATH = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(os.path.dirname(BASE_PATH), "data")  

def listar_ordenes_facturadas_enero():
    if os.getenv("USE_LOCAL_JSON", "false").lower() == "true":
        file_path = os.path.join(DATA_PATH, "ordenes_facturadas.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        ordenes = []
        page = 1
        while True:
            print(f"Consultando página {page}")
            url = (
                f"{BASE_URL}/api/oms/pvt/orders"
                "?per_page=100"
                "&f_invoicedDate=invoicedDate%3A%5B2024-01-01T00%3A00%3A00.000Z%20TO%202024-01-31T23%3A59%3A59.999Z%5D"
                "&f_status=invoiced"
                f"&page={page}"
            )
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()

            data = response.json()
            lista = data.get("list", [])
            if not lista:
                break

            ordenes.extend(lista)
            page += 1

        return ordenes


def obtener_detalle_orden(order_id, guardar_backup=True):
    if os.getenv("USE_LOCAL_JSON", "false").lower() == "true":
        detalles_path = os.path.join(DATA_PATH, "detalles_orden.json")
        print(f"Buscando detalle de orden {order_id} en {detalles_path}")
        with open(detalles_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            detalle = data.get(order_id)
            if detalle:
                return detalle
            else:
                raise ValueError(f" No se encontró el detalle de la orden '{order_id}' en el archivo JSON local")

    url = f"{BASE_URL}/api/oms/pvt/orders/{order_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    if guardar_backup:
        os.makedirs(RAW_ORDERS_PATH, exist_ok=True)
        with open(os.path.join(RAW_ORDERS_PATH, f"{order_id}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Backup guardado: {order_id}.json")

    return data

