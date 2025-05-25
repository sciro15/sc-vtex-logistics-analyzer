## VTEX API

*** nota importante ***
Durante el desarrollo de este proyecto, me enfrenté a un gran reto, ya que el token de autenticación de la API de VTEX que nos dieron por un periodo de 20 horas expiro en el momento en donde me disponia a descargar la informacion, lo que impedía la descarga de los datos reales desde dicha fuente.

Sin embargo, en lugar de detener el avance o rendirme ante la limitación, opté por simular las respuestas esperadas utilizando un archivo JSON con datos ficticios pero manteniendome lo mas fiel posible a la respuesta de la api. Esto me permitió continuar con el diseño, lógica y visualización de la solución propuesta.

Los datos utilizados en el entorno actual son simulados y no reflejan información real pero si una estructura semejante a ella.
No obstante, la aplicación está estructurada y preparada para funcionar con datos reales desde la API de VTEX, siempre y cuando se proporcione un token válido en el archivo .env y cambiando la variable USE_LOCAL_JSON la cual use para poder tener una logica que me permitiera continuar con el json pero adenas demostrar mi capacidad para traer la informacion directamente desde la api de VTEX.

Pido disculpas de antemano por no haber podido descargar los datos de la API. Aun así, he tratado de entregar una solución completa, funcional y organizada, enfocada en cumplir los requerimientos planteados.

estoy completamente dispuesto a realizar otra prueba técnica si es necesario o lo que se consideren mejor para esta situacion. Mi intención siempre fue mostrar mi compromiso y capacidad de resolver incluso ante contratiempos

## Pre-requisitos del Sistema
  - Python 3.8 o superior
  - SQLite (incluido con Python, no requiere instalación adicional)

## Configuración del Proyecto
# Instalar dependencias
  - pip install fastapi uvicorn sqlalchemy strawberry-graphql python-dotenv requests (revisar documento de requirements.txt)
# Variables de Entorno
Crear archivo .env basado en el siguiente ejemplo:
    VTEX_ACCOUNT=tu-account-name
    VTEX_TOKEN=tu-vtex-token
    USE_LOCAL_JSON=false

## Instrucciones de Ejecución
  # Api 
  - python -m uvicorn app.main:app --reload 
  - curl -X POST http://localhost:8000/sync-orders   -H "Content-Type: application/json"   --data-binary @data/ordenes_facturadas.json
  # Frontend
  - npm install
  - npm run dev
# Accede a:
  - Health check: http://localhost:8000/
  - GraphQL Playground: http://localhost:8000/graphql
# Endpoints Disponibles
  -  GET / - Health check para verificar que el servidor está corriendo
  -  POST /sync-orders - Endpoint para sincronizar órdenes desde VTEX (consumir JSON o respuesta de la api)

## Justificación de Decisiones Técnicas
# FastAPI
  - Alto rendimiento basado en Starlette y Pydantic.
  - Documentación automática con OpenAPI/Swagger integrada.
  - Tipado fuerte con validación automática de datos.
# SQLAlchemy + SQLite
  - ORM robusto para modelar relaciones complejas (FK, joins).
  - SQLite ligero, sin necesidad de configuración extra para desarrollo local.
# GraphQL (Strawberry)
  - Consultas flexibles que permiten obtener solo los datos necesarios.
  - Un único endpoint para evitar under/over-fetching.
  - Introspección automática del esquema para autogenerar documentación.

## Uso de la API
# Consultas GraphQL de ejemplo
  - Productos por Almacén : 
    query {
      productosPorAlmacen {
        almacen
        productos
      }
    }   
  - Ciudades de un Producto :
    query {
      ciudadesPorProducto(nombre: "PRODUCT-123")
    }
  - Almacenes por Ciudad :
    query {
      almacenesPorCiudad(ciudad: "Medellin")
    }
  - Movimientos por Fecha : 
    query {
      movimientosGenerales(
        desde: "2024-01-01T00:00:00"
        hasta: "2024-01-31T23:59:59"
      ) {
        producto
        almacen
        ciudadDestino
        fecha
      }
    }
  - Listar Datos :
    query {
      todasLasCiudades
      todosLosProductos
    }

## Modelo de Datos
  - Orders (1) ←→ (N) OrderItems (N) ←→ (1) Products
                     ↓
               Warehouses (1)

## Flujo de Sincronización
  - VTEX API / json  → FastAPI → SQLAlchemy → SQLite

## Arquitectura de Consultas
  - Client → GraphQL → Logic Layer → CRUD → Database


