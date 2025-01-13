import flet as ft
from View.logo import invoice_logo
import time
class colleation_tab_fun(ft.Container):
    def __init__(self, app_layout,page):
        self.app_layout=app_layout
        self.page=page
        super().__init__()
        # self.bgcolor='#f0f0f0'
        self.ink=True
        self.padding=ft.padding.all(10)
        # other necessary requirement  
        self.style_button=ft.ButtonStyle(
        animation_duration=290,
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
        # overlay_color=ft.Colors.TRANSPARENT,
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
        self.opiton= ft.TextField( value="OR",read_only=True,
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
                                            # label="Dealer Name", 
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            keyboard_type=ft.KeyboardType.NAME,
                                            width=200,col={"sm": 6, "md": 4, "xl": 0.8})
        self.search_customer = ft.TextField(
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
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter customer name",keyboard_type=ft.KeyboardType.NAME,
                                            width=200,col={"sm": 6, "md": 4, "xl": 3})
        self.search_address = ft.TextField( 
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
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.STREET_ADDRESS,
                                           width=200,col={"sm": 6, "md": 4, "xl": 3})
        self.search_mobile = ft.TextField(input_filter=ft.NumbersOnlyInputFilter(), 
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
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                          keyboard_type=ft.KeyboardType.PHONE,  
                                          label="Mobile Number",
                                          hint_text="Enter mobile number", 
                                          width=200,
                                          max_length=10,col={"sm": 6, "md": 4, "xl": 2}) 
        self.search_ID = ft.TextField(prefix_icon=ft.Icons.PERM_IDENTITY_OUTLINED,
                                      autofocus=True,
                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            capitalization=ft.TextCapitalization.CHARACTERS,
                                            border_radius=ft.border_radius.all(10),
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.TEXT,
                                      label="Customer ID ",
                                      hint_text="Name_Address_Mobile_Rank ", 
                                      width=200,col={"sm": 6, "md": 4, "xl": 3})
        search_button = ft.FilledButton(
        content=ft.Row([ft.Text("Search",weight=ft.FontWeight.BOLD,size=20,italic=True)]),
        tooltip="action",
        style=self.style_button,
        width=150,
        on_click=self.perform_search,
        height=50,
        ) 
        # Customer Detail Fields
        self.customer_name = ft.TextField(
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
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter customer name",keyboard_type=ft.KeyboardType.NAME,
                                            width=200,col={"sm": 6, "md": 12, "xl": 3})
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
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.STREET_ADDRESS,
                                           width=200,col={"sm": 6, "md": 12, "xl": 3})
        self.customer_mobile =  ft.TextField(input_filter=ft.NumbersOnlyInputFilter(), 
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
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                          keyboard_type=ft.KeyboardType.PHONE,  
                                          label="Mobile Number",
                                          hint_text="Enter mobile number", 
                                          width=200,
                                          max_length=10 ,col={"sm": 6, "md": 4, "xl": 2})
                
        # Entry Detail Fields
        self.amount = ft.TextField(col={"sm": 6, "md": 4, "xl": 2},label="Amount", width=200,                                            selection_color="#526E48",
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
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.remark = ft.TextField(col={"sm": 6, "md": 4, "xl": 2},label="Remark",width=200,multiline=True,keyboard_type=ft.KeyboardType.MULTILINE,
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
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),     )
        self.paid_by = ft.TextField(col={"sm": 6, "md": 4, "xl": 2},bgcolor="#EBEAFF",label="Paid By / Collect By", width=200,keyboard_type=ft.KeyboardType.NAME,
                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            border_radius=ft.border_radius.all(10),
                                            capitalization=ft.TextCapitalization.WORDS,
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),    )
        # Date Picker for Invoice Date
        self.invoice_date = ft.TextField(                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            border_radius=ft.border_radius.all(10),keyboard_type=ft.KeyboardType.DATETIME,label="Receiving Date",content_padding=8,suffix=ft.IconButton(
            icon=ft.Icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.handle_change,
                    on_dismiss=self.handle_dismissal,
                )
            )  # Function to call when icon button is clicked
        ),col={"sm": 6, "md": 4, "xl": 3})
        # Submit Button
        submit_button = ft.FilledButton(
        content=ft.Row([ft.Text("Add Collection",weight=ft.FontWeight.BOLD,size=16.5,italic=True)]),
        tooltip="action",
        style=self.style_button,
        width=150,
    
        height=50, on_click=self.add_collection, col={"sm": 2}
        )  
        self.content = ft.Column(
            [
                # ft.Divider(),
                ft.Text("Search Customer By Customer ID OR Customer Detail", size=30, weight="bold", color="#133E87"),
                ft.ResponsiveRow([self.search_ID,self.opiton,self.search_customer, self.search_address, self.search_mobile,], spacing=10,alignment=ft.MainAxisAlignment.CENTER),
                search_button,
                ft.Divider(),
                ft.ResponsiveRow([self.customer_name,
                                    self.customer_address, 
                                    self.customer_mobile,self.amount, 
                                ], spacing=10),
                # ft.Row([self.amount, self.invoice_date, self.remark, self.paid_by,submit_button,], spacing=10),
                ft.ResponsiveRow([ 
                                    self.invoice_date, 
                                    self.remark, 
                                    self.paid_by,
                                    submit_button,], spacing=10),
                ft.Divider(),
                ft.Text("Search Results:", size=18, weight="bold"),
                # self.results_list 
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            # padding=20 
        )   
    def add_collection(self,e):
        # Add Collection in DataBase through customer ID 
        print("add collection ")                     
    def perform_search(self,e):
        # perform search operation here
        # you can use the search_customer, search_address, search_mobile, search_ID fields to get
        # the search query from the user
        print("Perform search  ")