from typing import Union
import flet as ft    

class LoginPage:
    def __init__(self, page: ft.Page):
        
        self.page = page
        self.page.title = "LogIn"
        self.page.padding = 0
        # self.page.appbar=NavBar(self.page)
        # Create the UI elements
        self.user_id = self.create_user_id_field()
        self.password = self.create_password_field()
        self.hover_text = self.create_hover_text()
        self.need_help = self.create_help_button()
        self.login = self.create_login_button()
        self.reset_button = self.create_reset_button()
        self.login_txt = self.create_login_text()
        self.statement = self.create_statement_text()
        self.text_con = self.create_text_container()
        self.login_box = self.create_login_box()
        self.img = self.create_image()

        self.body = self.create_body_container()

        # Set the on_resize event handler
        self.page.on_resized = self.on_resize

        # Add the image to the page
        content=ft.Column(self.body)
        self.page.add(self.body)

    def create_user_id_field(self):
        return ft.TextField(
            label='Username',
            hint_text=' Enter your UserID',
            filled=True,
            autocorrect=False,
            capitalization=ft.TextCapitalization.CHARACTERS,
            color='RED',
            prefix_icon=ft.Icons.ACCOUNT_CIRCLE_SHARP,
            border_radius=ft.border_radius.all(20),
            error_style=ft.TextStyle(
                bgcolor=ft.Colors.GREY_900,
                decoration=ft.TextDecoration.UNDERLINE,
                italic=True
            )
        )
        # page for go to home page 

    def create_password_field(self):
        return ft.TextField(
            label='Password',
            hint_text=' Enter your Password',
            prefix_icon=ft.Icons.PASSWORD,
            filled=True,
            error_style=ft.TextStyle(
                bgcolor=ft.Colors.GREY_900,
                decoration=ft.TextDecoration.UNDERLINE,
                italic=True
            ),
            autocorrect=False,
            password=True,
            can_reveal_password=True,
            border_radius=ft.border_radius.all(20)
        )

    def create_hover_text(self):
        return ft.Text(
            value='Your User ID is GST NO.\n if you forgot your password then reset it.',
            visible=False,
            size=16,
            bgcolor='white',
            color=ft.Colors.RED_ACCENT_700
        )

    def create_help_button(self):
        return ft.ElevatedButton(
            text='Help',
            icon=ft.Icons.HELP,
            icon_color=ft.Colors.BLUE,
            on_hover=self.on_hover_need
        )

    def create_login_button(self):
        return ft.ElevatedButton(
            text='LogIn',
            icon=ft.Icons.LOGIN,
            icon_color=ft.Colors.BLUE,
            on_click=self.log_in_function
        )

    def create_reset_button(self):
        return ft.ElevatedButton(
            text='Reset',
            icon='reset',
            icon_color=ft.Colors.BLUE,
            on_click=self.reset_password
        )

    def create_login_text(self):
        return ft.Text(
            spans=[
                ft.TextSpan(
                    "LogIn",
                    ft.TextStyle(
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (900, 20), (499, 20), [ft.Colors.RED_ACCENT, ft.Colors.YELLOW_ACCENT]
                            )
                        ),
                    )
                )
            ]
        )

    def create_statement_text(self):
        return ft.Text(
            spans=[
                ft.TextSpan(
                    "Welcome Back\nPlease Enter Your Credential Information",
                    ft.TextStyle(
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (900, 20), (499, 20), [ft.Colors.BLACK45, ft.Colors.BLACK87]
                            )
                        ),
                    )
                )
            ]
        )

    def create_text_container(self):
        return ft.Container(
            content=ft.Column([
                self.create_first_text("श्री गणेशाय नमः ||"),
                self.create_first_text("श्री लक्ष्मी जी सदा सहाय ||"),
                self.create_first_text("श्री कुवेर जी सदा सहाय ||"),
                self.create_first_text("श्री शंकर जी सदा सहाय ||"),
                self.create_first_text("श्री काली जी सदा सहाय ||")
            ]),
            blur=ft.Blur(5, ft.BlurTileMode.MIRROR),
            width=500,
            ink=True,
            image_opacity=0.4,
            alignment=ft.alignment.center
        )

    def create_first_text(self, text):
        return ft.Text(
            spans=[
                ft.TextSpan(
                    text,
                    ft.TextStyle(
                        size=25,
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (900, 20), (499, 20), [ft.Colors.RED_ACCENT, ft.Colors.YELLOW_ACCENT]
                            )
                        ),
                    )
                )
            ]
        )

    def create_login_box(self):
        return ft.Container(
            blur=ft.Blur(5, ft.BlurTileMode.MIRROR),
            ink=True,
            image_opacity=0.8,
            width=500,
            height=500,
            padding=ft.padding.all(20),
            content=ft.Column(
                [
                    ft.Container(self.login_txt, alignment=ft.alignment.center),
                    self.statement,
                    self.user_id,
                    self.password,
                    ft.Row([self.need_help, self.login, self.reset_button], spacing=90, alignment=ft.MainAxisAlignment.END)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    def create_image(self):
        return ft.Image(
            src="assets/background/Prime.jpg",  # Replace with your image URL or file path
            fit=ft.ImageFit.FILL,  # How the image should fit in the space provided
            width=self.page.width,
            height=self.page.height
        )

    def create_body_container(self):
        return ft.Container(
            ft.Stack([self.img, ft.Container(ft.Column([self.text_con, self.login_box, self.hover_text]), alignment=ft.alignment.center)]),
        )

    def on_resize(self, event):
        self.img.width = self.page.width
        self.img.height = self.page.height
        self.page.update()

    def on_hover_need(self, e):
        self.hover_text.visible = e.data == 'true'
        self.page.update()

    def log_in_function(self, e):
        # self.page_go_function()
        # if self.user_id.value == "":
        #     self.user_id.error_text = "Please Enter Your User ID"
        #     self.password.error_text = "Please Enter Your Password"
        # elif self.password.value == "":
        #     self.password.error_text = "Please Enter Your Password"
        # else:
        #     self.page.go('/invoice')
        #     print(self.user_id.value)
        #     print(self.password.value)
        # print("Route go opiton click")
        self.page.go('/invoice')
        # print("Route go opiton click")
        self.page.update()

    def reset_password(self, e):
        # self.GST_No=
        container=ft.Container(content=ft.Column(controls=[
                ft.TextField(label='Enter New Password'),
                ft.TextField(label='Confirm Your Password')
            ]),width=500,height=400)
        reset_question = ft.AlertDialog(
            title=ft.Text("Reset Your Password"),
            content=container, 
            actions=[
                ft.TextButton('Next', on_click=self.update_password),
                ft.TextButton('Cancel', on_click=self.close_dialog)
            ],
            open=True
        )
        self.page.dialog = reset_question
        self.page.update()

    def update_password(self, e):
        container=ft.Container(content=ft.Column(controls=[
                ft.TextField(label='Enter New Password'),
                ft.TextField(label='Confirm Your Password')
            ]),width=100,height=100)
        reset = ft.AlertDialog(
            title=ft.Text("Reset Your Password"),
            content=container,
            actions=[
                ft.TextButton('Save', on_click=self.save_password),
                ft.TextButton('Cancel', on_click=self.close_dialog)
            ],
            open=True,
            adaptive=True,
            actions_padding=ft.padding.all(30),
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content_padding=ft.padding.all(40)
        )
        self.page.dialog = reset
        self.page.update()

    def save_password(self, e):
        # Logic to save the new password
        print("New password saved")
        self.page.dialog.open = False
        self.page.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()


# # Start the Flet application
ft.app(target=LoginPage, assets_dir='v_0_1\\View\\assets')
