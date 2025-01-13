import flet as ft
from View.logo import invoice_logo
from flet import TextField, ElevatedButton,Dropdown,Container
import time
from Model.buyyer import dealer_database
import datetime
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
        self.invoice_no=text_filed_style(label="Invoice Number",col1={ "md":2, "xl": 2})
        self.counter=0
        self.cupertino_date_picker=text_filed_style(col1={ "md": 2, "xl":2},label="Invoice Date",kbtype=ft.KeyboardType.DATETIME,content_padding=8,suffix=ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: self.app_layout.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.handle_change_invoice,
                    on_dismiss=self.handle_dismissal,
                )
            )  # Function to call when icon button is clicked
        ))
        self.Name_company=dropdown(label="Dealer IDs",
                                    hint_text="Select Dealer ID",
                                    # on_change=self.show_dealer_information, 
                                    col={"md": 3, "xl": 3})
        self.Amount=text_filed_style(label="Amount",col1={ "md": 2, "xl": 2},input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.database_reload()
        self.Nag=text_filed_style(label="Nag",col1={ "md": 1, "xl": 1})
        self.Sender_Trans=text_filed_style(label="Sender Transport Name",col1={ "md": 3, "xl":3})
        self.SGrNO=text_filed_style(label="Gr NO",col1={ "md": 1, "xl": 1})
        self.Receiver_tansport=text_filed_style(label="Receiver Transport Name",col1={ "md":2.5, "xl": 2.5})
        self.RGrNO=text_filed_style(label="Gr NO",col1={ "md": 1, "xl": 1})
        self.Receiving_date=text_filed_style(label="Receiving Date",kbtype=ft.KeyboardType.DATETIME,content_padding=8,suffix=ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: self.app_layout.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.handle_change,
                    on_dismiss=self.handle_dismissal,
                )
            )  # Function to call when icon button is clicked
        ),col1={ "md": 3, "xl": 3})
        self.transport_charge=text_filed_style(label="Transport Charge",col1={ "md": 1.8, "xl": 1.8},input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.FirstRow=ft.ResponsiveRow(
            [self.invoice_no,
             self.cupertino_date_picker,
             self.Name_company,
             self.Amount,self.Nag,
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
            [
             
             self.b,
             self.export,
             ]
        )
        
        # View Section Applied for 
        self.month_dropdown=dropdown(
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
    def database_reload(self, e=None):
        self.dealer_manager = dealer_database()
        self.dealer_ids = self.dealer_manager.list_dealers_with_company()
        self.Name_company.options = self.option_gen()  # Update options in the existing Dropdown
        self.app_layout.page.update()  # Notify the UI of the changes
        self.dealer_manager.close_connection()
    def option_gen(self):
        return  [
            ft.dropdown.Option(
                key=i['dealer_id'],
                text=i['company_name']
            )
            for i in self.dealer_ids
            ]
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
    

        
