import flet as ft
from Model.items import Item  
from flet import TextField, ElevatedButton

class text_filed_style(TextField):
    def __init__(self, label=None, capitalizationn=None, hint_text=None, 
                 prefix_text=None, leng=None, col=None, on_change=None, 
                 value=None, on_click=None, suffix=None, prefix_icon=None, 
                 kbtype=None, **kwargs):  # Add **kwargs
        super().__init__(**kwargs)  # Pass additional arguments to the parent TextField
        self.label = label
        self.keyboard_type=kbtype
        self.capitalization = capitalizationn
        self.hint_text = hint_text
        self.prefix_text = prefix_text
        self.max_length = leng
        self.value = value
        self.col = col
        self.on_change = on_change
        self.on_click = on_click
        self.suffix = suffix
        self.prefix_icon = prefix_icon
        
        # Style properties
        self.width = 200
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
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.SOLID,
            ),
        )


class button_style(ElevatedButton):
    def __init__(self, on_click=None, text=None, **kwargs):
        super().__init__(**kwargs)  # Pass additional arguments to the parent ElevatedButton
        self.on_click = on_click
        self.text = text
        
        # Button style
        self.style = ft.ButtonStyle(
            animation_duration=290,
            color={
                # ft.ControlState.DEFAULT: "#FFFFFF",  # White text by default
                ft.ControlState.HOVERED: "#3D3BF3",  # Light blue text on hover
                ft.ControlState.FOCUSED: "#000000",  # Cyan text on focus
            },
            bgcolor={
                # ft.ControlState.DEFAULT: "#3D3BF3",  # Red background by default
                "": "#FF2929",  # Default background color
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
        
class tab_invoice(ft.Container):
    def __init(self,page):
        super().__init__(**kwargs)
        # self.app_layout = app_layout
        self.page=page
        self.page = page
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        # database call item table import data 
        self.items_database=Item()
        self.items=self.items_database.list_items()
        # constant define 
        self.serial_number=1
        self.item_id_search=self.items
        self.items_name=self.items
        self.customer_mobile_search=['9794144305','979414439','951650030','9415863731']
        self.what=None
        self.loc=None
        self.padding=ft.padding.all(10)
        self.margin=ft.margin.all(0)
        # for search Id 
        self.list_items={
            name['item_id']:ft.ListTile(
                title=ft.Text(f"{name['item_id']} Stock->{name['stock']}"),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                trailing=ft.Text(f"{name['item_description']}"),
                on_click=self.printer,
                data=name['item_id']
            )
            for name in self.item_id_search
        }
        # for search Customer Details by Modlie
        self.list_customer_number={
            number:ft.ListTile(
                title=ft.Text(number),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer_number,
                data=number
            )
            for number in self.customer_mobile_search
        }    
        # for search goodes Description 
        self.list_items_description={
            name['item_description']:ft.ListTile(
                title=ft.Text(name['item_description']),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer_description,
                trailing=ft.Text(f"{name['item_id']} Stock->{name['stock']}"),
                data=name['item_description']
            )
            for name in self.items_name
        }
        # for customer detail for input 
        self.customer_name=text_filed_style(label='Customer Name',capitalizationn=ft.TextCapitalization.WORDS,kbtype=ft.KeyboardType.NAME)
        # self.customer_mobile
        # self.customer_address
        # customer Detail Column
        self.col1=self.Column([
            self.customer_name,
        ],alignment=ft.MainAxisAlignment.START,expand=2)
        # list view 
        self.search_results = ft.ListView(expand=1, spacing=4, padding=2,auto_scroll=True)
        self.search_number=ft.ListView(expand=1,spacing=4,padding=2,auto_scroll=True)
        self.search_description=ft.ListView(expand=1,spacing=4,padding=2,auto_scroll=True)
        
        # for item details 
        # self.item_id
        # self.item_description
        
        layout=ft.Text("run")
        self.content=ft.Column([layout,])
# Main Application
def main(page: ft.Page):
    page.title = "Custom GUI with Flet"
    page.bgcolor = "#F5F5F5"
    page.padding = 20
    h=tab_invoice(page)
    page.add(
        h,
    
    
    )
    page.update()


# Run the app
if __name__ == "__main__":
    ft.app(target=main)