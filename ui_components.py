"""
ui_components.py - Componentes de UI reutilizables
Colores, botones, tarjetas, graficas con contenedores Flet
"""
import flet as ft
from typing import Callable, Optional, List, Dict
from models import EstadoStock


# ──────────── PALETA ────────────

class Colores:
    AZUL_OSCURO    = "#1e3a8a"
    AZUL_PRIMARIO  = "#2563eb"
    AZUL_CLARO     = "#dbeafe"
    BLANCO         = "#ffffff"
    NEGRO          = "#0f172a"
    GRIS           = "#475569"
    GRIS_CLARO     = "#f1f5f9"
    GRIS_MUY_CLARO = "#f8fafc"
    VERDE          = "#16a34a"
    VERDE_CLARO    = "#dcfce7"
    ROJO           = "#dc2626"
    ROJO_CLARO     = "#fee2e2"
    AMARILLO       = "#d97706"
    AMARILLO_CLARO = "#fef3c7"
    MORADO         = "#7c3aed"
    MORADO_CLARO   = "#ede9fe"


# ──────────── BADGES ────────────

class Badge:
    """Etiquetas de colores para estados y urgencias"""

    @staticmethod
    def estado_stock(estado: EstadoStock) -> ft.Container:
        mapa = {
            EstadoStock.CRITICO: (Colores.ROJO, Colores.ROJO_CLARO),
            EstadoStock.BAJO:    (Colores.AMARILLO, Colores.AMARILLO_CLARO),
            EstadoStock.NORMAL:  (Colores.VERDE, Colores.VERDE_CLARO),
            EstadoStock.EXCESO:  (Colores.AZUL_PRIMARIO, Colores.AZUL_CLARO),
        }
        color_txt, color_bg = mapa.get(estado, (Colores.GRIS, Colores.GRIS_CLARO))
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=20,
            bgcolor=color_bg,
            content=ft.Text(estado.value, size=11, weight=ft.FontWeight.BOLD, color=color_txt)
        )

    @staticmethod
    def urgencia(urgencia: str) -> ft.Container:
        mapa = {
            "Urgente": (Colores.ROJO, Colores.ROJO_CLARO),
            "Pronto":  (Colores.AMARILLO, Colores.AMARILLO_CLARO),
            "Normal":  (Colores.VERDE, Colores.VERDE_CLARO),
        }
        color_txt, color_bg = mapa.get(urgencia, (Colores.GRIS, Colores.GRIS_CLARO))
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            border_radius=20,
            bgcolor=color_bg,
            content=ft.Text(urgencia, size=11, weight=ft.FontWeight.BOLD, color=color_txt)
        )

    @staticmethod
    def clase_abc(clase: str) -> ft.Container:
        mapa = {
            "A": (Colores.ROJO, Colores.ROJO_CLARO),
            "B": (Colores.AMARILLO, Colores.AMARILLO_CLARO),
            "C": (Colores.VERDE, Colores.VERDE_CLARO),
        }
        color_txt, color_bg = mapa.get(clase, (Colores.GRIS, Colores.GRIS_CLARO))
        return ft.Container(
            width=32, height=32,
            border_radius=16,
            bgcolor=color_bg,
            alignment=ft.alignment.center,
            content=ft.Text(clase, size=13, weight=ft.FontWeight.BOLD, color=color_txt)
        )


# ──────────── TARJETAS ────────────

class TarjetaMetrica:
    """Tarjeta con titulo, valor e icono para el dashboard"""

    @staticmethod
    def crear(titulo: str, valor: str, icono: str, color: str) -> ft.Container:
        return ft.Container(
            width=200,
            padding=20,
            border_radius=16,
            bgcolor=Colores.BLANCO,
            shadow=ft.BoxShadow(blur_radius=12, color="rgba(0,0,0,0.08)", offset=ft.Offset(0, 2)),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(titulo, size=13, color=Colores.GRIS),
                            ft.Container(
                                width=36, height=36, border_radius=18,
                                bgcolor=color + "22",
                                alignment=ft.alignment.center,
                                content=ft.Icon(icono, size=20, color=color)
                            ),
                        ]
                    ),
                    ft.Text(valor, size=26, weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                ]
            )
        )


# ──────────── GRAFICA DE BARRAS ────────────

class GraficaBarras:
    """Barra de progreso visual con Flet (sin librerias externas)"""

    @staticmethod
    def barra_horizontal(etiqueta: str, valor: float, maximo: float,
                         color: str, ancho_total: int = 500) -> ft.Container:
        """Una sola barra horizontal con porcentaje"""
        pct = min(100, (valor / maximo * 100)) if maximo > 0 else 0
        ancho_barra = int((pct / 100) * (ancho_total - 120))

        return ft.Container(
            padding=ft.padding.symmetric(vertical=6),
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(etiqueta, size=12, color=Colores.NEGRO),
                            ft.Text(f"{valor:.0f}", size=12, weight=ft.FontWeight.BOLD, color=color),
                        ]
                    ),
                    ft.Stack(
                        controls=[
                            # Fondo gris
                            ft.Container(
                                width=ancho_total - 120,
                                height=10,
                                border_radius=5,
                                bgcolor=Colores.GRIS_CLARO,
                            ),
                            # Barra de color
                            ft.Container(
                                width=max(4, ancho_barra),
                                height=10,
                                border_radius=5,
                                bgcolor=color,
                            ),
                        ]
                    ),
                ]
            )
        )

    @staticmethod
    def stock_producto(nombre: str, stock_actual: int, stock_minimo: int,
                       stock_maximo: int, unidad: str) -> ft.Container:
        """Barra de stock con marcadores de minimo"""
        pct = min(100, (stock_actual / stock_maximo * 100)) if stock_maximo > 0 else 0
        ancho_total = 400

        if stock_actual <= stock_minimo:
            color = Colores.ROJO
        elif stock_actual <= stock_minimo + 10:
            color = Colores.AMARILLO
        else:
            color = Colores.VERDE

        return ft.Container(
            padding=12,
            border_radius=10,
            bgcolor=Colores.BLANCO,
            shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.06)"),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(nombre, size=13, weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                            ft.Text(f"{stock_actual} / {stock_maximo} {unidad}",
                                    size=12, color=Colores.GRIS),
                        ]
                    ),
                    ft.Stack(
                        controls=[
                            ft.Container(width=ancho_total, height=12, border_radius=6,
                                         bgcolor=Colores.GRIS_CLARO),
                            ft.Container(
                                width=max(4, int(pct / 100 * ancho_total)),
                                height=12, border_radius=6, bgcolor=color
                            ),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text(f"Min: {stock_minimo}", size=10, color=Colores.GRIS),
                            ft.Text(" | ", size=10, color=Colores.GRIS),
                            ft.Text(f"{pct:.0f}% del maximo", size=10, color=Colores.GRIS),
                        ]
                    )
                ]
            )
        )

    @staticmethod
    def grafica_categorias(datos: List[Dict]) -> ft.Container:
        """Grafica de barras para consumo por categoria"""
        if not datos:
            return ft.Container(
                content=ft.Text("Sin datos de consumo aun", color=Colores.GRIS, size=13)
            )

        maximo = max(d['total'] for d in datos) or 1
        colores_cat = [
            Colores.AZUL_PRIMARIO, Colores.VERDE, Colores.AMARILLO,
            Colores.ROJO, Colores.MORADO, Colores.GRIS
        ]

        barras = []
        for i, d in enumerate(datos):
            color = colores_cat[i % len(colores_cat)]
            barras.append(
                GraficaBarras.barra_horizontal(
                    d['categoria'], d['total'], maximo, color, ancho_total=450
                )
            )

        return ft.Container(
            padding=16,
            border_radius=12,
            bgcolor=Colores.BLANCO,
            shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.08)"),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text("Consumo por Categoria", size=15,
                            weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                    ft.Text("Unidades totales de salida", size=12, color=Colores.GRIS),
                    ft.Divider(color=Colores.GRIS_CLARO),
                ] + barras
            )
        )

    @staticmethod
    def grafica_actividad_reciente(datos: List[Dict]) -> ft.Container:
        """Mini grafica de actividad (entradas vs salidas por dia)"""
        if not datos:
            return ft.Container(
                content=ft.Text("Sin actividad reciente", color=Colores.GRIS, size=13)
            )

        max_val = max(max(d['entradas'], d['salidas']) for d in datos) or 1
        alto_max = 80

        columnas = []
        for d in datos:
            h_entrada = max(4, int((d['entradas'] / max_val) * alto_max))
            h_salida  = max(4, int((d['salidas']  / max_val) * alto_max))
            dia_label = d['dia'][5:]  # solo MM-DD

            columnas.append(
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                    controls=[
                        ft.Row(
                            spacing=3,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(width=10, height=h_entrada,
                                             bgcolor=Colores.VERDE, border_radius=3),
                                ft.Container(width=10, height=h_salida,
                                             bgcolor=Colores.ROJO, border_radius=3),
                            ]
                        ),
                        ft.Text(dia_label, size=9, color=Colores.GRIS),
                    ]
                )
            )

        leyenda = ft.Row(
            spacing=16,
            controls=[
                ft.Row(spacing=4, controls=[
                    ft.Container(width=10, height=10, bgcolor=Colores.VERDE, border_radius=2),
                    ft.Text("Entradas", size=11, color=Colores.GRIS),
                ]),
                ft.Row(spacing=4, controls=[
                    ft.Container(width=10, height=10, bgcolor=Colores.ROJO, border_radius=2),
                    ft.Text("Salidas", size=11, color=Colores.GRIS),
                ]),
            ]
        )

        return ft.Container(
            padding=16,
            border_radius=12,
            bgcolor=Colores.BLANCO,
            shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.08)"),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text("Actividad Ultimos 7 Dias", size=15,
                            weight=ft.FontWeight.BOLD, color=Colores.NEGRO),
                    leyenda,
                    ft.Divider(color=Colores.GRIS_CLARO),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                        spacing=8,
                        controls=columnas
                    ),
                ]
            )
        )


# ──────────── CAMPOS Y BOTONES ────────────

class CampoTexto:
    @staticmethod
    def crear(label, icon=None, multilinea=False, width=300, password=False) -> ft.TextField:
        return ft.TextField(
            label=label,
            prefix_icon=icon,
            multiline=multilinea,
            max_lines=3 if multilinea else None,
            width=width,
            border_radius=10,
            password=password,
            can_reveal_password=password,
        )


class Boton:
    @staticmethod
    def primario(texto, on_click, ancho=300) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            text=texto, bgcolor=Colores.AZUL_PRIMARIO, color=Colores.BLANCO,
            width=ancho,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(vertical=12),
            ),
            on_click=on_click
        )

    @staticmethod
    def secundario(texto, on_click, ancho=300) -> ft.OutlinedButton:
        return ft.OutlinedButton(
            text=texto, width=ancho,
            style=ft.ButtonStyle(
                side=ft.BorderSide(2, Colores.AZUL_PRIMARIO),
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(vertical=12),
            ),
            on_click=on_click
        )

    @staticmethod
    def peligro(texto, on_click, ancho=150) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            text=texto, bgcolor=Colores.ROJO, color=Colores.BLANCO,
            width=ancho,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(vertical=10),
            ),
            on_click=on_click
        )


# ──────────── PESTANAS ────────────

class PestanaUI:
    def __init__(self, nombres: list):
        self.nombres = nombres
        self.botones = []

    def crear_botones(self, callback) -> list:
        self.botones = []
        for i, nombre in enumerate(self.nombres):
            btn = ft.ElevatedButton(
                text=nombre,
                bgcolor=Colores.AZUL_PRIMARIO if i == 0 else Colores.BLANCO,
                color=Colores.BLANCO if i == 0 else Colores.GRIS,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                on_click=lambda e, idx=i: callback(idx),
            )
            self.botones.append(btn)
        return self.botones

    def actualizar_activa(self, indice: int):
        for i, btn in enumerate(self.botones):
            btn.bgcolor = Colores.AZUL_PRIMARIO if i == indice else Colores.BLANCO
            btn.color = Colores.BLANCO if i == indice else Colores.GRIS

    def crear_barra(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(self.botones, spacing=8, scroll=ft.ScrollMode.AUTO),
            bgcolor=Colores.BLANCO,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border=ft.Border(bottom=ft.BorderSide(1, Colores.AZUL_CLARO)),
        )


# ──────────── NOTIFICACIONES ────────────

class Notificacion:
    @staticmethod
    def mostrar(page: ft.Page, mensaje: str, es_error=False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje, color=Colores.BLANCO),
            bgcolor=Colores.ROJO if es_error else Colores.VERDE,
            duration=3000,
        )
        page.snack_bar.open = True
        page.update()


# ──────────── TIPOGRAFIA ────────────

class Tipografia:
    @staticmethod
    def titulo_principal(texto) -> ft.Text:
        return ft.Text(texto, size=32, weight=ft.FontWeight.BOLD, color=Colores.NEGRO)

    @staticmethod
    def titulo_seccion(texto) -> ft.Text:
        return ft.Text(texto, size=22, weight=ft.FontWeight.BOLD, color=Colores.NEGRO)

    @staticmethod
    def subtitulo(texto) -> ft.Text:
        return ft.Text(texto, size=14, color=Colores.GRIS)

    @staticmethod
    def body(texto) -> ft.Text:
        return ft.Text(texto, size=14, color=Colores.NEGRO)
