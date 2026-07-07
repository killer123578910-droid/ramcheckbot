import sqlite3
def create_database():
    conn = sqlite3.connect("product.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,         
            name TEXT,
            quantity INTEGER,
            visiting INTEGER,
            source_url TEXT UNIQUE,
            category TEXT,
            time DATETIME
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
    upsert_sql = """
        INSERT INTO products (name, quantity, visiting, source_url, category, time)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(source_url) DO UPDATE SET
            name        = excluded.name,
            quantity    = excluded.quantity,
            visiting    = excluded.visiting,
            category    = excluded.category,
            time        = excluded.time;
    """
    snapshot_sql ="""
        INSERT INTO products_snapshot (product_id,time,prices,view,rating) VALUES (?, ?, ? ,? ,?)
    """
    crawltime=arr["crawl_time"]
    for key,value in arr.items():
        if key!="crawl_time":
            for i in value:
                name        = i.get("productName") or ""
                price       = i.get("price") or 0
                quantity    = i.get("quantity") or 0
                visiting    = i.get("visit") or 0
                source_url  = i.get("productUrl") or ""
                rating      = i.get("rating")
            
                if not source_url:
                    print(f"⚠️ Bỏ qua sản phẩm không có URL: {name}")
                    continue
                
                cursor.execute(upsert_sql,(name,quantity,visiting,source_url,key,crawltime))
                
                
                
                product_id=cursor.lastrowid
                if product_id==0:
                    cursor.execute("SELECT id FROM products where source_url = ?",(source_url,))
                    row=cursor.fetchone()
                    product_id=row[0] if row else None
                if product_id:
                    cursor.execute(snapshot_sql,(product_id,crawltime,price,visiting,rating))
    conn.commit()
    conn.close()