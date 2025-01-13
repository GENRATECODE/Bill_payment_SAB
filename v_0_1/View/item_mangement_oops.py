import mysql.connector
import flet as ft
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.city_code import city_codes
from Model.type_item import items_type
from View.logo import invoice_logo
from View.app_bar import NavBar_for

class ItemManagement:
    existing_ids = set(['a', 'abs', 'cde', 'a2', 'a5', 'anna Poliana'])
    existing_names = set(['abhay', 'hercules', 'hero', 'what', 'you'])

    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_ui()
    def setup_ui(self):
        self.page.scroll = ft.ScrollMode.ADAPTIVE

        self.search_results_id = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True, col={'sm': 3})
        self.search_results_name = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True, col={'md': 5})
        self.search_box_id = ft.TextField(label='Product ID', on_change=self.handle_id, col={'sm': 3})
        self.search_box_name = ft.TextField(label='Item Name', on_change=self.handle_name, col={'md': 5})

        self.btn_search = ft.ElevatedButton(
            "Search",
            style=ft.ButtonStyle(
                color={ft.ControlState.HOVERED: ft.Colors.WHITE, ft.ControlState.FOCUSED: ft.Colors.BLUE,
                       ft.ControlState.DEFAULT: ft.Colors.BLACK},
                bgcolor={ft.ControlState.FOCUSED: ft.Colors.PINK_200, "": ft.Colors.YELLOW},
                padding={ft.ControlState.HOVERED: 20},
                overlay_color=ft.Colors.TRANSPARENT,
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.BLUE),
                      ft.ControlState.HOVERED: ft.BorderSide(2, ft.Colors.BLUE)},
                shape={ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                       ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=2)},
            ),
            col={'xs': 2},
            icon='search'
        )

        self.btn_clear = ft.ElevatedButton(
            "Clear",
            style=ft.ButtonStyle(
                color={ft.ControlState.HOVERED: ft.Colors.WHITE, ft.ControlState.FOCUSED: ft.Colors.BLUE,
                       ft.ControlState.DEFAULT: ft.Colors.BLACK},
                bgcolor={ft.ControlState.FOCUSED: ft.Colors.PINK_200, "": ft.Colors.YELLOW},
                padding={ft.ControlState.HOVERED: 20},
                overlay_color=ft.Colors.TRANSPARENT,
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.BLUE),
                      ft.ControlState.HOVERED: ft.BorderSide(2, ft.Colors.BLUE)},
                shape={ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                       ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=2)},
            ),
            col={'xs': 2},
            icon=ft.Icons.CLEAR_SHARP,
            on_click=self.on_clear
        )

        self.search_container = ft.Container(
            content=ft.ResponsiveRow([self.search_box_id, self.search_box_name, self.btn_search, self.btn_clear]),
            width=self.page.width
        )

        self.result_container = ft.Container(
            content=ft.ResponsiveRow([self.search_results_id, self.search_results_name]),
            width=self.page.width
        )

        self.list_items_id = {
            name: ft.ListTile(
                title=ft.Text(name),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.update_value_id,
                data=name
            )
            for name in ItemManagement.existing_ids
        }

        self.list_item_name = {
            name: ft.ListTile(
                title=ft.Text(name),
                leading=ft.Image(src=invoice_logo, color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.update_value_name,
                data=name
            )
            for name in ItemManagement.existing_names
        }

        self.id_field = ft.TextField(label="Generate ID ", col={'md': 2})
        self.name_field = ft.TextField(label="Name", col={'md': 5})
        self.rate_field = ft.TextField(label="Rate", col={"md": 2})
        self.quantity_field_rate = ft.Dropdown(label=" Quantity Of Item",
                                               hint_text="Select your Quantity of Product",
                                               options=[
                                                   ft.dropdown.Option("PCS"),
                                                   ft.dropdown.Option("SET"),
                                                   ft.dropdown.Option("PKT"),
                                                   ft.dropdown.Option("GRS"),
                                                   ft.dropdown.Option("PAIR"),
                                                   ft.dropdown.Option("LT."),
                                                   ft.dropdown.Option("KG."),
                                                   ft.dropdown.Option("GM."),
                                                   ft.dropdown.Option("Dozen"),
                                               ],
                                               width=370, col={"md": 2})

        self.Type = ft.Dropdown(label="Type of Item",
                                hint_text="Cycle,Parts,Mobil,Tyre,Tube,AutoTyre,AutoTube",
                                options=[
                                    ft.dropdown.Option("Cycle Parts"),
                                    ft.dropdown.Option("Cycle Tube"),
                                    ft.dropdown.Option("Cycle Tyre"),
                                    ft.dropdown.Option("AutoTyre"),
                                    ft.dropdown.Option("AutoTube"),
                                    ft.dropdown.Option("Standard Cycle 22"),
                                    ft.dropdown.Option("Gents Cycle 20in"),
                                    ft.dropdown.Option("Ladies Cycle 20in"),
                                    ft.dropdown.Option("Gents Cycle 18in"),
                                    ft.dropdown.Option("Ladies Cycle 18in"),
                                    ft.dropdown.Option("Ranger Cycle 26"),
                                    ft.dropdown.Option("Ranger Cycle 24"),
                                    ft.dropdown.Option("Baby Cycle"),
                                    ft.dropdown.Option("Kid Cycle"),
                                    ft.dropdown.Option("Mobil"),
                                ],
                                width=370, col={"md": 2})

        self.Gst_rate = ft.TextField(label='Percentage Of GST', col={"md": 2})
        self.whole_sale = ft.TextField(label='Percentage of Wholesale Profit', col={"md": 2})
        self.retail_sale = ft.TextField(label='Percentage Of Retail Profit', col={"md": 2})
        self.Stock = ft.TextField(label='Stock', hint_text="Enter Total Box", col={"md": 2})
        self.Stock_per_box = ft.TextField(label='Packing', hint_text="Packing Number", col={"md": 2})
        self.supplier = ft.TextField(label="Supplier Name", col={"md": 3})
        self.location_of_Product = ft.TextField(label="Product Location Supplier", col={"md": 3})

        self.add_button_btn = ft.ElevatedButton(text="Add Item", on_click=self.add_into_database, col={"md": 2})
        self.generate_id_btn = ft.ElevatedButton(text="Generate ID", on_click=self.generate_id_function, col={"md": 2})
        self.reset_btn = ft.ElevatedButton(text="Reset", on_click=self.reset_entry_box, col={"md": 2})
        self.update_btn = ft.ElevatedButton(text="Update Item", on_click=self.update_item, col={"md": 2})
        self.delete_btn = ft.ElevatedButton(text="Delete Item", on_click=self.delete_item, col={"md": 2})
        self.export_as_csv_btn = ft.ElevatedButton(text="Export Item", on_click=self.export_item_csv, col={"md": 2})

        self.items_list = ft.Column([ft.Container(margin=5,
                                                  padding=4,
                                                  alignment=ft.alignment.center,
                                                  bgcolor=ft.Colors.BLUE_ACCENT,
                                                  content=ft.ResponsiveRow([
                                                      self.id_field, self.name_field,
                                                      self.Type,
                                                      self.quantity_field_rate,
                                                      self.rate_field,
                                                      self.Stock,
                                                      self.Stock_per_box,
                                                      self.supplier,
                                                      self.location_of_Product, self.Gst_rate, self.whole_sale,
                                                      self.retail_sale]),
                                                  border_radius=0, ),
                                     ])

        self.add_button = ft.Column([ft.Container(margin=10,
                                                  padding=10,
                                                  alignment=ft.alignment.center,
                                                  bgcolor=ft.Colors.BLUE_ACCENT,
                                                  content=ft.ResponsiveRow(
                                                      [self.generate_id_btn, self.add_button_btn, self.reset_btn,
                                                       self.update_btn, self.delete_btn, self.export_as_csv_btn]),
                                                  border_radius=10, ),
                                     ft.Divider(thickness=5, color="blue"),
                                     ])

        self.page.on_resized = self.on_resizes
        self.page.add(ft.Text('Search Item'),
                      ft.Divider(),
                      self.search_container,
                      self.result_container,
                      ft.Divider(), self.items_list,
                      ft.Divider(), self.add_button
                      )

    def on_clear(self, e):
        self.search_box_id.value = ''
        self.search_box_name.value = ''
        self.search_results_id.controls.clear()
        self.search_results_name.controls.clear()
        self.search_results_id.update()
        self.search_results_name.update()
        self.search_box_id.update()
        self.search_box_name.update()

    def add_into_database(self, e):
        if self.id_field.value:
            pass
        else:
            self.id_field.error_text = 'Please First Generate ID'
            self.id_field.update()

    def generate_id_function(self, e):
        if self.name_field.value:
            pass
        else:
            self.name_field.error_text = 'Please Enter Product Name'
            self.name_field.update()
            return
        if self.Type.value:
            pass
        else:
            self.Type.error_text = 'Please Enter Type of Item'
            self.Type.update()
            return
        if self.quantity_field_rate.value:
            pass
        else:
            self.quantity_field_rate.error_text = 'Please Enter Quantity'
            self.quantity_field_rate.update()
            return
        if self.rate_field.value:
            total = int(self.rate_field.value)
        else:
            self.rate_field.error_text = "Please Enter Rate of Item"
            self.rate_field.update()
            return
        if self.Stock.value:
            pass
        else:
            self.Stock.error_text = "Please Enter Stock of Item"
            self.Stock.update()
            return

        if self.Stock_per_box.value:
            pass
        else:
            self.Stock_per_box.error_text = "Please Enter Stock per Box of Item"
            self.Stock_per_box.update()
            return
        if self.supplier.value:
            pass
        else:
            self.supplier.error_text = "Please Enter Supplier Name"
            self.supplier.update()
            return
        if self.location_of_Product.value:
            pass
        else:
            self.location_of_Product.error_text = 'Please Enter Location of Product'
            self.location_of_Product.update()
            return
        if self.Gst_rate.value:
            gst = int(self.Gst_rate.value) / 100
        else:
            self.Gst_rate.error_text = 'Please Enter GST Rate'
            self.Gst_rate.update()
            return
        if self.whole_sale.value:
            profit = int(self.whole_sale.value) / 100
        else:
            self.whole_sale.error_text = 'Please Enter Whole Sale Rate'
            self.whole_sale.update()
            return
        if self.retail_sale.value:
            pass
        else:
            self.retail_sale.error_text = 'Please Enter Retail Sale Rate'
            self.retail_sale.update()
            return

        if self.location_of_Product.value:
            pass
        else:
            self.location_of_Product.error_text = 'Please Enter Location of Product'
            self.location_of_Product.update()
            return

        name = 6
        Rate = str(round(total + total * gst + total * profit))
        print(Rate)
        print(total + total * int(self.retail_sale.value) + total * int(self.Gst_rate.value) / 100)
        temp = ''
        supplier_digit = 3
        temp += items_type[self.Type.value]
        for word in self.name_field.value.split():
            if name != 0:
                if word.isdigit() or word in ["X", "1/2", "IBC", "1"]:
                    continue
                temp += word[0].upper()
                name -= 1
            else:
                break
        temp += Rate
        temp += city_codes[self.location_of_Product.value]
        for name_sale in self.supplier.value.split():
            if supplier_digit != 0:
                temp += name_sale[0].upper()
                supplier_digit -= 1
        unique_id = temp
        counter = 1
        while unique_id in ItemManagement.existing_ids:
            unique_id = f"{temp}{counter}"
            counter += 1

        self.id_field.value = unique_id
        self.id_field.update()
        print("generate_id")
        ItemManagement.existing_ids.add(unique_id)

    def reset_entry_box(self, e):
        self.Stock.value = ''
        self.Stock_per_box.value = ''
        self.search_box_id.value = ''
        self.search_box_name.value = ''
        self.search_results_id.controls.clear()
        self.search_results_name.controls.clear()
        self.name_field.value = ''
        self.id_field.value = ''
        self.rate_field.value = ''
        self.quantity_field_rate.value = ''
        self.Gst_rate.value = ''
        self.whole_sale.value = ''
        self.retail_sale.value = ''
        self.supplier.value = ''
        self.Type.value = ''
        self.location_of_Product.value = ''
        self.page.update()
        print("Reset")

    def update_item(self, e):
        pass

    def delete_item(self, e):
        pass

    def export_item_csv(self, e):
        pass

    def on_resizes(self, e):
        self.search_container.width = self.page.width
        self.result_container.width = self.page.width
        self.page.update()

    def update_value_id(self, e):
        print('update value id')
        self.search_results_id.controls.clear()
        self.search_results_id.update()

    def update_value_name(self, e):
        print('update value name')
        self.search_results_name.controls.clear()
        self.search_results_name.update()

    def handle_name(self, e):
        print('name')
        search_query = e.control.value.lower()
        self.search_results_name.controls = [
            self.list_item_name.get(n) for n in ItemManagement.existing_names if search_query in n.lower()
        ]
        self.search_results_name.update()

    def handle_id(self, e):
        print('id')
        search_query = e.control.value.lower()
        self.search_results_id.controls = [
            self.list_items_id.get(n) for n in ItemManagement.existing_ids if search_query in n.lower()
        ] if search_query else []
        self.search_results_id.update()

    def handle_search_bar(self, e):
        search_query = e.data.lower()
        self.search_box_id.controls = [
            self.list_items_id.get(n) for n in ItemManagement.existing_ids if search_query in n.lower()
        ] if search_query else []
        self.page.update()


# def main(page: ft.Page):
#     ItemManagement(page)


# ft.app(target=main, assets_dir='v_0_1/View/assets')
