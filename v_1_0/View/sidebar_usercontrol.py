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
import asyncio
import flet as ft
import math
from datetime import date

class Sidebar(ft.Container):

    def __init__(self, app_layout, page, *args,**kwargs):
        super().__init__()
        self.app_layout = app_layout
        self.nav_rail_visible = True
        self.page=page
        self.expand=2
        self.text_nav_style=ft.TextStyle( word_spacing=5,color="#6A1E55",weight=ft.FontWeight.BOLD,size=11,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
        # self.app_layout.page.on_resized=self.on_resize
        self.top_nav_items =[
                        NavigationRailDestination(
                label_content=Text("Dashboard",style=self.text_nav_style),
                label="Dashboard",
                icon=icons.SPACE_DASHBOARD_ROUNDED,
                selected_icon=icons.SPACE_DASHBOARD_ROUNDED,
                
            ),
               NavigationRailDestination(
                label_content=Text("Invoice",style=self.text_nav_style),
                label="Invoice",
                icon=icons.TEXT_SNIPPET_OUTLINED,
                selected_icon=icons.TEXT_SNIPPET_OUTLINED,
                
            ),
                              NavigationRailDestination(
                label_content=Text("Old Invoice ",style=self.text_nav_style),
                label="Previous_Invoice",
                icon=icons.TEXT_SNIPPET_OUTLINED,
                selected_icon=icons.TEXT_SNIPPET_OUTLINED,
                
            ),
            NavigationRailDestination(
                label_content=Text("Stock",style=self.text_nav_style),
                label="Stock Management",             
                icon=icons.FORMAT_LIST_BULLETED_ADD,
                selected_icon=icons.FORMAT_LIST_BULLETED_ADD
            ), 
                        

            NavigationRailDestination(
                label_content=Text("Transport Detail",style=self.text_nav_style),
                label="Transport Detail",
                icon=icons.EMOJI_TRANSPORTATION_ROUNDED,
                selected_icon=icons.EMOJI_TRANSPORTATION_ROUNDED
            ),
            NavigationRailDestination(
                label_content=Text("Dealer Detail",style=self.text_nav_style),
                label="Dealer Detail",
                icon=icons.BOOK_OUTLINED,
                selected_icon=icons.BOOK_OUTLINED
            ), 
            NavigationRailDestination(
                label_content=Text("Customer",style=self.text_nav_style),
                label="SubDealer Detail",
                icon=icons.MY_LIBRARY_BOOKS,
                selected_icon=icons.MY_LIBRARY_BOOKS
            ), 

            NavigationRailDestination(
                label_content=Text("Payment Detail",style=self.text_nav_style),
                label="Payment Detail",
                icon=icons.PERSON,
                selected_icon=icons.PERSON
            ),            NavigationRailDestination(
                label_content=Text("Daily Spend",style=self.text_nav_style),
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
        self.app_layout.page.update()

    async def top_nav_change(self, e):
        index = e if (type(e) == int) else e.control.selected_index
        # self.bottom_nav_rail.selected_index = None
        self.top_nav_rail.selected_index = index
        # self.view.update()
        if index == 0:
            print(f"0")
            self.app_layout.change_active_view("Dashboard")
            # self.page.route = "/boards"
        elif index == 1:
            print(f"1")
            self.app_layout.change_active_view("invoice_w")
            # self.page.route = "/members"
        elif index ==2 :
            print(f"2")
            self.app_layout.change_active_view("previous_invoice")
        elif index == 3:
            print(f"3")
            self.app_layout.change_active_view("Item_Management")
            # self.page.route = "/members"
        elif index ==4 :
            print(f"4")
            self.app_layout.change_active_view("transport")
        elif index ==5 :
            print(f"5")
            self.app_layout.change_active_view("Dealer")
            # self.page.route = "/members"
        elif index == 6:
            print(f"6")
            self.app_layout.change_active_view("SubDealer")
        elif index == 7:
            print(f"7")
            self.app_layout.change_active_view("payment")
            # self.page.route = "/members"
        elif index == 8:
            print(f"8")
            self.app_layout.change_active_view("Daily_spend_app")

            # self.page.route = "/members"
        # self.app_layout.page.update()
    # def on_resize(self,width,height):
    #     self.view.width =  256
    #     # self.sidebar_content.height=self.app_layout.page.window.height
    #     self.view.height=height
    #     # self.view.update()


