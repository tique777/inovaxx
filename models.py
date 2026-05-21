"""
models.py - Clases de datos de InnovaX
Contiene: Usuario, Producto, Movimiento y sus enums
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Categoria(Enum):
    ALIMENTOS = "Alimentos"
    BEBIDAS = "Bebidas"
    LIMPIEZA = "Limpieza"
    PAPELERIA = "Papelería"
    ELECTRONICO = "Electrónico"
    ROPA = "Ropa"
    OTRO = "Otro"


class TipoMovimiento(Enum):
    ENTRADA = "Entrada"
    SALIDA = "Salida"


class EstadoStock(Enum):
    CRITICO = "Critico"
    BAJO = "Bajo"
    NORMAL = "Normal"
    EXCESO = "Exceso"


class RolUsuario(Enum):
    EMPLEADO = "empleado"
    ADMINISTRADOR = "administrador"


@dataclass
class Usuario:
    nombre: str
    correo: str
    rol: str
    id: Optional[int] = None

    def es_admin(self):
        return self.rol == RolUsuario.ADMINISTRADOR.value


@dataclass
class Producto:
    nombre: str
    codigo: str
    categoria: str
    stock_actual: int
    stock_minimo: int
    stock_maximo: int
    precio: float
    unidad: str
    id: Optional[int] = None

    def calcular_estado(self) -> EstadoStock:
        # Determina si el stock esta en estado critico, bajo, normal o exceso
        if self.stock_actual <= self.stock_minimo:
            return EstadoStock.CRITICO
        elif self.stock_actual <= self.stock_minimo + 10:
            return EstadoStock.BAJO
        elif self.stock_actual >= self.stock_maximo:
            return EstadoStock.EXCESO
        return EstadoStock.NORMAL

    def valor_total(self) -> float:
        return self.stock_actual * self.precio

    def puede_descontar(self, cantidad: int) -> bool:
        return self.stock_actual >= cantidad

    def porcentaje_stock(self) -> float:
        # Porcentaje del stock actual respecto al maximo (para grafica de barra)
        if self.stock_maximo == 0:
            return 0
        return min(100, (self.stock_actual / self.stock_maximo) * 100)


@dataclass
class Movimiento:
    producto_id: int
    tipo: str
    cantidad: int
    usuario_id: int
    fecha: str
    notas: str = ""
    id: Optional[int] = None

    @classmethod
    def crear_entrada(cls, producto_id, cantidad, usuario_id, notas=""):
        return cls(
            producto_id=producto_id,
            tipo=TipoMovimiento.ENTRADA.value,
            cantidad=cantidad,
            usuario_id=usuario_id,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            notas=notas
        )

    @classmethod
    def crear_salida(cls, producto_id, cantidad, usuario_id, notas=""):
        return cls(
            producto_id=producto_id,
            tipo=TipoMovimiento.SALIDA.value,
            cantidad=cantidad,
            usuario_id=usuario_id,
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            notas=notas
        )

    def es_entrada(self):
        return self.tipo == TipoMovimiento.ENTRADA.value

    def es_salida(self):
        return self.tipo == TipoMovimiento.SALIDA.value
