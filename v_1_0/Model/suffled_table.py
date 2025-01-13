import mysql.connector
from mysql.connector import Error
import asyncio

# Created suffled Database 

class suffled_access_table:
    def __init__(self):
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
    def dealer_access_invoice(self, status):
        try:
            # Parameterized query with status filter
            query = """
            SELECT 
                d.company_name AS 'Company Name',
                b.invoice_number AS 'Invoice Number',
                b.amount AS 'Amount',
            b.invoice_date AS 'Date',
                DATEDIFF(CURDATE(), b.invoice_date) AS 'Days'
            FROM 
                buy b
            JOIN  
                dealer d ON b.dealer_id = d.dealer_id
            WHERE 
                b.status = %s  -- Filter by status
            ORDER BY  
                b.invoice_date;
            """
            self.cursor.execute(query, (status,))
            columns = [column[0] for column in self.cursor.description]  # Get column names
            print(f"{columns}")
            detail = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return detail
        except Error as err:
            print(f"Error Listing Dealer: {err}")
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
