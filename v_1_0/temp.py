import flet as ft
import datetime
from flet import TextField, ElevatedButton,Dropdown,Container
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
    
class InvoiceFilteringApp(Container):
    def __init__(self, page: ft.Page,**kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.page.title = "Invoice Filtering"
        self.page.padding = 20

        # Components
        self.dropdown_filter = dropdown(
            width=300,
            label="Search By",
            options=[
                ft.dropdown.Option("Date Range"),
                ft.dropdown.Option("Customer Mobile Number"),
                ft.dropdown.Option("Customer ID"),
                ft.dropdown.Option("Invoice Number"),
                ft.dropdown.Option("Type of Payment Method"),
                ft.dropdown.Option("Amount Range"),
                ft.dropdown.Option("Payment Status"),
            ],
            on_change=self.filter_option_changed,
        )

        self.input_fields = ft.Row()  # Container for dynamic input fields
        self.submit_button = button_style(text="Search", on_click=self.search_invoices, height=40,width=80)
        self.input_fields.controls.append(self.submit_button)
        
        # other neccseary deatil
        self.start_date=text_filed_style(label="Start Date",
                                         kbtype=ft.KeyboardType.DATETIME, 
                                         hint_text="YYYY-MM-DD",
                                         suffix=ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.start_date_func,
                    on_dismiss=self.handle_dismissal,
                )
            ) ),)
        self.end_date=text_filed_style(label="End Date",kbtype=ft.KeyboardType.DATETIME, hint_text="YYYY-MM-DD",
                                       suffix=ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: self.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.end_date_func,
                    on_dismiss=self.handle_dismissal,
                )
            ) ),)
        self.mobile=text_filed_style(label='Mobile Number',kbtype=ft.KeyboardType.NUMBER,leng=10,input_filter=ft.NumbersOnlyInputFilter())
        self.customer_id=text_filed_style(label='Customer ID',hint_text="R-RetailSale,W-wholeSale",kbtype=ft.KeyboardType.TEXT,capitalization=ft.TextCapitalization.CHARACTERS)
        self.invoice_number=text_filed_style(label='Invoice Number',kbtype=ft.KeyboardType.TEXT,capitalization=ft.TextCapitalization.CHARACTERS)
        self.amt_min=text_filed_style(label='Minimum Amount',kbtype=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.amt_max=text_filed_style(label='Maximum Amount',kbtype=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ),)
        self.payment_method=dropdown(
                    width=300,
                    label="Select Payment Method",
                    options=[
                        ft.dropdown.Option("Cash"),
                        ft.dropdown.Option("Online"),
                        ft.dropdown.Option("Net Banking"),
                        ft.dropdown.Option("Person Through"),
                    ],
                )
        self.payment_status=dropdown(
                    width=300,
                    label="Payment Status",
                    options=[
                        ft.dropdown.Option("Paid"),
                        ft.dropdown.Option("Unpaid"),
                        ft.dropdown.Option("Partially Paid"),
                    ],
                )
        # Add components to the page
        self.page.add(
            ft.Column(
                [
                    ft.Text("Invoice Filtering", size=20, weight="bold"),
                    self.dropdown_filter,
                    self.input_fields,
                    # self.submit_button,
                ],
                spacing=20,
            )
        )
    def start_date_func(self,e):
        self.start_date.value=e.control.value.strftime('%Y-%m-%d')
        self.start_date.update()
    def end_date_func(self,e): 
        self.end_date.value=e.control.value.strftime('%Y-%m-%d')
        self.end_date.update()
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
        self.page.update()
        # self.app_layout.page.update()     
    def filter_option_changed(self, e):
        selected_option = self.dropdown_filter.value
        self.input_fields.controls.clear()  # Clear previous fields

        # Update input fields based on the selected filter option
        if selected_option == "Date Range":
            self.input_fields.controls.extend([
                self.start_date,
                self.end_date,
            ])
            self.input_fields.controls.append(self.submit_button)
        elif selected_option == "Customer Mobile Number":
            self.input_fields.controls.append(
                self.mobile,  
            )
            self.input_fields.controls.append(self.submit_button)
        elif selected_option == "Customer ID":
            self.input_fields.controls.append(
                self.customer_id
            )
            self.input_fields.controls.append(self.submit_button)
        elif selected_option == "Invoice Number":
            self.input_fields.controls.append(
                self.invoice_number
            )
            self.input_fields.controls.append(self.submit_button)
        elif selected_option == "Type of Payment Method":
            self.input_fields.controls.append(
                self.payment_method,
            )
            self.input_fields.controls.append(self.submit_button)
        elif selected_option == "Amount Range":
            self.input_fields.controls.extend([
                self.amt_min,
                self.amt_max,
            ])
            self.input_fields.controls.append(self.submit_button)
        elif selected_option == "Payment Status":
            self.input_fields.controls.append(
               self.payment_status,
            )
            self.input_fields.controls.append(self.submit_button)

        # Update the page
        self.page.update()

    def search_invoices(self, e):
        # Logic for handling search action
        selected_filter = self.dropdown_filter.value

        print(f"Searching invoices by: {selected_filter}")
        for field in self.input_fields.controls:
            if isinstance(field, ft.Checkbox):
                print(f"{field.label}: {field.value}")
            elif isinstance(field, ft.Dropdown):
                print(f"{field.label}: {field.value}")
            else:
                print(f"{field.label}: {field.value}")


# Run the Flet app
def main(page: ft.Page):
    InvoiceFilteringApp(page)

ft.app(target=main)
