import sqlite3

def create_database():
    conn = sqlite3.connect("product.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,         
            name TEXT,
            prices INTEGER,
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

if __name__ == "__main__":
    create_database()