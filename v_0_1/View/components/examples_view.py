import flet as ft 

class ExamplesView(ft.Column):
    def __init__(self,gallery):
        super().__init__()
        self.gallery=gallery
        self.visible=False
        self.expand=True
        self.control_name_text=ft.Text(style=ft.TextThemeStyle.HEADLINE_MEDIUM)
        self.control_description=ft.Text(style=ft.TextThemeStyle.BODY_MEDIUM)
        self.examples=ft.Column(expand=True,spacing=10,scroll=ft.ScrollMode.AUTO)
        self.controls=[
            self.control_name_text,
            self.control_description,
            self.examples,
        ]
        def display(self,grid_item):
            self.visible=True
            self.examples.controls=[]
            self.control_name_text.value=grid_item.name
            self.control_description.value=grid_item.description
            for example in grid_item.examples:
                self.example.controls.append(
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    aligment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=ft.Texts(example.name,
                                                      style=ft.TextThemeStyle.TITLE_MEDIUM),
                                    weight=ft.FontWeight.W_500,
                                ),
                                ft.IconButton(
                                    content=ft.Image()
                                )
                            )
                        ]
                    )
                )