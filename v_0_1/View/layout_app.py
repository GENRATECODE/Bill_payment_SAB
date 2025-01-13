import flet as ft
from flet import (
    Control,
    Column,
    Container,
    IconButton,
    Page,
    Row,
    Text,
    TextButton,
    IconButton,
    ButtonStyle,
    PopupMenuButton,
    PopupMenuItem,
    TextField,
    border_radius,
    colors,
    icons,
    padding,
    border
)
# from View.item_mangement_oops import ItemManagement
# from View.Invoices import InvoiceApp
# from View.log_in_class import LoginPage
# from View.user import ProfileAPP  
from View.sidebar_app import Sidebar
class AppLayout(Row):
    def __init__(
        self,
        app,
        page: Page,
        *args,
        **kwargs
    ):
        super().__init__(*args,**kwargs)
        self.app = app
        self.page = page
        # self.page.on_resized = self.page_resize
        self.sidebar = Sidebar(self.page)
        self.toggle_nav_rail_button = ft.VerticalDivider(thickness=0.1,color=ft.Colors.TRANSPARENT)
        self._active_view: Control =ft.Text("active side")
        self.controls = [self.sidebar,self.toggle_nav_rail_button,
                                self.active_view]
    @property
    def active_view(self):
        return self._active_view
    @active_view.setter
    def active_view(self,view):
        self.active_view = self.app
        self.page.update()

    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.page.update()