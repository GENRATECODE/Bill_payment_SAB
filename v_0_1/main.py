from flet import *
from View.app_bar import NavBar_for
from View.log_in_class import LoginPage
from View.user_temp import ProfileAPP
from View.Invoices import InvoiceApp
from View.item_mangement_oops import ItemManagement

import flet as ft

def main(page: ft.Page):
    # Function to handle route changes
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        NavBar_for(page),
                        ft.ElevatedButton("Go to About Page", on_click=lambda _: page.go("/about")),
                    ],
                )
            )
        elif page.route == "/about":
            page.views.append(
                ft.View(
                    "/about",
                    [
                        ft.Text("About Page"),
                        ft.ElevatedButton("Go to Home Page", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    # Set the route change handler
    page.on_route_change = route_change

    # Navigate to the initial route ("/")
    page.go(page.route)

# Start the app


app(target=main, assets_dir="assets")    