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
class Sidebar(UserControl):
    def __init__(self,page):
        super().__init__()
        self.page=page
        self.page.on_resized=self.on_resized
        # self.app_layout = app_layout
        self.nav_rail_visible = True
        self.top_nav_items =[
                        NavigationRailDestination(
                label_content=Text("Invoice"),
                label="Invoice",
                icon=icons.TEXT_SNIPPET_OUTLINED,
                selected_icon=icons.TEXT_SNIPPET_OUTLINED,
                
            ),
            NavigationRailDestination(
                label_content=Text("Item Management"),
                label="Item_Management",             
                icon=icons.FORMAT_LIST_BULLETED_ADD,
                selected_icon=icons.FORMAT_LIST_BULLETED_ADD
            ), 

            NavigationRailDestination(
                label_content=Text("Stock Detail"),
                label="Item_Modify",
                icon=icons.PRICE_CHANGE_OUTLINED,
                selected_icon=icons.PRICE_CHANGE_OUTLINED
            ), 
            NavigationRailDestination(
                label_content=Text("Monthly Billing Entry"),
                label="Monthly_Billing_Entry",
                icon=icons.RESTORE_PAGE,
                selected_icon=icons.RESTORE_PAGE
            ),
            NavigationRailDestination(
                label_content=Text("Customer Detail"),
                label="Customer_Detail",
                icon=icons.BOOK_OUTLINED,
                selected_icon=icons.BOOK_OUTLINED
            ), 
            NavigationRailDestination(
                label_content=Text("PartyDetail"),
                label="Members",
                icon=icons.PERSON,
                selected_icon=icons.PERSON
            ), 
            NavigationRailDestination(
                label_content=Text("Dealer Detail"),
                label="Members",
                icon=icons.PERSON,
                selected_icon=icons.PERSON
            ),

        ]
        self.top_nav_rail = NavigationRail(
            selected_index=None,
            label_type=ft.NavigationRailLabelType.SELECTED,
            on_change=self.top_nav_change,
            destinations=self.top_nav_items,
            bgcolor=colors.BLUE,
            extended=True,
            height=self.page.window_height*85/100  
        ) 
        self.bottom_nav_rail = NavigationRail(
            height=self.page.window_height*10/100,
            selected_index=None,
            label_type=ft.NavigationRailLabelType.SELECTED,
            on_change=self.bottom_nav_change,
            extended=True,
            expand=True,

            bgcolor=colors.GREY,
        )
    def build(self):   
        self.view = Container(
            content=Column([
                Row([
                    Text("Workspace"),
                ], alignment="spaceBetween"),
                # divider
                # Container(
                #     bgcolor=colors.BLACK26,
                #     border_radius=border_radius.all(30),
                #     height=1,
                #     alignment=alignment.center_right,
                #     width=0
                # ),
                self.top_nav_rail,
                # divider
                # Container(
                #     bgcolor=colors.BLACK26,
                #     border_radius=border_radius.all(30),
                #     height=1,
                #     alignment=alignment.center_right,
                #     width=420
                # ),
                self.bottom_nav_rail
            ], tight=True),
            padding=padding.all(15),
            margin=margin.all(0),
            width=250,
            expand=True,
            bgcolor=colors.BLUE_GREY,
            visible=self.nav_rail_visible,
        )  
        return self.view
    def top_nav_change(self, e):
        # on_click=lambda _:self.page.go("/invoice")
        if int(e.control.selected_index)==0:
            self.page.go("/invoice")
            self.page.update()
        elif int(e.control.selected_index)==1:
            self.page.go("/item")
            self.page.update()
        else:
            print(f"{e},{e.control.selected_index}")
            print(f"Unexpected argument type in bottom_nav_change: {type(e)}")


    def bottom_nav_change(self, e):
        if isinstance(e, int):
            self.top_nav_rail.selected_index = None
            self.bottom_nav_rail.selected_index = e
        else:
            print(f"Unexpected argument type in bottom_nav_change: {type(e)}")

    def on_resized(self,e):
        self.top_nav_rail.height=self.page.height*80/100 - 100
        self.bottom_nav_rail=self.page.height*10/100
        self.view = self.page.width*30/100
        self.page.update() 