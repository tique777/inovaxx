"""
services.py - Logica de negocio de InnovaX
Separa las operaciones complejas de la base de datos y la UI
"""
from typing import List, Dict, Tuple
from datetime import datetime

from database import BaseDatos
from models import Producto, Movimiento


class ServicioInventario:
    """Operaciones de inventario: productos y movimientos"""

    def __init__(self):
        self.db = BaseDatos()

    def crear_producto(self, nombre, codigo, categoria, stock_actual,
                       stock_minimo, stock_maximo, precio, unidad) -> Tuple[bool, str]:
        return self.db.crear_producto(nombre, codigo, categoria, stock_actual,
                                      stock_minimo, stock_maximo, precio, unidad)

    def obtener_producto(self, pid: int) -> Producto:
        return self.db.obtener_producto(pid)

    def obtener_todos_productos(self) -> List[Producto]:
        return self.db.obtener_todos_productos()

    def obtener_productos_criticos(self) -> List[Producto]:
        return self.db.obtener_productos_criticos()

    def actualizar_producto(self, pid: int, **kwargs) -> Tuple[bool, str]:
        return self.db.actualizar_producto(pid, **kwargs)

    def eliminar_producto(self, pid: int) -> Tuple[bool, str]:
        return self.db.eliminar_producto(pid)

    def registrar_entrada(self, producto_id, cantidad, usuario_id, notas="") -> Tuple[bool, str]:
        mov = Movimiento.crear_entrada(producto_id, cantidad, usuario_id, notas)
        return self.db.crear_movimiento(mov)

    def registrar_salida(self, producto_id, cantidad, usuario_id, notas="") -> Tuple[bool, str]:
        mov = Movimiento.crear_salida(producto_id, cantidad, usuario_id, notas)
        return self.db.crear_movimiento(mov)

    def obtener_movimientos(self, limite=100) -> List[Dict]:
        return self.db.obtener_movimientos(limite)

    def obtener_movimientos_producto(self, pid: int, limite=200) -> List[Dict]:
        return self.db.obtener_movimientos_producto(pid, limite)

    def eliminar_movimiento(self, mid: int) -> Tuple[bool, str]:
        return self.db.eliminar_movimiento(mid)

    def obtener_resumen(self) -> Dict:
        return self.db.obtener_resumen()

    def calcular_consumo_promedio(self, pid: int, dias=30) -> float:
        """Calcula cuanto se consume por dia en promedio"""
        movimientos = self.db.obtener_movimientos_producto(pid, 500)
        salidas = [m for m in movimientos if m['tipo'] == 'Salida']

        if not salidas:
            return 0.0

        # Calcula dias entre la primera y ultima salida
        fechas = [datetime.strptime(m['fecha'], "%Y-%m-%d %H:%M:%S") for m in salidas]
        diferencia = (max(fechas) - min(fechas)).days

        if diferencia == 0:
            diferencia = 1  # Al menos 1 dia para no dividir entre 0

        total = sum(m['cantidad'] for m in salidas)
        return round(total / diferencia, 2)

    def estimar_dias_restantes(self, pid: int) -> int:
        """Cuantos dias dura el stock con el consumo actual"""
        producto = self.obtener_producto(pid)
        if not producto:
            return 0

        consumo = self.calcular_consumo_promedio(pid)
        if consumo == 0:
            return 999  # Sin historial, stock indefinido

        return int(producto.stock_actual / consumo)

    def obtener_consumo_por_categoria(self) -> List[Dict]:
        return self.db.obtener_consumo_por_categoria()

    def obtener_top_productos_consumo(self, limite=5) -> List[Dict]:
        return self.db.obtener_top_productos_consumo(limite)

    def obtener_movimientos_por_dia(self, dias=7) -> List[Dict]:
        return self.db.obtener_movimientos_por_dia(dias)


class ServicioUsuarios:
    """Operaciones de usuarios y autenticacion"""

    def __init__(self):
        self.db = BaseDatos()

    def crear_usuario(self, nombre, correo, contrasena, rol="empleado") -> Tuple[bool, str]:
        return self.db.crear_usuario(nombre, correo, contrasena, rol)

    def obtener_usuario(self, uid: int):
        return self.db.obtener_usuario(uid)

    def obtener_todos_usuarios(self):
        return self.db.obtener_todos_usuarios()

    def actualizar_usuario(self, uid: int, **kwargs) -> Tuple[bool, str]:
        return self.db.actualizar_usuario(uid, **kwargs)

    def eliminar_usuario(self, uid: int) -> Tuple[bool, str]:
        return self.db.eliminar_usuario(uid)


class ServicioPrediccion:
    """Prediccion de demanda y analisis de stock"""

    def __init__(self):
        self.inv = ServicioInventario()

    def predecir_producto(self, pid: int) -> Dict:
        """
        Devuelve un analisis completo de un producto:
        consumo diario, dias restantes, urgencia y recomendacion de compra
        """
        producto = self.inv.obtener_producto(pid)
        if not producto:
            return {}

        consumo_diario = self.inv.calcular_consumo_promedio(pid)
        consumo_mensual = round(consumo_diario * 30, 2)
        dias_restantes = self.inv.estimar_dias_restantes(pid)

        # Nivel de urgencia segun dias restantes
        if dias_restantes <= 5:
            urgencia = "Urgente"
        elif dias_restantes <= 15:
            urgencia = "Pronto"
        else:
            urgencia = "Normal"

        # Recomendar cuanto comprar para cubrir 30 dias
        if consumo_diario > 0:
            cantidad_recomendada = int(consumo_diario * 30)
        else:
            cantidad_recomendada = producto.stock_maximo - producto.stock_actual

        return {
            'producto_id': pid,
            'producto': producto.nombre,
            'codigo': producto.codigo,
            'categoria': producto.categoria,
            'stock_actual': producto.stock_actual,
            'stock_minimo': producto.stock_minimo,
            'stock_maximo': producto.stock_maximo,
            'unidad': producto.unidad,
            'precio': producto.precio,
            'consumo_diario': consumo_diario,
            'consumo_mensual': consumo_mensual,
            'dias_restantes': dias_restantes,
            'urgencia': urgencia,
            'cantidad_recomendada': cantidad_recomendada,
            'costo_recomendado': round(cantidad_recomendada * producto.precio, 2),
            'estado': producto.calcular_estado().value,
            'porcentaje_stock': producto.porcentaje_stock()
        }

    def predecir_todos(self) -> List[Dict]:
        """Predicciones de todos los productos ordenadas por urgencia"""
        productos = self.inv.obtener_todos_productos()
        predicciones = []

        for p in productos:
            pred = self.predecir_producto(p.id)
            if pred:
                predicciones.append(pred)

        # Urgente primero, luego Pronto, luego Normal
        orden = {'Urgente': 0, 'Pronto': 1, 'Normal': 2}
        predicciones.sort(key=lambda x: orden.get(x['urgencia'], 3))

        return predicciones

    def calcular_punto_reorden(self, pid: int, dias_entrega=7) -> int:
        """
        Punto de reorden: stock minimo para pedir antes de quedarse sin producto.
        Formula: consumo_diario * dias_entrega_proveedor + stock_seguridad
        """
        consumo = self.inv.calcular_consumo_promedio(pid)
        producto = self.inv.obtener_producto(pid)
        if not producto:
            return 0

        # Stock de seguridad = 20% del stock minimo del producto
        stock_seguridad = int(producto.stock_minimo * 0.2)
        return int(consumo * dias_entrega) + stock_seguridad

    def analisis_abc(self) -> List[Dict]:
        """
        Clasifica productos en A, B, C segun valor de consumo (Pareto).
        A = 20% de productos que generan 80% del movimiento/valor
        B = siguiente 30%
        C = restante 50%
        """
        productos = self.inv.obtener_todos_productos()
        datos = []

        for p in productos:
            consumo = self.inv.calcular_consumo_promedio(p.id)
            valor_movimiento = consumo * p.precio * 30  # valor mensual estimado
            datos.append({
                'producto': p.nombre,
                'producto_id': p.id,
                'consumo_mensual': round(consumo * 30, 1),
                'valor_mensual': round(valor_movimiento, 2),
                'precio': p.precio,
                'unidad': p.unidad
            })

        # Ordenar por valor de movimiento descendente
        datos.sort(key=lambda x: x['valor_mensual'], reverse=True)

        # Calcular porcentaje acumulado y asignar clase ABC
        total_valor = sum(d['valor_mensual'] for d in datos) or 1
        acumulado = 0
        for d in datos:
            acumulado += d['valor_mensual']
            pct = (acumulado / total_valor) * 100
            if pct <= 80:
                d['clase'] = 'A'
            elif pct <= 95:
                d['clase'] = 'B'
            else:
                d['clase'] = 'C'

        return datos
