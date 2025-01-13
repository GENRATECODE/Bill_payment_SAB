import flet as ft
from View.logo import invoice_logo
import time
class Daily_spend_app(ft.Container):
    def __init__(self,app_layout, page):
        self.app_layout=app_layout
        super().__init__()
        self.page = page
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        self.app_layout=app_layout
        self.app_layout.page.auto_scroll=True
        
        # self.content=self.layout#ft.Column([self.layout,],alignment=ft.MainAxisAlignment.START,scroll=ft.ScrollMode.ADAPTIVE)    
        self.first_row= ft.Row([ft.ElevatedButton("ADD", icon="add",on_click=self.add_function),
                                ft.ElevatedButton("Filter",icon="filter"),
                                ])
        self.data_table =  ft.DataTable(  
            columns=[

                ft.DataColumn(ft.Text("Description   ")),
                ft.DataColumn(ft.Text("Category")),
                ft.DataColumn(ft.Text('Where')),
                ft.DataColumn(ft.Text('Amount')),
            ],
            rows=[],bgcolor='#87A2FF',
            show_checkbox_column=True,
            data_row_color={'hovered': "#B8001F"},
            border=ft.border.all(2, 'Black'),
            divider_thickness=1,
            show_bottom_border=True,
            vertical_lines=ft.border.BorderSide(3, 'Black'),
            heading_row_color=ft.Colors.BLACK12,
            heading_row_height=60,
            border_radius=20,
        )
        self.content=ft.Column([self.first_row,
                                self.data_table,],expand=True)   
        self.app_layout.page.update()  

    def add_function(self,e):
        self.app_layout.page.update()
    def filter_function(self,e):
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
    

        
