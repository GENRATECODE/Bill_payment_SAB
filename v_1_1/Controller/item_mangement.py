import mysql.connector as mc


class item:
    def  __init__(self, name, price):
        self.mydb=mc.connect(host="localhost",
                            user="root",
                            passwd="admin",
                            database="bill_payment")
        self.cursor = self.mydb.cursor()
    def show_database(self):
        self.cursor.execute('SHOW DATABASE')
        return self.cursor
    def add_item(self,item_id,item_name,buyer_id,gst,buyying_rate,cost,profit,normal_sell_price):
        sql_querry="INSERT INTO item (item_id,product_name,purchase_buyer_id,gst_percentage,buying_rate,cost_price,profit,normal_sell_price) VALUES(%s,%s,%s,%d,%f,%f,%f,%f,%d)"
        item_add=(item_id,item_name,buyer_id,gst,buyying_rate,cost,profit,sell_price,stock)
        self.cursor.execute(sql_querry,item_add)
        self.mydb.commit()
    def  remove_item(self, item_id):
        sql_querry= "DELETE FROM items WHERE Item_ID=%s"
        self.cursor.execute(sql_querky, (item_id,))
        self.mydb.commit()
        
    def modify(self,columns,value):
        # columns should be a list of column names and value is also a list with the same number
        pass
    def  get_items(self):
        pass
    def get_stock(slef):
        pass
    def  set_stock(self, id, quantity):
        pass
    def  search_by_name(self, name):
        pass
    