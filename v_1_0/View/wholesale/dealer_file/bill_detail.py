import flet as ft
from flet import Dropdown,ElevatedButton
from Model.suffled_table import suffled_access_table
import asyncio
import mysql.connector  # Replace with your database connector library
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
    
# Async database handler (replace with your connection details)
class details_invoice(ft.Container):
    def __init__(self,app_layout,page):
        super().__init__()
        self.app_layout=app_layout
        self.page = page 
        self.expand=True
        self.margin=ft.margin.all(5)
        # self.suffled_data=suffled_access_table()
        # self.data=self.suffled_data.dealer_access_invoice(e.control.value)
        # self.suffled_data.close_connection()
        self.drop_down=dropdown(label="Invoice Sort",
                                hint_text="Invoice Detail",
                                options=[
                                    ft.dropdown.Option(text="One Month",key=30),
                                    ft.dropdown.Option(text="Two Month",key=60),
                                    ft.dropdown.Option(text="Three Month",key=90),
                                    ft.dropdown.Option(text="Four Month",key=120),
                                    ft.dropdown.Option(text="Five Month",key=150),
                                    ft.dropdown.Option(text="Six Month",key=180),
                                        ]
                                )
        self.drop_down_type=dropdown(label="Status Of Invoice",
                                hint_text="Status Of Invoice",
                                options=[
                                    ft.dropdown.Option(text="Pending",key='Unpaid'),
                                    ft.dropdown.Option(text="Paid",key="Paid"),
                                        ]
                                )
        self.result_show=ft.Column(expand=True)
        self.button_search=button_style(text="Search It",on_click=self.invoice_days_count)
        self.content=ft.Column([
            ft.Row([self.drop_down,self.drop_down_type,self.button_search]),
            ft.Divider(),
            self.result_show,
        ])
    def invoice_days_count(self,e):
        self.result_show.controls.clear()
        count=0
        print(self.data)
        self.suffled_data=suffled_access_table()
        self.data=self.suffled_data.dealer_access_invoice(self.drop_down_type.value)
        self.suffled_data.close_connection()
        # Fetch data from database
        self.result_show.controls.append(
            ft.Row([
        
            ft.Container(ft.Text("SR"),alignment=ft.Alignment(0.0, 0.0),expand=True, bgcolor="#4335A7", padding=10, width=100),
            ft.VerticalDivider(),
            ft.Container(ft.Text("Company Name"),alignment=ft.Alignment(0.0, 0.0),expand=True,bgcolor="#4335A7", padding=10, width=100),
            ft.VerticalDivider(),
            ft.Container(ft.Text("Invoice Number"),expand=True,alignment=ft.Alignment(0.0, 0.0), bgcolor="#4335A7", padding=10, width=100),
            ft.VerticalDivider(),
            ft.Container(ft.Text("Amount"), expand=True,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0), padding=10, width=100),
            ft.VerticalDivider(),
            ft.Container(ft.Text("Date"),expand=True, bgcolor="#4335A7", alignment=ft.Alignment(0.0, 0.0),padding=10, width=100),
            ft.VerticalDivider(),
            ft.Container(ft.Text("Days"),expand=True, bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0), padding=10, width=100),
                        ])
        )
        for i in self.data:
            
            if int(i['Days'])<=int(self.drop_down.value):
                count+=1
                self.result_show.controls.append(
                    ft.Row([
                ft.Container(ft.Text(f"{count}"),alignment=ft.Alignment(0.0, 0.0),expand=True, bgcolor="#4335A7", padding=10, width=100),ft.VerticalDivider(),
                ft.Container(ft.Text(f"{i['Company Name']}"),alignment=ft.Alignment(0.0, 0.0),expand=True,bgcolor="#4335A7", padding=10, width=100),ft.VerticalDivider(),
                ft.Container(ft.Text(f"{i['Invoice Number']}"),expand=True,alignment=ft.Alignment(0.0, 0.0), bgcolor="#4335A7", padding=10, width=100),ft.VerticalDivider(),
                ft.Container(ft.Text(f"{i['Amount']}"), expand=True,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0), padding=10, width=100),ft.VerticalDivider(),
                ft.Container(ft.Text(f"{i['Date']}"), expand=True,bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0), padding=10, width=100),ft.VerticalDivider(),
                ft.Container(ft.Text(f"{i['Days']}"),expand=True, bgcolor="#4335A7",alignment=ft.Alignment(0.0, 0.0), padding=10, width=100),
                        ])
                ) 
                self.result_show.controls.append(ft.Divider())
        #     continue()
        self.page.update()
        print(f"count {count} {e.control.value}")
# def main(page: ft.Page):
#     page.title = "Login Page with Loader"

#     # Login button
#     login_button = details_invoice(page,'n')

#     # Add elements to the page
#     page.add(
#     login_button
#     )

# # Run the app
# ft.app(target=main)
