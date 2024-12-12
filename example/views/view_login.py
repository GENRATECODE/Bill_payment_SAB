import flet
from flet import *
from math import pi
import time


class AnimatedBox(Container):
    def __init__(self, border_color, bg_color, rotate_angle):
        self.border_color = border_color
        self.bg_color = bg_color
        self.rotate_angle = rotate_angle
        super().__init__()
        self.content = self.build()

    def build(self):
        return Container(
            width=48,
            height=48,
            border=border.all(2.5, self.border_color),
            bgcolor=self.bg_color,
            border_radius=2,
            rotate=transform.Rotate(self.rotate_angle, alignment.center),
            animate_rotation=animation.Animation(700, "easeInOut"),
        )


class SignInButton(Container):
    def __init__(self, btn_name,on_click=None):
        self.btn_name = btn_name
        super().__init__()
        self.on_click= on_click
        self.content = Container(
            content=ElevatedButton(
                content=Text(
                    self.btn_name,
                    size=13,
                    weight="bold",
                ),
                style=ButtonStyle(
                    shape={
                        "": RoundedRectangleBorder(radius=8),
                    },
                    color={
                        "": "black",
                    },
                    bgcolor={"": "#7df6dd"},
                ),
                height=42,
                width=320,
                on_click=self.on_click
            ),
        )


class UserInputField(Container):
    def __init__(
        self,
        icon_name,
        text_hint,
        hide: bool,
        function_emails: bool,
        function_check: bool,
        on_change = None
    ):
        self.icon_name = icon_name
        self.text_hint = text_hint
        self.hide = hide
        self.on_change = on_change
        self.function_emails = function_emails
        self.function_check = function_check
        super().__init__()
        self.content = self.build()

    def prefix_email_containers(self):
        email_labels = ["@gmail.com", "@hotmail.com"]
        label_title = ["GMAIL", "MAIL"]
        _row = Row(spacing=1, alignment=MainAxisAlignment.END)
        for index, label in enumerate(email_labels):
            _row.controls.append(
                Container(
                    width=45,
                    height=30,
                    alignment=alignment.center,
                    content=Text(label_title[index], size=9, weight="bold"),
                    data=label,
                )
            )
        return Row(
            vertical_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.END,
            spacing=2,
            opacity=0,
            animate_opacity=200,
            offset=transform.Offset(0.35, 0),
            animate_offset=animation.Animation(400, "decelerate"),
            controls=[_row],
        )

    def off_focus_input_check(self):
        return Container(
            opacity=0,
            offset=transform.Offset(0, 0),
            animate=200,
            border_radius=6,
            width=18,
            height=18,
            alignment=alignment.center,
            content=Checkbox(
                fill_color="#7df6dd",
                check_color="black",
                disabled=True,
            ),
        )

    def build(self):
        return Container(
            width=320,
            height=40,
            border=border.only(
                bottom=border.BorderSide(0.5, "white54"),
            ),
            border_radius=6,
            content=Row(
                spacing=20,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Icon(
                        name=self.icon_name,
                        size=14,
                        opacity=0.85,
                    ),
                    TextField(
                        border_color="transparent",
                        bgcolor="transparent",
                        height=20,
                        width=200,
                        text_size=12,
                        content_padding=3,
                        cursor_color="white",
                        cursor_width=1,
                        color="white",
                        hint_text=self.text_hint,
                        hint_style=TextStyle(
                            size=11,
                            color="white54",
                        ),
                        on_change=self.on_change,
                        password=self.hide,
                    ),
                    self.prefix_email_containers(),
                    self.off_focus_input_check(),
                ],
            ),
        )


def logginView(page:Page):


    content = Card(
        width=408,
        height=612,
        elevation=15,
        content=Container(
            bgcolor="#23262a",
            border_radius=6,
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Divider(height=40, color="transparent"),
                    Stack(
                        controls=[
                            AnimatedBox("#e9665a", None, 0),
                            AnimatedBox("#7df6dd", "#23262a", pi / 4),
                        ]
                    ),
                    Divider(height=20, color="transparent"),
                    Column(
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            Text(
                                "Sign In Below", size=22, weight="bold", color="white54"
                            ),
                            Text(
                                "Advanced Python-Flet UI Concepts",
                                size=13,
                                weight="bold",
                                color="white54",
                            ),
                        ],
                    ),
                    Divider(height=30, color="transparent"),
                    UserInputField(
                        icons.PERSON_ROUNDED,
                        "Email",
                        False,
                        True,
                        True,
                    ),
                    Divider(height=1, color="transparent"),
                    UserInputField(
                        icons.LOCK_OUTLINE_ROUNDED,
                        "Password",
                        True,
                        False,
                        True,
                    ),
                    Divider(height=1, color="transparent"),
                    Row(
                        width=320,
                        alignment=MainAxisAlignment.END,
                        controls=[
                            Container(
                                content=Text(
                                    "Forgot Passowrd?", size=9, color="white54"
                                ),
                            )
                        ],
                    ),
                    Divider(height=45, color="transparent"),
                    SignInButton("Sign In",lambda _:page.go('/home')),
                    Divider(height=35, color="transparent"),
                    Text(
                        "Sign in form using Python and Flet",
                        size=10,
                        color="white54",
                    ),
                ],
            ),
        ),
    )
    content = Column(
        [
            Row(
                [
                    Column(
                        [content],
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
            )
        ],
        spacing=50,alignment=MainAxisAlignment.CENTER
    )

    return content
