
import flet as ft
from views.routing import Router
from loguru import logger
from Titlebar import TitleBar
from SiddBar import NavBar
from flet_restyle import *
# pip install flet_restyle
# pip install loguru


class App:

    def __init__(self, page: ft.Page):
        self.page = page
        # page.theme_mode ='dark'
        # page.bgcolor = ft.Colors.TRANSPARENT
        # page.decoration = ft.BoxDecoration(
        #     gradient=ft.LinearGradient(
        #         colors=[ft.Colors.GREEN, ft.Colors.BLUE],
        #         begin=ft.alignment.top_left,
        #         end=ft.alignment.bottom_right,
        #         stops=[0.0, 1.0],
        #     ),
        # )
        page.fonts = {
            "Kanit": "http://fonts.gstatic.com/s/acme/v5/-J6XNtAHPZBEbsifCdBt-g.ttf",
            "kaka":'http://fonts.gstatic.com/s/alice/v7/wZTAfivekBqIg-rk63nFvQ.ttf',
            'ss':'http://fonts.gstatic.com/s/amiko/v1/A7bjc3cOLJtGgpPGnxyHsw.ttf',
            'aa':'http://fonts.gstatic.com/s/amiko/v1/BaZst4RZ4sDyD3mH-BfVaA.ttf',
        }

        page.theme = ft.Theme(font_family="ss")
        FletReStyle.apply_config(page, FletReStyleConfigs())
        page.padding = 0
        page.spacing = 0
        page.window.always_on_top = True
        page.window.title_bar_hidden = True
        page.window.title_bar_buttons_hidden = True
        page.window.width, page.window.height = 900, 700
        page.window.min_height = 700
        page.window.min_width = 900
        page.on_error = self.handle_error
        self.router = Router(page)
        page.window.center()
        self.initialize()

    def handle_error(self, e: Exception):
        logger.error(f"Error in app: {e}")
        self.page.go("/404")  # 发生错误时转到错误页面或默认页面

    def initialize(self):
        """初始化应用"""
        try:
            self.setup_routes()
            self.handle_initial_navigation()
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            # 处理初始化失败的情况，比如展示错误页面或停止应用
            self.page.window.close()

    def setup_routes(self):
        """设置路由"""
        menu_items = [
            {
                "title": "Home",
                "route": "/home",
                "icon": ft.Icons.HOME,
            },
            {
                "title": "Chart",
                "route": "/404",
                "icon": ft.Icons.DASHBOARD,
            },
            {
                "title": "Bar",
                "route": "/about",
                "icon": ft.Icons.BAR_CHART,
            },
            {
                "title": "Data",
                "route": "/login",
                "icon": ft.Icons.DATA_THRESHOLDING_OUTLINED,
            },
            {
                "title": "Settings",
                "route": "/settings",
                "icon": ft.Icons.SETTINGS,
            },
        ]
        self.page.on_route_change = self.router.route_change
        self.page.add(
            ft.Row(
                [
                    ft.Card(
                        ft.Column([NavBar(self.page, menu_items)]),
                        margin=0,
                        elevation=10,
                    ),
                    ft.Column(
                        [
                            TitleBar(),
                            self.router.body,
                        ],
                        expand=True,
                        spacing=0,
                    ),
                ],
                expand=True,
                spacing=0,
            )
        )

    def handle_initial_navigation(self):
        """处理初始导航"""
        try:
            session = self.page.client_storage.get("session")
            target_route = "/home" if session else "/login"
            self.page.go(target_route)
        except Exception as e:
            logger.error(f"Error during initial navigation: {e}")
            self.page.go("/404")  # 发生错误时转到错误页面或默认页面


def main(page: ft.Page):
    """主函数"""
    try:
        App(page)
        
    except Exception as e:
        logger.error(f"Error in main function: {e}")


ft.app(target=main, assets_dir="assets")
