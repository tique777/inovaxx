git init"""
main.py - Punto de entrada de InnovaX
Controlador de navegacion entre pantallas
"""
import flet as ft
from screens import PantallaInicio, PantallaLogin, PanelEmpleado, PanelAdministrador
from ui_components import Colores


class App:
    """Controla la navegacion entre pantallas"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.usuario_actual = None
        self._configurar_pagina()
        self._ir_inicio()

    def _configurar_pagina(self):
        self.page.title = "InnovaX - Gestion de Inventario"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = Colores.GRIS_MUY_CLARO
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.window_width = 1400
        self.page.window_height = 900

    def _limpiar(self):
        self.page.controls.clear()
        self.page.update()

    def _ir_inicio(self):
        self._limpiar()
        pantalla = PantallaInicio(self.page, on_ir_login=lambda e: self._ir_login())
        self.page.add(pantalla.construir())
        self.page.update()

    def _ir_login(self):
        self._limpiar()
        pantalla = PantallaLogin(
            self.page,
            on_login=self._procesar_login,
            on_ir_inicio=lambda e: self._ir_inicio()
        )
        self.page.add(pantalla.construir())
        self.page.update()

    def _procesar_login(self, usuario):
        self.usuario_actual = usuario
        self._limpiar()

        # Datos del usuario como dict para pasar a los paneles
        datos_usuario = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            'rol': usuario.rol,
        }

        if usuario.es_admin():
            panel = PanelAdministrador(
                self.page, datos_usuario,
                on_cerrar_sesion=lambda e: self._cerrar_sesion()
            )
        else:
            panel = PanelEmpleado(
                self.page, datos_usuario,
                on_cerrar_sesion=lambda e: self._cerrar_sesion()
            )

        self.page.add(panel.construir())
        self.page.update()

    def _cerrar_sesion(self):
        self.usuario_actual = None
        self._ir_inicio()


def main(page: ft.Page):
    App(page)


if __name__ == "__main__":
    ft.app(target=main)
