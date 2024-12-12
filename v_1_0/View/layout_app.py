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

# page import for 
from View.dashboard import Dashboard #check 
from View.wholesale.dealer import Dealer # check 
from View.wholesale.subdealer import SubDealer # check 
from View.wholesale.payment_detail import Payment_entry
from View.wholesale.previous_invoice import Previous_Detail # check 
from View.wholesale.item_management import Item_Management #check 
from View.tax.Daily_spend import Daily_spend_app #check 
from View.tax.transport_entry import transport_entry_app
from View.logo import raj_distributor
import flet as ft
from View.sidebar_usercontrol import Sidebar
from View.home_page import HomePage
from View.invoice import Invoice_WholeSale # check
from View.user import ProfileAPP
import math
from datetime import date
class AppLayout(Row):
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
        home = PopupMenuItem(text="Home prime ", on_click=lambda _: page.go("/Home"))
        login_profile_button = PopupMenuItem(text="Log Out", on_click=lambda _: self.app.page.go("/"))
        profile_button = PopupMenuItem(text="Profile", on_click=lambda _: self.app.page.go("/profile"))
        setting_button = PopupMenuItem(text="Setting", on_click=lambda _: self.app.page.go("/setting"))
        self.views_page={
            "invoice_w":Invoice_WholeSale(self,self.page),
            "previous_invoice":Previous_Detail(self,self.page),
            "Dashboard":Dashboard(self,self.page),
            "Dealer":Dealer(self,self.page),
            "SubDealer": SubDealer(self,self.page),
            "Item_Management":Item_Management(self,self.page),
            "Daily_spend_app":Daily_spend_app(self,self.app ),
            "transport":transport_entry_app(self,self.app),
            "payment":Payment_entry(self,self.app)
        }
        self.today=date.today()
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
                    src=r"assets/logo/RD_LOGO.png",
                    color_blend_mode=ft.BlendMode.SRC_IN,
                    width=50,
                    height=50,
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
                    # bgcolor=ft.colors.YELLOW,
                    # size=48,
                    # text_align="start",
                    # italic=True,
                    # color=ft.colors.RED_ACCENT_400,
                ),
                on_tap=lambda _: page.go("/Home")
            ),
            center_title=True,
            toolbar_height=75,
            bgcolor=colors.WHITE,
            actions=[ft.Text(f"{self.today}",color='red'),Container(content=PopupMenuButton(items=self.appbar_item),
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
        self.app.page.update()

    def change_active_view(self,view_name):
        if view_name :
            self._active_view: Control=Container(content=self.views_page[view_name],expand=3,padding=10,
                                                    height=self.app.page.window.height,width=self.page.window.width-self.page.window.width*0.169)
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

    def page_resize(self, e=None):
        self.active_view.height=self.app.page.window.height
        # here add condition to side hide or unhide then 
        if self.sidebar.visible:
            self.active_view.width=self.app.page.window.width-self.app.page.window.width*0.169
        else:
            self.active_view.width=self.app.page.window.width
        self.app.page.update()

    def toggle_nav_rail(self, e):
        """
        Toggles the visibility of the sidebar.

        Args:
            e: The event instance.
        """
        self.sidebar.visible = not self.sidebar.visible
        self.page_resize()
        # self.page.update()
        
        