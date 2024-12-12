import flet as ft
from View.logo import invoice_logo
import time
import datetime
from Model.id_generator import dealer_ID
from Model.buyyer import dealer_database
class dealeradd(ft.Container):
    def __init__(self, app_layout,page):
        self.app_layout=app_layout
        self.page=page
        super().__init__()
        # self.bgcolor='#f0f0f0'
        self.expand=True
        self.ink=True
        self.padding=ft.padding.all(10)
        
        self.item2database=list()
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
        # overlay_color=ft.colors.TRANSPARENT,
        # elevation={"pressed":0,"":1},
        side={
            ft.ControlState.DEFAULT:ft.BorderSide(1, "#1D24CA"),
            ft.ControlState.HOVERED:ft.BorderSide(1,"#40A2D8")
        },
        shape={
            ft.ControlState.DEFAULT:ft.RoundedRectangleBorder(radius=5),
            ft.ControlState.HOVERED:ft.RoundedRectangleBorder(radius=12)
        }
        )
        self.Dealer_ID = ft.TextField(  on_submit=lambda e: self.add_button.focus()
                                            ,selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            border_radius=ft.border_radius.all(10), 
                                            capitalization=ft.TextCapitalization.CHARACTERS,
                                            label="Dealer ID", 
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter  Dealer ID",keyboard_type=ft.KeyboardType.NAME,
                                            width=200,col={"sm": 6, "md": 4, "xl": 4})
        self.Company_agent_name = ft.TextField(  autofocus=True,
                                            on_submit=lambda e: self.Company_name.focus(),
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
                                            label="Dealer Agent Name", 
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter  Dealer Agent Name",keyboard_type=ft.KeyboardType.NAME,
                                                                            width=200,col={"sm": 6, "md": 4, "xl": 4})
        self.Company_name = ft.TextField(  on_submit=lambda e: self.Gst.focus(),
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
                                            capitalization=ft.TextCapitalization.CHARACTERS,
                                            label="Company Name", 
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter  Company Name",keyboard_type=ft.KeyboardType.NAME,
                                            width=200,col={"sm": 6, "md": 4, "xl": 4})
        
        self.Mobile = ft.TextField(input_filter=ft.NumbersOnlyInputFilter(), on_submit=lambda e: self.Address.focus(),
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
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            keyboard_type=ft.KeyboardType.PHONE,  
                                            label="Mobile Number",
                                            hint_text="Enter mobile number", 
                                            width=200,
                                            max_length=10,col={"sm": 6, "md": 4, "xl": 3})
        self.Address = ft.TextField( on_submit=lambda e: self.Email.focus(),
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
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.STREET_ADDRESS,
                                           width=200,col={"sm": 6, "md": 4, "xl": 3}) 
        self.Gst = ft.TextField( on_submit=lambda e: self.Mobile.focus(),
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
                                           label="Gst No", 
                                           hint_text="GST Number",
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.STREET_ADDRESS,
                                           width=200,col={"sm": 6, "md": 4, "xl": 3}) 
        self.Email = ft.TextField(          icon=ft.icons.CONTACT_MAIL, on_submit=lambda e: self.Bank.focus(),
                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            # prefix_text="MR/M ",
                                            # fill_color="#1A1A1D" ,
                                            # suffix_text=".com",
                                            cursor_color="#1A1A1D",
                                            border_color="#1A1A1D",
                                            color="#1A1A1D",
                                            bgcolor="#EBEAFF",
                                            # capitalization=ft.TextCapitalization.WORDS,
                                            border_radius=ft.border_radius.all(10),
                                           label="Email ", suffix_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                           hint_text="Enter Email",
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.EMAIL,
                                           width=200,col={"sm": 6, "md": 4, "xl": 3}) 
        self.Account = ft.TextField(  on_submit=lambda e: self.Ifsc.focus(),
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
                                           label="Account Number", 
                                           hint_text="Enter Account Number",
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.TEXT,
                                           width=200,col={"sm": 8, "md":10 })
        self.Ifsc = ft.TextField( on_submit=lambda e: self.Branch.focus(),
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
                                           label="IFSC", 
                                           hint_text="SBIN0000123",
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.STREET_ADDRESS,
                                           width=200,col={"sm": 8, "md":10 })
        self.Branch = ft.TextField( on_submit=self.on_submit,
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
                                           label="Branch", 
                                           hint_text="Delhi or Kanpur or Delhi.",
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.STREET_ADDRESS,
                                           width=200,col={"sm": 8, "md":10 })
        self.Bank = ft.TextField( on_submit=lambda e: self.Account.focus(),
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
                                           label="Bank", 
                                           hint_text="SBI(State Bank of India) ",
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.STREET_ADDRESS,
                                           width=200,col={"sm": 8, "md":10 })

        self.add_button =ft.FilledButton(
        content=ft.Row([ft.Text("Add Item",weight=ft.FontWeight.BOLD,size=18,italic=True)]),
        tooltip="ADD",
        style=self.style_button,
        width=150,
        on_click=self.add,
        height=50,
        ) 

        self.summit_button =ft.FilledButton(
        content=ft.Row([ft.Text("Summit",weight=ft.FontWeight.BOLD,size=18,italic=True)]),
        tooltip="Summit",
        style=self.style_button,
        width=150,
        on_click=self.Summit,
        height=50,
        ) 
        self.right=ft.Column(
            [ft.Text("Account Detail", size=15, weight="bold", color="#133E87"),
              ft.ResponsiveRow([self.Bank,
                                 self.Account,
                                  self.Ifsc ,
                                  self.Branch ,
    ],alignment=ft.MainAxisAlignment.CENTER),
             
                                 
             ],expand=1,alignment=ft.MainAxisAlignment.CENTER
        )
        self.left=ft.Column(
            [ft.Text("Company Detail", size=15, weight="bold", color="#133E87"),
             ft.ResponsiveRow([
                 self.Dealer_ID,
                                  self.Company_agent_name,
                                  self.Company_name,
    ],alignment=ft.MainAxisAlignment.CENTER),
             ft.ResponsiveRow([self.Gst,
                                  self.Mobile,
                                  self.Address,self.Email,],alignment=ft.MainAxisAlignment.START),
             
             ],expand=3,horizontal_alignment=ft.CrossAxisAlignment.CENTER,alignment=ft.MainAxisAlignment.START
        )
        self.style_col=ft.TextStyle( word_spacing=5,color="#0D1282",weight=ft.FontWeight.BOLD,size=11,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
        self.temp_entry= ft.DataTable(expand=True,
                                        border=ft.border.all(2,"black"),
                                        border_radius=10,vertical_lines=ft.BorderSide(1, "black"),
                                        heading_row_color=ft.colors.BLACK12,
                                        data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
                                        divider_thickness=0,
                                        column_spacing=50,bgcolor="#EBEAFF",
                                                    columns=[
                ft.DataColumn(
                    ft.Text(" Dealer ID",color="#0D1282"),
                    # tooltip="ID" ,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Agent Name",style=self.style_col),
                    # tooltip=self.Item_Detail_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Company Name",style=self.style_col),
                    # tooltip=self.Item_Buy_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                                ft.DataColumn(
                    ft.Text("GST No",style=self.style_col),
                    # tooltip=self.Item_Buy_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                  ft.DataColumn(
                    ft.Text("Mobile",style=self.style_col),
                    # tooltip=self.Item_tax_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Address",style=self.style_col),
                    # tooltip=self.Item_retail_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Email",style=self.style_col),
                    # tooltip=self.Item_uni_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Bank Name",style=self.style_col),
                    # tooltip=self.Item_dealer_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Account",style=self.style_col),
                    # tooltip=self.Item_Wholesale_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("IFSC No",style=self.style_col),
                    # tooltip=self.Item_uni_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                                ft.DataColumn(
                    ft.Text("Branch",style=self.style_col),
                    # tooltip=self.Item_MRP_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),

                
            ],
                                        )
        self.content = ft.Column(
            [
                # ft.Divider(),
                ft.Text("Goods Entry Tab", size=30, weight="bold", color="#133E87"),
                ft.Row([
                                 self.left,self.right
                                ],vertical_alignment=ft.CrossAxisAlignment.START),

                ft.ResponsiveRow([ 
                                  
                                  ], spacing=10,alignment=ft.MainAxisAlignment.CENTER ),
                # ft.Row([self.amount, self.invoice_date, self.remark, self.paid_by,submit_button,], spacing=10),
                
                ft.Row([self.add_button ,self.summit_button,]),
                ft.Text(" Current Entry:", size=18, weight="bold", color="#133E87"),
                # self.results_list 
                ft.Row([self.temp_entry,],scroll=ft.ScrollMode.HIDDEN ,alignment=ft.MainAxisAlignment.CENTER,expand=True),
                
            ],

            scroll=ft.ScrollMode.AUTO,expand=True
            # padding=20 
        )
    def update_table(self):
        self.temp_entry.rows.clear()
        for i in self.item2database:
            self.temp_entry.rows.append(
            ft.DataRow(cells=[
            ft.DataCell(ft.Text(i["dealer_id"],style=self.style_col)), #1
            ft.DataCell(ft.Text(i["name_agent"],style=self.style_col)),#2
            ft.DataCell(ft.Text(i["company_name"],style=self.style_col)),#3
            ft.DataCell(ft.Text(i["gst"],style=self.style_col)),
             ft.DataCell(ft.Text(i["mobile"],style=self.style_col)),#4
            
            ft.DataCell(ft.Text(i["Address"],style=self.style_col)),# 6
            ft.DataCell(ft.Text(i["email"],style=self.style_col)),#5
            ft.DataCell(ft.Text(i["bank"],style=self.style_col)),# 6
            ft.DataCell(ft.Text(i["ACOUNT_NO"],style=self.style_col)),#7
            ft.DataCell(ft.Text(i["ifsc_NO"] ,style=self.style_col)),#9
            ft.DataCell(ft.Text(i["branch"],style=self.style_col)),#10
        ])
            )       
        self.temp_entry.update()
    def add(self,e):
        print('add button click')
        if  self.Dealer_ID.value=="":
            self.snack_bar_func("Dealer ID Empty")
            return
        elif self.Company_agent_name.value=="":
            self.snack_bar_func("Company Agent Name Empty")
            return
        elif self.Company_name.value=="":
            self.snack_bar_func("Company Name Empty")
            return
        elif self.Gst.value=="":
            self.snack_bar_func("GST Number Empty")
            return
        elif self.Mobile.value=="":
            self.snack_bar_func("Mobile Empty")
            return
        elif self.Address.value=="":
            self.snack_bar_func("Address Empty")
            return
        elif self.Email.value=="":
            self.snack_bar_func("Email Empty")
            return
        elif self.Account.value=='' or self.Ifsc.value==''or self.Bank.value==''and self.Branch.value=='':
            self.snack_bar_func("Bank Details Empty")
        else:
            self.item2database.append(
            {
                "dealer_id": self.Dealer_ID.value, #1
                "company_name": self.Company_name.value,#2
                "name_agent": self.Company_agent_name.value,#3
                "Address": self.Address.value,#4
                "gst":self.Gst.value,#5
                "ACOUNT_NO":self.Account.value,#6
                "ifsc_NO":self.Ifsc.value,#7
                "bank":self.Bank.value,#8
                "branch":self.Branch.value,#9,
                "mobile": self.Mobile.value,#10
                "email": self.Email.value#12
                
            }
        )
        self.Dealer_ID.value=''
        self.Company_name.value=""
        self.Company_agent_name.value=""
        self.Address.value=""
        self.Gst.value=""
        self.Account.value=""
        self.Ifsc.value=""
        self.Bank.value=""
        self.Branch.value=""
        self.Mobile.value=""
        self.Email.value=""
        self.Company_agent_name.focus()
        self.update_table()
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
    def on_submit(self,e):
        self.Dealer_ID.value=dealer_ID(self.Company_name.value,self.Gst.value)
        self.Dealer_ID.focus()
        self.app_layout.page.update()
    def Summit(self,e):
        print('summit button click ')
        if len(self.item2database)==0:
            self.snack_bar_func("Please Enter Dealer Detail")
        else:
            self.dealer_database_access=dealer_database()
            for i in self.item2database:
                self.dealer_database_access.add_dealer(tuple(i.values()))
            self.snack_bar_func(f"Successful Entry  Detail")
            self.dealer_database_access.close_connection()
            return 