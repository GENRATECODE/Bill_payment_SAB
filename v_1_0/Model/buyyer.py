import mysql.connector
from mysql.connector import Error
import asyncio
import pandas as pd
import aiomysql
import os
import asyncio
class dealer_database:
    def __init__(self):
        self.table_name = "dealer"
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
            print('Connection to database established.')
        except Error as err:
            print(f"Error connecting to database: {err}")

    def add_dealer(self, dealer_details):
        """Add a new dealer to the database."""
        try:
            query = f"""
            INSERT INTO {self.table_name} (
                dealer_id, company_name, name_agent, Address, gst, 
                ACOUNT_NO, ifsc_NO, bank, branch, mobile, email
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, dealer_details)
            self.conn.commit()
            print("Dealer added successfully.")
        except Error as err:
            print(f"Error adding dealer: {err}")

    def remove_dealer(self, dealer_id):
        """Remove a dealer by its ID ."""
        try:
            query = f"DELETE FROM {self.table_name} WHERE dealer_id = %s"
            self.cursor.execute(query, (dealer_id,))
            self.conn.commit()
            print("Dealer removed successfully.")
        except Error as err:
            print(f"Error removing dealer: {err}")

    def list_dealers(self):
        """List all dealers."""
        dealers=list()
        try:
            query = f"SELECT * FROM {self.table_name}"
            self.cursor.execute(query)
            dealer_ids = [row[0] for row in self.cursor.fetchall()]
            return dealer_ids
        except Error as err:
            print(f"Error listing dealers: {err}")
    def gst(self):
        """List all dealers."""
        dealers=list()
        try:
            query = f"SELECT gst FROM {self.table_name}"
            self.cursor.execute(query)
            dealer_ids = [row[0] for row in self.cursor.fetchall()]
            return dealer_ids
        except Error as err:
            print(f"Error listing dealers: {err}")
    def list_dealers_with_company(self):
        """List all dealers with their company names as a dictionary."""
        dealers = []
        try:
            query = f"SELECT dealer_id, company_name FROM {self.table_name}"
            self.cursor.execute(query)
            # Fetch all rows and convert them to a list of dictionaries
            columns = [column[0] for column in self.cursor.description]  # Get column names
            dealers = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return dealers
        except Error as err:
            print(f"Error listing dealers with company names: {err}")
        return dealers
    def get_dealer_details(self, dealer_id):
        """Retrieve details of a specific dealer."""
        try:
            # Ensure the connection is still alive
            if not self.conn.is_connected():
                self.conn.reconnect(attempts=3, delay=5)
                self.cursor = self.conn.cursor()

            query = f"SELECT * FROM {self.table_name} WHERE dealer_id = %s"
            self.cursor.execute(query, (dealer_id,))
            dealer = self.cursor.fetchone()
            if not dealer:
                print(f"No dealer found with ID: {dealer_id}")
                return None
            columns = [column[0] for column in self.cursor.description]
            print(f"Dealer details: {dealer}")
            return dict(zip(columns, dealer))
        except Error as err:
            print(f"Error fetching dealer details: {err}")
            return None

    def update_agent(self, name, mobile, dealer_id):
        try:
        # Ensure the connection is still alive
            if not self.conn.is_connected():
                self.conn.reconnect(attempts=3, delay=5)
                self.cursor = self.conn.cursor()

        # Use parameterized query to avoid SQL injection
            query = "UPDATE dealer SET name_agent = %s, mobile = %s WHERE dealer_id = %s;"
            self.cursor.execute(query, (name, mobile, dealer_id))
            self.conn.commit()  # Commit changes
        except Error as err:
            print(f"Error updating agent details: {err}")
            return None
    def close_connection(self):
        """Close the database connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
                print("Connection closed.")
        except Error as err:
            print(f"Error closing connection : {err}")

class dealer2excel:
    def __init__(self):
        self.table_name ="dealer"
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
# Example usage
# if __name__ == "__main__":
#     dealer_manager = dealer_database()

#     # # Add a new dealer
#     # dealer_manager.add_dealer((
#     #     "D001", "ABC Pvt Ltd", "John Doe", "123 Street, City", "GST1234567890123",
#     #     "1234567890", "IFSC12345", "XYZ Bank", "Main Branch", "9876543210", "abc@example.com"
#     # ))

#     # List all dealers
#     dealer_manager.list_dealers()

#     # Get a dealer's details
#     # dealer_manager.get_dealer_details("D001")

#     # Remove a dealer
#     dealer_manager.remove_dealer("RTL423")

#     # Close the connection
#     dealer_manager.close_connection()
