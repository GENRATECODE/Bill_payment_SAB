
import flet as ft

def SettingsView(page):
    
    def toggle_dark_mode(e):
        if page.theme_mode == "dark":
            page.theme_mode = "light"
            page.update()
        else: 
            page.theme_mode = "dark"
            page.update()

    def exit_app(e):
        e.page.client_storage.clear()
        page.window_destroy()

    def close_session(e):
        e.page.client_storage.clear()
        page.go("/login")
    
    content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("My Settings", size=30), 
                        ft.IconButton(icon=ft.Icons.SETTINGS_ROUNDED, icon_size=30),

                        ], 
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.TextButton("Light/Dark Mode", icon=ft.Icons.WB_SUNNY_OUTLINED, on_click=toggle_dark_mode),
                                ft.TextButton("Close Session", icon=ft.Icons.LOGOUT, icon_color="red", on_click=close_session),
                                ft.TextButton("Exit Application", icon=ft.Icons.CLOSE, icon_color="red", on_click=exit_app)
                            ],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            spacing=50,alignment=ft.MainAxisAlignment.CENTER
        )
    
                        
    
    return content