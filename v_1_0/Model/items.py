import mysql.connector
from mysql.connector import Error
import pandas as pd
import aiomysql
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
class Item:
    def __init__(self):
        self.table_name = "item"
        self.config = {
            'host': os.getenv("host"),
            'user': os.getenv("user"),
            'password': os.getenv("password"),
            'database': os.getenv("database"),
            'raise_on_warnings': True,
        }
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Connection established Item table")
        except Error as err:
            self.conn.close()
            print(f"Error connecting to database: {err}")

    def ensure_connection(self):
        """Ensure the database connection is active."""
        if not self.conn.is_connected():
            try:
                self.conn.reconnect(attempts=3, delay=5)
                self.cursor = self.conn.cursor()  # Recreate cursor
                print("Connection re-established")
            except Error as err:
                return f"Error reconnecting to database: {err}"

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
            return f"Error adding item: {err}"
        finally:
            # return "Item added successfully."
            self.close_connection()

    def remove(self, item_id):
        """Remove an item by its ID."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"DELETE FROM {self.table_name} WHERE item_id = %s"
            self.cursor.execute(query, (item_id,))
            self.conn.commit()
            
        except Error as err:
            return f"Error removing item: {err}"
        finally:
            self.close_connection()
            # return "Item removed successfully."

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
            return f"Error updating item: {err}"
        finally:
            self.close_connection()

    def get_item_details2id(self, item_id):
        """Retrieve details of an item."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"SELECT item_description, item_buy_unit,gst_percentage,wholesale_price FROM {self.table_name} WHERE item_id = %s"
            self.cursor.execute(query, (item_id,))
            columns = [column[0] for column in self.cursor.description]
            item = dict(zip(columns, self.cursor.fetchone()))
            # print(f"Item details: {item}")
            
        except Exception as e:
            return "Error fetching item details: {e}"
            # return None
        finally:
            return item
            self.close_connection()
    def stock_check(self):
        """Stock Query """
        self.ensure_connection()
        try:
            query=f"SELECT i.item_id,i.item_description,i.stock,i.reorder_level,d.company_name,i.Update_date FROM item i JOIN dealer d ON i.dealer_id = d.dealer_id;"
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            item = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            # print(f"Item details: {item}")
            
        except Error as err:
            print(f"Error fetching item details: {err}")
            return None
        finally:
            
            self.close_connection()
            return item
    def stock_check_specific(self,value):
        """Stock Query """
        self.ensure_connection()
        try:
            query=f"SELECT i.item_id, i.item_description, i.stock, i.reorder_level,d.company_name,i.Update_date FROM  item AS i Inner JOIN dealer AS d on i.dealer_id = d.dealer_id where i.dealer_id = d.dealer_id and i.item_id LIKE '{value}%'  ;"
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            item = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            # print(f"Item details: {item}")
            
        except Error as err:
            print(f"Error fetching item details: {err}")
            return None
        finally:
            
            self.close_connection()
            return item
            
    def get_item_details2description(self, description):
        """Retrieve details of an item."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"SELECT * FROM {self.table_name} WHERE item_description = %s"
            self.cursor.execute(query, (description,))
            columns = [column[0] for column in self.cursor.description]
            item = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            print(f"Item details: {item}")
            
        except Error as err:
            print(f"Error fetching item details: {err}")
            return None
        finally:
            self.close_connection()
            return item
    def list_items(self):
        """List all items."""
        self.ensure_connection()  # Ensure the database connection is active

        try:
            query = f"SELECT * FROM {self.table_name}"
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            items = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            # print(f"Items: {items}")
            
        except Error as err:
            print(f"Error listing items: {err}")
            return []
        finally:
            self.close_connection()
            return items
    # Close the database connection
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

# upload download in form of excel formate 
class database2excel:
    def __init__(self):
        self.table_name = "item"
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'admin',
            'db': 'rajdistributors_database'
        }
        try:
            self.conn = None
            self.cursor = None
            print("Class initialized.")
        except Exception as err:
            print(f"Error initializing class: {err}")
    
    async def connect_to_database(self):
        """Establish an asynchronous connection to the MySQL database."""
        try:
            self.conn = await aiomysql.connect(**self.config)
            self.cursor = await self.conn.cursor()
            print("Connection established")
        except Exception as err:
            print(f"Error connecting to database: {err}")
    
    async def ensure_connection(self):
        """Ensure the database connection is active."""
        if not self.conn or not self.conn.open:
            await self.connect_to_database()
    def correct_excel_file_path(self, excel_file_path):
        """Correct the file path to avoid invalid characters like ':'."""
        # Replace invalid characters with underscores
        excel_file_path = excel_file_path.replace(":", "_")
        # Ensure the directory exists, create if not
        dir_name = os.path.dirname(excel_file_path)
    async def fetch_data(self,path):
        """Fetch data from MySQL table asynchronously and return it as a pandas DataFrame."""
        await self.ensure_connection()
        try:
            # path=self.correct_excel_file_path(excel_file_path)
            query = f"SELECT * FROM {self.table_name}"
            await self.cursor.execute(query)
            result = await self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(result, columns=columns)
            df.to_excel(path, index=True, engine='openpyxl')
            
        except Exception as err:
            print(f"Error fetching data: {err}")
            return None
        finally:
            await self.close_connection()
            return f"Successfully Generate {path}"
    
    async def upload_data_from_excel(self, excel_file_path):
        """Upload data from the Excel file to the MySQL database."""
        try:
            df = pd.read_excel(excel_file_path, engine='openpyxl')
            await self.ensure_connection()
            for _, row in df.iterrows():
                values = tuple(row)
                placeholders = ', '.join(['%s'] * len(row))
                insert_query = f"INSERT INTO {self.table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
                await self.cursor.execute(insert_query, values)
            await self.conn.commit()
            print(f"Data successfully uploaded from {excel_file_path} to the database.")
        except Exception as err:
            print(f"Error uploading data from Excel: {err}")



    async def close_connection(self):
        """Close the database connection."""
        try:
            if self.cursor:
                await self.cursor.close()
            if self.conn:
                self.conn.close()
                print("Connection closed.")
        except Exception as err:
            print(f"Error closing connection: {err}")
