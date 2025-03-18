import asyncio
from Model.items import Item
from Model.items import database2excel
from datetime import datetime
import flet as ft
import pygtrie
import time
from flet import TextField, Dropdown,ElevatedButton
import mysql.connector  # Replace with your database connector library

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
        # self.icon_enabled_color="red"
        self.label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,))
    
# Async database handler (replace with your connection details)
class stock_modification(ft.Container):
    def __init__(self,app_layout,page):
        super().__init__()
        self.app_layout=app_layout
        self.page = page 
        self.expand=True
        self.margin=ft.margin.all(5)
        self.item_id=dropdown(label="Item ID's",
                                hint_text="Select Item Id for Modification",
                                # options=self.Modification_option
                                )
# serach logic define here 
        super().__init__()
        self.stock_items = []  # Placeholder for stock data from the database
        self.filtered_items = []  # To store filtered results
        self.search_text = ""  # For search query
        self.items_database = Item()  # Database access
        self.items = self.items_database.list_items()# Contains `id` and `description`
        self.data_base=self.items 

        self.list_items = {
            item['item_id']: ft.ListTile(
                leading=ft.Icon(name=ft.Icons.MOTORCYCLE_ROUNDED, color=ft.Colors.GREEN_400, size=30),
                title=ft.Text(f"{item['item_id']} "),
                trailing=ft.Text(item['item_description']),
                on_click=self.printer,
                hover_color="#A594F9",
                style=ft.ListTileStyle.LIST,
                text_color="#F5EFFF",
                data=item,
                min_leading_width=40   
            )
            for item in self.items
        }
        self.trie_for_id=self.build_trie(self.list_items)
        self.list_items_description = {
            name['item_description']: ft.ListTile(
                title=ft.Text(name['item_description']),
                leading=ft.Icon(name=ft.Icons.MOTORCYCLE_ROUNDED, color=ft.Colors.GREEN_400, size=30),
                on_click=self.printer_description,
                trailing=ft.Text(f"{name['item_id']} Stock->{name['stock']}"),
                data=name,
                hover_color="#A594F9",
                style=ft.ListTileStyle.LIST,
                text_color="#F5EFFF",
                min_leading_width=40
            )
            for name in self.items
        }
        self.trie=self.build_trie(self.list_items_description)
        # above list tile for search Result
# print(self.list_items)# this line code run according my will 
        self.select_value = ft.ListView(expand=1,item_extent=300, spacing=2, padding=2,cache_extent=500,auto_scroll=False)#ft.ListView(auto_scroll=True)
        self.search_description=ft.ListView(expand=1,item_extent=300, spacing=2, padding=2,cache_extent=500,auto_scroll=False)
        #using searchbar TextField 
        self.using_id=ft.TextField(width=500,
                                  hint_text="  Search Item Detail By ID :)",bgcolor="transparent",
                                  capitalization=ft.TextCapitalization.CHARACTERS, 
                           keyboard_type=ft.KeyboardType.NAME,border_color="transparent",content_padding=2,
                            text_size=14,height=50 , cursor_width=2,
                            on_change=self.on_search_change)
        self.using_description=ft.TextField(width=500,
                                  hint_text="   Search Item Detail By Name :)",bgcolor="transparent",
                                  capitalization=ft.TextCapitalization.CHARACTERS, 
                           keyboard_type=ft.KeyboardType.NAME,border_color="transparent",content_padding=2,
                            text_size=14,height=50 , cursor_width=2,
                            on_change=self.textbox_changed_description)
        # other need  Container 
        # other need  
        self.item_id_container=ft.Container(col={"sm": 6, "md": 6 ,"lg":6, "xl":6},
                                            height=70  ,
                                            width=720, 
                                            bgcolor="white10",
                                            border_radius=15,
                                            padding=ft.padding.only(top=15,left=21,right=21,bottom=15),
                                            # clip behv. makes sure there' no overflow
                                            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_IN_OUT),
                                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                            content=ft.Column(
                                                controls=[
                                                    ft.Row(spacing=10,
                                                           vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                           controls=[ft.Icon(name=ft.Icons.WIDGETS_SHARP,opacity=0.9),
                                                                     self.using_id,
                                                                    #  now  display result here 
                                                                    ft.IconButton(icon=ft.Icons.CLOSE_ROUNDED,
                                                                                  icon_color="red",tooltip="Clear Search",on_click=self.handle_close_id),
                                                                     ]),
                                                    # there will be data display
                                                    self.select_value,
                                                    # ft.Column(scroll="auto",expand=True,)
                                                    # next 
                                                ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.START
                                            ))
        self.item_name_container=ft.Container(col={"sm": 6, "md": 6,"lg":6 ,"xl":6},
                                            height=70  ,
                                            width=720, 
                                            bgcolor="white10",
                                            border_radius=15,
                                            padding=ft.padding.only(top=15,left=21,right=21,bottom=15),
                                            # clip behv. makes sure there' no overflow
                                            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
                                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                            content=ft.Column(
                                                controls=[
                                                    ft.Row(spacing=10,
                                                           vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                                           controls=[ft.Icon(name=ft.Icons.WIDGETS_SHARP,opacity=0.9),
                                                                     self.using_description,
                                                                    #  now  display result here 
                                                                    ft.IconButton(icon=ft.Icons.CLOSE_ROUNDED,
                                                                                  icon_color="red",tooltip="Clear Search",on_click=self.handle_close_name),
                                                                     ]),
                                                    # there will be data display
                                                    self.search_description,
                                                    # ft.Column(scroll="auto",expand=True,)
                                                    # next 
                                                ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.START
                                            ))
        # database access here 
        
        
        
        self.stock_items = []  # Placeholder for stock data from the database
        self.filtered_items = []  # To store filtered results
        self.search_text = ""  # For search query
        self.items_database = Item()  # Database access
        self.items = self.items_database.list_items()# Contains `id` and `description`
        self.data_base=self.items 
        self.items_database.close_connection()
        # text filed 
        self.readonly=text_filed_style(value="OR",read_only=True,col={})
        self.amount=text_filed_style(label="Buying Rate",keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ),hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2})
        self.mrp=text_filed_style(label="MRP",hint_text="Minimum Retail Price",keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ),col1={"sm": 6, "md": 4, "xl": 2})
        self.Gst=text_filed_style(label="GST",suffix="%",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2},keyboard_type=ft.NumbersOnlyInputFilter())
        self.Retail_Profit=text_filed_style(label="Retail Profit",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2},keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.WholeSale_profit=text_filed_style(label="WholeSale Profit",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2},keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.silver_profit=text_filed_style(label="CD Silver",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2},keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.Platinum_profit=text_filed_style(label="CD Platinum",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2},keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.Stock_detail=text_filed_style(label="STOCK",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2},keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.NumbersOnlyInputFilter())
        self.Stock_reorder=text_filed_style(label="Warning Stock",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2},input_filter=ft.NumbersOnlyInputFilter())
        # price calculation 
        self.Retail_price=text_filed_style(read_only=True,label="Retail Sale Price",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2})
        self.Whole_price=text_filed_style(read_only=True,label="Whole Sale Price",hint_text="100.00",col1={"sm": 6, "md": 4, "xl": 2})
        # button 
        self.Calculation=button_style(text="Calculate",on_click=self.calculation)
        self.Clear=button_style(text="Clear",on_click=self.clear_field)
        self.button_modify=button_style(text="Update",on_click=self.selected_item_to_edit)
        self.button_delete=button_style(text="Delete",on_click=self.delete_item_from_database)
        self.save_file_dialog = ft.FilePicker(on_result=self.download_item_in_excel_formate)
        self.button_excel_dwonload=button_style(text="Export Excel",bgcolor="Green" ,on_click=self.filepicker_iniciate )
        # Main Layout 
        self.content=ft.Column([
            ft.ResponsiveRow([self.item_id_container
                              ,self.item_name_container,],  alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Divider(),
             ft.ResponsiveRow([
                 self.amount,
                 self.mrp,
                 self.Gst,
                 self.Retail_Profit,
                 self.WholeSale_profit
                     ]),
             ft.ResponsiveRow([
                 self.silver_profit,self.Platinum_profit,self.Stock_detail,self.Stock_reorder
                     ]),
             ft.Row([self.Calculation,self.Clear]),
            ft.Divider(),
            ft.Row([self.Retail_price,self.Whole_price]),
            ft.Divider(),
            ft.Row([self.button_modify,self.button_delete,self.button_excel_dwonload ]),
            ft.Divider(),
        ],expand=True,scroll=ft.ScrollMode.ADAPTIVE )
   # search box function define here 
    def clear_field(self,e):
        self.using_id.value=""
        self.using_description.value=""
        self.amount.value=""
        self.mrp.value=""
        self.Gst.value=""
        self.Retail_Profit.value=""
        self.WholeSale_profit.value=""
        self.silver_profit.value=""
        self.Platinum_profit.value=""
        self.Stock_detail.value=""
        self.Stock_reorder.value=""
        self.Retail_price=""
        self.Whole_price=""
        self.update()
    def build_trie(self,data):
        """ Build a trie with item description"""
        trie=pygtrie.CharTrie()
        for key, value in data.items():
            trie[key.lower()]=value
        return trie
    def calculation(self,e):
        self.Retail_price.value = float(self.amount.value) * (1 + float(self.Gst.value) /100)+float(self.Retail_Profit.value)
        self.Whole_price.value=float(self.amount.value) * (1 + float(self.Gst.value) /100)+float(self.WholeSale_profit.value)
        self.Retail_price.update()
        self.Whole_price.update()
    def handle_close_id(self,e):
        self.item_id_container.height=70
        self.using_id.value=""
        self.select_value.controls.clear()
        self.item_id_container.update()
    def handle_close_name(self,e):
        self.item_name_container.height=70
        self.using_description.value=""
        self.select_value.controls.clear()
        self.item_name_container.update()
    def textbox_changed_description(self, string):
        # print("id on change through text Field")
        value=string.control.value.lower()
        try:
            result=[value for key, value in self.trie.items(prefix=value)]
            self.search_description.controls=result if value else []
            if len(self.search_description.controls)==0:
                self.item_name_container.height=70
            else: 
                self.item_name_container.height=min(200+(len(self.select_value.controls)*50),400)
        except:
            self.search_description.controls.clear()
            self.search_description.controls.append(
                ft.ListTile(
                    title=ft.Text("Sorry"),
                    leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                    on_click=lambda _ : self.snack_bar_func(f"Does not Find any Result"),
                    trailing=ft.Text(f"No Matches found"),
                    data="Not_found",  
                    hover_color='pink',
                    style=ft.ListTileStyle.LIST,
                    text_color='white'
            )
            )
            self.item_name_container.height=120 
        # self.searh_description.controls = [
        #     self.list_items_description.get(n['item_description']) for n in self.items  if str_number in n['item_description'].lower()
        # ] if str_number else []
        # if len(self.search_description.controls)==0:
        #     self.item_name_container.height=70
        # else: 
        #     self.itemc_name_container.height=min(120+(len(self.search_description.controls)*50),300)
        self.item_name_container.update()

    def on_search_change(self,e):  
        # print("Description change through text Field")
        search_query=e.control.value.lower()
        try:
            result=[value for key, value in self.trie_for_id.items(prefix=search_query)]
            self.select_value.controls=result if search_query else []
            print(result)
            if len(self.select_value.controls)==0:
                self.item_id_container.height=70
            else: 
                self.item_id_container.height=min(200+(len(self.select_value.controls)*50),300)
        except:
            self.select_value.controls.clear()
            self.select_value.controls.append(
                ft.ListTile(
                    title=ft.Text("Sorry"),
                    leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                    on_click=lambda _ : self.snack_bar_func(f"Does not Find any Result"),
                    trailing=ft.Text(f"No Matches found"),
                    data="Not_found",  
                    hover_color='pink',
                    style=ft.ListTileStyle.LIST,
                    text_color='white'
            )
            )
            self.item_id_container.height=170        
        # self.select_value.controls =[
        #     self.list_items.get(n['item_id']) for n in self.items if search_query in n['item_id'].lower() 
        # ] if search_query else []
        # if len(self.select_value.controls)==0:
        #     self.item_id_container.height=70
        # else: 
        #     self.item_id_container.height=min(120+(len(self.select_value.controls)*50),300)
        self.item_id_container.update()
    def printer(self, event):
        """Print the data of the selected ListTile. for IDS"""
        print(f"Selected Item: {event.control.data}")
        self.handle_close_id(e=None)
        value=event.control.data
        self.select_value.controls.clear()
        self.using_id.value=f"{value['item_id']}"
        self.using_description.value=f"{value['item_description']}"
        self.amount.value=f"{value['item_buy_rate']}"
        self.temp_br_rate=int(value['item_buy_rate']) # value temp rate 
        self.mrp.value=f"{value['mrp']}"
        self.Gst.value=f"{value['gst_percentage']}"
        self.Retail_Profit.value=f"{value['profit_retail']}"
        self.WholeSale_profit.value=f"{value['profit_wholesale']}"
        self.silver_profit.value=f"{value['sliver_discount']}"
        self.Platinum_profit.value=f"{value['platinum_discount']}"
        self.Stock_detail.value=f"{value['stock']}"
        self.Stock_reorder.value=f"{value['reorder_level']}"
        self.update()
    def start_loader(self):
        self.loader = ft.Container(
            content=ft.ProgressRing(),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.with_opacity(0.5,"BLACK"),  # Optional: Add a translucent background
            width=self.page.width,
            height=self.page.height
        )
        self.page.overlay.append(self.loader)
        self.page.update()
        self.loader.visible = True
        self.page.update()
        print("Start Loader")
    def close_loader(self):
        print("End Loader")
        if page.overlay:
            self.page.overlay.clear()
            self.page.update()
    async def download_item_in_excel_formate(self,e: ft.FilePickerResultEvent):
        """ Download Items raw mysql accessing through pandas mysql in formate in excel saving with filepicker"""
        formatted_time = time.strftime('%H_%M_%S', time.localtime())
        saving_path= e.path+f"{formatted_time}excel.xlsx" if e.path else "Cancelled!"
        try:
            if saving_path =="Cancelled!":
                self.snack_bar_func("Cancelled")
                return
            items=database2excel()
            raw_data= await items.fetch_data(saving_path)
            self.snack_bar_func(raw_data)
        except Exception as e:
            self.snack_bar_func(e)
    def sure_want_remove(self,e):
        # access to pass id and delete
        try:
            default_value=self.app_layout.page.session.get("password")
            print(f" default dialog close {default_value}")
            if self.password.value==default_value:
                self.close_dialog(e)
                access_remove=Item()
                result =  access_remove.remove(self.using_id.value)
                # print(f" def ault condition {default_value}")
                self.snack_bar_func("result")
                
            else :
                self.password.error_style=ft.TextStyle(color="red")
                self.password.error_text="Enter Wrong Password"
                self.password.update()
        except Exception as e:
            self.snack_bar_func(e)
        finally: 
            self.clear_field(e=None)
            self.Refresh_after_delete_data()
    def Refresh_after_delete_data(self):
        self.items_database = Item()  # Database access
        self.items = self.items_database.list_items()# Contains `id` and `description`
        self.data_base=self.items 
        self.list_items = {
            item['item_id']: ft.ListTile(
                leading=ft.Icon(name=ft.Icons.MOTORCYCLE_ROUNDED, color=ft.Colors.GREEN_400, size=30),
                title=ft.Text(f"{item['item_id']} "),
                trailing=ft.Text(item['item_description']),
                on_click=self.printer,
                hover_color="#A594F9",
                style=ft.ListTileStyle.LIST,
                text_color="#F5EFFF",
                data=item,
                min_leading_width=40   
            )
            for item in self.items
        }
        self.list_items_description = {
            name['item_description']: ft.ListTile(
                title=ft.Text(name['item_description']),
                leading=ft.Icon(name=ft.Icons.MOTORCYCLE_ROUNDED, color=ft.Colors.GREEN_400, size=30),
                on_click=self.printer_description,
                trailing=ft.Text(f"{name['item_id']} Stock->{name['stock']}"),
                data=name,
                hover_color="#A594F9",
                style=ft.ListTileStyle.LIST,
                text_color="#F5EFFF",
                min_leading_width=40
            )
            for name in self.items
        }
    def delete_item_from_database(self,e):
        print("Delete")
        if not self.on_button_click():
            return
        self.password=text_filed_style(label="Password",hint_text="Enter your Password",password=True, can_reveal_password=True)

        self.auth=ft.AlertDialog(
            title=ft.Text("Delete Item"),
                    modal=True,
                    content=ft.Column(width=500,height=300,controls=[ft.Text("Do you want to delete this file?"),
                                       ft.Row([ft.Text(f"User:- {self.app_layout.page.session.get('User')}"),self.password])]),
                    actions=[
        ft.TextButton(text="Yes", on_click=lambda _ : self.sure_want_remove(self.auth)),
        ft.TextButton(text="No", on_click=lambda e: self.close_dialog(self.auth)),
         ],
                )
        self.page.overlay.clear()
        self.page.overlay.append(self.auth)
        self.auth.open=True
        self.app_layout.page.update()
    def printer_description(self, event):
        """Print the data of the selected ListTile. Description"""
        value=event.control.data
        # first id 
        self.handle_close_name(e=None)
        value=event.control.data 
        self.select_value.controls.clear()
        self.using_id.value=f"{value['item_id']}"
        self.using_description.value=f"{value['item_description']}"
        self.amount.value=f"{value['item_buy_rate']}"
        self.mrp.value=f"{value['mrp']}"
        self.Gst.value=f"{value['gst_percentage']}"
        self.Retail_Profit.value=f"{value['profit_retail']}"
        self.WholeSale_profit.value=f"{value['profit_wholesale']}"
        self.silver_profit.value=f"{value['sliver_discount']}"
        self.Platinum_profit.value=f"{value['platinum_discount']}"
        self.Stock_detail.value=f"{value['stock']}"
        self.Stock_reorder.value=f"{value['reorder_level']}"
        self.update()
# end here 
    def access_database2modify(self,e):
        if not self.on_button_click():
            return
        # declaration to modify database 
        self.close_dialog(self.dialog)
        self.snack_bar_func(f"Accessing Database to modify data")
        print("access to modify ")
    def find_and_replace(self,original: str, target: str, replacement: str) -> str:
# Ensure the replacement is applied only if the target exists in the string
        if target in original:
            return original.replace(target, str(int(replacement)))
        else:
            raise ValueError(f"Target '{target}' not found in the original string.")
    def selected_item_to_edit(self,e):
        if self.temp_br_rate != str(self.amount.value):
            self.new_item_id=self.find_and_replace(str(self.using_id.value),str(int(self.temp_br_rate)),float(self.amount.value) )
            self.snack_bar_func("Item Details Modification Initiate")
            self.editbtn(self.using_id.value,self.new_item_id)
        print("Updation Modification Filed") 
    def editbtn(self,old_id,new_id):
        # changes need in here in page update
        self.temp_about = ft.Text('Authentication of Update',col={"md": 3})
        self.snack_bar_func(f"If Change Buy Rate then Product ID Also Change")
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Authentication"),
            content=ft.Container(content=ft.Column(controls=[ ft.Row([ft.Text(f"Old ID:- {old_id}"),ft.Text(f" New ID:- {new_id}")])
                ]),width=800,height=400),
            actions=[ft.TextButton("Save", on_click=self.access_database2modify),ft.TextButton("Close", on_click=lambda e: self.close_dialog(self.dialog))],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.overlay.clear()
        self.page.overlay.append(self.dialog)
        self.dialog.open=True
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
        self.page.update()
        # await asyncio.sleep(2)
    def close_dialog(self,dlg):
        dlg.open = False
        self.page.update()
    def filepicker_activate(self):
        self.page.overlay.clear()
        self.page.overlay.append(self.save_file_dialog)
        self.app_layout.page.update()
    def filepicker_iniciate(self,e):
        self.filepicker_activate()
        self.start_loader()
        self.save_file_dialog.save_file()
        self.app_layout.page.update()
        
# validator 

    def validate_fields(self, *fields):
        """
    Validates the provided text fields to ensure they are not empty.
    
    Args:
        *fields: List of text fields to validate.
    
    Returns:
        list: A list of labels of fields that are empty.
        """
        empty_fields = []

        for field in fields:
            if not field.value or field.value.strip() == "":
                empty_fields.append(field.label)  # Append the label of the field if empty
                field.error_text = f"{field.label} cannot be empty."
                field.update()  # Update the UI to reflect the error
            else:
                field.error_text = None  # Clear any previous error text
                field.update()

        return empty_fields

    def on_button_click(self):
    # List of all fields to validate
        fields_to_validate = [
        self.amount,
        self.mrp,
        self.Gst,
        self.Retail_Profit,
        self.WholeSale_profit,
        self.silver_profit,
        self.Platinum_profit,
        self.Stock_detail,
        self.Stock_reorder,
        ]
    
    # Validate the fields
        empty_fields = self.validate_fields(*fields_to_validate)

        if empty_fields:
        # If there are empty fields, display an error and stop
            error_message = f"The following fields are empty: {', '.join(empty_fields)}"
            self.snack_bar_func(error_message)
            return 0
        return 1

    # Proceed with button functionality (e.g., update, calculate, delete)
    # print("All fields are valid!")