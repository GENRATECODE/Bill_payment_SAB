import flet as ft

class Dashboard(ft.Container):
    def __init__(self,app_layout, page):
        super().__init__()
        self.page = page
        self.page.auto_scroll=False
        self.page.scroll=ft.ScrollMode.ADAPTIVE
        self.app_layout=app_layout
        self.content=self.build()
    def build(self):
        # Top bar (app bar) with navigation
        app_bar = ft.AppBar(
            title=ft.Text("Dashboard", size=24, weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.BLUE,
            actions=[
                ft.IconButton(icon=ft.Icons.HOME, tooltip="Overview", on_click=lambda _: self.page.go("/overview")),
                ft.IconButton(icon=ft.Icons.ASSESSMENT, tooltip="Reports", on_click=lambda _: self.page.go("/reports")),
                ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Settings", on_click=lambda _: self.page.go("/settings")),
                ft.IconButton(icon=ft.Icons.ACCOUNT_CIRCLE, tooltip="Profile"),
            ],
        )

        # Main content area with dashboard cards
        dashboard_content = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Card(
                                content=ft.Container(
                                    ft.Column(
                                        [
                                            ft.Text("Total Sales", size=20),
                                            ft.Text("$125,000", size=24, weight=ft.FontWeight.BOLD),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.Colors.GREEN_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ),
                            ft.Card(
                                content=ft.Container(
                                    ft.Column(
                                        [
                                            ft.Text("New Customers", size=20),
                                            ft.Text("300", size=24, weight=ft.FontWeight.BOLD),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.Colors.PURPLE_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ),
                            ft.Card(
                                content=ft.Container(
                                    ft.Column(
                                        [
                                            ft.Text("Pending Orders", size=20),
                                            ft.Text("45", size=24, weight=ft.FontWeight.BOLD),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    padding=ft.padding.all(20),
                                    width=250,
                                    height=150,
                                    bgcolor=ft.Colors.RED_200,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        scroll=ft.ScrollMode.ADAPTIVE,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Recent Sales", size=18, weight=ft.FontWeight.BOLD),
                                width=800,
                                padding=ft.padding.symmetric(vertical=20),
                            ),
                        ],
                    ),
                    ft.Row(
                        [
                            # Example of a table or chart container
                            ft.Container(
                                content=ft.Text("Data Table or Chart Here"),
                                width=800,
                                height=300,
                                bgcolor=ft.Colors.GREY_200,
                                border_radius=ft.border_radius.all(10),
                                padding=ft.padding.all(10),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=20,
                expand=True,
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            expand=True,
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.GREY_50,
      
        )


        # Main layout with a column (app bar, content, footer)
        return ft.Column(
            [
                dashboard_content,

            ],
            expand=True,
        )


# def main(page: ft.Page):
#     page.title = "Dashboard Without Sidebar"
#     page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
#     page.add(Dashboard(page))

# ft.app(target=main)
