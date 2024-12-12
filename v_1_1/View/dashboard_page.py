import flet as ft

class DashboardPage:
    def __init__(self, app,state):
        self.app = app
        self.state=state
    def build(self):
        return ft.Text("Welcome to the Dashboard",color="red")
