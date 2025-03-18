from flet import (
    UserControl,
    Column,
    Container,
    IconButton,
    Row,
    Text,
    IconButton,
    NavigationRail,
    NavigationRailDestination,
    TextField,
    alignment,
    border_radius,
    colors,
    icons,
    padding,
    margin,
)
import flet as ft
import math
from datetime import date
class Sidebar_tax(ft.Container):

    def __init__(self, app_layout, page, *args,**kwargs):
        super().__init__()
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.page=page
        self.today = date.today()
        # self.app_layout.page.on_resized=self.on_resize
        self.top_nav_items =[
                NavigationRailDestination(
                label_content=Text("Invoice"),
                label="Invoice",
                icon=icons.TEXT_SNIPPET_OUTLINED,
                selected_icon=icons.TEXT_SNIPPET_OUTLINED,
                
            ),
                NavigationRailDestination(
                label_content=Text("Previous Invoice"),
                label="Previous_Invoice",
                icon=icons.TEXT_SNIPPET_OUTLINED,
                selected_icon=icons.TEXT_SNIPPET_OUTLINED,
                
            ),
            NavigationRailDestination(
                label_content=Text("Transport Detail"),
                label="Transport Detail",
                icon=icons.EMOJI_TRANSPORTATION_ROUNDED,
                selected_icon=icons.EMOJI_TRANSPORTATION_ROUNDED
            ),
          NavigationRailDestination(
                label_content=Text("Daily Spend"),
                label="Daily Spend",
                icon=icons.PERSON,
                selected_icon=icons.PERSON
            ),
            

        ]
        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=ft.Colors.TRANSPARENT,
            extended=True,
            expand=True
            # height=110
        )
        # self.bottom_nav_rail = NavigationRail(
        #     selected_index=None,
        #     label_type="all",
        #     # on_change=self.bottom_nav_change,
        #     extended=True,
        #     expand=True,
        #     bgcolor=colors.BLUE_GREY,
        # )
        self.sidebar_content=Column([
                Row([
                    Text("Workspace"),
                ], alignment="center"),
                # divider
                ft.Divider(color="black",thickness=2),
                self.top_nav_rail,
                # divider
     
                ft.Text("©️ 2024 Raj Distributor"),
                # self.bottom_nav_rail
            ], tight=True,expand=True)     
        self.expand=1
        self.content=self.build()
    def build(self):
        self.view = Container(
            content=self.sidebar_content,
            padding=padding.all(15),
            margin=margin.all(0),
            width=256,
            # height=self.app_layout.page.window.height,
            # expand=True,
            # bgcolor=colors.BLUE_GREY,
            visible=self.nav_rail_visible,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                                        '#475569',
                    '#9ca3af'
                ],
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=math.pi / 3,
            ),
    
            border=ft.border.all(2.5, "purple"),
            border_radius=ft.border_radius.horizontal(10, 10)
        )
        return self.view

    def toggle_nav_rail(self, e):
        self.view.visible = not self.view.visible
        self.view.update()
        self.page.update()

    def top_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        # self.bottom_nav_rail.selected_index = None
        self.top_nav_rail.selected_index = index
        # self.view.update()
        if index == 0:
            print(f"1 to change invoice")
            self.app_layout.change_active_view("invoice_r")
            # self.page.route = "/members"
        elif index == 1 :
            print(f"2")
            self.app_layout.change_active_view("old_invoice")
        elif index == 2:
            print(f"3")
            self.app_layout.change_active_view("transport")
            # self.page.route = "/members"
        elif index ==3 :
            print(f"4")
            self.app_layout.change_active_view("Daily_Spend")
        self.page.update()



