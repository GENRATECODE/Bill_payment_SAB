from functools import partial
from typing import NamedTuple
import flet as ft

# 样式和配置分离到单独模块
class Colors:
    BG_COLOR = ft.Colors.BLACK87
    ICON_COLOR = ft.Colors.GREY
    HOVER_ICON_COLOR = "#f7f8ee"
    ACTIVE_ICON_COLOR = ft.Colors.WHITE
    TEXT_COLOR = ft.Colors.GREY
    HOVER_BG_COLOR = ft.Colors.WHITE10
    TRANSPARENT = ft.Colors.TRANSPARENT
    USER_DATA_BG_COLOR = ft.Colors.BLUE_GREY
    USER_DATA_TEXT_COLOR = ft.Colors.WHITE
    DIVIDER_COLOR = ft.Colors.WHITE30

class TextStyles:
    USER_DATA = {
        "size": 11,
        "weight": ft.FontWeight.BOLD,
        "opacity": 1,
        "animate_opacity": 200,
        "color": Colors.USER_DATA_TEXT_COLOR,
    }
    MENU_ITEM = {
        "size": 14,
        "opacity": 1,
        "animate_opacity": 200,
        "color": Colors.TEXT_COLOR,
    }

class NavBar(ft.Container):
    class MenuItem(NamedTuple):
        icon: str
        title: str
        route: str

    def __init__(self, page=None, menu_items: list[dict] = None):
        super().__init__()
        self.page = page
        self.active_item_index = -1
        self.setup_properties()
        self.change_sidebar = self._toggle_sidebar
        self.menu_items = self._create_menu_items(menu_items)
        # 创建 Ref 引用来控制透明度
        self.user_name_ref = ft.Ref[ft.Text]()
        self.user_description_ref = ft.Ref[ft.Text]()
        self.logout_text_ref = ft.Ref[ft.Text]()  # 修改这里的引用
        self.content = self._create_sidebar()

    def setup_properties(self):
        self.width = 62
        self.height = 600
        self.expand = True
        self.bgcolor = Colors.BG_COLOR
        self.border_radius = ft.border_radius.only(7,0,7,0)
        self.animate = ft.animation.Animation(500, ft.AnimationCurve.DECELERATE)
        self.alignment = ft.alignment.center
        self.padding = 10

    def _create_sidebar(self):
        return ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.alignment.center,
            controls=[
                self._create_user_data("W", "Tools", "flet-app"),
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_color=Colors.ACTIVE_ICON_COLOR,
                    on_click=self.change_sidebar,
                ),
                ft.Divider(height=5, color=Colors.TRANSPARENT),
                *self.menu_items,
                ft.Divider(height=2, color=Colors.DIVIDER_COLOR),
                self._create_container_item(
                    icon_name=ft.Icons.LOGOUT_ROUNDED,
                    title="Exit",
                    on_click=lambda _: self.page.window.close(),
                    text_ref=self.logout_text_ref,  # 传递给具体的文本控件
                ),
            ],
        )

    def _create_menu_items(self, btn_items):
        return [
            self._create_container_item(
                icon_name=item["icon"],
                title=item["title"],
                on_click=partial(self._on_menu_item_click, index, item["route"]),
                index=index,
            )
            for index, item in enumerate(btn_items)
        ]

    def _create_container_item(self, icon_name: str, title: str, on_click=None, index=None, text_ref=None):
        text_opacity = ft.Ref[ft.Text]()
        icon_button = self._create_icon_button(icon_name)
        container = ft.Container(
            width=180,
            height=45,
            border_radius=10,
            on_hover=lambda e: self._highlight_item(e, text_opacity, icon_button),
            on_click=on_click,
            content=ft.GestureDetector(
                content=ft.Row(
                    controls=[
                        icon_button,
                        ft.Text(
                            ref=text_ref or text_opacity,  # 如果传递了 text_ref，则使用它
                            value=title,
                            **TextStyles.MENU_ITEM,font_family= "Kanit"
                        ),
                    ]
                ),
                mouse_cursor=ft.MouseCursor.CLICK,
            ),
        )
        return container

    def _create_icon_button(self, icon_name):
        return ft.IconButton(
            disabled=True,
            mouse_cursor=ft.MouseCursor.CLICK,
            icon=icon_name,
            icon_size=18,
            icon_color=Colors.ICON_COLOR,
            # on_click=on_click,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=7)},
                overlay_color={"": Colors.TRANSPARENT},
            ),
        )

    def _highlight_item(self, e: ft.ControlEvent, text_opacity: ft.Ref[ft.Text], icon_button: ft.IconButton):
        is_hovered = e.data == "true"
        is_active = icon_button.icon_color == Colors.ACTIVE_ICON_COLOR

        if not is_active:
            icon_button.icon_color = Colors.HOVER_ICON_COLOR if is_hovered else Colors.ICON_COLOR

        e.control.bgcolor = Colors.HOVER_BG_COLOR if is_hovered else None
        e.control.update()

    def _on_menu_item_click(self, index, route, _):
        if self.active_item_index == index:
            return

        # 重置所有按钮的颜色
        for i, item in enumerate(self.menu_items):
            icon_button = item.content.content.controls[0]
            icon_button.icon_color = Colors.ICON_COLOR
            item.update()

        self.active_item_index = index
        icon_button = self.menu_items[index].content.content.controls[0]
        icon_button.icon_color = Colors.ACTIVE_ICON_COLOR
        self.menu_items[index].update()

        # 导航到指定页面
        self.page.go(route)

    def _create_user_data(self, title: str, name: str, description: str):
        return ft.Row(
            controls=[
                ft.Container(
                    width=42,
                    height=42,
                    bgcolor=Colors.USER_DATA_BG_COLOR,
                    alignment=ft.alignment.center,
                    border_radius=8,
                    content=ft.Text(
                        value=title,
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=Colors.USER_DATA_TEXT_COLOR,
                    ),
                ),
                ft.Column(
                    spacing=1,
                    controls=[
                        ft.Text(value=name, **TextStyles.USER_DATA, ref=self.user_name_ref),
                        ft.Text(value=description, **TextStyles.USER_DATA, ref=self.user_description_ref),
                    ],
                ),
            ]
        )

    def _toggle_sidebar(self, e):
        self.width = 200 if self.width == 62 else 62

        # 更新菜单项的文本透明度
        for item in self.menu_items:
            text_opacity = item.content.content.controls[1]
            text_opacity.opacity = 1 if self.width == 200 else 0
            text_opacity.update()

        # 更新用户数据和退出按钮的文本透明度
        refs = [self.user_name_ref, self.user_description_ref, self.logout_text_ref]
        for ref in refs:
            if ref.current:
                ref.current.opacity = 1 if self.width == 200 else 0
                ref.current.update()

        self.update()
