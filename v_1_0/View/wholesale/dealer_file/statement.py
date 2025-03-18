import flet as ft
from Model.buyyer import dealer_database
from flet import TextField,Dropdown,DataTable,ElevatedButton
from Model.user import User
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
    
class Statement(ft.Container):
    def __init__(self, app_layout, page):
        super().__init__()
        self.app_layout=app_layout
        self.page = page 
        self.expand=True
        self.margin=ft.margin.all(5)
        self.style_col=ft.TextStyle( word_spacing=5,color="#0D1282",weight=ft.FontWeight.BOLD,size=11,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
        self.reload = ft.IconButton(
            icon=ft.Icons.REFRESH_SHARP,
            icon_color="black",
            icon_size=30,
            tooltip="Reload Dealer IDs",
            on_click=self.database_reload
        )
        self.clear_information = ft.IconButton(
            icon=ft.Icons.CLEAR_SHARP,
            icon_color="red",
            icon_size=30,
            tooltip="Clear show Information",
            on_click=self.clear_view_result
        )
        self.list_dropdown=dropdown(label="Dealer IDs",width=300,
                                    hint_text="Select Dealer ID",
                                    on_change=self.show_dealer_information, 
                                    )
        self.row1=ft.Column([ ft.Row([self.list_dropdown,self.reload ,self.clear_information,],)
                                ],expand=4,alignment=ft.MainAxisAlignment.START,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.row2=ft.Column([],expand=8,alignment=ft.MainAxisAlignment.START,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.result_show=ft.Column(alignment=ft.MainAxisAlignment.START,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        row=ft.Row([self.row1,self.row2,],alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.CrossAxisAlignment.START)
        self.content=ft.Column([
           row,self.result_show
                                ],
                                alignment=ft.MainAxisAlignment.START,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.database_reload()
    def clear_view_result(self,e):
        self.list_dropdown.value=""
        self.row2.controls.clear()
        self.result_show.controls.clear()
        self.app_layout.page.update()
    def option_gen(self):
        return  [
            ft.dropdown.Option(
                key=i['dealer_id'],
                text=i['company_name']
            )
            for i in self.dealer_ids
            ]
    def database_reload(self, e=None):
        self.dealer_manager = dealer_database()
        self.dealer_ids = self.dealer_manager.list_dealers_with_company()
        self.list_dropdown.options = self.option_gen()  # Update options in the existing Dropdown
        self.app_layout.page.update()  # Notify the UI of the changes
        self.dealer_manager.close_connection()
    def show_dealer_information(self, e):
        """Display dealer information based on selected dealer ID."""
        self.list_dropdown.value=(self.list_dropdown.value).splitlines()[0]
        selected_id = self.list_dropdown.value
        self.list_dropdown.update()
        if not selected_id:
            self.snack_bar_func("Please select a Dealer ID")
            return
    
        # Fetch dealer data from the database
        self.dealer_data = self.dealer_manager.get_dealer_details(selected_id)  # Custom method in `dealer_database`
        if not self.dealer_data:
            self.snack_bar_func("No data found for the selected Dealer ID")
            return
        # Populate information_show with dealer details
        self.row2.controls.clear()
        self.result_show.controls.clear()
        self.row2.controls=[
            ft.Row([ft.Card(expand=3,
                                content=ft.Container(
                                    ft.Column(
                                        [  ft.Text("ID Details",size=25,color='black', weight="bold",style=self.style_col),
                                            
                                            
                                            ft.Row([
                                              ft.Text(f"Dealer ID: {self.dealer_data['dealer_id']}", weight="bold",style=self.style_col),         
                                                ft.Text(f"  GST: {self.dealer_data['gst']}",style=self.style_col),        ],expand=False,alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                                            ft.Row([
                                              ft.Text(f"Mobile: {self.dealer_data['mobile']}",style=self.style_col),         
                                              ft.Text(f"Email: {self.dealer_data['email']}",style=self.style_col),        ],expand=False,alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                                         
                                         
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=20,
                                    height=150,
                                    bgcolor=ft.Colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ),ft.Card(expand=4,
                                content=ft.Container(
                                    ft.Column(
                                        [   ft.Text("Bank Details",size=25,color='black', weight="bold"),
                                            ft.Row([
                                                
                                                    
                                                    ft.Text(f"Bank: {self.dealer_data['bank']}",style=self.style_col),
                                                    ft.Text(f"Branch: {self.dealer_data['branch']}",style=self.style_col),],expand=False,alignment=ft.MainAxisAlignment.SPACE_EVENLY),
                                            ft.Text(f"Account No: {self.dealer_data['ACOUNT_NO']}",style=self.style_col),
                                            ft.Text(f"IFSC Code: {self.dealer_data['ifsc_NO']}",style=self.style_col),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(30),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.Colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ),]),ft.Row([ft.Card(expand=1,
                                content=ft.Container(
                                    ft.Column(
                                        [  ft.Text(f" Amount Details ",color='black',size=25, weight="bold",style=self.style_col),
                                         ft.Text(f"OutStanding: {self.dealer_data['outstaing']} ",color='black', weight="bold",style=self.style_col),
                                            ft.Text(f" Advance : {self.dealer_data['advanced']}",style=self.style_col),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=20,
                                    height=150,
                                    bgcolor=ft.Colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ),ft.Card(expand=2,
                                content=ft.Container(on_long_press=self.editbtn,
                                    content=ft.Column(
                                        [   ft.Text("Company Details",color='black',size=25, weight="bold",style=self.style_col),
                                           ft.Text(f"Company Name: {self.dealer_data['company_name']}",style=self.style_col),
                                            ft.Text(f"Agent Name: {self.dealer_data['name_agent']}",style=self.style_col),
                                            ft.Text(f"Address: {self.dealer_data['address']}",style=self.style_col),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.Colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            )]),
        ]
        self.result_show.controls=[ft.Text("Transaction Detail", size=30,weight="bold",style=self.style_col),
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
            ],alignment=ft.MainAxisAlignment.CENTER
            )
                                   ]
        self.update_table_value()
        self.app_layout.page.update()
    def editbtn(self,e):
        self.temp_about = ft.Text('Edit Option To Dealer Details',col={"md": 3})
        self.com_name_id=text_filed_style(read_only=True,
                                    label='Dealer ID', 
                                    value=self.dealer_data['dealer_id']
                                    )
        self.com_name=text_filed_style(read_only=True,
                                    label='Company Name', 
                                    value=self.dealer_data['company_name']
                                    )
        self.agent_name=text_filed_style(
                                    label='Agent Name', 
                                    value=self.dealer_data['name_agent']
                                    )
        self.agent_Mobile=text_filed_style(
                                    label='Agent Number', 
                                    value=self.dealer_data['mobile']
                                    )
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Edit Bill"),
            content=ft.Container(
                content=ft.Column(controls=[
                    self.temp_about,
                    ft.Row([self.com_name_id,
                                      self.com_name,
                                        ],alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([
                                      self.agent_name,self.agent_Mobile,
                                        ],alignment=ft.MainAxisAlignment.CENTER)]),width=800,height=200),
            actions=[ft.TextButton("Save", 
                                   on_click=self.varify_authentication
                                   ),ft.TextButton("Close", on_click=lambda e: self.close_dialog(self.dialog))],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.overlay.clear()
        self.page.overlay.append(self.dialog)
        self.dialog.open=True
        self.app_layout.page.update()
    def close_dialog(self,dlg):
        dlg.open = False
        self.app_layout.page.update() 
    def varify_authentication(self, e):
        # Clear previous overlays and open verification dialog
        self.close_dialog(self.dialog)
        self.page.overlay.clear()
        user_name=self.app_layout.page.session.get_keys()[0]
        print(user_name)
        self.user_name=text_filed_style(value=user_name,label="User ID", password=False)
        self.password=text_filed_style(label="Password", password=True)
        self.dialog_verify = ft.AlertDialog(
            title=ft.Text("Verify Credentials"),
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Text("Enter Your User ID and Password"),
                    ft.Row([self.user_name,],alignment=ft.MainAxisAlignment.CENTER),
                    self.password
                ]),
                width=300,
                height=200
            ),
            actions=[
                ft.TextButton("Verify", on_click=self.update_details),
                ft.TextButton("Close", on_click=lambda e: self.close_dialog(self.dialog_verify))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        self.page.overlay.append(self.dialog_verify)
        self.dialog_verify.open = True
        self.page.update()
    def update_details(self, e):
        # Simulate authentication
        # Check credentials against the database
        if self.authenticate_user(self.user_name.value,self.password.value):
            # Update agent details in the database
            dealer_manager = dealer_database()
            dealer_manager.update_agent(
               self.agent_name.value,
              self.agent_Mobile.value,
               self.com_name_id.value
            )
            dealer_manager.close_connection()

            self.close_dialog(self.dialog_verify)

            self.snack_bar_func("Details updated successfully!")
        else:
            self.close_dialog(self.dialog_verify)
            self.snack_bar_func("Invalid User ID or Password")
    def authenticate_user(self, user_id, password):
        # Placeholder: Replace with actual database check
        return 1 if self.app_layout.page.session.get(user_id)==password else 0
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
                ]  ,alignment=ft.MainAxisAlignment.CENTER
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
