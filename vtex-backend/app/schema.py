import strawberry
from typing import List, Optional
from app.logic import (
    productos_por_almacen,
    ciudades_por_producto,
    almacenes_por_ciudad,
    movimientos_generales,
    todas_las_ciudades,
    todos_los_productos
)

@strawberry.type
class ProductosEnAlmacen:
    almacen: str
    productos: List[str]

@strawberry.type
class Movimiento:
    producto: str
    almacen: Optional[str]
    ciudad_destino: Optional[str]
    fecha: str

@strawberry.type
class Query:

    @strawberry.field
    def productos_por_almacen(self) -> List[ProductosEnAlmacen]:
        resultado = productos_por_almacen()
        return [ProductosEnAlmacen(almacen=k, productos=v) for k, v in resultado.items()]

    @strawberry.field
    def ciudades_por_producto(self, nombre: str) -> List[str]:
        return ciudades_por_producto(nombre)

    @strawberry.field
    def almacenes_por_ciudad(self, ciudad: str) -> List[str]:
        return almacenes_por_ciudad(ciudad)

    @strawberry.field
    def todas_las_ciudades(self) -> List[str]:
        return todas_las_ciudades()
    
    @strawberry.field
    def todosLosProductos(self) -> list[str]:
        return todos_los_productos()
    
    @strawberry.field
    def movimientos_generales(self, desde: str, hasta: str) -> List[Movimiento]:
        movimientos = movimientos_generales(desde, hasta)
        return [
            Movimiento(
                producto=m["producto"],
                almacen=m["almacen"],
                ciudad_destino=m["ciudad_destino"],
                fecha=m["fecha"],
            )
            for m in movimientos
        ]

schema = strawberry.Schema(query=Query)
