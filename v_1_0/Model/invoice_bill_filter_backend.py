import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector
from datetime import datetime
class InvoiceFilteringBackend:
    def __init__(self):
        self.config = {
            'host': os.getenv('host'),
            'user': os.getenv('user'),
            'password': os.getenv('password'),
            'database': os.getenv('database'),
            'raise_on_warnings': True,
        }
        try:
            self.connection = mysql.connector.connect(
            **self.config
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except Exception as err:
            self.connection.close()
            return {'error':e}
    def ensure_connection(self):
        """Ensure the database connection is active"""
        if not self.connection.is_connected():
            try:
                self.connection.reconnect(attempts=3, delay=5)
                self.cursor=self.connection.cursor(dictionary=True)
                # print("Connection Established")
            except Exception as err:
                # print(f"Error reconnecting to database: {err}")
                return {"error":err}
    def fetch_invoices(self, table_type, **kwargs):
        """
        Fetch invoices based on the selected table type (retail or wholesale) and additional filters.

        :param table_type: "RETAIL" or "WHOLESALE"
        :param kwargs: Additional parameters for filtering
        :return: List of matching invoices with customer details
        """
        self.ensure_connection()
        try:
            query = ""
            params = []
            if table_type == "sell_retail":
                query1 = """
                    SELECT sr.invoice_no, sr.amount, sr.sell_time, sr.cust_id,sr.unique_id, c.person_name, c.mobile, c.location
                    FROM sell_retail sr
                    JOIN Customer c ON sr.cust_id = c.cust_id
                    WHERE 1=1
                """
            elif table_type == "sell_wholesale":
                query1 = """
                    SELECT sw.invoice_no, sw.amount,sw.remark, sw.sell_time, sw.sell_wholesale_status, sw.cust_id, c.person_name, c.mobile, c.location
                    FROM sell_wholesale sw
                    JOIN Customer c ON sw.cust_id = c.cust_id
                    WHERE 1=1
                """
            # print(f"{query1,*params}")
        # Add filters based on kwargs
            if "start_date" in kwargs and "end_date" in kwargs:
                query = " ".join([query1 ," AND sw.sell_time BETWEEN %s AND %s" if table_type == "sell_wholesale" else " AND sr.sell_time BETWEEN %s AND %s"])
                params += [kwargs["start_date"], kwargs["end_date"]]
            if "mobile" in kwargs:
                query =" ".join([query1," AND c.mobile = %s"])
                params.append(kwargs["mobile"])
            if "customer_id" in kwargs:
                query = " ".join([query1," AND c.cust_id = %s"])
                params.append(kwargs["customer_id"])
            if "invoice_number" in kwargs:
                query = " ".join([query1," AND sw.invoice_no = %s" if table_type == "sell_wholesale" else " AND sr.invoice_no = %s"])
                params.append(kwargs["invoice_number"])
            if "payment_status" in kwargs and table_type == "sell_wholesale":
                query = " ".join([query1," AND sw.sell_wholesale_status = %s"])
                params.append(kwargs["payment_status"])
            if "min_amount" in kwargs and "max_amount" in kwargs:
                query = " ".join([query1," AND sw.amount BETWEEN %s AND %s" if table_type == "sell_wholesale" else " AND sr.amount BETWEEN %s AND %s"])
                params += [kwargs["min_amount"], kwargs["max_amount"]]
            
            # print(f"{query,*params}")
            self.cursor.execute(query, params)
            return {'result':self.cursor.fetchall()}
        except Exception as e:
            return {'error':e}
        finally:
            self.cursor.close()
            self.connection.close()
