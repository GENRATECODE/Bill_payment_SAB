import flet as ft
from flet import UserControl
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controller.invoice_tax import Invoice
from View.logo import invoice_logo
from Controller.invoice_option_tax import WInvoice

class InvoiceApp(UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.page.adaptive = True
        self.page.title = "Invoice Generation"
        self.page.auto_scroll = False
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.item_id_search = ['a', 'abs', 'cde', 'a2', 'a5']
        self.serial_number = 1
        self.items = []
        self.what = None
        self.loc = None
        self.selected_files = ft.Text()

        self.customer_name = ft.TextField(label="Customer Name", col={"md": 4})
        self.customer_address = ft.TextField(label="Customer Address", col={"md": 4})
        self.customer_mobile = ft.TextField(label="Customer Mobile Number", col={"md": 4}, keyboard_type=ft.KeyboardType.NUMBER, max_length=10)
        self.item_id = ft.TextField(label="Item Id", on_change=self.textbox_changed)
        self.search_results = ft.ListView(expand=1, spacing=10, padding=20,auto_scroll=True)
        self.item_names = ft.TextField(label="Description of Good", col={"md": 3})
        self.item_Qty = ft.TextField(label="QTY", col={"md": 3}, keyboard_type=ft.KeyboardType.NUMBER)
        self.item_unit = ft.Dropdown(label='Unit', hint_text="Select Unit of Goods", options=[
            ft.dropdown.Option("PCS"),
            ft.dropdown.Option("SET"),
            ft.dropdown.Option("PKT"),
            ft.dropdown.Option("GRS"),      
            ft.dropdown.Option("PAIR"),
            ft.dropdown.Option("LT."),
            ft.dropdown.Option("KG."),
            ft.dropdown.Option("GM."),
            ft.dropdown.Option("Dozen"),
        ], autofocus=True, col={"md": 3})
        self.temp_unit=ft.Dropdown(label='Unit Update', hint_text="Select Unit of Goods", options=[
            ft.dropdown.Option("PCS"),
            ft.dropdown.Option("SET"),
            ft.dropdown.Option("PKT"),
            ft.dropdown.Option("GRS"),
            ft.dropdown.Option("PAIR"),
            ft.dropdown.Option("LT."),
            ft.dropdown.Option("KG."),
            ft.dropdown.Option("GM."),
            ft.dropdown.Option("Dozen"),
        ], autofocus=True, col={"md": 3})
        self.item_rate = ft.TextField(label="Rate", keyboard_type=ft.KeyboardType.NUMBER, col={"md": 3})
        self.add_button = ft.ElevatedButton(text="Add Item", on_click=self.add_item, col={"md": 2})
        self.generate_bill_button = ft.ElevatedButton(text="Generate Bill", on_click=self.generate_bill, on_long_press=self.wgenerate_bill,col={"md": 2})
        # self.file_picker_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.reset_button = ft.ElevatedButton(text="Reset", on_click=self.reset_form, col={"md": 2})

        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Serial No.")),
                ft.DataColumn(ft.Text("Description of Goods")),
                ft.DataColumn(ft.Text("QTY")),
                ft.DataColumn(ft.Text('Unit')),
                ft.DataColumn(ft.Text('Rate')),
                ft.DataColumn(ft.Text("Total Amount (Rs)")),
                ft.DataColumn(ft.Text("Action"))
            ],
            rows=[],
            show_checkbox_column=True,
            data_row_color={'hovered': "0x30FF0000"},
            border=ft.border.all(2, 'Black'),
            divider_thickness=1,
            show_bottom_border=True,
            vertical_lines=ft.border.BorderSide(3, 'Black'),
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=60,
        )
        self.grand_total_amount = ft.Text("Grand Total: Rs. 0.00")
        self.bill_details = ft.Text("Total Bill: Rs. 0.00")
        self.CGST=ft.Text("CGST 6% Rs. 0.00")
        self.SGST=ft.Text("SGST 6% Rs. 0.00")
        # self.file_button = ft.ElevatedButton('Select Folder', icon=ft.icons.FOLDER, on_click=lambda _: self.file_picker_dialog.get_directory_path())

        self.temp_about = ft.Text('Enter Changes Want')
        self.temp_name = ft.TextField(label="Description of Goods")
        self.temp_Qty = ft.TextField(label="Quantity")
        self.temp_rate = ft.TextField(label="Rate")
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Bill"),
            content=ft.Column(controls=[self.temp_about, self.temp_name, self.temp_Qty, self.temp_unit,self.temp_rate]),
            actions=[ft.TextButton("Save", on_click=self.Update_item)],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        self.page.dialog = self.dialog
        # self.page.overlay.append(self.file_picker_dialog)

        self.page.add(
            ft.Column([
                ft.Row([ft.Text("Customer Detail", size=22)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(color=ft.colors.WHITE70),
                ft.Container(margin=10,
                             padding=10,
                             alignment=ft.alignment.center,
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.ResponsiveRow([self.customer_name, self.customer_address, self.customer_mobile, ]),
                             border_radius=10, ),
                ft.Row([ft.Text("Good Entry", size=22)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(color=ft.colors.WHITE70),
                ft.Container(margin=10,
                             padding=10, 
                             alignment=ft.alignment.center,
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.ResponsiveRow([self.item_id, self.search_results,
                                                       self.item_names,
                                                       self.item_Qty,
                                                       self.item_unit,
                                                       self.item_rate,
                                                       self.add_button,
                                                       self.generate_bill_button, self.reset_button]),
                             border_radius=10, ),
                ft.Divider(color=ft.colors.WHITE70),
                ft.Row(controls=[]),
                ft.Row([ft.Text("Good List", size=22)], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(color=ft.colors.WHITE70),
                ft.Container(margin=10,
                             padding=10,
                             alignment=ft.alignment.center,
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.ResponsiveRow([self.data_table, ]),
                             border_radius=10, ),
                ft.Divider(color=ft.colors.WHITE70),
                ft.Container(margin=10,
                             padding=10,
                             alignment=ft.alignment.center_left,
                             bgcolor=ft.colors.BLUE_ACCENT,
                             content=ft.Column([ft.Row([self.bill_details,
                                              ],
                                            alignment=ft.MainAxisAlignment.END, ),
                                                ft.Row([self.SGST,],alignment=ft.MainAxisAlignment.END),
                                                ft.Row([self.CGST,],alignment=ft.MainAxisAlignment.END),
                                                ft.Row([self.grand_total_amount,],alignment=ft.MainAxisAlignment.END),],
                ),#horizontal_alignment=ft.CrossAxisAlignment.END),
                             border_radius=10, ),
                ft.Divider(color=ft.colors.WHITE70),
                # self.file_button,
                # self.selected_files
            ], scroll=ft.ScrollMode.AUTO)
        )
        
        self.list_items = {
            name: ft.ListTile(
                title=ft.Text(name),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer,
                data=name
            )
            for name in self.item_id_search
        }
    def editbtn(self, e):
        self.what = e.control.data[1]
        print(self.what)
        self.loc = e.control.data[0] - 1
        self.temp_name.value = self.items[self.loc]['name']
        self.temp_Qty.value = self.items[self.loc]['quantity']
        self.temp_unit.value=self.items[self.loc]['unit']
        self.temp_rate.value = self.items[self.loc]['rate']
        print(f"Editing item at index {self.loc} for attribute {self.what}")
        self.page.dialog.open = True
        self.page.update()
    def printer(self, e):
        print(f"check value list {e.control.data}")
        self.item_id.value = e.control.data
        self.item_names.value = 'diynsh'
        self.item_names.update()
        self.item_Qty.value = 5
        self.item_Qty.update()
        self.item_rate.value = 5
        self.item_rate.update()
        self.search_results.controls.clear()
        self.page.update()

    def textbox_changed(self, string):
        str_lower = string.control.value.lower()
        self.search_results.controls = [
            self.list_items.get(n) for n in self.item_id_search if str_lower in n.lower()
        ] if str_lower else []
        self.page.update()

    def Update_item(self, e):
        self.page.dialog.open = False

        self.items[self.loc]['name'] = self.temp_name.value
        
        self.items[self.loc]['quantity'] = int(self.temp_Qty.value)
        
        self.items[self.loc]['unit']=self.temp_unit.value
        print(f"{self.items[self.loc]['unit']}")   
        self.items[self.loc]['rate'] = float(self.temp_rate.value)
        
        self.items[self.loc]['total'] = self.items[self.loc]['quantity'] * self.items[self.loc]['rate']
        self.temp_rate.value = ""
        self.temp_name.value = ""
        self.temp_unit.value=""
        self.temp_Qty.value = ""
        self.update_table()
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Serial No {self.loc+1} Update"))
        self.page.snack_bar.open = True
        self.page.update()



    def update_table(self):
        self.serial_number = 1
        self.data_table.rows.clear()
        for item in self.items:
            item['serial'] = self.serial_number
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(self.serial_number))),
                    ft.DataCell(ft.Text(item['name']), show_edit_icon=True, on_tap=self.editbtn, data=[self.serial_number, 'name']),
                    ft.DataCell(ft.Text(str(item['quantity'])), show_edit_icon=True, on_tap=self.editbtn, data=[self.serial_number, 'quantity']),
                    ft.DataCell(ft.Text(str(item['unit'])),show_edit_icon=True,on_tap=self.editbtn,data=[self.serial_number,'unit']),
                    ft.DataCell(ft.Text(f"Rs. {item['rate']:.2f}"), show_edit_icon=True, on_tap=self.editbtn, data=[self.serial_number, 'rate']),
                    ft.DataCell(ft.Text(f"Rs. {item['total']:.2f}")),
                    ft.DataCell(ft.Row([ft.IconButton("delete",icon_color='red',
                                            data=self.serial_number,
                                            on_click=self.del_data)
                        ])),

                ],selected=False,)
            )
            self.serial_number += 1
        amount_total=sum([item['total'] for item in self.items])
        bill_amt_total=amount_total*0.12
        self.bill_details.value=f"Total Bill Rs. {amount_total-bill_amt_total:.2f}" 
        self.CGST.value=f"CGST 6% Rs.{(amount_total*0.06):.2f}"
        self.SGST.value=f"SGST 6% Rs.{(amount_total*0.06):.2f}"
        self.grand_total_amount.value = f"Grand Total: Rs. {sum([item['total'] for item in self.items]):.2f}"
        self.page.update()

    def del_data(self, e):
        index = e.control.data - 1
        print(f"Deleting row {index}")
        del self.items[index]
        self.update_table()
        self.page.update()

    def add_item(self, e):
        if self.item_id.value=='' or self.item_names.value=='':
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Please Enter Goods Details"))
            self.page.snack_bar.open = True
            self.page.update()
            
        else: 
            item = {
            'serial': self.serial_number,
            'name': self.item_names.value,
            'quantity': int(self.item_Qty.value),
            'unit': self.item_unit.value,
            'rate': float(self.item_rate.value),
            'total': int(self.item_Qty.value) * float(self.item_rate.value),
            }
            self.item_id.value=''
            self.item_names.value=''
            self.item_Qty.value=''
            self.item_unit.value=''
            self.item_rate.value=''
            self.items.append(item)
            self.update_table()
            self.temp=self.serial_number-1
            self.page.snack_bar = ft.SnackBar(ft.Text(f"{self.temp} Item Added"))
            self.page.snack_bar.open = True
            self.page.update()
    def generate_pdf(self,desktop_path):# some modification needed 
        self.invoice=Invoice()
        self.invoice.custmer_detail(name_field=self.customer_name.value,address=self.customer_address.value,mobile_number=self.customer_mobile.value)
        # customer information
        self.invoice.item_description()
        for item in self.items:
            self.invoice.item(item_name=item['name'],qty=f"{item['quantity']}",unit=item['unit'],rate=f"Rs. {item['rate']:.2f}",amount=f"Rs. {item['total']:.2f}")
        # item in pdf 
        self.folder_name="Bills"
        self.folder_path=os.path.join(desktop_path,self.folder_name)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        pdf_path=os.path.join(self.folder_path,f'{self.customer_name.value}_tax.pdf')
        if os.path.exists(pdf_path):
            self.page.snack_bar=ft.SnackBar(ft.Text(f"File already exists:{pdf_path}.\n Please Close the file if it's open or choose a different name."))
            self.page.snack_bar.open=True
            self.page.update()
            return 
        try:
            self.invoice.generate_bill(pdf_path=pdf_path,grand_total=self.grand_total_amount.value,b_amt=self.bill_details.value,cgst=self.CGST.value,sgst=self.SGST.value)
            self.page.snack_bar=ft.SnackBar(ft.Text(f"PDF Generated Successfully! Saved to {pdf_path}"))
        except PermissionError:
             self.page.snack_bar = ft.SnackBar(ft.Text(f"Permission denied: {pdf_path}.\nPlease close the file if it's open, or choose a different name."))
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"An error occurred: {str(e)}"))
        self.page.snack_bar.open=True
        self.page.update()
    def wgenerate_pdf(self,desktop_path):
        self.invoice=WInvoice()
        self.invoice.custmer_detail(name_field=self.customer_name.value,address=self.customer_address.value,mobile_number=self.customer_mobile.value)
        # customer information
        self.invoice.item_description()
        for item in self.items:
            self.invoice.item(item_name=item['name'],qty=f"{item['quantity']}",unit=item['unit'],rate=f"Rs. {item['rate']:.2f}",amount=f"Rs. {item['total']:.2f}")
        # item in pdf 
        self.folder_name="Bills"
        self.folder_path=os.path.join(desktop_path,self.folder_name)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        pdf_path=os.path.join(self.folder_path,f'{self.customer_name.value}_optiontax.pdf')
        if os.path.exists(pdf_path):
            self.page.snack_bar=ft.SnackBar(ft.Text(f"File already exists: {pdf_path}.\nPlease close the file if it's open, or choose a different name."))
            self.page.snack_bar.open=True
            self.page.update()
            return 
        try:
            self.invoice.generate_bill(name=pdf_path,grand_total=self.grand_total_amount.value)
            self.page.snack_bar=ft.SnackBar(ft.Text(f"PDF Generated Successfully! Saved to {pdf_path}"))
        except PermissionError:
             self.page.snack_bar = ft.SnackBar(ft.Text(f"Permission denied: {pdf_path}.\nPlease close the file if it's open, or choose a different name."))
        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"An error occurred: {str(e)}"))
        self.page.snack_bar.open=True
        self.page.update()
    def wgenerate_bill(self,e):
        if self.items:
            if self.customer_name.value!='' or self.customer_address.value!='' or self.customer_mobile.value!='':
                if self.selected_files.value:
                    save_pdf=self.selected_files.value
                    self.wgenerate_pdf(save_pdf)
                else:
                    self.page.snack_bar=ft.SnackBar(ft.Text(f"Please Add Path To Save Bill in Profile Path"))
                    self.page.snack_bar.open=True
                    self.page.update()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Please Enter Customer Detail!!!"))
                self.page.snack_bar.open = True
                self.page.update()
        else:
            self.page.snack_bar=ft.SnackBar(ft.Text("Please Add Item into Table:)"
                                            ))
            self.page.snack_bar.open=True
            self.page.update()   
    def generate_bill(self, e):
        if self.items:
            if self.customer_name.value!='' or self.customer_address.value!='' or self.customer_mobile.value!='':
                if self.selected_files.value:
                    save_pdf=self.selected_files.value
                    self.generate_pdf(save_pdf)
                else:
                    self.page.snack_bar=ft.SnackBar(ft.Text(f"Please Add Path To Save Bill in Profile Path"))
                    self.page.snack_bar.open=True
                    self.page.update()
            else:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Please Enter Customer Detail!!!"))
                self.page.snack_bar.open = True
                self.page.update()
        else:
            self.page.snack_bar=ft.SnackBar(ft.Text("Please Add Item into Table:)"
                                            ))
            self.page.snack_bar.open=True
            self.page.update()
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
            self.items.clear()
            self.update_table()
            self.page.update()
        else:
            self.page.snack_bar=ft.SnackBar(ft.Text(f"Please Add Customer Detail also add Goods Detail"))
            self.page.snack_bar.open=True
            self.page.update()

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        self.selected_files.value = (
            e.path if e.path else "Cancelled!"
        )
        self.page.update()

# def main(page: ft.Page):
#     InvoiceApp(page)

# ft.app(target=main)
