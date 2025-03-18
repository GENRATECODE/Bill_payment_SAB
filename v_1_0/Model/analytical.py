import mysql.connector
from mysql.connector import Error
import pandas as pd
import aiomysql
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
class analysis_attributes:
    def __init__(self):
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