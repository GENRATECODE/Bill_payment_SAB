import flet as ft
from flet import PopupMenuItem,PopupMenuButton,Text,colors,Container,margin
from View.logo import raj_distributor
from View.sidebar_app import Sidebar


def NavBar_for(page):
    sidebar=Sidebar(page)
    def hide_unhide(e):
        sidebar.visible = not sidebar.visible
    page.update()
    custom_icon = ft.Container(ft.Image(
        src=raj_distributor,
        color_blend_mode=ft.BlendMode.SRC_IN,
        width=24,
        height=24    , tooltip="Menu" ,border_radius=ft.border_radius.all(80)),
        on_click=hide_unhide
        )
    home= PopupMenuItem(
            text="Home", 
            on_click=lambda _:page.go("/item")#self.login
            )
    login_profile_button = PopupMenuItem(
            text="Log Out", 
            on_click=lambda _:page.go("/login")#self.login
            )
    profile_button=PopupMenuItem(
            text="Profile",
            on_click=lambda _:page.go("/user")
        )
    
    appbar_items = [
            login_profile_button,
            PopupMenuItem(),  # divider
            profile_button,
            PopupMenuItem(),
            PopupMenuItem(text="Settings")
        ]
    appbar = ft.AppBar(
            leading=custom_icon,   
            leading_width=100,
            title=Text(f"🚲 Raj Distributor Billing 🚲", font_family="Pacifico",bgcolor=ft.colors.YELLOW,
                       size=48, text_align="start",italic=True,color=ft.colors.RED_ACCENT_400),
            center_title=True,
            toolbar_height=75,
            bgcolor=colors.WHITE,   
            actions=[
                Container(
                    content=PopupMenuButton(
                        items=appbar_items
                    ),
                    margin=margin.only(left=50, right=25)
                )
            ],
        )
    return appbar