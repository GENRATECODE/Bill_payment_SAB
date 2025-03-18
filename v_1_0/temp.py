import asyncio
import flet as ft
import pygtrie


class MySearch(ft.Container):
    def __init__(self):
        super().__init__()
        self.search = ft.TextField(
            label="Search",
            width=300,
            height=30,
            on_change=self.debounce_search,
        )
        self.car_names = [
            "Honda", "Mitsubishi", "Ford", "Saab", "Nissan", "Isuzu", "Volkswagen",
            "Toyota", "Mercedes-Benz", "Suzuki", "Corbin", "Dodge", "Chevrolet", 
            "GMC", "Cadillac", "BMW", "Land Rover", "Audi", "Acura", "Pontiac", 
            "Oldsmobile", "Hyundai", "Citroën", "Mercury", "Porsche", "Ch"
        ]
        self.trie = self.build_trie(self.car_names)
        self.search_result = ft.ListView(expand=True, spacing=5)
        self.content = ft.Column(
            [self.search, self.search_result],
            spacing=10,
            alignment="start",
        )
        self._debounce_task = None  # To store the reference to the debounce task

    def build_trie(self, data):
        """Build a trie with item descriptions."""
        trie = pygtrie.CharTrie()
        for item in data:
            trie[item.lower()] = item  # Store in lowercase for case-insensitive search
        return trie

    async def _debounce(self, query):
        """Debounce handler to delay search execution."""
        await asyncio.sleep(0.3)  # Delay for 300ms
        self.perform_search(query)

    def debounce_search(self, e):
        """Debounce logic for search."""
        query = e.control.value
        if self._debounce_task:  # Cancel the previous task if it exists
            self._debounce_task.cancel()
        self._debounce_task = asyncio.create_task(self._debounce(query))

    def perform_search(self, query):
        """Search the trie and update the ListView."""
        query = query.lower()  # Convert query to lowercase
        self.search_result.controls.clear()  # Clear old results

        if query:
            try:
                # Fetch results matching the prefix
                results = [value for key, value in self.trie.items(prefix=query)]
                if results:
                    for result in results:
                        self.search_result.controls.append(ft.Text(result))
                else:
                    self.search_result.controls.append(ft.Text("No matches found."))
            except KeyError:
                # No matches found; add a message
                self.search_result.controls.append(ft.Text("No matches found."))
        else:
            # Show all car names if the search field is empty
            for name in self.car_names:
                self.search_result.controls.append(ft.Text(name))

        self.search_result.update()


def main(page: ft.Page):
    page.title = "Search"
    page.add(MySearch())


if __name__ == "__main__":
    ft.app(target=main)
