import sqlite3

def create_tables():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories
                      (id INTEGER PRIMARY KEY, name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (id INTEGER PRIMARY KEY, category_id INTEGER, name TEXT, image TEXT, FOREIGN KEY (category_id) REFERENCES categories (id))''')
    conn.commit()
    conn.close()

def db_add_category(name):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def db_get_categories():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    conn.close()
    return categories
# print(db_get_categories())
def db_add_product(category_id, name, image):
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (category_id, name, image) VALUES (?, ?, ?)", (category_id, name, image))
    conn.commit()
    conn.close()

def db_get_products_by_category():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return products
if __name__ == '__main__':
    print(db_get_products_by_category())