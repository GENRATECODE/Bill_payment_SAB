import flet as ft
from View.Appbar import CustomAppBar
from View.side_nav import SideNav
from View.login_page import LoginPage
from View.Home import HomePage
from View.Profile import ProfilePage
from View.dashboard_page import DashboardPage
from View.applayout import AppLayout
import math
class MyApp:
    def __init__(self):
        self.shared_state = SharedState()  # Initialize shared state
        self.router = Router(self)
        self.app_layout=AppLayout(self)
        self.current_page = None
        self.side_nav_visible=True  
    def toggle_sidebar(self):
        self.side_nav_visible = not self.side_nav_visible
        self.update_view()
    def main(self, page: ft.Page):
        self.page = page

        # Set the initial route
        self.router.set_route("/login")
        self.update_view()

    def update_view(self):
        # Clear the page controls and rebuild the layout
        self.page.controls.clear()

        # Get the current page and build the layout
        if isinstance(self.current_page, (HomePage, ProfilePage, DashboardPage)):
            layout = self.app_layout.build(self.current_page)
            self.page.controls.append(layout)
        else:
            # For login or other pages that do not use the AppLayout
            self.page.controls.append(self.current_page.build())

        # Update the page
        self.page.update()
    def on_resize(self,e):
        if self.app_layout.side_nav_visible:
            self.app_layout.update_layout()


class Router:
    def __init__(self, app):
        self.app = app
        self.routes = {
            "/login": LoginPage,
            "/home": HomePage,
            "/profile": ProfilePage,
            "/dashboard": DashboardPage,
        }

    def set_route(self, route):
        if route in self.routes:
            # Only pass the app for LoginPage, and both app and state for other pages
            if route == "/login":
                self.app.current_page = self.routes[route](self.app)  # Only pass app
            else:
                self.app.current_page = self.routes[route](self.app, self.app.shared_state)  # Pass both app and state
            self.app.update_view()
        else:
            print(f"Route '{route}' not found")

            
class SharedState:
    def __init__(self):
        self.name="Admin"
        self.username = ""
        self.password = ""
        self.current_view = "home"  # Default view can be home

# Run the app
def main(page: ft.Page):  
    theme=ft.Theme()
    theme.page_transitions.windows=ft.PageTransitionTheme.CUPERTINO
    theme.dialog_theme=ft.DialogTheme()
    theme.data_table_theme=ft.DataTableTheme()
    theme.snackbar_theme=ft.SnackBarTheme()
    page.bgcolor = ft.colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(

        gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                    "#A594F9",
                    "#6439FF",
                    "#604CC3",
                    "#0B2F9F",
                    "#ED3EF7",
                    "#185519",
                    "#CB80AB",
                    "#181C14",
                ],
                tile_mode=ft.GradientTileMode.DECAL,
                rotation=math.pi / 7,
            ),
    )
    page.theme=theme
    app = MyApp()
    app.main(page)

ft.app(target=main)
