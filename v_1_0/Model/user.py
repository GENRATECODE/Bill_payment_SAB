import mysql.connector
from mysql.connector import Error
import asyncio
import base64
class User:
    def __init__(self, name):
        self.name = name
        self.connection = None
        print("Print System Try to Log")
    async def connect_db(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='admin',
                database='rajdistributors_database'
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    async def sign_up(self, username, password, gst, mobile, email, role="user"):
        if not self.connection:
            await self.connect_db()

        cursor = self.connection.cursor()
        query = """
        INSERT INTO shop (username, password, gst, mobile, email, role)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (username, password, gst, mobile, email, role))
            self.connection.commit()
            print(f"User '{username}' signed up successfully.")
        except Error as e:
            print(f"Failed to sign up user: {e}")
        finally:
            cursor.close()

    async def log_in(self, username, password):
        if not self.connection:
            await self.connect_db()

        cursor = self.connection.cursor()
        query = "SELECT * FROM shop WHERE username = %s AND password = %s"
        try:
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            if user:
                print(f"User '{username}' logged in successfully.")
                return True
            else:
                print("Invalid username or password.")
                return False
        except Error as e:
            print(f"Login failed: {e}")
            return False
        finally:
            cursor.close()
    async def get_user_details(self, username,password):
        if not self.connection:
            await self.connect_db()

        cursor = self.connection.cursor()
        query = "SELECT username, email, role, gst, mobile,role FROM shop WHERE username = %s"
        try:
            cursor.execute(query, (username,))
            user_details = cursor.fetchone()
            return user_details
        except Error as e:
            print(f"Failed to retrieve user details: {e}")
            return None
        finally:
            cursor.close()
    async def Lottie_icon(self, name):
        if not self.connection:
            await self.connect_db()
            
        cursor = self.connection.cursor()
        try:
            query = "SELECT file_data FROM lottie_files WHERE name = %s"
            await cursor.execute(query, (name,))
            result = await cursor.fetchone()
            print(f'{result[0].read()}')
            if result:
                base_data = base64.b64encode(result[0]).decode("utf-8")  # Directly encode binary data
                return base_data
            else:
                print(f"No data found for Lottie icon '{name}'")
                return None
        except Error as e:
            print(f"Failed to retrieve lottie icon: {e}")
            return None
        finally:
            cursor.close()

    async def upload_lottie(self, file_path, name):
        if not self.connection:
            await self.connect_db()

        cursor = self.connection.cursor()
        try:
            # Attempt to open the file
            try:
                with open(file_path, "rb") as file:
                    file_data = file.read()
            except FileNotFoundError:
                print(f"Error: File not found at '{file_path}'")
                return

            query = "INSERT INTO lottie_files (name, file_data) VALUES (%s, %s)"
            cursor.execute(query, (name, file_data))
            self.connection.commit()
            print(f"Lottie file '{name}' uploaded successfully.")
        except Error as e:
            print(f"Failed to upload lottie file: {e}")
        finally:
            cursor.close()

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed.")