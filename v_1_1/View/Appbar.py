import flet as ft
from flet import PopupMenuItem,PopupMenuButton,Text,colors,Container,margin
from View.logo import raj_distributor
import flet as ft

class CustomAppBar:
    def __init__(self, app):
        # self.title = title
        self.app = app
        self.custom_icon = ft.Container(ft.Image(
        src=raj_distributor,
        color_blend_mode=ft.BlendMode.SRC_IN,
        width=24,
        height=24    , tooltip="Menu" ,border_radius=ft.border_radius.all(80)),
        on_click=self.toggle_sidebar
        )
        self.home= PopupMenuItem(
            text="Home", 
            on_click=self.go_home#self.login
            )
        self.login_profile_button = PopupMenuItem(
            text="Log Out", 
            on_click=self.go_logout#self.login
            )
        self.profile_button=PopupMenuItem(
            text="Profile",
            # on_click=lambda _:page.go("/user")
            )
    
        self.appbar_items = [
            self.login_profile_button,
            PopupMenuItem(),  # divider
            self.profile_button,
            PopupMenuItem(),
            PopupMenuItem(text="Settings")
            ]
    def build(self):
        return ft.AppBar(
            leading=self.custom_icon,   
            leading_width=100,
            title=Text(f"🚲 Raj Distributor Billing 🚲", font_family="Pacifico",bgcolor=ft.Colors.YELLOW,
                       size=48, text_align="start",italic=True,color=ft.Colors.RED_ACCENT_400),
     
            center_title=True,
            toolbar_height=75,
            bgcolor=colors.WHITE,   
            actions=[
                Container(
                    content=PopupMenuButton(
                        items=self.appbar_items
                    ),
                    margin=margin.only(left=50, right=25)
                )
            ],
        )
    def toggle_sidebar(self,e):
        self.app.app_layout.toggle_side_nav()
    def go_logout(self,e):
        self.app.router.set_route("/login")
    def go_home(self, e):
        self.app.router.set_route("/home")
    def go_profile(self, e):
        self.app.router.set_route("/profile")

