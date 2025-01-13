import flet as ft

def main(page: ft.Page):
    def handle_tap(e):
        search_bar.open_view()
    def printer(e):
        print(f"{e.control.data}")
        stock.value=f"{e.control.data}"
        search_bar.close_view()
        page.update()
    def on_search_change(e):
        search_query = e.control.value.lower()
        # Update search_results with ListTile for each matched item
        search_results.controls = [
            ft.ListTile(
                title=ft.Text(item),  # Display the item name as the title
                leading=ft.Icon(ft.Icons.SEARCH),  # Optional icon for each ListTile
                trailing=ft.Text("Details"),  # Optional trailing text
                hover_color="pink",  # Change color on hover
                data=f"{1} hello mini",
                on_click=printer # Action on click
            )
            for item in items
            if search_query in item.lower()
        ] if search_query else []
        page.update()

    items = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]

    search_results = ft.ListView()  # To display filtered results

    search_bar = ft.SearchBar(
        bar_hint_text="Search for a fruit...",
        on_tap=handle_tap,
        on_change=on_search_change,  # Event triggered on typing
        controls=[search_results]  # Child controls displayed in dropdown
    )
    stock =ft.Text("Heelo")
    page.add(search_bar,stock,)


ft.app(target=main)

# Run the app
if __name__ == "__main__":
    ft.app(target=main)
