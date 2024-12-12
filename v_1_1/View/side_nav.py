import flet as ft
from flet import NavigationRailDestination,Text,icons,NavigationRail,Column,Row
import math
class SideNav:
    def __init__(self, app):
        self.app = app
        super().__init__()
        self.top_nav_items =[
            NavigationRailDestination(
                label_content=Text("Dashboard"),
                label="Dashboard",
                icon=icons.SPACE_DASHBOARD_ROUNDED,
                selected_icon=icons.SPACE_DASHBOARD_ROUNDED,
                
            ),
            NavigationRailDestination(
                label_content=Text("Invoice"),
                label="Invoice",
                icon=icons.TEXT_SNIPPET_OUTLINED,
                selected_icon=icons.TEXT_SNIPPET_OUTLINED,
                
            ),
                NavigationRailDestination(
                label_content=Text("Previous Invoice "),
                label="Previous_Invoice",
                icon=icons.TEXT_SNIPPET_OUTLINED,
                selected_icon=icons.TEXT_SNIPPET_OUTLINED,
                
            ),
            NavigationRailDestination(
                label_content=Text("Stock Management"),
                label="Stock Management",             
                icon=icons.FORMAT_LIST_BULLETED_ADD,
                selected_icon=icons.FORMAT_LIST_BULLETED_ADD
            ), 
                        NavigationRailDestination(
                label_content=Text("Stock Detail"),
                label="Stock Detail For Specific Item",             
                icon=icons.FORMAT_LIST_BULLETED_ADD,
                selected_icon=icons.FORMAT_LIST_BULLETED_ADD
            ), 


            NavigationRailDestination(
                label_content=Text("Transport Detail"),
                label="Transport Detail",
                icon=icons.EMOJI_TRANSPORTATION_ROUNDED,
                selected_icon=icons.EMOJI_TRANSPORTATION_ROUNDED
            ),
            NavigationRailDestination(
                label_content=Text("Dealer Detail"),
                label="Dealer Detail",
                icon=icons.BOOK_OUTLINED,
                selected_icon=icons.BOOK_OUTLINED
            ), 
            NavigationRailDestination(
                label_content=Text("SubDealer Detail"),
                label="SubDealer Detail",
                icon=icons.MY_LIBRARY_BOOKS,
                selected_icon=icons.MY_LIBRARY_BOOKS
            ), 

            NavigationRailDestination(
                label_content=Text("Payment Detail"),
                label="Payment Detail",
                icon=icons.PERSON,
                selected_icon=icons.PERSON
            ),            NavigationRailDestination(
                label_content=Text("Daily Spend"),
                label="Daily Spend",
                icon=icons.PERSON,
                selected_icon=icons.PERSON
            ),
            

        ]
        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type="all",
            on_change=self.on_nav_change,
            destinations=self.top_nav_items,
            bgcolor=ft.colors.TRANSPARENT,
            extended=True,
            expand=True
            # height=110
        )
        self.sidebar_content=Column([
                Row([
                    Text("Workspace"),
                ], alignment="center"),
                # divider
                ft.Divider(color="black",thickness=2),
                self.top_nav_rail,
                # divider

                # self.bottom_nav_rail
            ], tight=True,)        
    def build(self):
        return ft.Container(content=self.sidebar_content,
                            padding=ft.padding.all(15),
            margin=ft.margin.all(0),
            width=256,
            height=self.app.page.window.height,
            expand=True,
            # extended=True,
                gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                    "0xff1f005c",
                    "0xff5b0060",
                    "0xff870160",
                    "0xffac255e",
                    "0xffca485c",
                    "0xffe16b5c",
                    "0xfff39060",
                    "0xffffb56b",
                ],
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=math.pi / 3,
            ),
    
            border=ft.border.all(2.5, "purple"),
            border_radius=ft.border_radius.horizontal(10, 10))

    def on_nav_change(self, e):
        if e.control.selected_index == 0:
            self.app.router.set_route("/home")
        elif e.control.selected_index == 1:
            self.app.router.set_route("/profile")
        elif e.control.selected_index == 2:
            self.app.router.set_route("/dashboard")
