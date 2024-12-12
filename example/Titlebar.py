import flet as ft

class TitleBar(ft.Row):
    def __init__(self):
        super().__init__()
        self.isolated = True
        self.spacing =0
        self.controls = [
            ft.WindowDragArea(self._create_drag_area(), expand=True, maximizable=False),
            self._create_control_panel(),
        ]

    def _create_drag_area(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(width=2),
                    ft.Icon(ft.icons.ALL_INCLUSIVE_OUTLINED, color=ft.colors.WHITE54),
                    ft.Text("All-Tools",color=ft.colors.WHITE54),
                ],
                spacing=15,
            ),
            bgcolor=ft.colors.TRANSPARENT,
            height=35,
        )

    def _create_control_panel(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    self._create_control_button("一", self._window_minimize, ft.colors.BLUE_400),
                    self._create_control_button("☐", self._window_maximize, ft.colors.BLUE_400),
                    self._create_control_button("✕", self._window_close, ft.colors.RED_400),
                ],
                spacing=0,
            ),
            bgcolor=ft.colors.TRANSPARENT,theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.colors.WHITE))
        )

    def _create_control_button(self, text, on_click, hover_color):
        return ft.Container(
            content=ft.ElevatedButton(
                text=text,
                elevation=0,
                height=35,
                on_click=on_click,
                on_hover=lambda e: self._on_hover(e, hover_color),
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
                bgcolor=ft.colors.TRANSPARENT,
                color=ft.colors.WHITE,
            )
        )

    def _window_minimize(self, _):
        self.page.window.minimized = True
        self.page.update()

    def _window_maximize(self, e):
        self.page.window.maximized = not self.page.window.maximized
        e.control.text = "❐" if self.page.window.maximized else "☐"
        self.page.update()

    def _window_close(self, _):
        self.page.window.close()

    def _on_hover(self, e, hover_color):
        e.control.bgcolor = hover_color if e.data == "true" else ft.colors.TRANSPARENT
        e.control.update()
