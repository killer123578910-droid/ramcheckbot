import sqlite3
import random
from datetime import datetime,timedelta
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
                price       = i.get("price")
                quantity    = i.get("quantity") or 0
                visiting    = i.get("visit") or 0
                source_url  = i.get("productUrl") or ""
                rating      = i.get("rating")
                
                
                if price!=0:
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
    
def simulate7days():
    conn = sqlite3.connect("product.db")
    cursor = conn.cursor()
    ngaydau=datetime.strptime("2026-07-08T21:20:43.862753","%Y-%m-%dT%H:%M:%S.%f")
    cursor.execute("SELECT product_id,prices,view,rating FROM products_snapshot where time=?",("2026-07-08T21:20:43.862753",))
    productid=cursor.fetchall()
    
    
    snapshot_sql ="""
        INSERT INTO products_snapshot (product_id,time,prices,view,rating) VALUES (?, ?, ? ,? ,?)
    """
    
    
    n=1
    for i in range(7):
        
        
        
        ngayht=ngaydau+ timedelta(days=n)
        for product_id,prices,view,rating in productid:
            thaydoigia=random.uniform(-0.3,0.3)
            thaydoiview=random.uniform(0.01,0.2)
            thaydoirating=random.uniform(-0.1,0.1)
            
            nprice=int(prices+prices*thaydoigia)
            nview=int(view+view*thaydoiview)
            nrating=float(f"{rating+rating*thaydoirating:.1f}")
            
            cursor.execute(snapshot_sql,(product_id,ngayht,nprice,nview,nrating))
        n+=1
    conn.commit()
    conn.close()