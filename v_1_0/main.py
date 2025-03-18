import flet as ft


from flet import  Theme,View,Colors,Icons,margin,padding,Text,TextField,RoundedRectangleBorder,Row,TemplateRoute,Page,Icon,PopupMenuButton,PopupMenuItem,AlertDialog, AppBar, Column,Container,ElevatedButton
from View.logo import raj_distributor
# all Page import in there 

# from View.app_bar import NavBar_for
from View.layout_app import AppLayout
from View.layout_app_sec import AppLayout_sec
from View.log_in_class import LoginPage
# from View.sidebar import Sidebar
from View.home_page import HomePage 
# from View.dashboard import Dashboard


class ShopMangement:
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.page.on_route_change = self.route_change  # Assign the route change handler
        self.page.padding=0
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        # self.page.show_semantics_debugger=True
        # Page LISt 

        page.title = "Bill And Management "
        # page.padding = 0  # Ensure no padding on the page
        # page.spacing = 0  # No extra spacing between items
        page.theme = ft.Theme(font_family="Verdana",
                              page_transitions=ft.PageTransitionsTheme(
        android=ft.PageTransitionTheme.OPEN_UPWARDS,
        ios=ft.PageTransitionTheme.CUPERTINO,
        macos=ft.PageTransitionTheme.FADE_UPWARDS,
        linux=ft.PageTransitionTheme.ZOOM,
        windows=ft.PageTransitionTheme.CUPERTINO
    ))  
        # size 
        page.window.maximized=True
        # page.theme.page_transitions.windows = "cupertino"
        page.fonts = {
                "sonic": "assets/font/Freedom-10eM.ttf",
                "im_font": "assets/font/IMFellDoublePicaSC-Regular.ttf",
                "inflt": "assets/font/InflateptxBase-ax3da.ttf",
                "Pacifico": "Pacifico-Regular.ttf"
            }
        page.auto_scroll=False  
        page.scroll=ft.ScrollMode.ADAPTIVE
        page.adaptive=True  
        page.bgcolor = ft.Colors.WHITE

        page.update()
    # it was run fine with old version of flet NOw
        # self.layout=AppLayout(page)
        # Initialize the app to navigate to the current route
        self.page.go(self.page.route)
    
    def route_change(self, route):
        # Clear current views before adding new one
        # self.page.views.clear()  
        if self.page and self.page.views:
            self.page.views.clear()
            print("Page View Clear now")
        # Determine which view to display based on the current route
        if self.page.route == "/":
            login_page = LoginPage(self.page)
            self.page.views.append(
                ft.View(
                    "/",decoration=ft.BoxDecoration(
                        # blend_mode=ft.BlendMode.COLOR_BURN,
                            image=ft.DecorationImage(
                                src="background/startup_application.jpg",
                            fit=ft.ImageFit.FILL,
                            # opacity=0.5,
                            )
                        ),
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    bgcolor=ft.Colors.TRANSPARENT,
                    controls=[login_page,
                    ],padding=2,
                )
            )
        elif self.page.route == "/Home":
  # Ensure `home.build` returns a valid control
            self.layout=AppLayout(self,self.page,page_name="Home")
             # Switch to HomePage view
            self.page.views.append(
                ft.View(
                    "/Home",
                    decoration=ft.BoxDecoration(
                        blend_mode=ft.BlendMode.COLOR_BURN,
                        
                        gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                    '#475569',
                    '#9ca3af'
                ]),
                        ),
                 bgcolor=ft.Colors.TRANSPARENT,
                    appbar=self.layout.appbarpage,
                    controls=[
                       self.layout,

                    ],padding=0,
                )
            )
        elif self.page.route == "/Home2":
  # Ensure `home.build` returns a valid control
            self.layout_sec=AppLayout_sec(self,self.page,page_name="Home")
             # Switch to HomePage view
            self.page.views.append(
                ft.View(
                    "/Home2",
                    decoration=ft.BoxDecoration(
                        blend_mode=ft.BlendMode.COLOR_BURN,
                        
                        gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.Alignment(0.8, 1),
                colors=[
                     '#475569',
                    '#9ca3af'
                ]),
                        ),
                 bgcolor=ft.Colors.TRANSPARENT,
                    appbar=self.layout_sec.appbarpage,
                    controls=[
                       self.layout_sec,

                    ],padding=0,
                )
            )
        elif self.page.route == "/profile2":
            
            self.layout_sec=AppLayout_sec(self,self.page,page_name="profile")
            self.page.views.append(
                ft.View(
                    "/profile2",
                    appbar=self.layout_sec.appbarpage,
                    controls=[
                        ft.Text("Profile section"),
                        # self.layout_sec,  
                        ft.ElevatedButton("Go to Log Out", on_click=lambda _: self.page.go("/")),
                        # ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/Home")),
                    ],padding=0,
                )
            ) 
        elif self.page.route == "/profile":
            
            self.layout=AppLayout(self,self.page,page_name="profile")
            self.page.views.append(
                ft.View(
                    "/profile",
                    appbar=self.layout.appbarpage,
                    controls=[
                        # ft.Text("Profile section"),
                        self.layout,  
                        # ft.ElevatedButton("Go to Log Out", on_click=lambda _: self.page.go("/")),
                        # ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/Home")),
                    ],padding=0,
                )
            ) 
        elif self.page.route == "/setting":
            self.layout=AppLayout(self,self.page,page_name="Setting")
            self.page.views.append(
                ft.View(
                    "/setting",
                    appbar=self.layout.appbarpage,
                    controls=[
                        ft.Text("Setting section"),
                        ft.ElevatedButton("Go to Log Out", on_click=lambda _: self.page.go("/")),
                        ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/Home")),
                    ],
                )
            )
        elif self.page.route == "/setting2":
            self.layout_sec=AppLayout_sec(self,self.page,page_name="Setting")
            self.page.views.append(
                ft.View(
                    "/setting2",
                    appbar=self.layout_sec.appbarpage,
                    controls=[
                        ft.Text("Setting section"),
                        ft.ElevatedButton("Go to Log Out", on_click=lambda _: self.page.go("/")),
                        ft.ElevatedButton("Home", on_click=lambda _: self.page.go("/Home")),
                    ],
                )
            )         

        else:

            self.layout=AppLayout(self,self.page,page_name="default")
            self.page.views.append(
                ft.View(
                    "/default",
                    appbar=self.layout.appbarpage,
                    controls=[self.layout,
                        ft.Text("Default Page"),
                        ft.ElevatedButton("Go to Log In", on_click=lambda _: self.page.go("/")),
                    ],
                )
            )

        # Update the page with the new view
        self.page.update()

    def toggle_nav_rail(self, e):
        """
        Toggles the visibility of the sidebar.

        Args:
            e: The event instance.
        """
        print("Toggle nav rail triggered")
        self.sidebar.visible = not self.sidebar.visible
        print(f"Sidebar visibility: {self.sidebar.visible}")
        # self.toggle_nav_rail_button.selected = not self.toggle_nav_rail_button.selected
        self.layout.page_resize()
        self.page.update()

def main():
    ft.app(target=ShopMangement, assets_dir="../assets")
if __name__ == "__main__":
    main()
    print("hello")
    