import flet as ft
from flet import DataTable,TextField, DataColumn, DataRow, DataCell, Text, ControlState, BorderSide, RoundedRectangleBorder

from Model.items import Item
from flet import DataTable,Container,Dropdown,TextField, ElevatedButton
from Controller.invoice_option_tax import WInvoice
import win32print
import os
import win32api
from Model.type_item import items_type
class text_filed_style(TextField):
    def __init__(self, label=None, capitalizationn=None, hint_text=None, 
                 prefix_text=None, leng=None, col1=None, on_change=None, 
                 value=None, input_filter=None,on_click=None, suffix=None, prefix_icon=None, 
                 kbtype=None, **kwargs):  # Add **kwargs
        super().__init__(**kwargs)
        self.label = label
        self.keyboard_type = kbtype
        self.input_filter=input_filter
        self.capitalization = capitalizationn
        self.hint_text = hint_text
        self.prefix_text = prefix_text
        self.max_length = leng
        self.value = value
        self.col = col1
        self.on_change = on_change
        self.on_click = on_click
        self.suffix = suffix
        self.prefix_icon = prefix_icon
        
        # Style properties
        # self.width = 200
        self.cursor_color = "#1A1A1D"
        self.focused_color = "#3B1E54"
        self.focused_bgcolor = "#C6E7FF"
        self.border_color = "#1A1A1D"
        self.color = "#1A1A1D"
        self.bgcolor = "#EBEAFF"
        self.border_radius = ft.border_radius.all(10)
        
        # Label style
        self.label_style = ft.TextStyle(
            word_spacing=5,
            color="#6A1E55",
            size=16,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.SOLID,
            ),
        )
        
class dropdown(Dropdown):
    def __init__(self,label,  hint_text,**kwargs):
        super().__init__(**kwargs)
        self.label=label
        self.hint_text=hint_text
        self.counter_style=counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,))
        self.border_radius=ft.border_radius.all(10)
        self.border_color="#1A1A1D"
        self.bgcolor="#EBEAFF"
        self.color="#1A1A1D"
        self.focused_bgcolor="#C6E7FF"
        self.focused_color="#3B1E54"
        self.select_icon_enabled_color="red"
        self.label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,))
        
class button_style(ElevatedButton):
    def __init__(self, on_click=None, text=None, bgcolor=None,**kwargs):  # Fix kwargs
        super().__init__(**kwargs)
        self.on_click = on_click
        self.text = text
        
        # Button style
        self.style = ft.ButtonStyle(
            animation_duration=290,
            color={
                ft.ControlState.HOVERED: "#3D3BF3",  # Light blue text on hover
                ft.ControlState.FOCUSED: "#000000",  # Cyan text on focus
            },
            bgcolor={
                "": bgcolor if bgcolor else "#FF2929",  # Default background color
                ft.ControlState.HOVERED: "#000000",  # Black background on hover
            },
            elevation={"pressed": 0, "": 1},
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(1, "#1D24CA"),
                ft.ControlState.HOVERED: ft.BorderSide(1, "#40A2D8"),
            },
            shape={
                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=12),
            },
        )

class stock_detail(Container):
    def __init__(self, app_layout,page, **kwargs):
        super().__init__(**kwargs)
        # Page Setup something
        self.app_layout=app_layout
        self.page=page
        self.padding = ft.padding.all(0)
        self.margin=ft.margin.all(1)
        self.item_check=dropdown(label="Goods Type",value='All',hint_text="Select Which Good Check Stock",col={"md":3},
                                 options=[
            ft.dropdown.Option(text="ALL",key="all")]
                                 )
        self.option_fun()
        self.item_wight=dropdown(label="Filter",hint_text="Sort by ",col={"md":3},
                                 options=[
            ft.dropdown.Option("All"),                               
            ft.dropdown.Option("Low"),
            ft.dropdown.Option("High"),
        ])
        self.search=button_style(text="Search It",on_click=self.stock_show) # feature add on_click function
        # using Column
        self.result_show=ft.Column(expand=True,alignment=ft.MainAxisAlignment.CENTER,scroll=ft.ScrollMode.ADAPTIVE)
        # Page Item added here below also define layout of page 
        self.content=ft.Column([
                         ft.Row([ ft.Stack(
            [
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Stock Details",
                            ft.TextStyle(
                                size=60,
                                weight=ft.FontWeight.BOLD,
                                foreground=ft.Paint(
                                    color=ft.Colors.BLUE_700,
                                    stroke_width=6,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                ),
                ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Stock Details",
                            ft.TextStyle(
                                size=60,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREY_300,
                            ),
                        ),
                    ],
                ),
            ]
        ),                       
                                        ],alignment=ft.MainAxisAlignment.CENTER ),
                         ft.Divider(color=ft.Colors.TRANSPARENT),
                         ft.Row([self.item_check,self.item_wight,self.search],alignment=ft.MainAxisAlignment.CENTER ),
                         ft.Divider(color=ft.Colors.TRANSPARENT),
                         ft.Row([self.result_show,],alignment=ft.MainAxisAlignment.CENTER) ,
                         
                                ])
        # print test
    def option_fun(self):
        for k,v  in items_type.items():
            self.item_check.options.append(
                ft.dropdown.Option(text=k,key=v)
            )
# self.datatable.rows.append()
    def on_hover_function(self,e):
        # print(f"Hover Event Triggered: {e.data}")
        e.control.bgcolor="#ECE852" if e.data =="true" else ft.Colors.TRANSPARENT
        e.control.update()
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
    def stock_show(self,e): 
        if not self.item_check.value or not self.item_wight.value:
            # Optionally, you can show a message here that both dropdowns need to be selected
            self.snack_bar_func("Please select values in both dropdowns")
            return  # Exit the function if any dropdown is unselected
        
        try:
            count=0
            self.result_show.controls.clear()
            data_access=Item()
            if self.item_wight.value=="All":
                print("All")
                if self.item_check.value=="all":
                    result=data_access.stock_check()
                    self.result_show.controls.append(
                        ft.Row([
        
                            ft.Container(ft.Text("SR",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=1,border_radius=ft.border_radius.only(5,15,20,8),alignment=ft.Alignment(0.0, 0.0), bgcolor="#4335A7", padding=10, width=80),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item ID",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=4,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),bgcolor="#4335A7", padding=10, width=150),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item Description",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=10,alignment=ft.Alignment(0.0, 0.0),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),border_radius=ft.border_radius.only(5,15,20,8), bgcolor="#4335A7", padding=10, width=300),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Stock",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Label",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2, bgcolor="#4335A7", alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),padding=10, width=80,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Company Name",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=6, bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                                # ft.VerticalDivider(),                        ft.VerticalDivider(),
                            ft.Container(ft.Text("Last Update",size=16,weight=ft.FontWeight.BOLD,color='#131010'), expand=3,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                        ]))
                    for i in result:
                        self.result_show.controls.append(ft.Divider())
                        count+=1
                        if  i['stock']<i['reorder_level']:
                            self.style_col=ft.TextStyle( word_spacing=5,color="#C62300",weight=ft.FontWeight.BOLD,size=13 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
                        else:
                            self.style_col=ft.TextStyle( word_spacing=5,color="#22177A",weight=ft.FontWeight.BOLD,size=13 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
                        self.result_show.controls.append(
                            ft.Row([
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{count}",style=self.style_col),expand=1,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=80 ),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_id']}",style=self.style_col),expand=5,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=150),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_description']}",style=self.style_col),expand=11,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=300),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i[ 'stock']}",style=self.style_col), expand=2,bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),

                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['reorder_level']}",style=self.style_col),expand=2, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                # ft.VerticalDivider(),  
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['company_name']}",style=self.style_col),expand=6, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['Update_date']}",style=self.style_col),expand=3, bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),
                                # ft.VerticalDivider(),
                        ])
                            )
                    self.result_show.controls.append(ft.Divider())
                else: 
                    print("specific vlaue123")
                    result=data_access.stock_check_specific(self.item_check.value)
                    self.result_show.controls.append(
                        ft.Row([
    
                            ft.Container(ft.Text("SR",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=1,border_radius=ft.border_radius.only(5,15,20,8),alignment=ft.Alignment(0.0, 0.0), bgcolor="#4335A7", padding=10, width=80),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item ID",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=4,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),bgcolor="#4335A7", padding=10, width=150),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item Description",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=10,alignment=ft.Alignment(0.0, 0.0),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),border_radius=ft.border_radius.only(5,15,20,8), bgcolor="#4335A7", padding=10, width=300),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Stock",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Label",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2, bgcolor="#4335A7", alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),padding=10, width=80,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Company Name",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=6, bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                                # ft.VerticalDivider(),                        ft.VerticalDivider(),
                            ft.Container(ft.Text("Last Update",size=16,weight=ft.FontWeight.BOLD,color='#131010'), expand=3,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                        ]))
                    for i in result:
                        self.result_show.controls.append(ft.Divider())
                        count+=1
                        if  i['stock']<i['reorder_level']:
                            self.style_col=ft.TextStyle( word_spacing=5,color="#C62300",weight=ft.FontWeight.BOLD,size=13 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
                        else:
                            self.style_col=ft.TextStyle( word_spacing=5,color="#22177A",weight=ft.FontWeight.BOLD,size=13 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
                        self.result_show.controls.append(
                            ft.Row([
        
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{count}",style=self.style_col),expand=1,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=80 ),
                                # ft.VerticalDivider(),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_id']}",style=self.style_col),expand=5,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=150),
                                # ft.VerticalDivider(),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_description']}",style=self.style_col),expand=11,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=300),
                                # ft.VerticalDivider(),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i[ 'stock']}",style=self.style_col), expand=2,bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),
                                # ft.VerticalDivider(),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['reorder_level']}",style=self.style_col),expand=2, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                # ft.VerticalDivider(),  
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['company_name']}",style=self.style_col),expand=6, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['Update_date']}",style=self.style_col),expand=3, bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),
                                # ft.VerticalDivider(),
                        ])
                            )
                    self.result_show.controls.append(ft.Divider())
            elif self.item_wight.value=="Low":
                print("All")
                if self.item_check.value=="all":
                    result=data_access.stock_check()
                    self.result_show.controls.append(
                        ft.Row([
        
                            ft.Container(ft.Text("SR",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=1,border_radius=ft.border_radius.only(5,15,20,8),alignment=ft.Alignment(0.0, 0.0), bgcolor="#4335A7", padding=10, width=80),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item ID",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=4,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),bgcolor="#4335A7", padding=10, width=150),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item Description",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=10,alignment=ft.Alignment(0.0, 0.0),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),border_radius=ft.border_radius.only(5,15,20,8), bgcolor="#4335A7", padding=10, width=300),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Stock",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Label",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2, bgcolor="#4335A7", alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),padding=10, width=80,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Company Name",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=6, bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                                # ft.VerticalDivider(),                        ft.VerticalDivider(),
                            ft.Container(ft.Text("Last Update",size=16,weight=ft.FontWeight.BOLD,color='#131010'), expand=3,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                        ]))
                    for i in result:
                        
                        count+=1
                        if  i['stock']<i['reorder_level']:
                            self.result_show.controls.append(ft.Divider())
                            self.style_col=ft.TextStyle( word_spacing=5,color="#C62300",weight=ft.FontWeight.BOLD,size=13 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
                            self.result_show.controls.append(
                            ft.Row([
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{count}",style=self.style_col),expand=1,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=80 ),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_id']}",style=self.style_col),expand=5,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=150),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_description']}",style=self.style_col),expand=11,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=300),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i[ 'stock']}",style=self.style_col), expand=2,bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),

                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['reorder_level']}",style=self.style_col),expand=2, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                # ft.VerticalDivider(),  
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['company_name']}",style=self.style_col),expand=6, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['Update_date']}",style=self.style_col),expand=3, bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),
                                # ft.VerticalDivider(),
                            ])
                            )
                    self.result_show.controls.append(ft.Divider())
                else: 
                    print("specific vlaue ")
                    result=data_access.stock_check_specific(self.item_check.value)
                    self.result_show.controls.append(
                        ft.Row([
    
                            ft.Container(ft.Text("SR",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=1,border_radius=ft.border_radius.only(5,15,20,8),alignment=ft.Alignment(0.0, 0.0), bgcolor="#4335A7", padding=10, width=80),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item ID",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=4,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),bgcolor="#4335A7", padding=10, width=150),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item Description",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=10,alignment=ft.Alignment(0.0, 0.0),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),border_radius=ft.border_radius.only(5,15,20,8), bgcolor="#4335A7", padding=10, width=300),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Stock",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Label",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2, bgcolor="#4335A7", alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),padding=10, width=80,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Company Name",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=6, bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                                # ft.VerticalDivider(),                        ft.VerticalDivider(),
                            ft.Container(ft.Text("Last Update",size=16,weight=ft.FontWeight.BOLD,color='#131010'), expand=3,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                        ]))
                    self.result_show.controls.append(ft.Divider())
                    for i in result:
                        
                        count+=1
                        if  i['stock']<i['reorder_level']:
                            self.style_col=ft.TextStyle( word_spacing=5,color="#C62300",weight=ft.FontWeight.BOLD,size=13 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
                            self.result_show.controls.append(
                            ft.Row([
        
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{count}",style=self.style_col),expand=1,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=80 ),
                                # ft.VerticalDivider(),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_id']}",style=self.style_col),expand=5,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=150),
                                # ft.VerticalDivider(),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_description']}",style=self.style_col),expand=11,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=300),
                                # ft.VerticalDivider(),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i[ 'stock']}",style=self.style_col), expand=2,bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),
                                # ft.VerticalDivider(),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['reorder_level']}",style=self.style_col),expand=2, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                # ft.VerticalDivider(),  
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['company_name']}",style=self.style_col),expand=6, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['Update_date']}",style=self.style_col),expand=3, bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),
                                # ft.VerticalDivider(),
                                ])
                            )
                            self.result_show.controls.append(ft.Divider())
            else :
                print("High")
                if self.item_check.value=="all":
                    result=data_access.stock_check()
                    self.result_show.controls.append(
                        ft.Row([
        
                            ft.Container(ft.Text("SR",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=1,border_radius=ft.border_radius.only(5,15,20,8),alignment=ft.Alignment(0.0, 0.0), bgcolor="#4335A7", padding=10, width=80),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item ID",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=4,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),bgcolor="#4335A7", padding=10, width=150),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item Description",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=10,alignment=ft.Alignment(0.0, 0.0),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),border_radius=ft.border_radius.only(5,15,20,8), bgcolor="#4335A7", padding=10, width=300),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Stock",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Label",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2, bgcolor="#4335A7", alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),padding=10, width=80,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Company Name",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=6, bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                                # ft.VerticalDivider(),                        ft.VerticalDivider(),
                            ft.Container(ft.Text("Last Update",size=16,weight=ft.FontWeight.BOLD,color='#131010'), expand=3,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                        ]))
                    self.result_show.controls.append(ft.Divider())
                    for i in result:
                        
                        count+=1
                        if  i['stock']>i['reorder_level']:
                            
                            self.style_col=ft.TextStyle( word_spacing=5,color="#22177A",weight=ft.FontWeight.BOLD,size=13 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
                            self.result_show.controls.append(
                            ft.Row([
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{count}",style=self.style_col),expand=1,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=80 ),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_id']}",style=self.style_col),expand=5,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=150),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_description']}",style=self.style_col),expand=11,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=300),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i[ 'stock']}",style=self.style_col), expand=2,bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),

                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['reorder_level']}",style=self.style_col),expand=2, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                # ft.VerticalDivider(),  
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['company_name']}",style=self.style_col),expand=6, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['Update_date']}",style=self.style_col),expand=3, bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),
                                # ft.VerticalDivider(),
                            ])
                            )
                            self.result_show.controls.append(ft.Divider())
                else: 
                    print("specific vlaue ")
                    result=data_access.stock_check_specific(self.item_check.value)
                    self.result_show.controls.append(
                        ft.Row([
    
                            ft.Container(ft.Text("SR",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=1,border_radius=ft.border_radius.only(5,15,20,8),alignment=ft.Alignment(0.0, 0.0), bgcolor="#4335A7", padding=10, width=80),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item ID",size=16,weight=ft.FontWeight.BOLD,color='#131010'),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),expand=4,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),bgcolor="#4335A7", padding=10, width=150),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Item Description",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=10,alignment=ft.Alignment(0.0, 0.0),shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,),border_radius=ft.border_radius.only(5,15,20,8), bgcolor="#4335A7", padding=10, width=300),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Stock",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Label",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=2, bgcolor="#4335A7", alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8),padding=10, width=80,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                            # ft.VerticalDivider(),
                            ft.Container(ft.Text("Company Name",size=16,weight=ft.FontWeight.BOLD,color='#131010'),expand=6, bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                                # ft.VerticalDivider(),                        ft.VerticalDivider(),
                            ft.Container(ft.Text("Last Update",size=16,weight=ft.FontWeight.BOLD,color='#131010'), expand=3,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.only(5,15,20,8), padding=10, width=100,shadow=ft.BoxShadow(spread_radius=1,blur_radius=15,color="#8D77AB",offset=ft.Offset(0, 0),blur_style=ft.ShadowBlurStyle.OUTER,)),
                        ]))
                    for i in result:
                        self.result_show.controls.append(ft.Divider())
                        count+=1
                        if  i['stock']>i['reorder_level']:
                            self.style_col=ft.TextStyle( word_spacing=5,color="#22177A",weight=ft.FontWeight.BOLD,size=13 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
                            self.result_show.controls.append(
                            ft.Row([
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{count}",style=self.style_col),expand=1,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=80 ),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_id']}",style=self.style_col),expand=5,alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=150),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['item_description']}",style=self.style_col),expand=11,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),bgcolor=ft.Colors.TRANSPARENT, padding=10, width=300),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i[ 'stock']}",style=self.style_col), expand=2,bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),

                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['reorder_level']}",style=self.style_col),expand=2, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
             
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['company_name']}",style=self.style_col),expand=6, bgcolor=ft.Colors.TRANSPARENT, alignment=ft.Alignment(0.0, 0.0),border_radius=ft.border_radius.all(10),padding=10, width=80),
                                ft.Container(on_hover=self.on_hover_function,ink=False,content=ft.Text(f"{i['Update_date']}",style=self.style_col),expand=3, bgcolor=ft.Colors.TRANSPARENT,alignment=ft.Alignment(0.0, 0.0), border_radius=ft.border_radius.all(10),padding=10, width=100),
                            ])
                            )
                    self.result_show.controls.append(ft.Divider())
        except Exception as err:
            print(f"Error Fetching Item Details: {err}")
            self.snack_bar_func(f"{err}")
        finally:
            self.app_layout.update()
            data_access.close_connection()
    
