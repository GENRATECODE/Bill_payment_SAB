import flet as ft
import datetime

import base64
# Sample data storage (In-memory for demonstration purposes)
# In a real-world application, consider using a database.
customers = []
payments = []
spends = []

class CollectionPage(ft.Container):
    def __init__(self, page, app_layout):
        super().__init__()
        self.page = page
        self.app_layout = app_layout
        self.bgcolor = '#f0f0f0'
        
        # Search Fields
        self.search_customer = ft.TextField(label="Customer Name", hint_text="Enter customer name", width=200)
        self.search_address = ft.TextField(label="Address", hint_text="Enter address", width=200)
        self.search_mobile = ft.TextField(label="Mobile Number", hint_text="Enter mobile number", width=200)
        search_button = ft.ElevatedButton("Search", on_click=self.perform_search)
        
        # Customer Detail Fields
        self.customer_name = ft.TextField(label="Customer Name", hint_text="Enter customer name", width=200)
        self.customer_address = ft.TextField(label="Address", width=200)
        self.customer_mobile = ft.TextField(label="Mobile Number", width=200)
        
        # Entry Detail Fields
        self.amount = ft.TextField(label="Amount", width=200)
        self.remark = ft.TextField(label="Remark", width=200)
        self.paid_by = ft.TextField(label="Paid By / Collect By", width=200)
        
        # Date Picker for Invoice Date
        self.invoice_date = ft.TextField(label="Receiving Date",content_padding=8,suffix=ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.handle_change,
                    on_dismiss=self.handle_dismissal,
                )
            )  # Function to call when icon button is clicked
        ),col={"sm": 6, "md": 4, "xl": 2})
        
        # Submit Button
        submit_button = ft.ElevatedButton("Add Collection", on_click=self.add_collection)
        
        # Results List
        self.results_list = ft.ListView(expand=True)
        
        # Build content layout
        self.content = ft.Column(
            [
                ft.Text("Collection Entry", size=24, weight="bold", color="#133E87"),
                ft.Row([self.search_customer, self.search_address, self.search_mobile, search_button], spacing=10),
                ft.Divider(),
                ft.Row([self.customer_name, self.customer_address, self.customer_mobile], spacing=10),
                ft.Row([self.amount, self.invoice_date, self.remark, self.paid_by], spacing=10),
                submit_button,
                ft.Divider(),
                ft.Text("Search Results:", size=18, weight="bold"),
                self.results_list
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            # padding=20
        )
        self.controls = [self.content]
    
    def show_date_picker(self):
        date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2020, month=1, day=1),
            last_date=datetime.datetime(year=2100, month=12, day=31),
            initial_date=datetime.datetime.today(),
            on_change=self.date_selected,
            on_dismiss=self.handle_dismissal,
        )
        self.page.dialog = date_picker
        date_picker.open = True
        self.page.update()
    
    def date_selected(self, e):
        self.invoice_date.value = e.control.value.strftime('%d-%m-%Y')
        self.page.dialog = None
        self.page.update()
    
    def handle_dismissal(self, e):
        self.page.dialog = None
        self.page.snack_bar = ft.SnackBar(ft.Text("Date picker dismissed"))
        self.page.update()
    
    def perform_search(self, e):
        # Clear previous results
        self.results_list.controls.clear()
        
        # Retrieve search criteria
        name = self.search_customer.value.lower()
        address = self.search_address.value.lower()
        mobile = self.search_mobile.value
        
        # Perform search
        for customer in customers:
            if (name in customer['name'].lower() or not name) and \
               (address in customer['address'].lower() or not address) and \
               (mobile in customer['mobile'] or not mobile):
                self.results_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(customer['name']),
                        subtitle=ft.Text(f"Address: {customer['address']}, Mobile: {customer['mobile']}"),
                        on_click=lambda e, c=customer: self.populate_fields(c)
                    )
                )
        if not self.results_list.controls:
            self.results_list.controls.append(ft.Text("No matching records found."))
        self.page.update()
    
    def populate_fields(self, customer):
        self.customer_name.value = customer['name']
        self.customer_address.value = customer['address']
        self.customer_mobile.value = customer['mobile']
        self.page.update()
    
    def add_collection(self, e):
        # Validate inputs
        if not self.customer_name.value or not self.amount.value or not self.invoice_date.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please fill in all required fields."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Add to customers list if new
        existing = next((c for c in customers if c['mobile'] == self.customer_mobile.value), None)
        if not existing:
            customers.append({
                'name': self.customer_name.value,
                'address': self.customer_address.value,
                'mobile': self.customer_mobile.value
            })
        
        # Add collection entry
        collection_entry = {
            'customer_name': self.customer_name.value,
            'address': self.customer_address.value,
            'mobile': self.customer_mobile.value,
            'amount': self.amount.value,
            'invoice_date': self.invoice_date.value,
            'remark': self.remark.value,
            'paid_by': self.paid_by.value
        }
        payments.append(collection_entry)  # Assuming 'payments' list stores collections
        self.page.snack_bar = ft.SnackBar(ft.Text("Collection added successfully!"))
        self.page.snack_bar.open = True
        self.clear_fields()
        self.page.update()
    
    def clear_fields(self):
        self.customer_name.value = ""
        self.customer_address.value = ""
        self.customer_mobile.value = ""
        self.amount.value = ""
        self.invoice_date.value = ""
        self.remark.value = ""
        self.paid_by.value = ""

class PaymentPage(ft.Container):
    def __init__(self, page, app_layout):
        super().__init__()
        self.page = page
        self.app_layout = app_layout
        self.bgcolor = '#f0f0f0'
        
        # Payment Fields
        self.dealer_id = ft.TextField(label="Dealer ID", hint_text="Enter dealer ID", width=200)
        self.dealer_name = ft.TextField(label="Dealer Name", hint_text="Enter dealer name", width=200)
        self.dealer_mobile = ft.TextField(label="Mobile Number", hint_text="Enter mobile number", width=200)
        self.dealer_address = ft.TextField(label="Address", width=200)
        self.payment_amount = ft.TextField(label="Amount", width=200)
        self.bill_invoice_number = ft.TextField(label="Bill/Invoice Number", width=200)
        self.payment_method = ft.Dropdown(
            label="Payment Method",
            options=[
                ft.dropdown.Option("Cash"),
                ft.dropdown.Option("Credit Card"),
                ft.dropdown.Option("Bank Transfer"),
                ft.dropdown.Option("Mobile Payment")
            ],
            width=200
        )
        
        # Submit Button
        submit_button = ft.ElevatedButton("Add Payment", on_click=self.add_payment)
        
        # Results List
        self.payment_list = ft.ListView(expand=True)
        
        # Build content layout
        self.content = ft.Column(
            [
                ft.Text("Bill Payment Entry", size=24, weight="bold", color="#133E87"),
                ft.Row([self.dealer_id, self.dealer_name, self.dealer_mobile], spacing=10),
                ft.Row([self.dealer_address], spacing=10),
                ft.Row([self.payment_amount, self.bill_invoice_number, self.payment_method], spacing=10),
                submit_button,
                ft.Divider(),
                ft.Text("Payment Records:", size=18, weight="bold"),
                self.payment_list
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            # padding=20
        )
        self.controls = [self.content]
    
    def add_payment(self, e):
        # Validate inputs
        if not self.dealer_id.value and not self.dealer_name.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please enter Dealer ID or Dealer Name."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        if not self.payment_amount.value or not self.bill_invoice_number.value or not self.payment_method.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please fill in all required fields."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Add to payments list
        payment_entry = {
            'dealer_id': self.dealer_id.value,
            'dealer_name': self.dealer_name.value,
            'dealer_mobile': self.dealer_mobile.value,
            'dealer_address': self.dealer_address.value,
            'amount': self.payment_amount.value,
            'bill_invoice_number': self.bill_invoice_number.value,
            'payment_method': self.payment_method.value
        }
        payments.append(payment_entry)
        self.page.snack_bar = ft.SnackBar(ft.Text("Payment added successfully!"))
        self.page.snack_bar.open = True
        self.add_payment_to_list(payment_entry)
        self.clear_fields()
        self.page.update()
    
    def add_payment_to_list(self, payment):
        self.payment_list.controls.append(
            ft.ListTile(
                title=ft.Text(f"Dealer: {payment['dealer_name'] or payment['dealer_id']}"),
                subtitle=ft.Text(f"Amount: {payment['amount']}, Method: {payment['payment_method']}"),
            )
        )
    
    def clear_fields(self):
        self.dealer_id.value = ""
        self.dealer_name.value = ""
        self.dealer_mobile.value = ""
        self.dealer_address.value = ""
        self.payment_amount.value = ""
        self.bill_invoice_number.value = ""
        self.payment_method.value = ft.DropdownOption(selected=False)

class SpendPage(ft.Container):
    def __init__(self, page, app_layout):
        super().__init__()
        self.page = page
        self.app_layout = app_layout
        self.bgcolor = '#f0f0f0'
        
        # Spend Fields
        self.spend_type = ft.Dropdown(
            label="Type",
            options=[
                ft.dropdown.Option("Office Supplies"),
                ft.dropdown.Option("Travel"),
                ft.dropdown.Option("Utilities"),
                ft.dropdown.Option("Entertainment"),
                ft.dropdown.Option("Other")
            ],
            width=200
        )
        self.description = ft.TextField(label="Description", width=200)
        self.amount = ft.TextField(label="Amount", width=200)
        self.paid_by = ft.TextField(label="Paid By", width=200)
        self.spend_date = ft.TextField(label="Receiving Date",content_padding=8,suffix=ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.handle_change,
                    on_dismiss=self.handle_dismissal,
                )
            )  # Function to call when icon button is clicked
        ),col={"sm": 6, "md": 4, "xl": 2})
        
        # Submit Button
        submit_button = ft.ElevatedButton("Add Spend", on_click=self.add_spend)
        
        # Results List
        self.spend_list = ft.ListView(expand=True)
        
        # Build content layout
        self.content = ft.Column(
            [
                ft.Text("Spend Entry", size=24, weight="bold", color="#133E87"),
                ft.Row([self.spend_type, self.description, self.amount], spacing=10),
                ft.Row([self.paid_by, self.spend_date], spacing=10),
                submit_button,
                ft.Divider(),
                ft.Text("Spend Records:", size=18, weight="bold"),
                self.spend_list
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            # padding=20
        )
        self.controls = [self.content]
    
    def show_date_picker(self):
        date_picker = ft.DatePicker(
            first_date=datetime.datetime(year=2020, month=1, day=1),
            last_date=datetime.datetime(year=2100, month=12, day=31),
            initial_date=datetime.datetime.today(),
            on_change=self.date_selected,
            on_dismiss=self.handle_dismissal,
        )
        self.page.dialog = date_picker
        date_picker.open = True
        self.page.update()
    
    def date_selected(self, e):
        self.spend_date.value = e.control.value.strftime('%d-%m-%Y')
        self.page.dialog = None
        self.page.update()
    
    def handle_dismissal(self, e):
        self.page.dialog = None
        self.page.snack_bar = ft.SnackBar(ft.Text("Date picker dismissed"))
        self.page.update()
    
    def add_spend(self, e):
        # Validate inputs
        if not self.spend_type.value or not self.amount.value or not self.spend_date.value:
            self.page.snack_bar = ft.SnackBar(ft.Text("Please fill in all required fields."))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Add to spends list
        spend_entry = {
            'type': self.spend_type.value,
            'description': self.description.value,
            'amount': self.amount.value,
            'paid_by': self.paid_by.value,
            'date': self.spend_date.value
        }
        spends.append(spend_entry)
        self.page.snack_bar = ft.SnackBar(ft.Text("Spend added successfully!"))
        self.page.snack_bar.open = True
        self.add_spend_to_list(spend_entry)
        self.clear_fields()
        self.page.update()
    
    def add_spend_to_list(self, spend):
        self.spend_list.controls.append(
            ft.ListTile(
                title=ft.Text(f"Type: {spend['type']}"),
                subtitle=ft.Text(f"Amount: {spend['amount']}, Paid By: {spend['paid_by']}, Date: {spend['date']}"),
            )
        )
    
    def clear_fields(self):
        self.spend_type.value = ""
        self.description.value = ""
        self.amount.value = ""
        self.paid_by.value = ""
        self.spend_date.value = ""

class MainApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Collection and Payment Tabs"
        self.build_interface()
      
    def build_interface(self):
        with open(r"D:\Bill_payment_SAB\v_1_0\assets\josn_icon\5.json", "rb") as lottie_file:
            lottie_base64_collection = base64.b64encode(lottie_file.read()).decode("utf-8")
        with open(r"D:\Bill_payment_SAB\v_1_0\assets\josn_icon\1.json", "rb") as lottie_file:
            lottie_base64_payment = base64.b64encode(lottie_file.read()).decode("utf-8")
        with open(r"D:\Bill_payment_SAB\v_1_0\assets\josn_icon\3.json", "rb") as lottie_file:
            lottie_base64_spend = base64.b64encode(lottie_file.read()).decode("utf-8")
    
        # Load Lottie animations for icons 
        collection_icon  = ft.Lottie(animate=True, fit='SCALE_DOWN', src_base64=lottie_base64_collection, width=100,  height=100,reverse=True )
        payment_icon = ft.Lottie(animate=True, fit='SCALE_DOWN', src_base64=lottie_base64_payment, width=100,  height=100,reverse=True )
        spend_icon = ft.Lottie(animate=True, fit='SCALE_DOWN', src_base64= lottie_base64_spend, width=100,  height=100,reverse=True )
        
        # Initialize Pages with references to main page and layout
        collection_page = CollectionPage(self.page, self)
        payment_page = PaymentPage(self.page, self)
        spend_page = SpendPage(self.page, self)
        
        # Define Tabs
        collection_tab = ft.Tab(
            text="Collection",
            tab_content=ft.Row([ft.Text("Collection"),collection_icon,],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            content=collection_page.content
        )
        payment_tab = ft.Tab(
            text="Bill Payment",
             tab_content=ft.Row([ft.Text("Bill Payment"),payment_icon,],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            content=payment_page.content
        )
        spend_tab = ft.Tab(
            text="Spend",
             tab_content=ft.Row([ft.Text("Spend"),spend_icon,],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            content=spend_page.content
        )
        
        # Configure Tabs
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[collection_tab, payment_tab, spend_tab],
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
        
        # Add the TabBar to the page
        self.page.add(tabs)

def main(page: ft.Page):
    app = MainApp(page)

# Run the application
ft.app(target=main, assets_dir="assets")
