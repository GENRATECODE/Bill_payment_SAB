import flet as ft
from View.logo import invoice_logo
import time
from  View.tax.invoice_tab_seceleted import tab_invoice 
import asyncio 

class Invoice_Retail(ft.Container):
    def __init__(self,app_layout, page):
        self.app_layout=app_layout
        super().__init__()
        self.page = page
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        self.app_layout=app_layout
        self.app_layout.page.auto_scroll=True
        self.items=[]
        self.customer_count=1
        # add in asyncio in add flet option 
        
        self.tabs_d=ft.Tabs(
            # selected_index=0,
            expand=True,
            animation_duration=300,tabs=[
                ft.Tab(
                    text=f"First Number",
                    content=tab_invoice (self,self.app_layout),
                    tab_content=ft.Row([ft.Text(f"Invoice"),ft.IconButton(
                    icon=ft.Icons.ADD,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Add New Tap",on_click=self.new
                ),],expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    # tab_content=ft.IconButton()
                ),
            ]
            # ,on_click=self.new
            ,scrollable=True
            ,tab_alignment=ft.TabAlignment.START
        )
        self.content=self.tabs_d 
        # self.expand=True
        self.app_layout.page.update()  
    def new(self, e):
        self.customer_count += 1
        new_tab_index = len(self.tabs_d.tabs)

    # Correctly creating the new tab without referencing 'new_tab' in its content
        new_tab = ft.Tab(
        text=f"{self.customer_count}",
        content=tab_invoice(self, self.app_layout),  # Assuming you want to create a new tab with similar content
        tab_content=ft.Row([
            ft.Text(f"New Portal {self.customer_count}"),
            ft.IconButton(
                icon=ft.Icons.CLOSE,
                icon_color="red",
                icon_size=20,
                tooltip="Close Tab", on_click=self.tab_update
            ),
        ], expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        self.tabs_d.tabs.append(new_tab)
        self.tabs_d.selected_index = new_tab_index
    
        self.app_layout.page.update()

    def tab_update(self, e):
    # Prevent deletion of the first tab (index 0)
        print(f"Number of Tab {len(self.tabs_d.tabs)}" )
        if len(self.tabs_d.tabs) == 1:
        # If there is only one tab, display a message and don't delete
            self.snack_bar_func("Main Tab cannot be closed")
            return

        if self.tabs_d.selected_index == 0:
            # If the selected tab is the first tab, display a message and don't delete
            self.snack_bar_func("Main Tab cannot be closed")
            return
        else:
        # If it's not the first tab, allow deletion
            del self.tabs_d.tabs[-1]
            self.customer_count -=1
            # self.tabs_d.tabs.remove()
            self.snack_bar_func("Tab closed")
    
    # Update the layout after deletion
        self.app_layout.page.update()

 
    def snack_bar_func(self,text):
        
        snack_bar=ft.SnackBar(
            content=ft.Text(text),
            action="Alright!",
            action_color="Pink",
            dismiss_direction=ft.DismissDirection.HORIZONTAL 
        )
        # self.page.snack_bar=snack_bar
        self.page.overlay.clear()
        self.page.overlay.append(snack_bar)
        snack_bar.open=True
        self.app_layout.page.update() 
