import flet as ft
from View.logo import invoice_logo
import time
import datetime
from Model.id_generator import Id_gen
from Model.type_item import items_type
from Model.items import Item
from Model.buyyer import dealer_database
class Item_Add(ft.Container):
    def __init__(self, app_layout,page):
        self.app_layout=app_layout
        self.page=page
        
        super().__init__()
        # self.bgcolor='#f0f0f0'
        self.database=Item()
        self.item_data_base=Item()
        self.expand=True
        self.ink=True
        self.padding=ft.padding.all(10)
        # other necessary requirement  
        self.item2database=list()
        self.dealer_database=dealer_database()
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

        self.Item_name = ft.TextField(  autofocus=True,
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
                                            label="Item Description", 
                                            label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=16,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            hint_text="Enter Product Name",keyboard_type=ft.KeyboardType.NAME,
                                            width=200,col={"sm": 6, "md": 4, "xl": 4})

        # Buying Rate 
        self.amount_buy = ft.TextField(col={"sm": 6, "md": 4, "xl": 1.5},label="BDP", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Billing Dealer Price",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.GST = ft.TextField(col={"sm":  5, "md":  4, "xl": 1.5},label="IGST Percentage", width=200,  suffix_text="%",                                     selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Product Buying Rate",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,
                                            input_filter=ft.NumbersOnlyInputFilter(),max_length=3)
        self.profit_retail = ft.TextField(col={"sm":  5, "md":  4, "xl": 1.5},label="Retail Rate", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Product  Rate",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.profit_wholesale = ft.TextField(col={"sm":  5, "md":  4, "xl": 1.5},label="Profit Wholesale", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Product Profit Amount",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.sliver= ft.TextField(col={"sm":  5, "md":  4, "xl": 1.5},label="Discount Sliver", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Sliver Discount Amount",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.platinum=ft.TextField(col={"sm":  5, "md":  4, "xl": 1.5},label="Discount Platinum", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Product Discount Amount",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.MRP = ft.TextField(col={"sm":  5, "md":  4, "xl": 1.5} ,label="MRP ", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Product MRP ",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,input_filter=ft.InputFilter(
            allow=True,
            regex_string=r"^\d*\.?\d*$",  # Matches whole numbers and decimals
            replacement_string=""
        ))
        self.item_unit_wholesale = ft.Dropdown(label='Unit', width=200,hint_text="Unit of Good", options=[
            ft.dropdown.Option("Dozen"),
            ft.dropdown.Option("PCS"),
            ft.dropdown.Option("SET"),
            ft.dropdown.Option("PKT"),
            ft.dropdown.Option("GRS"),      
            ft.dropdown.Option("PAIR"),
            ft.dropdown.Option("LT."),
            ft.dropdown.Option("KG."),
            ft.dropdown.Option("GM."),
            ft.dropdown.Option("ML."),
        ],border_radius=ft.border_radius.all(10),
                                       counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                                border_color="#1A1A1D",
                                                bgcolor="#EBEAFF",
                                                color="#1A1A1D",
                                        focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            icon_content=ft.Icon(ft.icons.AD_UNITS_SHARP ),
                                            icon_enabled_color="#1A1A1D",label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                  
        )
        self.buy_unit=self.item_unit_retail = ft.Dropdown(col={"sm": 6, "md": 4, "xl": 2},label='Unit', width=200,hint_text="Buy Unit", options=[
            ft.dropdown.Option("Dozen"),
            ft.dropdown.Option("PCS"),
            ft.dropdown.Option("SET"),
            ft.dropdown.Option("PKT"),
            ft.dropdown.Option("GRS"),      
            ft.dropdown.Option("PAIR"),
            ft.dropdown.Option("LT."),
            ft.dropdown.Option("KG."),
            ft.dropdown.Option("GM."),
            ft.dropdown.Option("ML."),
        ],border_radius=ft.border_radius.all(10),
                                       counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                                border_color="#1A1A1D",
                                                bgcolor="#EBEAFF",
                                                color="#1A1A1D",
                                        focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            icon_content=ft.Icon(ft.icons.AD_UNITS_SHARP ),
                                            icon_enabled_color="#1A1A1D",label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                  
        )
        self.item_unit_retail = ft.Dropdown(label='Unit', width=200,hint_text="Unit of Good", options=[
            ft.dropdown.Option("Dozen"),
            ft.dropdown.Option("PCS"),
            ft.dropdown.Option("SET"),
            ft.dropdown.Option("PKT"),
            ft.dropdown.Option("GRS"),      
            ft.dropdown.Option("PAIR"),
            ft.dropdown.Option("LT."),
            ft.dropdown.Option("KG."),
            ft.dropdown.Option("GM."),
            ft.dropdown.Option("ML."),
        ],border_radius=ft.border_radius.all(10),
                                       counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                                border_color="#1A1A1D",
                                                bgcolor="#EBEAFF",
                                                color="#1A1A1D",
                                        focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            icon_content=ft.Icon(ft.icons.AD_UNITS_SHARP ),
                                            icon_enabled_color="#1A1A1D",label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                  
        )
        self.product_type = ft.Dropdown(label='Type', hint_text="Type of Product", options=[
            ft.dropdown.Option(key) for key in items_type.keys()],col={"sm": 6, "md": 4, "xl":2},border_radius=ft.border_radius.all(10),
                                       counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                                border_color="#1A1A1D",
                                                bgcolor="#EBEAFF",
                                                color="#1A1A1D",
                                        focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            icon_content=ft.Icon(ft.icons.AD_UNITS_SHARP ),
                                            icon_enabled_color="#1A1A1D",label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                  
        )
        self.dealer_ID = ft.Dropdown(label='Dealer IDs', width=200,hint_text="Select Dealer ID",border_radius=ft.border_radius.all(10),
                                       counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                                border_color="#1A1A1D",
                                                bgcolor="#EBEAFF",
                                                color="#1A1A1D",
                                        focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            icon_content=ft.Icon(ft.icons.AD_UNITS_SHARP ),
                                            icon_enabled_color="#1A1A1D",label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,)),
                                  col={"sm": 6, "md": 4, "xl": 2.3}
        )
        self.Stock= ft.TextField(col={"sm": 6, "md": 4, "xl": 2.3},label="Stock", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            hint_text="Product Stock",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,
                                            input_filter=ft.NumbersOnlyInputFilter())
        self.Stock_warning= ft.TextField(col={"sm": 6, "md": 4, "xl": 2.3},label="Stock Warning Label", width=200,                                            selection_color="#526E48",
                                            focused_bgcolor="#C6E7FF",
                                            focused_color="#3B1E54",
                                            
                                            hint_text="Product Warning Limit",
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
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),keyboard_type=ft.KeyboardType.NUMBER,
                                            input_filter=ft.NumbersOnlyInputFilter())
        Add_button = ft.FilledButton(
        content=ft.Row([ft.Text("Add Item",weight=ft.FontWeight.BOLD,size=18,italic=True)]),
        tooltip="ADD",
        style=self.style_button,
        width=150,
        on_click=self.perform_search,
        height=50,
        ) 

        
        # Date Picker for Invoice Date
        self.Update_date = ft.TextField(                                            selection_color="#526E48",
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
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,)),
                                            border_radius=ft.border_radius.all(10),keyboard_type=ft.KeyboardType.DATETIME,label="Last Date Update",content_padding=8,suffix=ft.IconButton(
            icon=ft.icons.CALENDAR_MONTH,  # Use any icon you prefer
            on_click=lambda e: self.app_layout.page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2023, month=1, day=1),
                    last_date=datetime.datetime(year=2099, month=12, day=1),
                    on_change=self.handle_change,
                    on_dismiss=self.handle_dismissal,
                )
            )  # Function to call when icon button is clicked
        ),col={"sm": 6, "md": 4, "xl": 3})
        self.style_col=ft.TextStyle( word_spacing=5,color="#0D1282",weight=ft.FontWeight.BOLD,size=11,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),blur_style=ft.ShadowBlurStyle.SOLID,))
        self.data_table_item=ft.DataTable(expand=False,
                                        border=ft.border.all(2,"black"),
                                        border_radius=10,vertical_lines=ft.BorderSide(1, "black"),
                                        heading_row_color=ft.colors.BLACK12,
                                        data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
                                        divider_thickness=0,
                                        column_spacing=30,bgcolor="#EBEAFF",
                                                    columns=[
                ft.DataColumn(
                    ft.Text("ID",color="#0D1282"),
                    # tooltip="Item ID" 
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Description",style=self.style_col),
                    # tooltip=self.Item_Detail_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("BDP",style=self.style_col),
                    # tooltip=self.Item_Buy_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                                ft.DataColumn(
                    ft.Text("BR Unit",style=self.style_col),
                    # tooltip=self.Item_Buy_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                  ft.DataColumn(
                    ft.Text("GST",style=self.style_col),
                    # tooltip=self.Item_tax_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Profit R",style=self.style_col),
                    # tooltip=self.Item_retail_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Unit Retail",style=self.style_col),
                    # tooltip=self.Item_uni_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                
                ft.DataColumn(
                    ft.Text("Profit W",style=self.style_col),
                    # tooltip=self.Item_Wholesale_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Unit WholeSale",style=self.style_col),
                    # tooltip=self.Item_uni_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                                ft.DataColumn(
                    ft.Text("MRP",style=self.style_col),
                    # tooltip=self.Item_MRP_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),

                ft.DataColumn(
                    ft.Text("Dealer Id",style=self.style_col),
                    # tooltip=self.Item_dealer_tooltip,
                    # numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                  ft.DataColumn(
                    ft.Text("Stock",style=self.style_col),
                    # tooltip=self.Item_stock_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Warning Label",style=self.style_col),
                    # tooltip=self.Item_LS_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Retail Rate",style=self.style_col),
                    # tooltip=self.Item_RR_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),

                ft.DataColumn(
                    ft.Text("WholeSale Rate",style=self.style_col),
                    # tooltip=self.Item_WR_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("PR Discount",style=self.style_col),
                    # tooltip=self.Item_WR_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),                                ft.DataColumn(
                    ft.Text("SR Discount",style=self.style_col),
                    # tooltip=self.Item_WR_tooltip,
                    numeric=True,
                    # on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
                                        )
        self.summit_button=ft.FilledButton(
        content=ft.Row([ft.Text("Summit",weight=ft.FontWeight.BOLD,size=18,italic=True)]),
        tooltip="Summit",
        style=self.style_button,
        width=150,
        on_click=self.summit,
        height=50,
        ) 

        self.right=ft.Column(
            [ft.Text("Retail Rate Entry", size=15, weight="bold", color="#133E87"),
             ft.Row([self.profit_retail,self.item_unit_retail,],alignment=ft.MainAxisAlignment.CENTER)
             ],expand=2,horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.left=ft.Column(
            [ft.Text("Wholesale Rate Entry", size=15, weight="bold", color="#133E87"),
             ft.Row([self.profit_wholesale,self.item_unit_wholesale,],alignment=ft.MainAxisAlignment.CENTER),
             ft.Row([self.sliver,self.platinum],alignment=ft.MainAxisAlignment.CENTER),
             
             ],expand=2,horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.database_reload() 
        self.content = ft.Column(
            [
                # ft.Divider(),
                ft.Text("Goods Entry Tab", size=30, weight="bold", color="#133E87"),
                ft.ResponsiveRow([self.Item_name,self.product_type,self.amount_buy,self.buy_unit,self.GST,
                                ], spacing=10,alignment=ft.MainAxisAlignment.CENTER),

                ft.ResponsiveRow([ self.MRP,self.dealer_ID,self.Stock,self.Stock_warning], spacing=10,alignment=ft.MainAxisAlignment.CENTER ),
                # ft.Row([self.amount, self.invoice_date, self.remark, self.paid_by,submit_button,], spacing=10),
                ft.Row([self.left,self.right],alignment=ft.MainAxisAlignment.CENTER),Add_button ,
                ft.Text(" Current Entry:", size=18, weight="bold", color="#133E87"),
                # self.results_list 
                ft.Row([ self.data_table_item,],scroll=ft.ScrollMode.HIDDEN ),self.summit_button,
                
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            # padding=20 
        )   
    def summit(self,e):
        if len(self.item2database)==0:
            self.snack_bar_func( f"Entry Table Empty")
            return 
        else:
            self.snack_bar_func( f"Collection  Added")
            print(len(self.item2database))
            for i in self.item2database:
                print(f"{i.values()}")
                self.item_data_base.add(list(i.values()))
        # Add Collection in DataBase through customer ID 
        self.app_layout.page.update()
        print("add collection ")                     
    def perform_search(self,e):
        # perform search operation here
        # you can use the search_customer, search_address, search_mobile, search_ID fields to get
        # the search query from the user
        if self.Item_name.value=='' or  self.amount_buy.value=='':
            self.snack_bar_func( f"Please Enter Goods Details")
        else:
            self.item2database.append(
                        {
                            "Item_Id":Id_gen(items_type[self.product_type.value],self.Item_name.value,self.amount_buy.value,self.dealer_ID.value),
                            "Item_name": self.Item_name.value,
                            "amount_buy": self.amount_buy.value,
                            "buy_unit": self.buy_unit.value,
                            "GST": self.GST.value,
                            "profit_retail": self.profit_retail.value,
                            "item_unit_retail": self.item_unit_retail.value,
                            "Retail":float(self.amount_buy.value)*float(self.GST.value)/100+float(self.amount_buy.value)+float(self.profit_retail.value),
                            "WholeSale":float(self.amount_buy.value)*float(self.GST.value)/100+float(self.amount_buy.value)+float(self.profit_wholesale.value),
                            "profit_wholesale": self.profit_wholesale.value,
                            "sliver_discount":int(self.sliver.value),
                            "platinum_discount":self.platinum.value,  
                            "item_unit_wholesale": self.item_unit_wholesale.value,
                            "MRP": self.MRP.value,
                            "dealer_ID":(self.dealer_ID.value).split("\n")[0],
                            "Stock": self.Stock.value,
                            "Stock_warning": self.Stock_warning.value,
                            "Update_date": datetime.datetime.now().date()
                        }
                        )
            self.Item_name.value=""
            self.amount_buy.value=""
            self.GST.value=""
            self.profit_retail.value=""
            self.profit_wholesale.value=""
            self.MRP.value=""
            self.item_unit_retail.value=""
            self.item_unit_wholesale.value=""
            self.dealer_ID.value=""
            self.Stock.value=""
            self.Stock_warning.value=""
            self.update_table()
    def update_table(self):
        self.data_table_item.rows.clear()
        for i in self.item2database:
            self.data_table_item.rows.append(
                ft.DataRow(cells=[
            ft.DataCell(ft.Text(i["Item_Id"],style=self.style_col)), #1
            ft.DataCell(ft.Text(i["Item_name"],style=self.style_col)),#2
            ft.DataCell(ft.Text(i["amount_buy"],style=self.style_col)),#3
             ft.DataCell(ft.Text(i["buy_unit"],style=self.style_col)),#4
            ft.DataCell(ft.Text(i["GST"],style=self.style_col)),#5
            ft.DataCell(ft.Text(i["profit_retail"],style=self.style_col)),# 6
            ft.DataCell(ft.Text(i["item_unit_retail"],style=self.style_col)),#7
            ft.DataCell(ft.Text(i["profit_wholesale"] ,style=self.style_col)),#9
            ft.DataCell(ft.Text(i["item_unit_wholesale"],style=self.style_col)),#10
            ft.DataCell(ft.Text(i["MRP"],style=self.style_col)),#11
            
            ft.DataCell(ft.Text(i["dealer_ID"],style=self.style_col)),#12
            ft.DataCell(ft.Text(i["Stock"] ,style=self.style_col)),#13
            ft.DataCell(ft.Text(i["Stock_warning"],style=self.style_col)),#14
            ft.DataCell(ft.Text((int(i["Retail"])),style=self.style_col)),#15
             ft.DataCell(ft.Text((int(i["WholeSale"])),style=self.style_col)),#16
             ft.DataCell(ft.Text((int(i["sliver_discount"])),style=self.style_col)),#17
             ft.DataCell(ft.Text((int(i["platinum_discount"])),style=self.style_col)),#18
        ]))
        self.app_layout.page.update()
        print("Perform search  ")
    def handle_change(self,e):
        self.snack_bar_func(f"Date changed: {e.control.value.strftime('%d-%m-%Y')}")
        self.Update_date.value=e.control.value.strftime('%d-%m-%Y')
        self.app_layout.page.update()  
    def handle_dismissal(self,e):
        self.snack_bar_func(f"DatePicker dismissed")
    def option_gen(self):
        return [ft.dropdown.Option(f"{i['dealer_id']}\n{i['company_name']}") for i in self.dealer_ids]
    def database_reload(self):
        self.dealer_manager = dealer_database()
        self.dealer_ids = self.dealer_manager.list_dealers_with_company()
        self.dealer_ID.options = self.option_gen()  # Update options in the existing Dropdown
        self.app_layout.page.update()  # Notify the UI of the changes
        self.dealer_manager.close_connection()
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