# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'billing_system'
}

def create_database():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
def add_item_to_db(name, price, quantity):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
    conn.commit()
    conn.close()

def remove_item_from_db(item_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    conn.commit()
    conn.close()

def get_all_items():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

create_database()
