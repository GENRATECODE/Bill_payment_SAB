import flet as ft
from View.logo import invoice_logo
import time
import asyncio  
from Model.buyyer import dealer_database

class Statement(ft.Container):
    def __init__(self, app_layout, page):
        self.app_layout = app_layout
        super().__init__()
        self.page = page
        self.page.auto_scroll = False
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.app_layout = app_layout
        self.app_layout.page.auto_scroll = True
        self.items = []
        self.expand = True
        self.dealer_ids = []
        self.style_col=ft.TextStyle( word_spacing=5,color="#0D1282",weight=ft.FontWeight.BOLD,size=11,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
        self.idlist = ft.Dropdown(
            label='Dealer ID',
            hint_text="Search By Dealer ID",
            options=[],
            width=200,
            border_radius=ft.border_radius.all(10),
            counter_style=ft.TextStyle(
                word_spacing=5,
                color="#6A1E55",
                size=18,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.colors.BLUE_GREY_300,
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.SOLID,
                )
            ),on_change=self.show_dealer_information, 
            border_color="#1A1A1D",
            bgcolor="#EBEAFF",
            color="#1A1A1D",
            focused_bgcolor="#C6E7FF",
            focused_color="#3B1E54",
            icon_content=ft.Icon(ft.icons.AD_UNITS_SHARP),
            icon_enabled_color="#1A1A1D",
            label_style=ft.TextStyle(
                word_spacing=5,
                color="#6A1E55",
                size=18,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.colors.BLUE_GREY_300,
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.SOLID,
                )
            ),
        )

        self.reload = ft.IconButton(
            icon=ft.icons.REFRESH_SHARP,
            icon_color="black",
            icon_size=30,
            tooltip="Reload Dealer IDs",
            on_click=self.database_reload
        )
        self.clear_information = ft.IconButton(
            icon=ft.icons.CLEAR_SHARP,
            icon_color="black",
            icon_size=30,
            tooltip="Clear show Information",
            on_click=self.clear_view_result
        )
        self.tool_for_serach = ft.Column([
            ft.Text("Select ID for Dealer statement", size=30, weight="bold", color="#133E87"),
            ft.Row([self.idlist, self.reload, self.clear_information])
        ], expand=2,alignment=ft.MainAxisAlignment.START,)
        self.information_show = ft.Column(expand=4,alignment=ft.MainAxisAlignment.START)
        self.result_show = ft.Column(expand=True,alignment=ft.MainAxisAlignment.CENTER,scroll=ft.ScrollMode.ADAPTIVE)
        self.content = ft.Column(
            [ft.Container(content=ft.Row([self.tool_for_serach, self.information_show],),padding=ft.padding.all(10)),
             self.result_show,
             
             ],
            expand=True
        )
        self.database_reload()  # Initial load
        self.app_layout.page.update()
    def clear_view_result(self,e):
        self.information_show.controls.clear()
        self.result_show.controls.clear()
        self.app_layout.page.update()
    def option_gen(self):
        return [ft.dropdown.Option(i) for i in self.dealer_ids]

    def database_reload(self, e=None):
        self.dealer_manager = dealer_database()
        self.dealer_ids = self.dealer_manager.list_dealers()
        self.idlist.options = self.option_gen()  # Update options in the existing Dropdown
        self.app_layout.page.update()  # Notify the UI of the changes
        self.dealer_manager.close_connection()
    def show_dealer_information(self, e):
        """Display dealer information based on selected dealer ID."""
        selected_id = self.idlist.value
        if not selected_id:
            self.snack_bar_func("Please select a Dealer ID")
            return
    
        # Fetch dealer data from the database
        dealer_data = self.dealer_manager.get_dealer_details(selected_id)  # Custom method in `dealer_database`
        if not dealer_data:
            self.snack_bar_func("No data found for the selected Dealer ID")
            return
        # Populate information_show with dealer details
        self.information_show.controls.clear()
        self.result_show.controls.clear()
        self.information_show.controls=[
            ft.Row([ft.Card(expand=2,
                                content=ft.Container(
                                    ft.Column(
                                        [  ft.Text("ID Details",color='black', weight="bold",style=self.style_col),
                                            
                                            
                                            ft.Row([
                                              ft.Text(f"Dealer ID: {dealer_data['dealer_id']}", weight="bold",style=self.style_col),         
                                                ft.Text(f"  GST: {dealer_data['gst']}",style=self.style_col),        ],expand=False,alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                                         ft.Text(f"Mobile: {dealer_data['mobile']}",style=self.style_col),
                                         ft.Text(f"Email: {dealer_data['email']}",style=self.style_col),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ),ft.Card(expand=2,
                                content=ft.Container(
                                    ft.Column(
                                        [   ft.Text("Company Details",color='black', weight="bold",style=self.style_col),
                                           ft.Text(f"Company Name: {dealer_data['company_name']}",style=self.style_col),
                                            ft.Text(f"Agent Name: {dealer_data['name_agent']}",style=self.style_col),
                                            ft.Text(f"Address: {dealer_data['Address']}",style=self.style_col),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            )]),ft.Row([ft.Card(
                                content=ft.Container(
                                    ft.Column(
                                        [ft.Text("Amount Details",color='black', weight="bold",style=self.style_col),
                                        ft.Text(f"OutStanding: ₹{dealer_data['outstaing']}", size=14, weight=ft.FontWeight.BOLD,style=self.style_col),
                                        ft.Text(f"Advance : ₹{dealer_data['advanced']}", size=14, weight=ft.FontWeight.BOLD,style=self.style_col),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ),ft.Card(expand=True,
                                content=ft.Container(
                                    ft.Column(
                                        [   ft.Text("Bank Details",color='black', weight="bold"),
                                            ft.Row([
                                                
                                                    
                                                    ft.Text(f"Bank: {dealer_data['bank']}",style=self.style_col),
                                                    ft.Text(f"Branch: {dealer_data['branch']}",style=self.style_col),],expand=False,alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                                            ft.Text(f"Account No: {dealer_data['ACOUNT_NO']}",style=self.style_col),
                                            ft.Text(f"IFSC Code: {dealer_data['ifsc_NO']}",style=self.style_col),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(30),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            )]),
        ]
        self.result_show.controls=[ft.Text("Transaction Detail", size=25,weight="bold",style=self.style_col),
                                   ft.Row(
            [
            ft.Container(ft.Text("Sr"), bgcolor="lightblue", padding=10, width=100),
            ft.Container(ft.Text("Invoice Number"), bgcolor="lightblue", padding=10, width=150),
            ft.Container(ft.Text("Amount"), bgcolor="lightblue", padding=10, width=100),
            ft.Container(ft.Text("Status"), bgcolor="lightblue", padding=10, width=150),
            ft.Container(ft.Text("Payment ID"), bgcolor="lightblue", padding=10, width=150),
            ft.Container(ft.Text("Payment Amount"), bgcolor="lightblue", padding=10, width=150),
            ft.Container(ft.Text("Remark"), bgcolor="lightblue", padding=10, width=200),
            ft.Container(ft.Text("Date"), bgcolor="lightblue", padding=10, width=150),
            ]
            )
                                   ]
        self.update_table_value()
        self.app_layout.page.update()
    def update_table_value(self):
        data = {
        "payment id": [1, 2, 3, 4, 5, 6],
        "invoice number": [112, 144, 145, 1345, 1667, 267],
        "date": [2022, 2022, 2022, 2022, 2022, 2023],
        "amount": [100, 200, 300, 400, 500, 600],
        "status": ['paid', 'unpaid', 'paid', 'unpaid', 'paid', 'unpaid'],
        "payment amount": [3434, 4353, 34324, 23432, 2342, 23423],
        "remark": [
            "deposit bank transfer invoice number 112",
            "deposit bank transfer invoice number 112",
            "deposit bank transfer invoice number 112",
            "deposit bank transfer invoice number 112",
            "deposit bank transfer invoice number 112",
            "deposit bank transfer invoice number 112"
        ]
        }
        for i in range(len(data["payment id"])):
            data_row = ft.Row(
                [
                ft.Container(ft.Text(str(i + 1)), padding=10, width=100),  # Sr column (Index + 1)
                ft.Container(ft.Text(str(data["invoice number"][i])), padding=10, width=150),
                ft.Container(ft.Text(str(data["amount"][i])), padding=10, width=100),
                ft.Container(ft.Text(data["status"][i]), padding=10, width=150),
                ft.Container(ft.Text(str(data["payment id"][i])), padding=10, width=150),
                ft.Container(ft.Text(str(data["payment amount"][i])), padding=10, width=150),
                ft.Container(ft.Text(data["remark"][i]), padding=10, width=200),
                ft.Container(ft.Text(str(data["date"][i])), padding=10, width=150),
                ]   
                )
            self.result_show.controls.append(data_row)
        self.app_layout.page.update()
    def snack_bar_func(self, text):
        snack_bar = ft.SnackBar(
            content=ft.Text(text),
            action="Alright!",
            action_color="Pink",
            dismiss_direction=ft.DismissDirection.HORIZONTAL
        )
        self.page.overlay.clear()
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        self.app_layout.page.update()
