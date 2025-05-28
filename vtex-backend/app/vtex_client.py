import os
import requests
import json
import time
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
        max_retries = 3
        
        while True:
            print(f"Consultando página {page}")
            url = (
                f"{BASE_URL}/api/oms/pvt/orders"
                "?per_page=100"
                "&f_invoicedDate=invoicedDate%3A%5B2024-01-01T00%3A00%3A00.000Z%20TO%202024-01-31T23%3A59%3A59.999Z%5D"
                "&f_status=invoiced"
                f"&page={page}"
            )
            
            for retry in range(max_retries):
                try:
                    response = requests.get(url, headers=HEADERS, timeout=30)
                    
                    if response.status_code == 400:
                        print(f"Error 400 en página {page}. Posiblemente no hay más páginas.")
                        return ordenes
                    
                    response.raise_for_status()
                    break
                    
                except requests.exceptions.RequestException as e:
                    print(f"Error en página {page}, intento {retry + 1}: {e}")
                    if retry == max_retries - 1:
                        print(f"Falló después de {max_retries} intentos. Retornando órdenes obtenidas hasta ahora.")
                        return ordenes
                    time.sleep(2 ** retry)  
            else:
                print(f"No se pudo obtener la página {page} después de {max_retries} intentos.")
                return ordenes

            try:
                data = response.json()
            except json.JSONDecodeError:
                print(f"Error al decodificar JSON en página {page}")
                return ordenes
            
            lista = data.get("list", [])

            if not lista:
                print(f"No hay más órdenes en página {page}. Total obtenidas: {len(ordenes)}")
                break
           
            paging = data.get("paging", {})
            total_pages = paging.get("pages", None)
            
            if total_pages and page >= total_pages:
                print(f"Alcanzada la última página ({total_pages}). Total órdenes: {len(ordenes) + len(lista)}")
                ordenes.extend(lista)
                break
            
            ordenes.extend(lista)
            print(f"Página {page} procesada. Órdenes acumuladas: {len(ordenes)}")
            
            time.sleep(0.5)
            page += 1
            
            if page > 50:  # Adjust this limit as needed
                print(f"Alcanzado límite de seguridad de páginas ({page}). Terminando.")
                break

        print(f"Proceso completado. Total de órdenes obtenidas: {len(ordenes)}")
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
                raise ValueError(f"No se encontró el detalle de la orden '{order_id}' en el archivo JSON local")

    max_retries = 3
    for retry in range(max_retries):
        try:
            url = f"{BASE_URL}/api/oms/pvt/orders/{order_id}"
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo detalle de orden {order_id}, intento {retry + 1}: {e}")
            if retry == max_retries - 1:
                raise
            time.sleep(2 ** retry)

    return None