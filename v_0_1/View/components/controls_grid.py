import flet as ft

class ControlsGrid(ft.GridView):
    def __init__(self,gallery):
        self.expand=1
        self.runs_count=5
        self.max_extent=250
        self.child_aspect_ratio=3.0
        self.spacing=10
        self.runs_count=10
        self.gallery=gallery
    def grid_item_clicked(self,e):
        route=f"{self.page.route}/{e.control.data.id}"
        self.page.go(route)
    def display(self):
        self.visible=True
        self.controls=[]
        for grid_item in self.gallery.selected_control_group.grid_items:
            self.controls.append(
                ft.Container(
                    on_click=self.grid_item_clicked,
                    data=grid_item,
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    border_radius=5,
                    padding=15,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ft.Icon(name=ft.Icons.FOLDER_OPEN),
                                  ft.Text(
                                      value=grid_item,
                                      weight=ft.FontWeight.W_500,
                                      size=14,
                                  ),],
                    ),
                )
            )