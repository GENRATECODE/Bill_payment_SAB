
import mysql
class item:
    def __init__(self):
        self.table_name="Item_management"
        config={
            'user':'SBP_Payment',
            'password':'admin',
            'host':'127.0.0.1',
            'database':'your_database',
            'raise_on_warnings':True
        }
        self.conn=mysql.connector.connect(**config)
        self.cursor=self.conn.cursor()
        print('Connection established')
    def name_get(self):
        try:
            query=(f"")
            self.cursor.execute(query,(config['database'],self.table_name))
            # if cursor
        except mysql.connector.Error as err:
            print(f'Error From Database : {err}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("Connection closed")
        
    def id_get(self):
        try:
            query=(f"")
            self.cursor.execute(query,(config['database'],self.table_name))
            # if cursor
        except mysql.connector.Error as err:
            print(f'Error From Database : {err}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("Connection closed")
        
    def details_of_item(self):
        try:
            query=(f"")
            self.cursor.execute(query,(config['database'],self.table_name))
            # if cursor
        except mysql.connector.Error as err:
            print(f'Error From Database : {err}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("Connection closed")
                pass
    def add(self):
        try:
            query=(f"")
            self.cursor.execute(query,(config['database'],self.table_name))
            # if cursor
        except mysql.connector.Error as err:
            print(f'Error From Database : {err}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("Connection closed")
            #    pass
    def remove(self,items):
        try:
            query=(f"")
            self.cursor.execute(query,(config['database'],self.table_name))
            # if cursor
        except mysql.connector.Error as err:
            print(f'Error From Database : {err}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("Connection closed")
                pass
    def display_items(self,Type):
        try:
            query=(f"")
            self.cursor.execute(query,(config['database'],self.table_name))
            # if cursor
        except mysql.connector.Error as err:
            print(f'Error From Database : {err}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("Connection closed")
                pass
    def modify(self):
        try:
            query=(f"")
            self.cursor.execute(query,(config['database'],self.table_name))
            # if cursor
        except mysql.connector.Error as err:
            print(f'Error From Database : {err}')
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("Connection closed")
                pass
    
if __name__ =="__main__":
    product=item()
    