# import itertools
# from flet import (
#     UserControl,
#     Column,
#     Row,
#     FloatingActionButton,
#     ElevatedButton,
#     Text,
#     GridView,
#     Container,
#     TextField,
#     AlertDialog,
#     Container,
#     icons,
#     border_radius,
#     border,
#     colors,
#     Page,
#     padding,
#     alignment,
#     margin
# )
# import flet as ft

# class HomePage(Container):
#     def __init__(self,app_layout,page:Page,*args,**kwargs):
#         super().__init__()


#         self.app =app_layout
#         self.page=page
#         # self.page.resized=self.on_resizing
#         # here write whole code here 
#         self.board_lists = [
#          ft.Row(controls=[Text("Welcome In the Shop Management System ->"*7,no_wrap=False)])
#         ]
#         self.app.page.vertical_alignment=ft.MainAxisAlignment.START
#         self.padding=ft.padding.all(15)
#         self.list_wrap = Column(
#             controls=self.board_lists,
#             # vertical_alignment="start",
#             # visible=False,
#             # scroll="auto",
#             expand=True,
#             # width=(self.app.page.window_width - 50),
#             # height=(self.app.page.window_height - 95),
#             alignment=ft.MainAxisAlignment.START,
#         )
#         self.content=self.list_wrap
#         self.padding=ft.padding.all(15)
#         self.margin=ft.margin.all(0)
#         self.height=self.app.page.window.height
#         # Container(
#         #     content=self.list_wrap,
#         #     data=self,
#         #     width=self.app.page.window.width,
#         #     margin=margin.only(right=50),
#         #     padding=padding.all(10),
#         #     # height=self.app.page.window.height,
#         #     expand=1,
#         #     gradient=ft.LinearGradient(
#         #         begin=ft.alignment.top_left,
#         #         end=ft.Alignment(0.7,1),
#         #         colors=[
#         #             "0xff1f005c",
#         #             "0xff5b0060",
#         #             "0xff870160",
#         #             "0xffac255e",
#         #             "0xffca485c",
#         #             "0xffe16b5c",
#         #             "0xfff39060",
#         #             "0xffffb56b",
#         #         ]
#         #     ),
#         #     animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
#         #     # col={"sm": 2, "md":2, "xl": 2},
#         # )

#         # self.expand=True
# Home page class
import flet as ft
from flet import *

class HomePage(ft.Container):
    def __init__(self,app_layout, page,):
        super().__init__(app)
        self.app_layout = app_layout
        self.page=page
        self.app_layout.page.vertical_alignment = ft.MainAxisAlignment.START
        self.content=self.build()
    def build(self):
        return Container(content=ft.Column([
            ft.Text("Welcome to the Home Page:->"*10,color="red"),
            ft.ElevatedButton("Go to Profile", on_click=print("worked on Homepage")),
            # ft.TextField(value=self.state.name, label="Enter your name",
                        #  on_change=self.update_name
                        #  )
          
        ],alignment=ft.MainAxisAlignment.START),padding=ft.padding.all(15),bgcolor='grey',
            margin=ft.margin.all(0),height=self.app_layout.page.window.height)
    def resize(self, nav_rail_extended, width, height):
        # self.width = (
        #     width -256  ) if nav_rail_extended else (width+256)
        # # self.list_wrap.height=height
        # self.height = height
        # self.list_wrap.update()
        # self.view.update()
        self.app_layout.page.update()