import flet as ft
from View.logo import invoice_logo
import time
import asyncio 
import base64 
from View.wholesale.payment_file.collection_tab import colleation_tab_fun
from View.wholesale.payment_file.payment2dealer import payment_tab_fun
class Payment_entry(ft.Container):
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
        # Define Tabs
        with open(r"D:\Bill_payment_SAB\v_1_0\assets\josn_icon\5.json", "rb") as lottie_file:
            lottie_base64_collection = base64.b64encode(lottie_file.read()).decode("utf-8")
        with open(r"D:\Bill_payment_SAB\v_1_0\assets\josn_icon\1.json", "rb") as lottie_file:
            lottie_base64_payment = base64.b64encode(lottie_file.read()).decode("utf-8")
               
        #icon related 
        # lottie_base64_collection= self.User.Lottie_icon('collection')
        # lottie_base64_payment=  self.User.Lottie_icon('payment')
        collection_icon  = ft.Lottie( src_base64=lottie_base64_collection,animate=True, fit='SCALE_DOWN', width=100,  height=100,reverse=True )
        payment_icon = ft.Lottie(src_base64=lottie_base64_payment,animate=True, fit='SCALE_DOWN',  width=100,  height=100,reverse=True )
        collection_tab = ft.Tab(
            text="Collection",
            tab_content=ft.Row([ft.Text("Collection",size=24),collection_icon,],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            content=colleation_tab_fun(self,self.page)
        ) 
        payment_tab = ft.Tab(
            text="Bill Payment",
             tab_content=ft.Row([ft.Text("Bill Payment",size=24),payment_icon,],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            content=payment_tab_fun(self,self.page)
        )        
        self.tabs_d=ft.Tabs(
            # selected_index=0,
            selected_index=0,
            tabs=[ collection_tab, payment_tab ],
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
