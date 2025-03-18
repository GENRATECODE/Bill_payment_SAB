import mysql.connector
from mysql.connector import Error
import pandas as pd
import aiomysql
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

class custmers:
    def __init__(self):
        self.table_name = "Customer"
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
            print("Connection established Customer Table")
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
                self.close_connection()
                print(f"Error reconnecting to database: {err}")
    def add(self):
        pass
    def  remove(self,item):
        pass
    def cust_fetch_wholesale(self):
        self.ensure_connection()
        try:
            query=f"SELECT cust_id,person_name,mobile,location from {self.table_name} where cust_type=%s"
            self.cursor.execute(query,('WHOLE_SALE',))
            columns = [column[0] for column in self.cursor.description]
            item = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        except Exception as e:
            return "Error fetching item details: {e}"
            # return None
        finally:
            return item
            self.close_connection()
    def cust_fetch_retail(self):
        self.ensure_connection()
        try:
            query=f"SELECT cust_id,person_name,mobile,location from {self.table_name} where cust_type=%s"
            self.cursor.execute(query,('RETAIL_SALE',))
            columns = [column[0] for column in self.cursor.description]
            item = dict(zip(columns, self.cursor.fetchall()))
        except Exception as e:
            return "Error fetching item details: {e}"
            # return None
        finally:
            return item
            self.close_connection()
    def modify(self):
        pass
    def  search(self):
        pass
    def credit(self):
        pass
    def debit(sef):
        pass
    def  check_balance(self):
        pass
    def update(self):
        pass
    
if __name__ =="__main__":
    product=item()
    