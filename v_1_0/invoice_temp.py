import flet as ft
from View.logo import invoice_logo
import time
from flet import TextField, ElevatedButton,Dropdown
from Controller.invoice_option_tax import WInvoice
import win32print
import os
import pygtrie
import win32api
from rapidfuzz import process
from Model.items import Item  
import asyncio
from Model.custmer import custmers

# Edit text_filed_style
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

class dropdown(Dropdown):
    def __init__(self,label,  **kwargs):
        super().__init__(**kwargs)
        self.label=label
        self.counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
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
        # self.icon_enabled_color="red"
        self.label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,))
        
class tab_invoice(ft.Container):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # self.app_layout=app_layout
        # self.page = page
        self.padding = ft.padding.all(2)
        self.margin = ft.margin.all(0)
        self.expand=6
        self.style_col=ft.TextStyle( word_spacing=5,color="#0D1282",weight=ft.FontWeight.BOLD,size=14 ,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
        # Database call for item table import data
        self.debounce_task=None # Task to handle debouncing
        self.items_database = Item() # database connection
        self.items = self.items_database.list_items()# item
        self.items_database.close_connection() # close connection 
        self.goods_detail=list()
        self.discount_dict=dict()
        # customer Details Entry here 
        self.customer_=custmers()
        self.customer_detail=self.customer_.cust_fetch_wholesale()
        # Constants and initialization
        self.serial_number = 1
        self.item_id_search = self.items
        self.items_name = self.items
        self.list_items = {  
            name['item_id'].lower(): ft.ListTile(
                title=ft.Text(f"{name['item_id']} Stock->{name['stock']}"),
                leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                trailing=ft.Text(f"{name['item_description']}"),
                on_click=self.printer,
                hover_color='pink',
                style=ft.ListTileStyle.LIST,
                text_color='white',
                data=name
            )
            for name in self.item_id_search
        }
        self.trie_for_id=self.build_trie(self.list_items)
        # Create item description search list
        self.list_items_description = {
            "".join((name['item_description'].lower()).split()): ft.ListTile(
                title=ft.Text(f"{name['item_description']}"),
                leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer_description,
                trailing=ft.Text(f"{name['item_id']} Stock->{name['stock']}"),
                data=name,
                hover_color='pink',
                style=ft.ListTileStyle.LIST,
                text_color='white'
            )
            for name in self.items_name
        }
        self.trie=self.build_trie(self.list_items_description)
        # Create customer list for search by Mobile Number
        self.list_customer_number = {
            i['mobile'] : ft.ListTile(
                title=ft.Text(f"{str(i['mobile'])}"),
                leading=ft.Text(f"{i['cust_id']}"),
                on_click=self.printer_number,
                data=i,
                trailing=ft.Text(f"{i['person_name']}"),
                hover_color='pink',
                style=ft.ListTileStyle.LIST,
                text_color='white'
            
            )
            for i in self.customer_detail}
        # listView define for search view 
        self.search_results = ft.ListView(expand=1,item_extent=300, spacing=2, padding=2,cache_extent=500,auto_scroll=False)
        self.search_number=ft.ListView(expand=1,spacing=2,item_extent=300,padding=2,cache_extent=500,auto_scroll=False)
        self.search_description=ft.ListView(expand=1,spacing=2,item_extent=300,padding=2,auto_scroll=False)
        
        self.default_outstanding_amount=ft.Text("₹0.00",color="#FFD700",weight=ft.FontWeight.W_100)
        self.card =ft.Card(
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS_WITH_SAVE_LAYER,
                        color="#2A9D8F",
                        content=ft.Container(
                            width=200,
                            height=100,
                            content=ft.Column(
                                [
                                    ft.Text("Outstanding Amount", color="#FFD700", size=14),
                                    self.default_outstanding_amount,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),col={"md":8},
                        elevation=2,
                        shadow_color="#FF748B",
                    )
        # button_click define here 
        self.add_button=button_style(text='Add',on_click=self.add_items,col={"sm": 6, "md": 4, "xl": 2},icon=ft.Icons.ADD_OUTLINED)
        self.reset_button=button_style(text='Reset',on_click=self.reset,col={"sm": 6, "md": 4, "xl": 2},icon=ft.Icons.RESET_TV_SHARP)
        self.bill_button=button_style(text='Print Bill',on_click=self.bill_gen,col={"sm": 6, "md": 4, "xl": 3},icon=ft.Icons.LOCAL_PRINT_SHOP_OUTLINED)
        # customer Entry 
        self.customer_name = text_filed_style(
                            label='Customer Name', 
                            capitalizationn=ft.TextCapitalization.WORDS, 
                            kbtype=ft.KeyboardType.NAME,
                            col=7
                        )
        self.customer_address = text_filed_style(
                                    label='Customer Address',
                                    capitalizationn=ft.TextCapitalization.WORDS,
                                    kbtype=ft.KeyboardType.STREET_ADDRESS,
                                    col=7,  # Matching column width
                                    hint_text="Saidpur, Ghazipur"
                                )
        self.customer_mobile=text_filed_style(
            label='Customer Mobile',
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=self.textbox_changed_number,
            prefix_text=f"+{91 }",
            hint_text="9415863731",
            leng=10
        )
        # goods entry element define here 
        
        self.rank=ft.Dropdown(label='rank',color = "#1A1A1D",bgcolor = "#EBEAFF",options=[
            ft.dropdown.Option(key="None",text="None"),
            ft.dropdown.Option(key='sliver_discount',text='Sliver'),
            ft.dropdown.Option(key='platinum_discount',text='Platinum'),
        ],hint_text=" Discount", col={"md":3},value="None",width=200)
        self.item_id=text_filed_style(label='ID',
                                    capitalizationn=ft.TextCapitalization.CHARACTERS,
                                    kbtype=ft.KeyboardType.STREET_ADDRESS,
                                    on_change=self.textbox_changed,
                                      # Matching column width
                                      expand=True,
                                    hint_text="CY,TY,PT")
        
        self.item_name=text_filed_style(label='Name',
                                    capitalizationn=ft.TextCapitalization.CHARACTERS,
                                    kbtype=ft.KeyboardType.STREET_ADDRESS,on_change=self.textbox_changed_description,
                                      # Matching column width
                                      expand=True,
                                    hint_text="Product Name")
        self.item_rate=text_filed_style(label='RATE',
                                    capitalizationn=ft.TextCapitalization.CHARACTERS,
                                    kbtype=ft.KeyboardType.NUMBER,
                                    col1={ "md": 3},  # Matching column width
                                    hint_text="Rate",input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.unit=ft.DropdownM2(label="Unit",hint_text="Unit of Good",options=[
            ft.dropdown.Option("Dozen"),
            ft.dropdown.Option("PCS"),
            ft.dropdown.Option("SET"),
            ft.dropdown.Option("PKT"),
            ft.dropdown.Option("GRS"),      
            ft.dropdown.Option("PAIR"),
            ft.dropdown.Option("LT."),
            ft.dropdown.Option("KG."),
            ft.dropdown.Option("GM."),
            ft.dropdown.Option("ML."),
        ],col={"md":3})
        self.item_QTY=text_filed_style(label='Quntity',
                                    capitalizationn=ft.TextCapitalization.CHARACTERS,
                                    kbtype=ft.KeyboardType.NUMBER,
                                    col1={"md":3},  # Matching column width
                                    hint_text="QTY",input_filter=ft.NumbersOnlyInputFilter())
        # Row and Column define here 
        self.item_id_container=ft.Container(expand=False,
                                            height=0  ,
                                            # width =200,
                                            bgcolor="white10",
                                            border_radius=15,
                                            padding=ft.padding.only(top=15,left=21,right=21,bottom=15),
                                            # clip behv. makes sure there' no overflow
                                            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_IN_OUT),
                                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                            content=ft.Column(
                                                controls=[
                                                    # there will be data display
                                                    self.search_results,
                                                    # ft.Column(scroll="auto",expand=True,)
                                                    # next 
                                                ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.START
                                            ))
        self.item_name_container=ft.Container(expand=False,
                                            height=0  ,
                                            # width =200,
                                            bgcolor="white10",
                                            border_radius=15,
                                            padding=ft.padding.only(top=15,left=21,right=21,bottom=15),
                                            # clip behv. makes sure there' no overflow
                                            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
                                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                            content=ft.Column(
                                                controls=[
                        
                                                    # there will be data display
                                                    self.search_description,
                                                    # ft.Column(scroll="auto",expand=True,)
                                                    # next 
                                                ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.START
                                            ))
        customer_col=ft.Column([ft.Row([ft.Text("Enter Customer Detail", size=18,style=self.style_col)], alignment=ft.MainAxisAlignment.CENTER),
                                ft.Divider(),
                                ft.ResponsiveRow(
                [self.customer_name, self.customer_address,self.customer_mobile,self.search_number],
                spacing=10,
                run_spacing=10,
            ),

                                ])
        
        item_col=ft.Column([ft.Row([ft.Text("Entry Goods ", size=18,style=self.style_col)], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Divider(),
                            ft.ResponsiveRow(
                            [self.item_id,
                            self.item_id_container,], spacing=10, run_spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY# Add responsive fields here,
                            ,vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                            
                            ft.ResponsiveRow(
                            [self.item_name,
                            self.item_name_container,], spacing=10, run_spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY# Add responsive fields here,
                            ,vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                            
                            ft.ResponsiveRow(
                            [self.item_rate,self.unit,self.item_QTY,self.rank,], spacing=10, run_spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY# Add responsive fields here,
                            ,vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),ft.ResponsiveRow(
                            [self.add_button,self.reset_button,self.bill_button], spacing=10, run_spacing=10  # Add responsive fields here
                            ,alignment=ft.MainAxisAlignment.END
                        ),ft.Divider(),
                            ],alignment=ft.MainAxisAlignment.START)
        # row define here
        goods_details_col=ft.Column([ft.Row([ft.Text("Goods Detail", size=24 ,style=self.style_col)], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Divider(),
                                    
                                     ])
        # Container Define Here    
        Customer_detail=ft.Container(padding=20,expand=3,bgcolor='RED',content=customer_col)
        Item_detail=ft.Container(padding=20,expand=7,bgcolor='#EBEAFF',content=item_col)
        goods_details=ft.Container(padding=20,expand=3,bgcolor='#EBEAFF',content=goods_details_col)     
        self.content=ft.Column(
            [ft.Row([Customer_detail,Item_detail],expand=6),
             goods_details,
             ],expand=True
        )       
        
        # Layout Design Here 
    def handle_close_id_filed(self,e):
        self.item_id.value=""
        self.item_id_container.height=0
        self.search_results.controls.clear()
        self.item_id_container.update()
    def handle_close_name_filed(self,e):
        self.item_name_container.height=0
        self.item_name.value=""
        self.search_description.controls.clear()
        self.item_name_container.update()
    def printer(self,e):
        print("id click ")
        print(f"{e.control.data} printed or not")
        id=e.control.data
        self.handle_close_name_filed(e=None)
        self.handle_close_id_filed(e=None)
        # print(id)
        self.item_id.value=id['item_id']
        self.item_name.value=id['item_description']
        self.item_rate.value=id['wholesale_price']
        self.unit.value=id['unit_wholesale']
        self.discount_dict=id
        self.search_results.controls.clear()
        self.item_QTY.focus()
        self.app_layout.page.update() 
    def printer_number(self,e):
        print("click on list tile on number")
        print(f"{e.control.data} ")
    def printer_description(self,e):
        print("click on list tile on description")
        print(f"{e.control.data} ")
        self.id=e.control.data
        # print(description)
        self.handle_close_name_filed(e=None)
        self.handle_close_id_filed(e=None)
        self.item_id.value=self.id['item_id']
        self.item_name.value=self.id['item_description']
        self.item_rate.value=self.id['wholesale_price']
        self.unit.value=self.id['unit_wholesale']
    # Determine discount value based on rank
        self.discount_dict=self.id
        self.search_description.controls.clear()
        self.item_QTY.focus()
        self.app_layout.page.update() 
    def textbox_changed_description(self,e):
        str_number = e.control.value.lower()
        # print(f"update value{str_number}")
        try :
            result=[value for key, value in self.trie.items(prefix=str_number)]
            self.search_description.controls = result if str_number else []
            if len(self.search_description.controls)==0:
                self.item_name_container.height=0
            else: 
                self.item_name_container.height=min(120+(len(self.search_description.controls)*50),200)
        except:
            self.search_description.controls.clear()
            self.search_description.controls.append(
                ft.ListTile(
                    title=ft.Text("Sorry"),
                    leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                    on_click=self.printer_description,
                    trailing=ft.Text(f"No Matches found"),
                    data="Not_found",  
                    hover_color='pink',
                    style=ft.ListTileStyle.LIST,
                    text_color='white'
            )
            )
            self.item_name_container.height=100
        self.item_name_container.update()
    def textbox_changed(self,e):
        str_lower = e.control.value.lower()
        try:
            result=[value for key, value in self.trie_for_id.items(prefix=str_lower)]
            self.search_results.controls=result if str_lower else []
            if len(self.search_results.controls)==0:
                self.item_id_container.height=0
            else: 
                self.item_id_container.height=min(120+(len(self.search_results.controls)*50),200)
        except:
            self.search_results.controls.clear()
            self.search_results.controls.append(
                ft.ListTile(
                    title=ft.Text("Sorry"),
                    leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                    on_click=self.printer_description,
                    trailing=ft.Text(f"No Matches found"),
                    data="Not_found",  
                    hover_color='pink',
                    style=ft.ListTileStyle.LIST,
                    text_color='white'
            )
            )
            self.item_name_container.height=100
        # if len(self.search_results.controls)==0:
        #     self.item_id_container.height=0
        # else: 
        #     self.item_id_container.height=min(120+(len(self.search_results.controls)*50),300)
        self.item_id_container.update()
    def textbox_changed_number(self,e):
        str_number = e.control.value
        self.search_number.controls = [
            self.list_customer_number.get(n['mobile']) for n in self.customer_detail if str_number in n['mobile']
        ] if str_number else [] 
        self.search_number.update()
    def add_items(self,e):
        print("Add button click ")
        if self.item_id.value=='' or self.item_name.value=='':
            self.snack_bar_func(f"Please Enter Goods Details")
            return
        try:
             
            self.goods_detail.append(
            {
                "item_id": self.item_id.value,
                "item_description": self.item_name.value,
                "rate":float(self.item_rate.value),
                "unit":self.unit.value,
                "quantity":int(self.item_QTY.value),
                "total_amount":float(self.item_rate.value)*float(self.item_QTY.value),
             "discount": 0 if self.rank.value == 'None' else float(self.discount_dict[self.rank.value])*float(self.item_QTY.value)
             }
             
            )
            print(f"{self.goods_detail[0]['discount']}")
            print(f"{self.rank.value}")

        except ValueError as ve:
            self.snack_bar_func(f"Invalid input: {ve}")
            return
        self.item_id.value =""
        self.item_name.value =""
        self.item_rate.value =""
        self.unit.value =""
        self.item_QTY.value =""
        self.rank.value="None"
        self.search_results.controls.clear()
        self.search_description.controls.clear()
        self.update_table()
    def update_table(self,e=None):
        self.datatable.rows.clear()
        serial=1
        for i in self.goods_detail:
            self.datatable.rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(f"{serial}",style=self.style_col)),
                ft.DataCell(ft.Text(i["item_id"],style=self.style_col), show_edit_icon=True, on_tap=self.editbtn, data=[serial, "item_id"]),
                ft.DataCell(ft.Text(i['item_description'],style=self.style_col), show_edit_icon=True, on_tap=self.editbtn, data=[serial,"item_description"]),
                ft.DataCell(ft.Text(i["quantity"],style=self.style_col), show_edit_icon=True, on_tap=self.editbtn, data=[serial,"quantity"]),
                ft.DataCell(ft.Text(i["unit"],style=self.style_col), show_edit_icon=True, on_tap=self.editbtn, data=[serial, "unit"]),
                ft.DataCell(ft.Text(i["rate"],style=self.style_col), show_edit_icon=True, on_tap=self.editbtn, data=[serial,"rate"]),
                ft.DataCell(ft.Text(f"Rs.{i['total_amount']:.2f}",style=self.style_col)),
                ft.DataCell(ft.Row([ft.IconButton("delete",icon_color='red',
                                            data=serial,
                                            on_click=self.del_data)
                        ]))
            ])
            )
            serial+=1
        DISCOUNT_VALUE=sum(item['discount'] for item in self.goods_detail)
        self.grand_total_amount.value=f"Grand Total: Rs.{sum(item['total_amount'] for item in self.goods_detail):.2f}"
        self.item_discount.value =f"{DISCOUNT_VALUE}"
        self.datatable.update()
    def editbtn(self,e):
        self.temp_about = ft.Text('Enter Changes Want',col={"md": 3})
        print("Edit button on DataTable")
        self.what = e.control.data[1]
        self.loc = e.control.data[0] - 1
        print(f"{self.loc} location of where edit")
        # textfield and button click 
        self.item_id.value = self.goods_detail[self.loc]["item_id"]
        self.item_name.value = self.goods_detail[self.loc]["item_description"]
        self.item_rate.value = self.goods_detail[self.loc]["rate"]
        self.unit.value = self.goods_detail[self.loc]["unit"]
        self.item_QTY.value = self.goods_detail[self.loc]["quantity"]
        # self.snack_bar_func(f"Edit Function Open")
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Bill"),
            content=ft.Container(content=ft.Column(controls=[self.temp_about, ft.ResponsiveRow([self.item_id,self.search_results,self.item_name,self.search_description,self.item_QTY,self.unit,self.item_rate ])]),width=800,height=400),
            actions=[ft.TextButton("Save", on_click=self.Update_table_edit),ft.TextButton("Close", on_click=lambda e: self.close_dialog(self.dialog))],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.overlay.clear()
        self.page.overlay.append(self.dialog)
        self.dialog.open=True
        self.app_layout.page.update()
    def reset(self,e):
        print("reset click ")
        self.item_id.value=""
        self.item_name.value=""
        self.item_rate.value=""
        self.unit.value=""
        self.item_QTY.value=""
        self.search_results.controls.clear()
        self.search_description.controls.clear()
        self.customer_address.value=""
        self.customer_name.value=""
        self.customer_mobile.value=""
        self.rank.value="None"
        self.goods_detail.clear()
        self.content.update()
    def bill_gen(self,e):
        pass 
    def build_trie(self,data):
        """ Build a trie with item description"""
        trie=pygtrie.CharTrie()
        for key, value in data.items():
            trie[key.lower()]=value
        return trie
    
async def main(page: ft.Page):
    page.title = "Price Tag Generator"
    page.add(tab_invoice())

ft.app(target=main,assets_dir="../assets")