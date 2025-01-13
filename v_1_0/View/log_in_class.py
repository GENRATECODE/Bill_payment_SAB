
from Model.user import User
import asyncio
import flet as ft
import asyncio
from flet import * 
class LoginPage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        
        # self.page.padding = 0  # Ensure no padding on the page
        self.page.adaptive=True
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
        # self.img = self.create_image()

        self.content= self.create_body_container()
        self.user=User('Sytem :)')
        # Set the on_resize event handler
        # self.page.on_resized = self.on_resize
        

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
            on_click=self.on_hover_need
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
            # opacity=0.4,
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
            # opacity=0.8,
            width=500,
            height=500,
            padding=ft.padding.all(5),
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


    def create_body_container(self):
        #    
        text_col_1_2=ft.Column([self.create_first_text("श्री लक्ष्मी जी सदा सहाय ||"),      
                                           self.create_first_text("श्री कुवेर जी सदा सहाय ||"),],alignment=ft.MainAxisAlignment.CENTER)
        text_col_2_2=ft.Column([self.create_first_text("श्री शंकर जी सदा सहाय ||"),self.create_first_text("श्री काली जी सदा सहाय ||"),],)
        # row who that login and text in one row    
        main_row=ft.Row([text_col_1_2,self.login_box, text_col_2_2,],alignment=ft.MainAxisAlignment.CENTER,spacing=40)   
        # who all bind on column
        main_col=ft.Column([self.create_first_text("श्री गणेशाय नमः ||"),     
                            main_row,  
                            ],
                        #    expand=True,
                           alignment=ft.MainAxisAlignment.START,horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=100) 

        # return ft.Column([,ft.Row([,self.login_box,ft.Column([]),])]        
        #                     ,alignment=ft.MainAxisAlignment.CENTER,expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        return  ft.Container(main_col)
        # return main_col
    def snack_bar_func(self,text):
        
        snack_bar=ft.SnackBar(
            content=ft.Text(text),
            action="Alright!",
            action_color="Pink",
            dismiss_direction=ft.DismissDirection.HORIZONTAL 
        )
        # self.page.snack_bar=snack_bar
        # self.page.overlay.clear()
        self.page.overlay.append(snack_bar)
        snack_bar.open=True
        self.page.update()   
    def on_hover_need(self, e):
        self.snack_bar_func("You Username is GST NO OR Email Address")

    async def log_in_function(self, e):
        
        flag = await self.user.log_in(self.user_id.value.lower(),self.password.value)
        working_dir = await self.user.working_dir(self.user_id.value.lower(),self.password.value)
        if( self.user_id.value == "" and self.password.value=="") or not flag:
            self.user_id.error_text = "Please Enter Your User ID"
            self.password.error_text = "Please Enter Your Password"
            self.page.update()
        elif self.user_id.value == "" :
            self.user_id.error_text = "Please Enter Your User ID"
            self.page.update()
        elif self.password.value == "":
            self.password.error_text = "Please Enter Your Password"
            self.page.update()
            
        elif (self.user_id.value).lower()=="superadmin" and flag:
            self.page.session.set(self.user_id.value,self.password.value)
            self.page.session.set("User",self.user_id.value)
            self.page.session.set("password",self.password.value)
            self.page.session.set("working_dir",working_dir)
            self.page.session.set("who","WholeSale")
            print("Login button clicked")
            self.page.go("/Home")  # Change the route to /home on login
            self.snack_bar_func("Login successful! Welcome back.")
            self.page.update()
        elif (self.user_id.value).lower()=="admin" and flag:
            self.page.session.set(self.user_id.value,self.password.value)
            self.page.session.set("User",self.user_id.value)
            self.page.session.set("password",self.password.value)
            self.page.session.set("working_dir",working_dir)
            self.page.session.set("who","RetailSale")
            print("Login button clicked")
            self.page.go("/Home2")  # Change the route to /home on login
            self.snack_bar_func("Login successful! Welcome back.")
            self.page.update()       
        else:
            print("go to else part where to give a error message")
            # self.page.go('/invoice')
            # print(self.user_id.value)
            # print(self.password.value)


    def reset_password(self, e):
        container = ft.Container(content=ft.Column(controls=[
            ft.TextField(label='Enter New Password'),
            ft.TextField(label='Confirm Your Password')
        ]), width=500, height=400)
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
        print("New password saved")
        self.page.dialog.open = False
        self.page.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()

# # Start the Flet application
# ft.app(target=LoginPage.body, assets_dir='../assets')
