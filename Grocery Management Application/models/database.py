import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            price REAL,
                            stock INTEGER)""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            items TEXT,
                            total REAL,
                            payment_method TEXT)""")
        self.conn.commit()

    def add_product(self, name, price, stock):
        self.cur.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        self.conn.commit()

    def get_products(self):
        self.cur.execute("SELECT * FROM products")
        return self.cur.fetchall()

    def delete_product(self, product_id):
        self.cur.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()
    
    def update_stock(self, product_id, new_stock):
        self.cur.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, product_id))
        self.conn.commit()

    def add_order(self, items, total, payment_method):
        self.cur.execute("INSERT INTO orders (items, total, payment_method) VALUES (?, ?, ?)", (items, total, payment_method))
        self.conn.commit()
    
    def get_orders(self):
        self.cur.execute("SELECT * FROM orders")
        return self.cur.fetchall()
    
    def close(self):
        self.conn.close()
