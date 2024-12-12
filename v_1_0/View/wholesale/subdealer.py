import flet as ft
from View.logo import invoice_logo
import time
class SubDealer(ft.Container):
    def __init__(self,app_layout, page):
        self.app_layout=app_layout
        super().__init__()
        self.page = page
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        self.app_layout=app_layout
        self.app_layout.page.auto_scroll=True
        
        # self.content=self.layout#ft.Column([self.layout,],alignment=ft.MainAxisAlignment.START,scroll=ft.ScrollMode.ADAPTIVE)    
        customer_tab = ft.Tab(
            text="Customer Detail",
            tab_content=ft.Row([ft.Text("Customer Detail",size=24),],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            # content=colleation_tab_fun(self,self.page)
        ) 
        customer_mode_tab = ft.Tab(
            text="Customers ",
            tab_content=ft.Row([ft.Text("Modification",size=24),],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            # content=payment_tab_fun(self,self.page)
        ) 
        customer_analytical_tab = ft.Tab(
            text="Stock",
            tab_content=ft.Row([ft.Text("Current Stock",size=24),],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            # content=payment_tab_fun(self,self.page)
        )         
        self.tabs_d=ft.Tabs(
            # selected_index=0,
            selected_index=0,
            tabs=[customer_tab,customer_mode_tab,customer_analytical_tab ],
            expand=True,
            divider_color="#608BC1",
            animation_duration=300,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER,
            indicator_tab_size=True,
            scrollable=False,
            tab_alignment=ft.TabAlignment.FILL,
            unselected_label_color="#FA4032",
            unselected_label_text_style=ft.TextStyle(
                size=16,
                italic=True,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color='#FF4545',
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER,
                )
            )
        )
        self.content=self.tabs_d 
        self.expand=True
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