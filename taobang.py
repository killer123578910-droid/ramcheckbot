import sqlite3
matra={
    283:"Ram",
    284:"SSD",
    279:"VGA",
    278:"MAIN"}
def create_database():
    conn = sqlite3.connect("product.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,         
            name TEXT,
            quantity INTEGER,
            visiting INTEGER,
            source_url TEXT,
            categoty TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products_snapshot(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            time DATETIME NOT NULL,
            prices REAL,
            view INTEGER,
            rating REAL,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE                
        )        
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS features(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            time DATETIME NOT NULL,
            feature_json TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE                
        )        
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            time DATETIME NOT NULL,
            rule_score REAL,
            ml_prob REAL,
            total_score REAL,
            label TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE                
        )        
    ''')
    


    conn.commit()
    conn.close()
    
def insert(arr):
    conn = sqlite3.connect("product.db")
    cursor = conn.cursor()
    for key,value in arr.items():
        for i in value:
            cursor.execute("INSERT INTO products (name,quantity,visiting,source_url,categoty) VALUES (?, ?, ?, ?, ?)",(i["productName"],i["quantity"],i["visit"],i["productUrl"],key))

    conn.commit()
    conn.close()