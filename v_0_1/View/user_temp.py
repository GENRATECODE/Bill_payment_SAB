import flet as ft
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controller.bill_number_generator_sec import onlyread_sec, update_sec
from Controller.bill_number_generator import onlyread, update
from View.app_bar import NavBar
class ProfileAPP:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.padding = 0
        self.page.fonts = {
            "sonic": "assets/font/Freedom-10eM.ttf",
            "im_font": "assets/font/IMFellDoublePicaSC-Regular.ttf",
            "inflt": "assets/font/InflateptxBase-ax3da.ttf"
        }
        self.default = 'assets/logo/Raj Distributor.jpg'
        self.result_photo = ft.Text('')
        self.file_result=ft.Text('')
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

        # Dialog 
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Your Profile"),
            content_padding=10, 
            actions_padding=10,  
            content=ft.Column(controls=[
                self.from_name_who_field,
                self.GST_no_field,
                self.invoice_bill_who_gst_field,
                self.invoice_bill_no_gst_field,
                self.email_field,
                self.mobile_no_field,
                self.address_show_field,
                self.file_button,
                self.file_result,
                self.profile_photo_icon,
                self.result_photo,
            ], spacing=10, alignment=ft.MainAxisAlignment.START),
            actions=[
                ft.TextButton('Cancel'),
                ft.TextButton('Save')
            ]
        )

        self.page.dialog = self.dialog
        self.page.overlay.append(self.bill_path_picker)
        self.page.overlay.append(self.profile_photo_picker)

        # UI Variable
        self.profile = None
        self.body = None

        # Temp variable
        self.path_bill = 'Temp Di'
        self.temp_name = "Raj Distributor Company"
        self.temp_mobile = '+91 9415863731'
        self.email_txt = 'enter mail'
        self.GST = 'check'
        self.src = 'assets/logo/Raj Distributor.jpg'
        self.mobile_txt = 'enter number'

        # Icon Text-
        self.form_name = None
        self.GST_no = None
        self.invoice_bill_gst = None
        self.invoice_bill_no_gst = None
        self.btn = None
        self.mobile = None

        # Profile image
        self.profile_img = None

        # Column separated
        self.col_data = None

        # Profile Picture and data board
        self.profile_box = None

        # Layout
        self.data_layout = None

        # Background Image
        self.img = None

        # Create the body of the page
        self.col = None
        self.body = None
        self.alert = None
        self.main()

    def photo_upload_result(self, e: ft.FilePickerResultEvent):
        try:
            self.result_photo.value = e.files[0].path   
            self.result_photo.update()   
        except Exception as ex:
            print(f'Error: {ex}')

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        self.file_result.value = e.path if e.path else "Cancelled!"
        self.file_result.update()

    def on_resize(self, e):
        self.img.width = self.page.width
        self.img.height = self.page.height
        self.page.update()

    def editbtn(self, e):
        self.page.dialog.open = True
        self.page.update()  

    def on_hovers(self, e):
        e.control.bgcolor = "orange" if e.data == "true" else "blue"
        e.control.update()

    def main(self):
        # Initialize form fields

        # Text Needed
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
        self.photo_upload_who = ft.Text("Profile Photo", color='#00224D', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")

        # Value Text
        self.form_name = ft.Text(self.temp_name, size=22, weight=ft.FontWeight.BOLD, color='#1C0A00', font_family='im_font')
        self.GST_no = ft.Text(self.GST, size=22, weight=ft.FontWeight.BOLD, font_family='Times', color='#1C0A00')
        self.invoice_bill_gst = ft.Text(f"{onlyread():04d}", color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family='im_font')
        self.invoice_bill_no_gst = ft.Text(f"{onlyread_sec():04d}", color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.email = ft.Text(self.email_txt, color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.mobile_value = ft.Text(self.mobile_txt, color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")
        self.bill_path_value = ft.Text("Enter Value", color='#1C0A00', size=22, weight=ft.FontWeight.BOLD, font_family="im_font")

        self.btn = ft.ElevatedButton(
            'Edit',
            icon='edit',
            bgcolor='BLUE',
            on_click=self.editbtn,
            on_hover=self.on_hovers
        )

        # Profile image
        self.profile_img = ft.Image(height=200, width=200, border_radius=ft.border_radius.all(80))

        self.mobile = ft.Text(self.temp_mobile, color='red')

        # Background Image
        self.img = ft.Image(
            src="assets/background/Background Profile.jpg",  # Replace with your image URL or file path
            fit=ft.ImageFit.FILL,  # How the image should fit in the space provided
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
                    ft.Row([self.profile_img], spacing=90, alignment=ft.MainAxisAlignment.CENTER),
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
                    ft.Row([self.address_show_who, self.form_name], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Row([self.btn], spacing=90, alignment=ft.MainAxisAlignment.CENTER)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )    

        # Body - whole profile section 
        self.body = ft.Container(
            ft.Stack([
                self.img,
                ft.Container(
                    ft.Column([self.text_con, self.profile_box]),
                    alignment=ft.alignment.center
                ) 
            ])
        )
        
        # Page on_resize event handler
        self.page.on_resize = self.on_resize
        
        # Add form fields to the page
        self.page.add(self.body)

# def main(page: ft.Page):
#     # Initialize and display the profile form
#     ProfileAPP(page)

# # Run the app
# ft.app(target=main, assets_dir='v_0_1/View/assets')
