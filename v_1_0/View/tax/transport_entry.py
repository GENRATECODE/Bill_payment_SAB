import flet as ft
from View.logo import invoice_logo
import time
import datetime
class transport_entry_app(ft.Container):
    def __init__(self,app_layout, page):
        self.app_layout=app_layout
        super().__init__()
        self.page = page
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        self.app_layout=app_layout
        self.app_layout.page.auto_scroll=True
        self.margin=20
        self.padding=10   #df
        self.items=[]
        self.invoice_no=ft.TextField(label="Invoice Number",col={"sm": 6, "md": 4, "xl": 2})
        self.counter=0
        self.cupertino_date_picker=ft.TextField(label="Invoice Date",content_padding=8,suffix=ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: self.app_layout.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.handle_change_invoice,
                    on_dismiss=self.handle_dismissal,
                )
            )  # Function to call when icon button is clicked
        ),col={"sm": 6, "md": 4, "xl": 2})
        self.Name_company=ft.TextField(label="Company Name",col={"sm": 6, "md": 4, "xl": 2})
        self.Amount=ft.TextField(label="Amount",col={"sm": 6, "md": 4, "xl": 2})
        self.Nag=ft.TextField(label="Nag",col={"sm": 6, "md": 4, "xl": 2})
        self.Sender_Trans=ft.TextField(label="Sender Transport Name",col={"sm": 6, "md": 4, "xl": 2})
        self.SGrNO=ft.TextField(label="Gr NO",col={"sm": 6, "md": 4, "xl": 2})
        self.Receiver_tansport=ft.TextField(label="Receiver Transport Name",col={"sm": 6, "md": 4, "xl": 2})
        self.RGrNO=ft.TextField(label="Gr NO",col={"sm": 6, "md": 4, "xl": 2})
        self.Receiving_date=ft.TextField(label="Receiving Date",content_padding=8,suffix=ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: self.app_layout.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.handle_change,
                    on_dismiss=self.handle_dismissal,
                )
            )  # Function to call when icon button is clicked
        ),col={"sm": 6, "md": 4, "xl": 2})
        self.transport_charge=ft.TextField(label="Transport Charge",col={"sm": 6, "md": 4, "xl": 2})
        self.FirstRow=ft.ResponsiveRow(
            [self.invoice_no,
             self.cupertino_date_picker,
             self.Name_company,
             self.Amount,
             self.Nag,
             self.Sender_Trans,
             self.SGrNO,
             self.Receiver_tansport,
             self.RGrNO,
             self.Receiving_date,
             self.transport_charge
             ]
        )
        self.b = ft.ElevatedButton(text="ADD", icon='add',on_click=self.add_button,col={"sm": 6, "md": 4, "xl": 2})
        self.export=ft.ElevatedButton(text="Export Excel Formate",icon='excel',bgcolor='green', on_click=self.export_excel,col={"sm": 6, "md": 4, "xl": 2})
        self.secRow=ft.ResponsiveRow(
            [self.b,
             self.export,
             ]
        )
        
        # View Section Applied for 
        self.month_dropdown=ft.Dropdown(
                        label="Month",
            hint_text="Choose your Month?",
        width=300,
        options=[
            ft.dropdown.Option("January"),
            ft.dropdown.Option("February"),
            ft.dropdown.Option("March"),
            ft.dropdown.Option("April"),
            ft.dropdown.Option("May"),
            ft.dropdown.Option("June"),
            ft.dropdown.Option("July"),
            ft.dropdown.Option("August"),
            ft.dropdown.Option("September"),
            ft.dropdown.Option("October"),
            ft.dropdown.Option("November"),
            ft.dropdown.Option("December"),


        ],
    )
        # for dataTable
        self.datatable=ft.DataTable(
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.BorderSide(3, "blue"),
            horizontal_lines=ft.BorderSide(1, "green"),
            columns=[
                ft.DataColumn(ft.Text("Sr No")),
                ft.DataColumn(ft.Text("Invoice Number")),
                ft.DataColumn(ft.Text("Invoice Date"), numeric=True),
                ft.DataColumn(ft.Text("Company Name")),
                ft.DataColumn(ft.Text("Amount")),
                ft.DataColumn(ft.Text("Nag"), numeric=True),
                ft.DataColumn(ft.Text("Sender Transport Name")),
                ft.DataColumn(ft.Text("Gr No")),
                ft.DataColumn(ft.Text("Receiver Transport Name"), numeric=True),
                 ft.DataColumn(ft.Text("Gr No")),
                ft.DataColumn(ft.Text("Receiving Date")),
                ft.DataColumn(ft.Text("Transport Charge"), numeric=True),

            ],expand=True
        )
        self.datatable_container = ft.Row(
        controls=[self.datatable,],scroll=ft.ScrollMode.ADAPTIVE
        )

        self.layout=ft.Column([self.FirstRow,self.secRow,ft.Divider(height=9, thickness=3),self.month_dropdown,self.datatable_container,
        ],expand=True,scroll=ft.ScrollMode.ADAPTIVE)
        self.content=self.layout 
        self.app_layout.page.update()  

    def handle_change_invoice(self,e):
        self.snack_bar_func(f"Date changed: {e.control.value.strftime('%d-%m-%Y')}")
        self.cupertino_date_picker.value=e.control.value.strftime('%d-%m-%Y')
        self.app_layout.page.update()
    def handle_change(self,e):
        self.snack_bar_func(f"Date changed: {e.control.value.strftime('%d-%m-%Y')}")
        self.Receiving_date.value=e.control.value.strftime('%d-%m-%Y')
        self.app_layout.page.update()  
    def add_button(self,e):
        print("Add Item")
        self.items.append((self.counter,self.invoice_no.value,self.cupertino_date_picker.value,self.Name_company.value,self.Amount.value,self.Nag.value,self.Sender_Trans.value,self.SGrNO.value,self.Receiver_tansport.value,self.RGrNO.value,self.Receiving_date.value,self.transport_charge.value))
        self.counter+=1
        self.datatable.rows.append(self.items[-1])
        self.app_layout.page.update() 
    def export_excel(self,e):
        print("Export Item")
    def handle_dismissal(self,e):
        self.snack_bar_func(f"DatePicker dismissed")
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
    

        
