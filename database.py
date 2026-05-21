"""
database.py - Conexion y operaciones con SQLite
Patron repository: todo lo de BD queda aqui
"""
import sqlite3
import hashlib
from typing import List, Optional, Dict, Tuple
from datetime import datetime

from models import Usuario, Producto, Movimiento


class ConexionDB:
    """Context manager para abrir/cerrar conexion de forma segura"""

    def __init__(self, ruta: str):
        self.ruta = ruta
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.ruta)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            if exc_type:
                self.conn.rollback()
            self.conn.close()


class BaseDatos:
    DB_PATH = "innovax.db"

    def __init__(self):
        self.db_path = self.DB_PATH
        self._crear_tablas()

    def _crear_tablas(self):
        """Crea las tablas si no existen"""
        with ConexionDB(self.db_path) as conn:
            c = conn.cursor()

            c.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT UNIQUE NOT NULL,
                    contrasena TEXT NOT NULL,
                    rol TEXT NOT NULL DEFAULT 'empleado',
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            c.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    stock_actual INTEGER NOT NULL DEFAULT 0,
                    stock_minimo INTEGER NOT NULL DEFAULT 5,
                    stock_maximo INTEGER NOT NULL DEFAULT 100,
                    precio REAL NOT NULL DEFAULT 0,
                    unidad TEXT NOT NULL DEFAULT 'unidad',
                    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            c.execute("""
                CREATE TABLE IF NOT EXISTS movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    usuario_id INTEGER NOT NULL,
                    fecha DATETIME NOT NULL,
                    notas TEXT,
                    FOREIGN KEY (producto_id) REFERENCES productos(id),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            """)

            conn.commit()

    # ──────────── USUARIOS ────────────

    def crear_usuario(self, nombre, correo, contrasena, rol="empleado") -> Tuple[bool, str]:
        if not nombre or not correo or not contrasena:
            return False, "Todos los campos son requeridos"
        try:
            with ConexionDB(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES (?, ?, ?, ?)",
                    (nombre, correo, self._hash(contrasena), rol)
                )
                conn.commit()
                return True, "Usuario creado exitosamente"
        except sqlite3.IntegrityError:
            return False, "El correo ya esta registrado"
        except Exception as e:
            return False, str(e)

    def obtener_usuario(self, uid: int) -> Optional[Usuario]:
        try:
            with ConexionDB(self.db_path) as conn:
                row = conn.execute(
                    "SELECT id, nombre, correo, rol FROM usuarios WHERE id = ?", (uid,)
                ).fetchone()
                if row:
                    return Usuario(id=row[0], nombre=row[1], correo=row[2], rol=row[3])
        except Exception:
            pass
        return None

    def obtener_todos_usuarios(self) -> List[Usuario]:
        try:
            with ConexionDB(self.db_path) as conn:
                rows = conn.execute(
                    "SELECT id, nombre, correo, rol FROM usuarios"
                ).fetchall()
                return [Usuario(id=r[0], nombre=r[1], correo=r[2], rol=r[3]) for r in rows]
        except Exception:
            return []

    def autenticar_usuario(self, correo, contrasena) -> Tuple[bool, Optional[Usuario]]:
        try:
            with ConexionDB(self.db_path) as conn:
                row = conn.execute(
                    "SELECT id, nombre, correo, rol, contrasena FROM usuarios WHERE correo = ?",
                    (correo,)
                ).fetchone()
                if row and self._verificar(contrasena, row[4]):
                    return True, Usuario(id=row[0], nombre=row[1], correo=row[2], rol=row[3])
        except Exception:
            pass
        return False, None

    def actualizar_usuario(self, uid: int, **kwargs) -> Tuple[bool, str]:
        campos = {k: v for k, v in kwargs.items() if k in ('nombre', 'correo', 'rol') and v}
        if not campos:
            return False, "Nada que actualizar"
        try:
            sets = ", ".join(f"{k} = ?" for k in campos)
            vals = list(campos.values()) + [uid]
            with ConexionDB(self.db_path) as conn:
                conn.execute(f"UPDATE usuarios SET {sets} WHERE id = ?", vals)
                conn.commit()
                return True, "Usuario actualizado"
        except Exception as e:
            return False, str(e)

    def eliminar_usuario(self, uid: int) -> Tuple[bool, str]:
        try:
            with ConexionDB(self.db_path) as conn:
                conn.execute("DELETE FROM usuarios WHERE id = ?", (uid,))
                conn.commit()
                return True, "Usuario eliminado"
        except Exception as e:
            return False, str(e)

    # ──────────── PRODUCTOS ────────────

    def crear_producto(self, nombre, codigo, categoria, stock_actual,
                       stock_minimo, stock_maximo, precio, unidad) -> Tuple[bool, str]:
        if not nombre or not codigo:
            return False, "Nombre y codigo son requeridos"
        try:
            with ConexionDB(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO productos
                    (codigo, nombre, categoria, stock_actual, stock_minimo, stock_maximo, precio, unidad)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (codigo, nombre, categoria, stock_actual, stock_minimo, stock_maximo, precio, unidad))
                conn.commit()
                return True, "Producto creado exitosamente"
        except sqlite3.IntegrityError:
            return False, "El codigo ya existe"
        except Exception as e:
            return False, str(e)

    def obtener_producto(self, pid: int) -> Optional[Producto]:
        try:
            with ConexionDB(self.db_path) as conn:
                row = conn.execute(
                    "SELECT id, nombre, codigo, categoria, stock_actual, stock_minimo, stock_maximo, precio, unidad FROM productos WHERE id = ?",
                    (pid,)
                ).fetchone()
                if row:
                    return Producto(id=row[0], nombre=row[1], codigo=row[2], categoria=row[3],
                                    stock_actual=row[4], stock_minimo=row[5], stock_maximo=row[6],
                                    precio=row[7], unidad=row[8])
        except Exception:
            pass
        return None

    def obtener_todos_productos(self) -> List[Producto]:
        try:
            with ConexionDB(self.db_path) as conn:
                rows = conn.execute(
                    "SELECT id, nombre, codigo, categoria, stock_actual, stock_minimo, stock_maximo, precio, unidad FROM productos ORDER BY nombre"
                ).fetchall()
                return [Producto(id=r[0], nombre=r[1], codigo=r[2], categoria=r[3],
                                 stock_actual=r[4], stock_minimo=r[5], stock_maximo=r[6],
                                 precio=r[7], unidad=r[8]) for r in rows]
        except Exception:
            return []

    def obtener_productos_criticos(self) -> List[Producto]:
        try:
            with ConexionDB(self.db_path) as conn:
                rows = conn.execute(
                    "SELECT id, nombre, codigo, categoria, stock_actual, stock_minimo, stock_maximo, precio, unidad FROM productos WHERE stock_actual <= stock_minimo ORDER BY stock_actual ASC"
                ).fetchall()
                return [Producto(id=r[0], nombre=r[1], codigo=r[2], categoria=r[3],
                                 stock_actual=r[4], stock_minimo=r[5], stock_maximo=r[6],
                                 precio=r[7], unidad=r[8]) for r in rows]
        except Exception:
            return []

    def actualizar_producto(self, pid: int, **kwargs) -> Tuple[bool, str]:
        permitidos = ('nombre', 'categoria', 'stock_minimo', 'stock_maximo', 'precio', 'unidad', 'stock_actual')
        campos = {k: v for k, v in kwargs.items() if k in permitidos and v is not None}
        if not campos:
            return False, "Nada que actualizar"
        try:
            sets = ", ".join(f"{k} = ?" for k in campos)
            vals = list(campos.values()) + [pid]
            with ConexionDB(self.db_path) as conn:
                conn.execute(f"UPDATE productos SET {sets} WHERE id = ?", vals)
                conn.commit()
                return True, "Producto actualizado"
        except Exception as e:
            return False, str(e)

    def eliminar_producto(self, pid: int) -> Tuple[bool, str]:
        try:
            with ConexionDB(self.db_path) as conn:
                conn.execute("DELETE FROM productos WHERE id = ?", (pid,))
                conn.commit()
                return True, "Producto eliminado"
        except Exception as e:
            return False, str(e)

    # ──────────── MOVIMIENTOS ────────────

    def crear_movimiento(self, mov: Movimiento) -> Tuple[bool, str]:
        producto = self.obtener_producto(mov.producto_id)
        if not producto:
            return False, "Producto no encontrado"
        if mov.es_salida() and not producto.puede_descontar(mov.cantidad):
            return False, f"Stock insuficiente. Disponible: {producto.stock_actual}"

        try:
            with ConexionDB(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO movimientos (producto_id, tipo, cantidad, usuario_id, fecha, notas)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (mov.producto_id, mov.tipo, mov.cantidad, mov.usuario_id, mov.fecha, mov.notas))

                # Actualizar stock segun tipo
                if mov.es_entrada():
                    nuevo = producto.stock_actual + mov.cantidad
                else:
                    nuevo = producto.stock_actual - mov.cantidad

                conn.execute("UPDATE productos SET stock_actual = ? WHERE id = ?",
                             (nuevo, mov.producto_id))
                conn.commit()
                return True, "Movimiento registrado exitosamente"
        except Exception as e:
            return False, str(e)

    def obtener_movimientos(self, limite=100) -> List[Dict]:
        try:
            with ConexionDB(self.db_path) as conn:
                rows = conn.execute("""
                    SELECT m.id, m.producto_id, m.tipo, m.cantidad,
                           m.usuario_id, m.fecha, m.notas,
                           p.nombre, u.nombre
                    FROM movimientos m
                    JOIN productos p ON m.producto_id = p.id
                    JOIN usuarios u ON m.usuario_id = u.id
                    ORDER BY m.fecha DESC LIMIT ?
                """, (limite,)).fetchall()

                return [{
                    'id': r[0], 'producto_id': r[1], 'tipo': r[2],
                    'cantidad': r[3], 'usuario_id': r[4], 'fecha': r[5],
                    'notas': r[6], 'producto_nombre': r[7], 'usuario_nombre': r[8]
                } for r in rows]
        except Exception:
            return []

    def obtener_movimientos_producto(self, pid: int, limite=200) -> List[Dict]:
        try:
            with ConexionDB(self.db_path) as conn:
                rows = conn.execute("""
                    SELECT tipo, cantidad, fecha, usuario_id
                    FROM movimientos WHERE producto_id = ?
                    ORDER BY fecha DESC LIMIT ?
                """, (pid, limite)).fetchall()
                return [{'tipo': r[0], 'cantidad': r[1], 'fecha': r[2], 'usuario_id': r[3]} for r in rows]
        except Exception:
            return []

    def eliminar_movimiento(self, mid: int) -> Tuple[bool, str]:
        """Revierte un movimiento y restaura el stock"""
        try:
            with ConexionDB(self.db_path) as conn:
                row = conn.execute(
                    "SELECT producto_id, tipo, cantidad FROM movimientos WHERE id = ?", (mid,)
                ).fetchone()
                if not row:
                    return False, "Movimiento no encontrado"

                pid, tipo, cantidad = row[0], row[1], row[2]
                # Revertir: si era entrada restamos, si era salida sumamos
                if tipo == "Entrada":
                    conn.execute("UPDATE productos SET stock_actual = stock_actual - ? WHERE id = ?",
                                 (cantidad, pid))
                else:
                    conn.execute("UPDATE productos SET stock_actual = stock_actual + ? WHERE id = ?",
                                 (cantidad, pid))

                conn.execute("DELETE FROM movimientos WHERE id = ?", (mid,))
                conn.commit()
                return True, "Movimiento revertido"
        except Exception as e:
            return False, str(e)

    def obtener_resumen(self) -> Dict:
        try:
            with ConexionDB(self.db_path) as conn:
                total = conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
                criticos = conn.execute(
                    "SELECT COUNT(*) FROM productos WHERE stock_actual <= stock_minimo"
                ).fetchone()[0]
                normales = conn.execute(
                    "SELECT COUNT(*) FROM productos WHERE stock_actual > stock_minimo"
                ).fetchone()[0]
                valor = conn.execute(
                    "SELECT COALESCE(SUM(stock_actual * precio), 0) FROM productos"
                ).fetchone()[0]

                return {
                    'total_productos': total,
                    'productos_criticos': criticos,
                    'productos_normales': normales,
                    'valor_inventario': valor
                }
        except Exception:
            return {'total_productos': 0, 'productos_criticos': 0,
                    'productos_normales': 0, 'valor_inventario': 0}

    def obtener_consumo_por_categoria(self) -> List[Dict]:
        """Retorna consumo total por categoria (para graficas)"""
        try:
            with ConexionDB(self.db_path) as conn:
                rows = conn.execute("""
                    SELECT p.categoria, SUM(m.cantidad) as total
                    FROM movimientos m
                    JOIN productos p ON m.producto_id = p.id
                    WHERE m.tipo = 'Salida'
                    GROUP BY p.categoria
                    ORDER BY total DESC
                """).fetchall()
                return [{'categoria': r[0], 'total': r[1]} for r in rows]
        except Exception:
            return []

    def obtener_top_productos_consumo(self, limite=5) -> List[Dict]:
        """Top productos con mayor consumo (salidas)"""
        try:
            with ConexionDB(self.db_path) as conn:
                rows = conn.execute("""
                    SELECT p.nombre, p.unidad, SUM(m.cantidad) as total_salidas
                    FROM movimientos m
                    JOIN productos p ON m.producto_id = p.id
                    WHERE m.tipo = 'Salida'
                    GROUP BY p.id
                    ORDER BY total_salidas DESC
                    LIMIT ?
                """, (limite,)).fetchall()
                return [{'nombre': r[0], 'unidad': r[1], 'total': r[2]} for r in rows]
        except Exception:
            return []

    def obtener_movimientos_por_dia(self, dias=7) -> List[Dict]:
        """Movimientos de los ultimos N dias agrupados por dia"""
        try:
            with ConexionDB(self.db_path) as conn:
                rows = conn.execute("""
                    SELECT DATE(fecha) as dia,
                           SUM(CASE WHEN tipo='Entrada' THEN cantidad ELSE 0 END) as entradas,
                           SUM(CASE WHEN tipo='Salida' THEN cantidad ELSE 0 END) as salidas
                    FROM movimientos
                    WHERE fecha >= DATE('now', ?)
                    GROUP BY dia
                    ORDER BY dia ASC
                """, (f'-{dias} days',)).fetchall()
                return [{'dia': r[0], 'entradas': r[1], 'salidas': r[2]} for r in rows]
        except Exception:
            return []

    # ──────────── UTILIDADES ────────────

    @staticmethod
    def _hash(clave: str) -> str:
        import hashlib
        return hashlib.sha256(clave.encode()).hexdigest()

    @staticmethod
    def _verificar(clave: str, hash_guardado: str) -> bool:
        import hashlib
        return hashlib.sha256(clave.encode()).hexdigest() == hash_guardado
