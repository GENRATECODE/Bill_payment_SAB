from flet import (
    ButtonStyle,
    Column,
    Container,
    Control,
    IconButton,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    RoundedRectangleBorder,
    Row,
    Text,
    TextButton,
    TextField,
    border,
    border_radius,
    colors,
    icons,
    padding,
    ResponsiveRow,
)
from View.dashboard import Dashboard
from View.logo import raj_distributor
import flet as ft
from View.sidebar_tax import Sidebar_tax as Sidebar
from View.home_page import HomePage
from View.tax.invoice_sec import Invoice_Retail
from View.tax.transport_entry import transport_entry_app
from View.tax.filterinvoice import Old_invoice_app
from View.tax.Daily_spend  import Daily_spend_app
import math  
from datetime import date
class AppLayout_sec(Row):
    """
    A custom layout for the application.

    Args:
        app: The Flet application instance.
        page: The Flet page instance.
        page_name: The name of the current page.

    Attributes:
        appbar: The application bar instance.
        sidebar: The sidebar instance.
        active_view: The currently active view instance.
        controls: A list of controls to be displayed.

    Methods:
        page_resize: Updates the layout when the page is resized.
        toggle_nav_rail: Toggles the visibility of the sidebar.

    Example:
        >>> app = ft.App(target=AppLayout)
        >>> page = ft.Page()
        >>> app_layout = AppLayout(app, page, "Home")
    """

    def __init__(self, app, page: Page, page_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.page.on_resized = self.page_resize
        self.sidebar_width=self.app.page.window.width*0.184
        self.sidebar = Container(Sidebar(self, self.page),width=self.sidebar_width)
        home = PopupMenuItem(text="Home sec", on_click=lambda _: page.go("/Home2")  )
        login_profile_button = PopupMenuItem(text="Log Out", on_click=self.session_clear)
        profile_button = PopupMenuItem(text="Profile", on_click=lambda _: self.app.page.go("/profile2"))
        setting_button = PopupMenuItem(text="Setting", on_click=lambda _: self.app.page.go("/setting2"))
        self.today=date.today()
        self.user_name=self.app.page.session.get_keys()[0]
        self.appbar_item = [
            home,
            PopupMenuItem(),  # Divider
            login_profile_button,
            PopupMenuItem(),  # Divider
            profile_button,
            PopupMenuItem(),  # Divider
            setting_button
        ]
        self.appbarpage=ft.AppBar(
            leading=ft.Container(
                ft.Image(
                    src=raj_distributor,
                    color_blend_mode=ft.BlendMode.SRC_IN,
                    width=24,
                    height=24,
                    tooltip="Menu",
                    border_radius=ft.border_radius.all(80),
                ),
                on_click=self.toggle_nav_rail,  # Call to toggle sidebar on click
                     
            ),
            leading_width=100,
            title=ft.GestureDetector(
                
                content=Text(tooltip="Home ",
                    spans=[
                ft.TextSpan(
                    "🚲 RAJ DISTRIBUTORS  🚲",
                    ft.TextStyle(
                        size=50,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.SweepGradient(
                center=ft.alignment.center,
                start_angle=0.0,
                end_angle=math.pi * 2,
                colors=[
                    "0xFF4285F4",
                    "0xFF34A853",
                    # "0xFFFBBC05",
                    # "0xFFEA4335",
                    # "0xFF4285F4",
                ],
                stops=[.25,
                #  0.25,
                    #    0.5, 0.75,
                       1.0],
            ),

                        ),
                    ),
                ),
            ],
        
                    # f"🚲 RAJ DISTRIBUTORS  🚲",
                    # font_family="Pacifico",
                    # bgcolor=ft.Colors.YELLOW,
                    # size=48,
                    # text_align="start",
                    # italic=True,
                    # color=ft.Colors.RED_ACCENT_400,
                ),
                on_tap=lambda _: page.go("/Home2")
            ),
            center_title=True,
            toolbar_height=75,
            bgcolor=colors.WHITE,
            actions=[ft.Text(f"{self.today}",color='red'),ft.Text(f"\t User: {self.user_name}",color='red'),Container(content=PopupMenuButton(items=self.appbar_item),
                                margin=ft.margin.only(left=50,right=25))]
        )           
        # self.members_view = HomePage(self.page)
        self.expand=True
        self.spacing=1
        self.controls.clear()
        if page_name == "Home":
            self._active_view: Control = Container(HomePage(self,self.page),expand=True)
            self.controls = [self.sidebar,  self.active_view]
        else:
            self._active_view: Control = Container(ft.Text("Default Error 404{page_name}"), expand=4)

        self.toggle_nav_rail_button = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_400,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail,
        )
        
        

    @property
    def active_view(self):
        """
        Gets the currently active view.

        Returns:
            Control: The active view instance.
        """
        return self._active_view

    @active_view.setter
    def active_view(self, view):
        """
        Sets the currently active view.

        Args:
            view: The new active view instance.
        """
        self._active_view = view
        self.controls[-1] = self._active_view
        # self.sidebar.sync_board_destinations()
        self.page.update()

    def change_active_view(self,view_name):
        if view_name =="invoice_r":
            self._active_view: Control=Container(content=Invoice_Retail(self,self.page),expand=True,padding=10,height=self.app.page.window.height,width=self.app.page.window.width-self.app.page.window.width*0.169)
            self.controls=[self.sidebar,self.active_view]
            self.app.page.update()
        elif view_name == "transport":
            self._active_view: Control=Container(content=transport_entry_app(self,self.page),expand=True,padding=10,height=self.app.page.window.height,width=self.app.page.window.width-self.app.page.window.width*0.169)
            self.controls=[self.sidebar,self.active_view]
            self.app.page.update()
        elif view_name == "old_invoice":
            self._active_view: Control=Container(content=Old_invoice_app(self,self.page),expand=True,padding=10,height=self.app.page.window.height,width=self.app.page.window.width-self.app.page.window.width*0.169)
            self.controls=[self.sidebar,self.active_view]
            self.app.page.update()
        elif view_name == "Daily_Spend":
            self._active_view: Control=Container(content=Daily_spend_app(self,self.page),expand=True,padding=10,height=self.app.page.window.height,width=self.app.page.window.width-self.app.page.window.width*0.169)
            self.controls=[self.sidebar,self.active_view]
            self.app.page.update()
        else:
            self._active_view: Control=Container(content=Text("default Page in change in view section in layout "),bgcolor='red')
            self.controls=[self.sidebar,self.active_view]
            self.app.page.update()

        """
        Changes the active view in the AppLayout based on the view name.

        Args:
            view_name (str): The name of the view to display.
        """
    def session_clear(self,e):
        print("session values clear sec")
        self.app.page.session.clear()
        self.app.page.go("/")
    def page_resize(self, e=None):
        # self.active_view.resize(
        #         self.sidebar.visible, self.app.page.window.width, self.app.page.window.height,
        #     )
        # self.sidebar.on_resize(self.app.page.window.width*0.25,self.app.page.window.height)
        # self.sidebar.update()
        self.active_view.height=self.app.page.window.height
        # here add condition to side hide or unhide then 
        if self.sidebar.visible:
            self.active_view.width=self.app.page.window.width-self.app.page.window.width*0.169
        else:
            self.active_view.width=self.app.page.window.width
        # self.sidebar.width=self.app.page.window.width*0.184
        # self.sidebar.height=self.app.page.window.height
        self.app.page.update()

    def toggle_nav_rail(self, e):
        """
        Toggles the visibility of the sidebar.

        Args:
            e: The event instance.
        """
        self.sidebar.visible = not self.sidebar.visible
        self.page_resize()
        self.page.update()
        
        