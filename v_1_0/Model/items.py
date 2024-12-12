import mysql.connector
from mysql.connector import Error

class Item:
    def __init__(self):
        self.table_name = "item"
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin',
            'database': 'rajdistributors_database',
            'raise_on_warnings': True,
        }
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Connection established")
        except Error as err:
            print(f"Error connecting to database: {err}")

    def ensure_connection(self):
        """Ensure the database connection is active."""
        if not self.conn.is_connected():
            try:
                self.conn.reconnect(attempts=3, delay=5)
                self.cursor = self.conn.cursor()  # Recreate cursor
                print("Connection re-established")
            except Error as err:
                print(f"Error reconnecting to database: {err}")

    def add(self, item_details):
        """Add a new item to the database."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"""
            INSERT INTO {self.table_name} 
            (       item_id,     
                    item_description,
                    item_buy_rate, 
                    item_buy_unit,
                    gst_percentage, 
                    profit_retail,
                    item_retail_unit, 
                    retail_price, 
                    wholesale_price,
                    profit_wholesale, 
                    sliver_discount, 
                    platinum_discount, 
                    unit_wholesale,
                    mrp, 
                    dealer_id, 
                    stock, 
                    reorder_level, update_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, item_details)
            self.conn.commit()
            print("Item added successfully.")
        except Error as err:
            print(f"Error adding item: {err}")

    def remove(self, item_id):
        """Remove an item by its ID."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"DELETE FROM {self.table_name} WHERE item_id = %s"
            self.cursor.execute(query, (item_id,))
            self.conn.commit()
            print("Item removed successfully.")
        except Error as err:
            print(f"Error removing item: {err}")

    def update(self, item_id, updates):
        """Update an item's details."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE item_id = %s"
            values = list(updates.values()) + [item_id]
            self.cursor.execute(query, values)
            self.conn.commit()
            print("Item updated successfully.")
        except Error as err:
            print(f"Error updating item: {err}")

    def get_item_details2id(self, item_id):
        """Retrieve details of an item."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"SELECT item_description, item_buy_unit,gst_percentage,wholesale_price FROM {self.table_name} WHERE item_id = %s"
            self.cursor.execute(query, (item_id,))
            columns = [column[0] for column in self.cursor.description]
            item = dict(zip(columns, self.cursor.fetchone()))
            print(f"Item details: {item}")
            return item
        except Error as err:
            print(f"Error fetching item details: {err}")
            return None
    def get_item_details2description(self, description):
        """Retrieve details of an item."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"SELECT * FROM {self.table_name} WHERE item_description = %s"
            self.cursor.execute(query, (description,))
            columns = [column[0] for column in self.cursor.description]
            item = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            print(f"Item details: {item}")
            return item
        except Error as err:
            print(f"Error fetching item details: {err}")
            return None
    def list_items(self):
        """List all items."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"SELECT item_id, item_description,stock FROM {self.table_name}"
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            items = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            print(f"Items: {items}")
            return items
        except Error as err:
            print(f"Error listing items: {err}")
            return []

    def close_connection(self):
        """Close the database connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
                print("Connection closed.")
        except Error as err:
            print(f"Error closing connection: {err}")
