import flet as ft
from View.logo import invoice_logo
import time
from Controller.invoice_tax import Invoice
class tab_invoice(ft.Container):
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
        self.item_id_search=['a','abs','cde','a2']# for id serach
        self.serial_number=1
        self.items_name=['Sheat','Sheat Cover','Chain'] # for item serach
        self.customer_mobile_search=['9794144305','979414439','951650030','9415863731']
        self.what=None
        self.loc=None
        self.app_layout.page.vertical_alignment = ft.MainAxisAlignment.START
        self.padding=ft.padding.all(10)
        self.margin=ft.margin.all(0)
        self.height=self.app_layout.page.window.height
        self.uniqure_id=ft.TextField(label="Unique Id", col={"md": 4})
        # for search Id 
        self.list_items={
            name:ft.ListTile(
                title=ft.Text(name),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer,
                data=name
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
            name:ft.ListTile(
                title=ft.Text(name),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer_description,
                data=name
            )
            for name in self.items_name
        }
        # for customer deatil input
        self.customer_name = ft.TextField(label="Customer Name", col={"md": 4})#,on_change=self.tab_update)
        self.customer_address = ft.TextField(label="Customer Address", col={"md": 4})
        self.customer_mobile = ft.TextField(label="Customer Mobile Number", col={"md": 4}, on_change=self.textbox_changed_number,keyboard_type=ft.KeyboardType.NUMBER, max_length=10)
        # seach logic define 
        self.item_id = ft.TextField(label="Item Id", on_change=self.textbox_changed)
        self.search_results = ft.ListView(expand=1, spacing=4, padding=2,auto_scroll=True)
        self.search_number=ft.ListView(expand=1,spacing=4,padding=2,auto_scroll=True)
        self.search_description=ft.ListView(expand=1,spacing=4,padding=2,auto_scroll=True)
        # other thing define here 
        self.item_names = ft.TextField(label="Description of Good",on_change=self.textbox_changed_description)
        self.item_Qty = ft.TextField(label="QTY", keyboard_type=ft.KeyboardType.NUMBER)
        self.item_unit = ft.Dropdown(label='Unit', hint_text="Unit of Good", options=[
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
        ])
        self.temp_unit=ft.Dropdown(label='Unit Update', hint_text="Select Unit of Goods", options=[
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
        ], autofocus=True, col={"md": 3})
        self.item_rate = ft.TextField(label="Rate", keyboard_type=ft.KeyboardType.NUMBER, col={"md":5})
        self.item_gst=ft.TextField(label="IGST",suffix_text="%", keyboard_type=ft.KeyboardType.NUMBER, col={"md":4},value=0)
        self.item_discount = ft.TextField(label="Discount", value=0.00,keyboard_type=ft.KeyboardType.NUMBER,width=200,height=36)
        self.add_button = ft.ElevatedButton(text="Add", on_click=self.add_item, col={"md": 6})  
        self.generate_bill_button = ft.ElevatedButton(text="Generate Bill", on_click=self.generate_bill, col={"md": 6})
        # self.file_picker_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.reset_button = ft.ElevatedButton(text="Reset", on_click=self.reset_form, col={"md": 6})

        self.data_table = ft.DataTable(  
            columns=[
                ft.DataColumn(ft.Text("SN.")),
                ft.DataColumn(ft.Text("Description   ")),
                ft.DataColumn(ft.Text("QTY")),
                ft.DataColumn(ft.Text('Unit')),
                ft.DataColumn(ft.Text('Rate')),
                ft.DataColumn(ft.Text('IGST')),
                ft.DataColumn(ft.Text("Total Amount (Rs)")),
                ft.DataColumn(ft.Text("Action"))
            ],
            rows=[],bgcolor='#87A2FF',
            show_checkbox_column=True,
            data_row_color={'hovered': "#B8001F"},
            border=ft.border.all(2, 'Black'),
            divider_thickness=1,
            show_bottom_border=True,
            vertical_lines=ft.border.BorderSide(3, 'Black'),
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=60,expand=3,
        )
        self.grand_total_amount = ft.Text("Grand Total: Rs. 0.00")
        self.payable_amount = ft.Text("Payable Amount: Rs. 0.00")

        # self.file_button = ft.ElevatedButton('Select Folder', icon=ft.icons.FOLDER, on_click=lambda _: self.file_picker_dialog.get_directory_path())

        self.temp_about = ft.Text('Enter Changes Want',col={"md": 3})
        self.temp_name = ft.TextField(label="Description of Goods",col={"md": 3})
        self.temp_Qty = ft.TextField(label="Quantity",col={"md": 3})
        self.temp_rate = ft.TextField(label="Rate",col={"md": 3})
        self.temp_gst=ft.TextField(label="GST",col={"md": 3})

        self.layout =   ft.Row([
            ft.Column([ft.Container(margin=10,
                             padding=10,
                            #  width=250,
                             alignment=ft.alignment.top_center,
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.ResponsiveRow([ft.Row([ft.Text("Goods Entry",text_align=ft.TextAlign.CENTER,color="#1E3E62",size=16)], alignment=ft.MainAxisAlignment.CENTER,expand=True),
                                                        self.item_id, 
                                                    self.search_results,
                                                       self.item_names,
                                                       self.search_description,
                                                       self.item_Qty,
                                                       self.item_unit,
                                                       self.item_rate,  self.item_gst, self.add_button,
]), 
                             border_radius=10, ),
                       ft.Container(margin=3,
                             padding=5,
                            #  width=250,
                             alignment=ft.alignment.top_center,
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.ResponsiveRow([                                                    
                                                       self.generate_bill_button, self.reset_button]),
                             border_radius=10, ),
                       ft.Container(margin=2,
                             padding=2,
                            #  width=250,
                             alignment=ft.alignment.top_center,
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.ResponsiveRow([
                                   ft.Row([self.grand_total_amount,],alignment=ft.MainAxisAlignment.END),
                                                                      ft.Row([self.item_discount,],alignment=ft.MainAxisAlignment.END),
                                                                     ft.Row([self.payable_amount,],alignment=ft.MainAxisAlignment.END),
                                 ]),
                             border_radius=10, )], col={"sm": 6, "md": 4, "xl": 2},expand=1, scroll=ft.ScrollMode.AUTO,spacing=0),    # Left side
            ft.Column([  # Right side
                               
                                ft.Container(margin=10,
                             padding=10,    
                             alignment=ft.alignment.center,
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.ResponsiveRow([ft.Row([ft.Text("Customer Details",text_align=ft.TextAlign.CENTER,color="#1E3E62",size=16)], alignment=ft.MainAxisAlignment.CENTER,expand=True),self.customer_name, self.customer_address, self.customer_mobile,ft.Row([self.search_number],alignment=ft.MainAxisAlignment.END),]),
       
                             border_radius=10, ),
                                
                                ft.Container(margin=10,
                             padding=10,
                             alignment=ft.alignment.top_center,
                             bgcolor=ft.colors.TRANSPARENT,
                             content= ft.Row(
        [self.data_table,],scroll=ft.ScrollMode.ADAPTIVE,expand=3
        ),
                             border_radius=10, expand=3),
                                ft.Container(margin=10,
                             padding=10,
                             alignment=ft.alignment.center_right,    
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.ResponsiveRow([self.uniqure_id, ]),
                             border_radius=10, expand=True),
            ], expand=3, scroll=ft.ScrollMode.AUTO)
        ],alignment=ft.MainAxisAlignment.START,expand=True,vertical_alignment=ft.CrossAxisAlignment.START)
                # Add a floating button to add new customer tabs

        # self.app_layout.page.floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT
        # self.tab_name=ft.Text(f"{self.customer_name.value}")

        self.content=self.layout#ft.Column([self.layout,],alignment=ft.MainAxisAlignment.START,scroll=ft.ScrollMode.ADAPTIVE)    
        self.app_layout.page.update()  
    

    def textbox_changes(self,string):
        str_lower=string.control.value.lower()
        self.search_results.controls=[
            self.list_items.get(n) for n in self.item_id_search if str_lower in n.lower()
        ] if str_lower else []
        self.app_layout.page.update()
    # id printer auto  complition
    def printer(self, e):
        print(f"check value list {e.control.data}")
        self.item_id.value = e.control.data
        self.item_names.value = 'diynshy'
        self.item_names.update()
        self.item_Qty.value = 5
        self.item_Qty.update()
        self.item_rate.value = 5
        self.item_rate.update()
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
        self.search_results.controls.clear()
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
            self.list_items.get(n) for n in self.item_id_search if str_lower in n.lower()
        ] if str_lower else []
        self.app_layout.page.update()
    # for mobile numnber search 
    def textbox_changed_number(self,string):
        str_number = string.control.value
        self.search_number.controls = [
            self.list_customer_number.get(n) for n in self.customer_mobile_search if str_number in n
        ] if str_number else []
        self.app_layout.page.update()
    # for seach by goods description 
    def textbox_changed_description(self, string):
        str_number = string.control.value
        self.search_description.controls = [
            self.list_items_description.get(n) for n in self.items_name if str_number in n.lower()
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
        if self.item_id.value=='' or self.item_names.value=='':
            self.snack_bar_func( f"Please Enter Goods Details")
        else: 
            item = {
            'serial': self.serial_number,
            'name': self.item_names.value,
            'quantity': int(self.item_Qty.value),
            'unit': self.item_unit.value,
            'rate': float(self.item_rate.value),
            'gst':  float(self.item_gst.value),
            'total': int(self.item_Qty.value) * float(self.item_rate.value),
            }
            self.item_id.value=''
            self.item_names.value=''
            self.item_Qty.value=''
            self.item_unit.value=''
            self.item_rate.value=''
            self.item_gst.value=0.0
            self.items.append(item)
            self.update_table()
            self.temp=self.serial_number-1
            self.snack_bar_func(f"{self.temp} Item Added")
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
            rate=item['rate']-item['rate']*item['gst']/100
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
        self.invoice=Invoice()
        self.invoice.customer_detail(self.customer_name.value,self.customer_address.value ,self.customer_mobile.value,"","")
        self.invoice.item_description()
        for item in self.items:
            self.invoice.item(item['name'],item['quantity'],item['unit'],item['rate']-item['rate']*item['gst']/100,item['gst'],item['total'])
        payable_amount=sum([item['total'] for item in self.items])
        self.payable_amount.value = f"Payable Amount: Rs. {(sum([item['total'] for item in self.items])-int(self.item_discount.value)):.2f}"
        
        self.invoice.generate_bill("D:\Bill_payment_SAB\test",payable_amount,self.item_discount.value,f" {(sum([item['total'] for item in self.items])-int(self.item_discount.value)):.2f}")
        self.app_layout.page.update()