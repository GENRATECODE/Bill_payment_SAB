# Home page class
import flet as ft
from flet import *
class Page:
    def __init__(self, app):
        self.app = app
        super().__init__()
    def build(self):
        raise NotImplementedError("This method should be overridden by subclasses")
    
class HomePage(Page):
    def __init__(self, app, state):
        super().__init__(app)
        self.app=app
        self.state=state
        self.app.page.vertical_alignment = ft.MainAxisAlignment.START
    def build(self):
        return Container(content=ft.Column([
            ft.Text("Welcome to the Home Page:->"*10,color="red"),
            ft.ElevatedButton("Go to Profile", on_click=self.navigate_to_profile),
            # ft.TextField(value=self.state.name, label="Enter your name",
                        #  on_change=self.update_name
                        #  )
          
        ],alignment=ft.MainAxisAlignment.START),padding=ft.padding.all(15),
            margin=ft.margin.all(0),height=self.app.page.window.height)

    def update_name(self, e):
        self.state.name = e.control.value

    def navigate_to_profile(self, e):
        self.app.router.set_route("/profile")
