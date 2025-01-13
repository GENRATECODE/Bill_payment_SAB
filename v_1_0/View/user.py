import flet as ft
import os
import sys
from flet import UserControl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controller.bill_number_generator_sec import onlyread_sec, update_sec
from Controller.bill_number_generator import onlyread, update

class ProfileAPP(UserControl):  # Inherit from UserControl
    def __init__(self, page: ft.Page):
        super().__init__()  # Call the parent class constructor
        self.page = page

        self.default = 'assets/logo/Raj Distributor.jpg'  # Default image path
        self.page.on_resized=self.on_resize 
        self.result_photo = ft.Text('')
        self.file_result = ft.Text('')
        # self.page.vertical_alignment=ft.MainAxisAlignment.CENTER
        # self.page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
        # Edit option
        self.from_name_who_field = ft.TextField(label='Enter Your Form Name')
        self.GST_no_field = ft.TextField(label='Enter Your GST NO')
        self.invoice_bill_who_gst_field = ft.TextField(label='Enter Your Custom Bill No.')
        self.invoice_bill_no_gst_field = ft.TextField(label='Enter Your Custom Bill No. WGST')
        self.email_field = ft.TextField(label='Enter Your Email ID')
        self.mobile_no_field = ft.TextField(label='Enter Your Mobile No')
        self.bill_path_picker = ft.FilePicker(on_result=self.pick_files_result)
        self.address_show_field = ft.TextField(label='Enter Your Address')
        self.profile_photo_picker = ft.FilePicker(on_result=self.photo_upload_result)

        self.file_button = ft.ElevatedButton('Select Folder', icon=ft.Icons.FOLDER, on_click=lambda _: self.bill_path_picker.get_directory_path())
        self.profile_photo_icon = ft.ElevatedButton('Select Profile Photo', icon=ft.Icons.EMOJI_PEOPLE, on_click=lambda _: self.profile_photo_picker.pick_files(allow_multiple=True))
        dialog_column = ft.Column(controls=[
            ft.Row([self.from_name_who_field, self.GST_no_field],),
            ft.Row([self.invoice_bill_who_gst_field, self.invoice_bill_no_gst_field],),
            ft.Row([self.email_field, self.mobile_no_field],),
            self.address_show_field,
            self.file_button,
            self.file_result,
            self.profile_photo_icon,
            self.result_photo,
        ], spacing=10, alignment=ft.MainAxisAlignment.START)
        
        # Dialog
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Your Profile"),
            content_padding=10,
            actions_padding=10,
            content=ft.Container(content=dialog_column, width=600, height=400),
            actions=[
                ft.TextButton('Cancel', on_click=self.close_dialog),
                ft.TextButton('Save', on_click=self.save_dialog)
            ]
        )

        self.page.dialog = self.dialog
        self.page.overlay.append(self.bill_path_picker)
        self.page.overlay.append(self.profile_photo_picker)

        # Temp variables
        self.path_bill_temp = 'Temp Dir'
        self.temp_name = " Company"
        self.temp_mobile = '+91'
        self.email_txt_temp = 'enter mail'
        self.GST_temp = 'check'
        self.src_temp = 'assets/logo/Raj_distributos.png'  # Default profile picture
        self.mobile_txt_temp = 'enter number' 
        self.bill_no_t = 'None'
        self.bill_no = 'None'
        self.address_temp = "None"

        # Profile image as CircleAvatar
        # Profile image as CircleAvatar (embed ft.Image inside content)
        self.profile_img = ft.CircleAvatar(
            content=ft.Image(src=self.src_temp, fit=ft.ImageFit.CONTAIN),
            radius=100  ,
            tooltip="Profile Photo"
        )  # Initial image
        self.mobile = ft.Text(self.temp_mobile, color='red')

    def photo_upload_result(self, e: ft.FilePickerResultEvent):
        # Update the profile photo after a new one is picked
        try:
            if e.files:
                self.src_temp = e.files[0].path  # Update with new photo path
                self.profile_img.background_image = self.src_temp  # Update the CircleAvatar's image
                self.result_photo.value = self.src_temp
                self.result_photo.update()
                self.profile_img.update()  # Refresh the CircleAvatar with the new image
            else:
                self.result_photo.value = "Cancelled"
                self.result_photo.update()
        except Exception as ex:
            print(f'Error: {ex}')

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        try:
            self.file_result.value = e.path if e.path else "Cancelled!"
            self.file_result.update()
        except Exception as ex:
            print(f'Error: {ex}')

    def save_dialog(self, e):
        self.page.dialog.open = False
        self.temp_name = self.from_name_who_field.value
        self.GST_temp = self.GST_no_field.value
        self.bill_no_t = self.invoice_bill_who_gst_field.value
        self.bill_no = self.invoice_bill_no_gst_field.value
        self.email_txt_temp = self.email_field.value
        self.temp_mobile = self.mobile_no_field.value
        self.path_bill_temp = self.file_result.value
        self.address_temp = self.address_show_field.value
        self.form_name.value = self.temp_name
        self.GST_no.value = self.GST_temp
        self.invoice_bill_gst.value = self.bill_no_t
        self.invoice_bill_no_gst.value = self.bill_no
        self.email.value = self.email_txt_temp
        self.mobile_value.value = self.temp_mobile
        self.bill_path_value.value = self.path_bill_temp
        self.address_value.value = self.address_temp
        self.profile_img.background_image = self.src_temp  # Update the CircleAvatar image
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Saved Edit Your Detail"))
        self.page.snack_bar.open = True
        self.page.update()

    def on_resize(self, e):
        self.img.width = self.page.window.width
        self.img.height = self.page.window.height
        self.page.update()

    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Close Edit Option"))
        self.page.snack_bar.open = True
        self.page.update()

    def editbtn(self, e):
        self.page.dialog.open = True
        self.page.update()

    def on_hovers(self, e):
        e.control.bgcolor = "orange" if e.data == "true" else "blue"
        e.control.update()

    def build(self):
        # Define the structure of your Profile page here in the build method
        self.profile = ft.Text(
            spans=[
                ft.TextSpan(
                    "Profile",
                    ft.TextStyle(
                        size=60,
                        font_family='sonic',
                        weight=ft.FontWeight.BOLD,
                        foreground=ft.Paint(
                            gradient=ft.PaintLinearGradient(
                                (900, 20), (499, 20), [ft.Colors.RED_ACCENT, ft.Colors.YELLOW_ACCENT]
                            )
                        ),
                    ),
                ),
            ],
        )

        # Name Text   
        self.form_name_who = ft.Text("Form Name", size=22, weight=ft.FontWeight.BOLD, color='#00224D', font_family='im_font')
        self.GST_no_who = ft.Text("GST No.", size=22, weight=ft.FontWeight.BOLD, font_family='Times', color='#00224D')
        self.invoice_bill_gst_who = ft.Text("Current Bill -t> no:", color='#00224D', size=22, weight=ft.FontWeight.BOLD, font_family='im_font')
        self.invoice_bill_no_gst_who = ft.Text("Current Bill no", color='#00224D', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.email_who = ft.Text('Email', color='#00224D', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.mobile_who = ft.Text('Mobile No', color='#00224D', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.bill_path_who = ft.Text("PDF Of Invoice Save Location", color='#00224D', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.address_show_who = ft.Text("Address Shop", color='#00224D', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")

        # Value Text
        self.form_name = ft.Text(self.temp_name, size=22, weight=ft.FontWeight.BOLD, color='#1C0A00', font_family='im_font')
        self.GST_no = ft.Text(self.GST_temp, size=22, weight=ft.FontWeight.BOLD, font_family='Times', color='#1C0A00')
        self.invoice_bill_gst = ft.Text(self.bill_no_t, color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family='im_font')
        self.invoice_bill_no_gst = ft.Text(self.bill_no, color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.email = ft.Text(self.email_txt_temp, color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.mobile_value = ft.Text(self.mobile_txt_temp, color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.bill_path_value = ft.Text(self.path_bill_temp, color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.address_value = ft.Text(self.address_temp, color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.btn = ft.ElevatedButton(
            'Edit',
            icon='edit',
            bgcolor='BLUE',
            on_click=self.editbtn,
            on_hover=self.on_hovers
        )

        # Background Image
        self.img = ft.Image(
            src="assets/background/Background Profile.jpg",
            fit=ft.ImageFit.FILL,
            width=self.page.width,
            height=self.page.height
        )

        # Text Container
        self.text_con = ft.Container(
            content=ft.Column([self.profile]),
            blur=ft.Blur(5, ft.BlurTileMode.MIRROR),
            width=800,
            ink=True,
            image_opacity=0.4,
            alignment=ft.alignment.center
        )

        # Profile Box
        self.profile_box = ft.Container(
            blur=ft.Blur(5, ft.BlurTileMode.MIRROR),
            ink=True,
            image_opacity=0.8,
            width=800,
            padding=ft.padding.all(20),
            content=ft.Column(
                [
                    ft.Row([self.profile_img], spacing=90, alignment=ft.MainAxisAlignment.CENTER),  # Use CircleAvatar
                    ft.Divider(),
                    ft.Row([
                        self.form_name_who, self.form_name,
                        ft.VerticalDivider(),
                        self.GST_no_who, self.GST_no,
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Row([
                        self.invoice_bill_gst_who, self.invoice_bill_gst,
                        ft.VerticalDivider(),
                        self.invoice_bill_no_gst_who, self.invoice_bill_no_gst,
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Row([
                        self.email_who, self.email,
                        ft.VerticalDivider(),
                        self.mobile_who, self.mobile_value,
                    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Row([self.bill_path_who, self.bill_path_value], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Row([self.address_show_who, self.address_value], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Row([self.btn], spacing=90, alignment=ft.MainAxisAlignment.CENTER)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

        # Body - whole profile section
        return ft.Container(
            ft.Stack([
                self.img,
                ft.Container(
                    ft.Column([self.text_con, self.profile_box]),
                    alignment=ft.alignment.center
                )
            ])
        )
