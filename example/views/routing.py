import flet as ft
from views.view_home import HomeView
from views.view_about import AboutView
from views.view_settings import SettingsView
from views.view_login import logginView
from loguru import logger


class Router:
    def __init__(self, page, default_route="/home", not_found_route="/404"):
        self.page = page

        # 初始化并存储视图类，而非实例
        self.routes = {}
        self.instances = {}  # 存储已实例化的视图对象
        self.default_route = default_route
        self.not_found_route = not_found_route

        # 注册路由
        self.add_route("/home", HomeView)
        self.add_route("/about", AboutView)
        self.add_route("/settings", SettingsView)
        self.add_route("/login", logginView)

        # 设置 404 页面
        self.add_route(
            not_found_route,
            lambda _: ft.Column(
                [
                    ft.Container(
                        height=100
                    ),
                    ft.Row(
                        [ft.Text("404", size=68)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [ft.Text("Page Not Found", size=28)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                # alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        # 设置初始页面
        self.body = ft.Container(
            content=self.get_view(self.default_route), expand=True, margin=5
        )

    def add_route(self, path, view_class):
        """注册路由的方法，仅存储视图类"""
        self.routes[path] = view_class

    def get_view(self, path):
        """获取视图实例，使用懒加载"""
        if path not in self.instances:
            if path in self.routes:
                self.instances[path] = self.routes[path](self.page)
            else:
                self.instances[path] = self.routes[self.not_found_route](self.page)
        return self.instances[path]

    def route_change(self, route):
        current_route = route.route
        logger.info(f"route: {current_route}")
        # 获取视图实例并更新
        self.body.content = self.get_view(current_route)
        self.body.update()
