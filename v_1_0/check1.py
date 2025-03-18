import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector
from datetime import datetime
class InvoiceFilteringBackend:
    def __init__(self, host, user, password, database):
        self.config = {
            'host': os.getenv(host),
            'user': os.getenv(user),
            'password': os.getenv(password),
            'database': os.getenv(database),
            'raise_on_warnings': True,
        }
        try:
            self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Exception as err:
            self.connection.close()
    def ensure_connection(self):
        """Ensure the database connection is active"""
        if not self.connection.is_connected():
            try:
                self.connection.reconnect(attempts=3, delay=5)
                self.cursor=self.connection.cursor(dictionary=True)
                print("Connection Established")
            except Error as err:
                print(f"Error reconnecting to database: {err}")
    def fetch_invoices(self, table_type, **kwargs):
        """
        Fetch invoices based on the selected table type (retail or wholesale) and additional filters.

        :param table_type: "RETAIL" or "WHOLESALE"
        :param kwargs: Additional parameters for filtering
        :return: List of matching invoices with customer details
        """
        self.ensure_connection()
        try:
            query = ""
            params = []
            if table_type == "sell_retail":
                query1 = """
                    SELECT sr.invoice_no, sr.amount, sr.sell_time, sr.cust_id,sr.unique_id, c.person_name, c.mobile, c.location
                    FROM sell_retail sr
                    JOIN Customer c ON sr.cust_id = c.cust_id
                    WHERE 1=1
                """
            elif table_type == "sell_wholesale":
                query1 = """
                    SELECT sw.invoice_no, sw.amount,sw.remark, sw.sell_time, sw.sell_wholesale_status, sw.cust_id, c.person_name, c.mobile, c.location
                    FROM sell_wholesale sw
                    JOIN Customer c ON sw.cust_id = c.cust_id
                    WHERE 1=1
                """
            print(f"{query1,*params}")
        # Add filters based on kwargs
            if "start_date" in kwargs and "end_date" in kwargs:
                query = " ".join([query1 ," AND sw.sell_time BETWEEN %s AND %s" if table_type == "sell_wholesale" else " AND sr.sell_time BETWEEN %s AND %s"])
                params += [kwargs["start_date"], kwargs["end_date"]]
            if "mobile" in kwargs:
                query =" ".join([query1," AND c.mobile = %s"])
                params.append(kwargs["mobile"])
            if "customer_id" in kwargs:
                query = " ".join([query1," AND c.cust_id = %s"])
                params.append(kwargs["customer_id"])
            if "invoice_number" in kwargs:
                query = " ".join([query1," AND sw.invoice_no = %s" if table_type == "sell_wholesale" else " AND sr.invoice_no = %s"])
                params.append(kwargs["invoice_number"])
            if "payment_status" in kwargs and table_type == "sell_wholesale":
                query = " ".join([query1," AND sw.sell_wholesale_status = %s"])
                params.append(kwargs["payment_status"])
            if "min_amount" in kwargs and "max_amount" in kwargs:
                query = " ".join([query1," AND sw.amount BETWEEN %s AND %s" if table_type == "sell_wholesale" else " AND sr.amount BETWEEN %s AND %s"])
                params += [kwargs["min_amount"], kwargs["max_amount"]]
            
            print(f"{query,*params}")
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            return e
        finally:
            self.cursor.close()
        

    def update_wholesale_status(self, invoice_no):
        """
        Update the status of a wholesale invoice from 'Unpaid' to 'Paid'.
        some code update needed as pr requirement,as download 
        :param invoice_no: Invoice number to update
        :return: Success message or error message
        """
        try:
            # Check current status
            self.cursor.execute(
                "SELECT sell_wholesale_status FROM sell_wholesale WHERE invoice_no = %s", (invoice_no,)
            )
            result = self.cursor.fetchone()

            if not result:
                return {"status": "error", "message": "Invoice not found"}

            current_status = result["sell_wholesale_status"]
            if current_status == "Paid":
                return {"status": "error", "message": "Cannot change status from 'Paid' to 'Unpaid'"}

            # Update status to 'Paid'
            self.cursor.execute(
                "UPDATE sell_wholesale SET sell_wholesale_status = 'Paid' WHERE invoice_no = %s", (invoice_no,)
            )
            self.connection.commit()
            return {"status": "success", "message": f"Invoice {invoice_no} status updated to 'Paid'"}
        except Exception as e:
            self.connection.rollback()
            return {"status": "error", "message": str(e)}

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        
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
        self.table_type_dropdown = dropdown(
            label="Select Table Type",
            options=[
                ft.dropdown.Option(text="RETAIL",key="sell_retail"),
                ft.dropdown.Option(text="WHOLESALE",key="sell_wholesale"),
            ],
            on_change=self.table_type_changed,
            width=300,
        )
        self.dropdown_filter = dropdown(
            width=300,
            label="Search By",
            options=[
                ft.dropdown.Option("Date Range"),
                ft.dropdown.Option("Customer Mobile Number"),
                ft.dropdown.Option("Customer ID"),
                ft.dropdown.Option("Invoice Number"),
                # ft.dropdown.Option("Type of Payment Method"),
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
                    first_date=datetime.datetime(year=2000, month=1, day=1),
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
                    first_date=datetime.datetime(year=2000, month=1, day=1),
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
        self.list_view=ft.ListView(expand=True,auto_scroll=False)
        self.result_container=ft.Container(content=self.list_view,height=550,padding=10,border=ft.border.all(1,ft.Colors.GREY))
        self.content=ft.Column(
                [
                    # ft.Text("Invoice Filtering", size=20, weight="bold"),
                    ft.Row([self.table_type_dropdown,
                    self.dropdown_filter,]),
                    self.input_fields,self.result_container,
                    # self.submit_button,
                ],
                spacing=20,expand=True
            )
    def start_date_func(self,e):
        self.start_date.value=e.control.value.strftime('%Y-%m-%d')
        self.start_date.update()
    def end_date_func(self,e): 
        self.end_date.value=e.control.value.strftime('%Y-%m-%d')
        self.end_date.update()
        
    def handle_dismissal(self,e):
        self.snack_bar_func(f"DatePicker dismissed{e}")
        
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
    def table_type_changed(self, e):
        """Handles table type selection (Retail or Wholesale)."""
        selected_table = self.table_type_dropdown.value
        self.list_view.controls.clear()
        if selected_table == "sell_retail":
            self.list_view.controls.append(ft.Row([
                ft.Container(ft.Text("SR No."),expand=2),
                ft.Container(ft.Text("Invoice No."),expand=4),
                ft.Container(ft.Text("amount"),expand=4),
                ft.Container(ft.Text("Customer Name"),expand=5),
                ft.Container(ft.Text("Unique ID"),expand=4),
                ft.Container(ft.Text("Date Time"),expand=5),
                ft.Container(ft.Text("Action"),expand=2),
            ],expand=True))
            
        else:
            self.list_view.controls.append(ft.Row([
                
                ft.Container(ft.Text("SR No."),expand=2),
                ft.Container(ft.Text("Invoice No."),expand=4),
                ft.Container(ft.Text("amount"),expand=4),
                ft.Container(ft.Text("Remark"),expand=5),
                ft.Container(ft.Text("Customer Name"),expand=5),
                ft.Container(ft.Text("Status"),expand=3),
                ft.Container(ft.Text("Date Time"),expand=5),
                ft.Container(ft.Text("Days"),expand=3),
                ft.Container(ft.Text("Action"),expand=2),
            ],expand=True))
        self.list_view.controls.append(ft.Divider())
        self.update() 
    
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
        # elif selected_option == "Type of Payment Method":
        #     self.input_fields.controls.append(
        #         self.payment_method,
        #     )
        #     self.input_fields.controls.append(self.submit_button)
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
        self.update()
    def database_access(self):
        # Access the database based on the selected filter option
        self.backend = InvoiceFilteringBackend(
        host=os.getenv('host'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        database=os.getenv('database')
            )
    def download_pdf(self,e):
        # Download the PDF report based on the selected filter option
        print(f"Hello pdf downloader{e.control.data}")
        e.control.icon=ft.Icons.FILE_DOWNLOAD_DONE
        self.update()
    def search_invoices(self, e):
        if self.dropdown_filter.value=="Payment Status" and self.table_type_dropdown.value=="sell_retail":
            self.snack_bar_func(f"We are not give Credit On Retail Sale")
            return
        self.table_type_changed(e=None)
        # Logic for handling search action
        selected_table = self.table_type_dropdown.value
        selected_filter = self.dropdown_filter.value
        filter_params = {}
        print(f"Searching invoices by: {selected_filter},{selected_table }")
        # Gather input data
        if selected_filter == "Date Range":
            filter_params["start_date"] = self.start_date.value
            filter_params["end_date"] = self.end_date.value
        elif selected_filter == "Customer Mobile Number":
            filter_params["mobile"] = self.mobile.value
        elif selected_filter == "Customer ID":
            filter_params["customer_id"] = self.customer_id.value
        elif selected_filter == "Invoice Number":
            filter_params["invoice_number"] = self.invoice_number.value
        elif selected_filter == "Type of Payment Method":
            filter_params["payment_method"] = self.payment_method.value
        elif selected_filter == "Amount Range":
            filter_params["min_amount"] = self.amt_min.value
            filter_params["max_amount"] =self.amt_max.value
        elif selected_filter == "Payment Status":
            filter_params["payment_status"] = self.payment_status.value
        # fetchs data from the backend
        self.database_access()
        results=self.backend.fetch_invoices(selected_table, **filter_params )
        if results is None:
            self.snack_bar_func("No results returned or an error occurred during query execution.")
            
            return
        print(f"result :){results}")
        self.snack_bar_func(f"Result Are showing Total Result:) {len(results)}")
        if selected_table == "sell_retail":
            count=0
            for i in results:
                count+=1
                self.list_view.controls.append(ft.Row([
                ft.Container(ft.Text(f"{count}"),expand=2),
                ft.Container(ft.Text(f"{i['invoice_no']}"),expand=4),
                ft.Container(ft.Text(f"{i['amount']}"),expand=4),
                ft.Container(ft.Text(f"{i['person_name']}"),expand=5),
                ft.Container(ft.Text(f"{i['unique_id']}"),expand=4),
                ft.Container(ft.Text(f"{i['sell_time']}"),expand=5),
                ft.Container(ft.IconButton(icon=ft.Icons.FILE_DOWNLOAD_ROUNDED,icon_color="Green",data=[self.table_type_dropdown.value,i['invoice_no']],on_click=self.download_pdf),expand=2),
                ],expand=True))
                self.list_view.controls.append(ft.Divider())
            
        else:
            count=0
            for i in results:
                count+=1
                self.list_view.controls.append(ft.Row([
                ft.Container(ft.Text(f"{count}"),expand=2),
                ft.Container(ft.Text(f"{i['invoice_no']}"),expand=4),
                ft.Container(ft.Text(f"{i['amount']}"),expand=4),
                ft.Container(ft.Text(f"{i['remark']}"),expand=5),
                ft.Container(ft.Text(f"{i['person_name']}"),expand=5),
                ft.Container(ft.Text(f"{i['sell_wholesale_status']}"),expand=3),
                ft.Container(ft.Text(f"{i['sell_time']}"),expand=5),
                ft.Container(ft.Text(f"{(datetime.datetime.now().date()-i['sell_time'].date()).days}"),expand=3),
                ft.Container(ft.IconButton(icon=ft.Icons.FILE_DOWNLOAD_ROUNDED,icon_color="Green",data=[self.table_type_dropdown.value,i['invoice_no']],on_click=self.download_pdf),expand=2),
                ],expand=True))
                self.list_view.controls.append(ft.Divider())
        self.list_view.update()

# Run the Flet app
def main(page: ft.Page):
    
    page.add(InvoiceFilteringApp(page))
ft.app(target=main)