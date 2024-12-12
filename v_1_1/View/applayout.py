import flet as ft
from View.Appbar import CustomAppBar
import flet as ft
from View.side_nav import SideNav
class AppLayout:
    def __init__(self, app):
        self.app = app
        self.side_nav_visible = True  # Sidebar initially visible
        self.side_nav_width = 256 #self.app.page.window.width//4 if self.side_nav_visible else 0# Width of the sidebar

    def build(self, current_page):
        # Build AppBar
        app_bar = CustomAppBar(self.app).build()

        # Build SideNav (animated)
        side_nav = self.build_side_nav() if self.side_nav_visible else None

        # Build Content Area
        content_area = ft.Container(
            content=current_page.build(),
            expand=True,
            bgcolor=ft.colors.WHITE,
        )

        # Layout Row (with animated Sidebar)
        if side_nav:
            layout = ft.Row([
                ft.Container(
                    content=side_nav,
                    width=self.side_nav_width if self.side_nav_visible else 0,
                    # duration=500,  # Animation duration in milliseconds
                    animate=ft.animation.Animation(10000000, ft.AnimationCurve.BOUNCE_OUT)
                ),
                content_area
            ], expand=True)
        else:
            layout = ft.Row([content_area], expand=True)
        self.app.page.appbar=app_bar
        # Return AppBar and Layout as Page Controls
        return ft.Column([layout], expand=True)

    def build_side_nav(self):
        return SideNav(self.app).build()

    def toggle_side_nav(self):
        self.side_nav_visible = not self.side_nav_visible
        self.app.update_view()  # Call the app's update_view to re-render the layout
