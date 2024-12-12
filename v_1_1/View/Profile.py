import flet as ft
from flet import *

class Page:
    def __init__(self, app):
        self.app = app

    def build(self):
        raise NotImplementedError("This method should be overridden by subclasses")
    
class ProfilePage(Page):
    def __init__(self, app, state):
        super().__init__(app)
        self.app=app
        self.state=state

    def build(self):
        return ft.Column([
            ft.Text(f"Welcome to the Profile Page, {self.state.name}"),
            ft.ElevatedButton("Go to Home", on_click=self.navigate_to_home)
        ])

    def navigate_to_home(self, e):
        self.app.router.set_route("/")