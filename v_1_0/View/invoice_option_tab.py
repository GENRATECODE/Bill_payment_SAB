import flet as ft
from View.logo import invoice_logo
import time
from Controller.invoice_option_tax import WInvoice
import win32print
import os
import win32api
from Model.items import Item  
class tab_invoice(ft.Container):
    def __init__(self,app_layout, page):
        self.app_layout=app_layout
        super().__init__()
        self.page = page
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        self.app_layout=app_layout

        
        self.items_database=Item()
        self.items=self.items_database.list_items()
        self.customer_count=1
        self.item_id_search=self.items# for id serach
        self.serial_number=1
        self.items_name=self.items # for item serach
        self.customer_mobile_search=['9794144305','979414439','951650030','9415863731']
        self.what=None
        self.loc=None
        self.app_layout.page.vertical_alignment = ft.MainAxisAlignment.START
        self.padding=ft.padding.all(10)
        self.margin=ft.margin.all(0)
        self.height=self.app_layout.page.window.height
        self.style_button=ft.ButtonStyle(
        animation_duration=500,
        color={
            # ft.ControlState.DEFAULT: "#FFFFFF",  # White text by default
            ft.ControlState.HOVERED: "#3D3BF3",  # Light blue text on hover
            ft.ControlState.FOCUSED:  "#000000", #"#FF2929 ",  # Cyan text on focus
        },
        bgcolor={
            # ft.ControlState.DEFAULT: "#3D3BF3",  # Red background by default
            "":"#FF2929",   # Black background on hover
            ft.ControlState.HOVERED: "#000000",  # Black background on focus
        },
        # shadow_color="#453C67",
        # padding={ft.ControlState.HOVERED:20},
        # overlay_color=ft.colors.TRANSPARENT,
        elevation={"pressed":0,"":1},
        side={
            ft.ControlState.DEFAULT:ft.BorderSide(1, "#1D24CA"),
            ft.ControlState.HOVERED:ft.BorderSide(1,"#40A2D8")
        },
        shape={
            ft.ControlState.DEFAULT:ft.RoundedRectangleBorder(radius=5),
            ft.ControlState.HOVERED:ft.RoundedRectangleBorder(radius=12)
        }
        )
        # self.uniqure_id=ft.TextField(label="Unique Id", col={"md": 4})
        # for search Id 
        self.list_items={
            name['item_id']:ft.ListTile(
                title=ft.Text(name['item_id']),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                trailing=ft.Text(name['item_description']),
                on_click=self.printer,
                data=name['item_id']
            )
            for name in self.item_id_search
        }
        # for search Customer Details by Modlie
        self.list_customer_number={
            number:ft.ListTile(
                title=ft.Text(number),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer_number,
                data=number
            )
            for number in self.customer_mobile_search
        }    
        # for search goodes Description 
        self.list_items_description={
            name['item_description']:ft.ListTile(
                title=ft.Text(name['item_description']),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer_description,
                trailing=ft.Text(name['item_id']),
                data=name['item_description']
            )
            for name in self.items_name
        }
        # for customer deatil input
        self.customer_name =  ft.TextField(
                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            border_radius=ft.border_radius.all(10),
                                            capitalization=ft.TextCapitalization.WORDS,
                                            label="Customer Name", 
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter customer name",keyboard_type=ft.KeyboardType.NAME,
                                            width=200, col={"sm": 8, "md": 9})#,on_change=self.tab_update)
        self.customer_address =ft.TextField(  
                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            capitalization=ft.TextCapitalization.WORDS,
                                            border_radius=ft.border_radius.all(10),
                                           label="Address", 
                                           hint_text="Enter address",
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.STREET_ADDRESS,
                                           width=200, col={"sm": 8, "md": 9})
        self.customer_mobile =ft.TextField(input_filter=ft.NumbersOnlyInputFilter(), 
                                           prefix_text=f"+{91 }",
                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            border_radius=ft.border_radius.all(10),
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                          keyboard_type=ft.KeyboardType.PHONE,  
                                          label="Mobile Number",
                                          hint_text="Enter mobile number", 
                                          width=200,
                                          max_length=10, col={"sm": 8, "md": 9}, on_change=self.textbox_changed_number)
        # seach logic define 
        self.item_id = ft.TextField( autofocus=True,
                                    selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            border_radius=ft.border_radius.all(10),
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter Product ID",
                                    label="Item Id", on_change=self.textbox_changed)
        self.search_results = ft.ListView(expand=1, spacing=4, padding=2,auto_scroll=True)
        self.search_number=ft.ListView(expand=1,spacing=4,padding=2,auto_scroll=True)
        self.search_description=ft.ListView(expand=1,spacing=4,padding=2,auto_scroll=True)
        # other thing define here 
        self.item_names =  ft.TextField(
                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            border_radius=ft.border_radius.all(10),
                                            # capitalization=ft.TextCapitalization.WORDS,
                                            label="Customer Name", 
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter customer name",
                                 on_change=self.textbox_changed_description)
        self.item_Qty = ft.TextField(input_filter=ft.NumbersOnlyInputFilter(), 
                                           prefix_text=f"QTY",
                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            border_radius=ft.border_radius.all(10),
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                          keyboard_type=ft.KeyboardType.PHONE,  
                                          label="Quantity ",
                                        #   hint_text="Quantity of Item", 
                                          width=200,
                                         col={ "md":3})
        self.item_unit =ft.Dropdown(label='Unit', hint_text="Unit of Good", options=[
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
        ],col={"md":3},border_radius=ft.border_radius.all(10),
                                       counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                                border_color="#1A1A1D",
                                                bgcolor="#EBEAFF",
                                                color="#1A1A1D",
                                        focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            icon_content=ft.Icon(ft.icons.AD_UNITS_SHARP ),
                                            icon_enabled_color="#1A1A1D",label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                  
        )
        self.temp_unit=ft.Dropdown(label='Unit', hint_text="Unit of Good", options=[
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
        ],col={ "md": 3},border_radius=ft.border_radius.all(10),
                                       counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                                border_color="#1A1A1D",
                                                bgcolor="#EBEAFF",
                                                color="#1A1A1D",
                                        focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            icon_content=ft.Icon(ft.icons.AD_UNITS_SHARP ),
                                            icon_enabled_color="#1A1A1D",label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                  
        )
        self.item_rate = ft.TextField(label="Amount", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="15000.00",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            border_radius=ft.border_radius.all(10),
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=15,
                                             color=ft.colors.BLUE_GREY_300,
                                            offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
                                                                    allow=True,
                                            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
                                            replacement_string=""
                                            ),col={"md":3})
        self.item_gst= ft.TextField(label="IGST ", width=200,  suffix_text="%",                                     selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Product Buying Rate",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            border_radius=ft.border_radius.all(10),
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,
                                            input_filter=ft.NumbersOnlyInputFilter(),max_length=3, col={"md":3},value=0)
        self.item_discount = ft.TextField(label="Discount", value=0.00,keyboard_type=ft.KeyboardType.NUMBER,width=200,height=36)
        self.add_button = ft.ElevatedButton(style=self.style_button,text="Add", on_click=self.add_item, col={"md": 3})  
        self.generate_bill_button = ft.ElevatedButton(text="Generate Bill", style=self.style_button,on_click=self.generate_bill, col={"md": 3})
        # self.file_picker_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.reset_button = ft.ElevatedButton(text="Reset",style=self.style_button, on_click=self.reset_form, col={"md": 3})
        self.style_col=ft.TextStyle( word_spacing=5,color="#0D1282",weight=ft.FontWeight.BOLD,size=11,shadow=ft.BoxShadow(
                                                spread_radius=1,  
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
        self.data_table = ft.DataTable(  
            columns=[ft.DataColumn(ft.Text("Item ID",style=self.style_col)),
                ft.DataColumn(ft.Text("SN.",style=self.style_col)),
                ft.DataColumn(ft.Text("Description ",style=self.style_col)),
                ft.DataColumn(ft.Text("QTY",style=self.style_col)),
                ft.DataColumn(ft.Text('Unit',style=self.style_col)),
                ft.DataColumn(ft.Text('Rate',style=self.style_col)),
                ft.DataColumn(ft.Text('IGST',style=self.style_col)),
                ft.DataColumn(ft.Text("Total Amount (Rs)",style=self.style_col)),
                ft.DataColumn(ft.Text("Action",style=self.style_col))
            ],
            rows=[],bgcolor='#EBEAFF',
            show_checkbox_column=True,
            data_row_color={'hovered': "#B8001F"},
            border=ft.border.all(2, 'Black'),
            divider_thickness=1,
            show_bottom_border=True,
            vertical_lines=ft.border.BorderSide(3, 'Black'),
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=60,expand=True,
        )
        self.items_database.close_connection()
        self.grand_total_amount = ft.Text("Grand Total: Rs. 0.00")
        self.payable_amount = ft.Text("Payable Amount: Rs. 0.00")

        # self.file_button = ft.ElevatedButton('Select Folder', icon=ft.icons.FOLDER, on_click=lambda _: self.file_picker_dialog.get_directory_path())

        self.temp_about = ft.Text('Enter Changes Want',col={"md": 3})
        self.temp_name = ft.TextField(label="Description of Goods",col={"md": 3})
        self.temp_Qty = ft.TextField(label="Quantity",col={"md": 3})
        self.temp_rate = ft.TextField(label="Rate",col={"md": 3})
        self.temp_gst=ft.TextField(label="GST",col={"md": 3})

        self.left_side= ft.Container(margin=10,
                             padding=10,    
                             alignment=ft.alignment.center,
                             bgcolor=ft.colors.TRANSPARENT,
                             ink=True,blur=ft.Blur(60,10, ft.BlurTileMode.REPEATED),
                             content=ft.Column([ft.ResponsiveRow([ft.Row([ft.Text("Customer Details",text_align=ft.TextAlign.CENTER,color="#1E3E62",size=16)], alignment=ft.MainAxisAlignment.CENTER,expand=True),self.customer_name, self.customer_address, self.customer_mobile,ft.Row([self.search_number],alignment=ft.MainAxisAlignment.END),],alignment=ft.MainAxisAlignment.START ),
                                       
                                                      ft.Container(margin=2,
                             padding=2,
                            #  width=250,
                            ink=True,blur=ft.Blur(60,10, ft.BlurTileMode.REPEATED),
                             alignment=ft.alignment.top_center,
                             bgcolor=ft.colors.TRANSPARENT,
                             content=ft.ResponsiveRow([
                                   ft.Row([self.grand_total_amount,],alignment=ft.MainAxisAlignment.END),
                                                                      ft.Row([self.item_discount,],alignment=ft.MainAxisAlignment.END),
                                                                     ft.Row([self.payable_amount,],alignment=ft.MainAxisAlignment.END),
                                 ]),
                             border_radius=10, ),]),
                                expand=3,
                             border_radius=10, )
        self.right_side=ft.Column([ft.Container(margin=10,
                                    padding=10,
                            #  width=250,
                                    alignment=ft.alignment.top_center,
                                    bgcolor=ft.colors.TRANSPARENT,
                                    ink=True,blur=ft.Blur(60,10, ft.BlurTileMode.REPEATED),
                                            content=ft.ResponsiveRow([ft.Row([ft.Text("Goods Entry",text_align=ft.TextAlign.CENTER,color="#1E3E62",size=16)], alignment=ft.MainAxisAlignment.CENTER,expand=True),
                                                        self.item_id, 
                                                    self.search_results,
                                                       self.item_names,
                                                       self.search_description,
                                                       self.item_Qty,
                                                       self.item_unit,
                                                       self.item_rate,  self.item_gst, ]), 
                                                        border_radius=10, ),
                                   ft.Container(margin=2,
                                            padding=2,
                            #  width=250,
                                    ink=True,blur=ft.Blur(60,10, ft.BlurTileMode.REPEATED),
                                    alignment=ft.alignment.center_right,
                                    bgcolor=ft.colors.TRANSPARENT,
                                    content=ft.ResponsiveRow([ self.add_button,                                                   
                                    self.generate_bill_button, self.reset_button],alignment=ft.MainAxisAlignment.END),
                                    border_radius=10, ),],expand=4)
        self.content=ft.Column([ft.Row([self.left_side,self.right_side]),
                                ft.Container(margin=10,
                             padding=10,
                             alignment=ft.alignment.top_center,
                             bgcolor=ft.colors.TRANSPARENT,
                             ink=True,blur=ft.Blur(60,10, ft.BlurTileMode.REPEATED),
                             content= ft.Row(
        [self.data_table,],scroll=ft.ScrollMode.ADAPTIVE,expand=True
        ),
                             border_radius=10, expand=True),])
        self.app_layout.page.update()  
    

    def textbox_changes(self,string):
        str_lower=string.control.value.lower()
        self.search_results.controls=[
            self.list_items.get(n['item_id']) for n in self.item_id_search if str_lower in n['item_id'].lower()
        ] if str_lower else []
        self.app_layout.page.update()
    # id printer auto  complition
    def printer(self, e):
        values2db=Item()
        result=values2db.get_item_details2id(e.control.data)
        print(f"check value list {e.control.data} check type {type(result)}result=>{result}")
        self.item_id.value = e.control.data
        print(f"{result}")
        self.item_names.value = str(result['item_description'])
        self.item_rate.value = float(result['wholesale_price'])
        self.item_gst.value=float(result['gst_percentage'])
        self.search_results.controls.clear()
        self.app_layout.page.update()    
    # on change on text update to print auto complition
    def printer_description(self, e):
        print(f"check value list {e.control.data}")
        
        self.item_id.value ="Id update"
        self.item_names.value = e.control.data
        self.item_names.update()
        self.item_Qty.value = 5
        self.item_Qty.update()
        self.item_rate.value = 5
        self.item_rate.update()
        self.search_description.controls.clear()
        self.app_layout.page.update()    
    # on change on text update to print auto complition
    def printer_number(self,e):
        print(f"check value list {e.control.data}")
        self.customer_mobile.value=e.control.data
        self.customer_name.value='abhay S'
        self.customer_address.value='Saidpur'
        self.search_number.controls.clear()      
        self.app_layout.page.update() 
    def textbox_changed(self, string):
        str_lower = string.control.value.lower()
        self.search_results.controls = [
            self.list_items.get(n['item_id']) for n in self.item_id_search if str_lower in n['item_id'].lower()
        ] if str_lower else []
        self.page.update()
    # for mobile numnber search 
    def textbox_changed_number(self,string):
        str_number = string.control.value.lower()
        self.search_number.controls = [
            self.list_customer_number.get(n) for n in self.customer_mobile_search if str_number in n
        ] if str_number else []
        self.app_layout.page.update()
    # for search by goods description 
    def textbox_changed_description(self, string):
        str_number = string.control.value
        self.search_description.controls = [
            self.list_items_description.get(n['item_description']) for n in self.items_name if str_number in n['item_description'].lower()
        ] if str_number else []
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
    def add_item(self, e):
        if self.item_id.value == '' or self.item_names.value == '':
            self.snack_bar_func(f"Please Enter Goods Details")
            return

        try:
            item = {
                'serial': self.serial_number,
                'name': self.item_names.value,
                'quantity': int(self.item_Qty.value),
                'unit': self.item_unit.value,
                'rates': float(self.item_rate.value),
                'gst': float(self.item_gst.value),
                'total': int(self.item_Qty.value) * float(self.item_rate.value)
            }
        except ValueError as ve:
            self.snack_bar_func(f"Invalid input: {ve}")
            return

        self.item_id.value = ''
        self.item_names.value = ''
        self.item_Qty.value = ''
        self.item_unit.value = ''
        self.item_rate.value = ''
        self.item_gst.value = 0.0
        self.items.append(item)
        self.update_table()
        self.serial_number +=1
        self.temp = self.serial_number - 1
        self.snack_bar_func(f"{self.temp} Item Added")
        self.app_layout.page.update()
    def update_table(self):
        self.data_table.rows.clear()
        for item in self.items:
            print(f"items dictionary {item} keys{item.keys()} value{item.values()}")
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f"{item['serial']}",style=self.style_col)),
                    ft.DataCell(ft.Text(f"{item['serial']}",style=self.style_col)),
                    ft.DataCell(ft.Text(f"{item['serial']}",style=self.style_col)),
                    ft.DataCell(ft.Text(f"{item['serial']}",style=self.style_col)),
                    ft.DataCell(ft.Text(f"{item['serial']}",style=self.style_col)),
                    ft.DataCell(ft.Text(f"{item['serial']}",style=self.style_col)),
                    ft.DataCell(ft.Text(f"{item['serial']}",style=self.style_col)),
                    ft.DataCell(ft.Text(f"{item['serial']}",style=self.style_col))
                ])
            )
        self.app_layout.page.update()
    def del_data(self, e):
        index = e.control.data - 1
        print(f"Deleting row {index}")
        del self.items[index]
        self.update_table()
        self.page.update()
        
    def update_table(self):
        self.serial_number = 1
        self.data_table.rows.clear()
        
        for item in self.items:
            item['serial'] = self.serial_number
            rate=item['rates']-item['rates']*item['gst']/100
            item['total']=float(item['quantity'])*float(item['rate'])
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(self.serial_number))),
                    ft.DataCell(ft.Text(item['name']), show_edit_icon=True, on_tap=self.editbtn, data=[self.serial_number, 'name']),
                    ft.DataCell(ft.Text(str(item['quantity'])), show_edit_icon=True, on_tap=self.editbtn, data=[self.serial_number, 'quantity']),
                    ft.DataCell(ft.Text(str(item['unit'])),show_edit_icon=True,on_tap=self.editbtn,data=[self.serial_number,'unit']),
                    ft.DataCell(ft.Text(f"Rs.{rate:.2f}"), show_edit_icon=True, on_tap=self.editbtn, data=[self.serial_number, 'rate']),
                    ft.DataCell(ft.Text(f"{item['gst']:.2f}%"), show_edit_icon=True, on_tap=self.editbtn, data=[self.serial_number, 'gst']),
                    ft.DataCell(ft.Text(f"Rs.{item['total']:.2f}")),
                    ft.DataCell(ft.Row([ft.IconButton("delete",icon_color='red',
                                            data=self.serial_number,
                                            on_click=self.del_data)
                        ])),

                ],selected=False,)
            )
            self.serial_number += 1
        amount_total=sum([item['total'] for item in self.items])
        bill_amt_total=amount_total*0.12
        self.grand_total_amount.value = f"Grand Total: Rs. {sum([item['total'] for item in self.items]):.2f}"
        self.app_layout.page.update()
    def editbtn(self, e):
        self.what = e.control.data[1]
        print(self.what)
        self.loc = e.control.data[0] - 1
        self.temp_name.value = self.items[self.loc]['name']
        self.temp_Qty.value = self.items[self.loc]['quantity']
        self.temp_unit.value=self.items[self.loc]['unit']
        self.temp_rate.value = self.items[self.loc]['rate']
        self.temp_gst.value=self.items[self.loc]['gst']
        print(f"Editing item at index {self.loc} for attribute {self.what}")
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Bill"),
            content=ft.Container(content=ft.Column(controls=[self.temp_about, self.temp_name, ft.ResponsiveRow([self.temp_Qty, self.temp_unit,self.temp_rate,self.temp_gst])]),width=800,height=400),
            actions=[ft.TextButton("Save", on_click=self.Update_table_edit),ft.TextButton("Close", on_click=lambda e: self.close_dialog(self.dialog))],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        # self.page.dialog=self.dialog
        self.app_layout.page.overlay.clear()
        self.app_layout.page.overlay.append(self.dialog)
        self.dialog.open=True
        self.app_layout.page.update()
    def close_dialog(self,dlg):
        dlg.open = False
        self.app_layout.page.update()
    def Update_table_edit(self, e):
        self.close_dialog(self.dialog)
        # self.page.dialog.open=False
        self.items[self.loc]['name'] = self.temp_name.value
        self.items[self.loc]['quantity'] = float(self.temp_Qty.value)
        self.items[self.loc]['unit'] = self.temp_unit.value
        self.items[self.loc]['rate'] = float(self.temp_rate.value)
        self.items[self.loc]['gst'] = float(self.temp_gst.value)
        self.update_table()
        
        
    def reset_form(self, e):
        if self.items:
            self.customer_name.value = ""
            self.customer_address.value = ""
            self.customer_mobile.value = ""
            self.item_id.value = ""
            self.item_names.value = ""
            self.item_Qty.value = ""
            self.item_unit.value = ""
            self.item_rate.value = ""
            self.item_gst.value=0.0
            self.items.clear()
            self.update_table()
            self.app_layout.page.update()
        else:
            self.snack_bar_func(f"Please Add Customer Detail also add Goods Detail")
    def generate_bill(self,e):
        print("generate_bill function in invoice.py")
        self.invoice=WInvoice()
        self.invoice.customer_detail(self.customer_name.value,self.customer_address.value ,self.customer_mobile.value)
        self.invoice.item_description()
        for item in self.items:
            self.invoice.item(item['name'],item['quantity'],item['unit'],item['rate']/100,item['total']/100)
        payable_amount=sum([item['total'] for item in self.items])
        self.payable_amount.value = f"Payable Amount: Rs. {(sum([item['total'] for item in self.items])-int(self.item_discount.value))/100:.2f}"
        self.invoice.footer()
        self.invoice.generate_bill(
            self.customer_name.value,
            payable_amount,
            self.item_discount.value,
            10,
            f" {(sum([item['total'] for item in self.items])-int(self.item_discount.value)):.2f}")
        bill_filename=os.path.join("D:\\", "Bill_payment_SAB", "test", f"{self.customer_name.value}.pdf")
        self.print_bill(bill_filename)
        self.app_layout.page.update()
    def print_bill(self, bill_file):
        # This will print the bill on the default printer
        printer_name = win32print.GetDefaultPrinter()
        win32api.ShellExecute(
            0,
            "print",
            bill_file,  # Path to the generated bill file (could be a PDF or DOCX)
            None,
            ".",
            0
        )

        # print(f"Printing {bill_file} on {printer_name}")