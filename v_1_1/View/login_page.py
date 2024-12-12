import flet as ft

class LoginPage:
    def __init__(self, app):
        self.app = app

    def build(self):
        return ft.Column([
            ft.Text("Login Page"),
            ft.TextField(label="Username"),
            ft.TextField(label="Password"),
            ft.ElevatedButton("Login", on_click=self.login),
        ], alignment=ft.MainAxisAlignment.CENTER)

    def login(self, e):
        # On successful login, navigate to the home page
        self.app.router.set_route("/home")
