import flet as ft
from View.logo import invoice_logo
import time
import asyncio
class Old_invoice_app(ft.Container):
    def __init__(self,app_layout, page):
        self.app_layout=app_layout
        super().__init__()
        self.page = page
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        self.app_layout=app_layout
        self.app_layout.page.auto_scroll=True
        
        # self.content=self.layout#ft.Column([self.layout,],alignment=ft.MainAxisAlignment.START,scroll=ft.ScrollMode.ADAPTIVE)    
        
        self.content=ft.Text("Old Invoice")
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
    

        
