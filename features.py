import sqlite3
import json
import numpy as np

def zscore(x: float, mean: float, std: float) -> float:
    return 0.0 if std < 1e-9 else (x-mean) / std

def build_feature_row(product, snapshots_last3):
    p = [s[0] for s in snapshots_last3]
    v = [s[1] for s in snapshots_last3]

    price_pct = (p[-1] - p[0]) / max(p[0], 1e-9) if len(p) >= 2 else 0.0
    views_pct = (v[-1] - v[0]) / max(v[0], 1) if len(v) >= 2 else 0.0
    price_delta = float(p[-1] - p[0]) if len(p) >= 2 else 0.0

    mean_price = float(np.mean(p)) if p else 1e-9
    std_price = float(np.std(p)) if p else 0.0

    feats = {
        "name_length": len(product[1]),
        "category": product[2],
        "price_log": float(np.log1p(product[-1])) if product[3] else 0.0,

        "price_delta": price_delta,
        "price_pct_change": float(price_pct),
        "views_pct_change": float(views_pct),
        "price_ma3": mean_price,
        "price_volatility3": float(std_price / max(mean_price,1e-9)),

        "is_price_shock": 0,
        "is_views_spike": 0
    }
    return feats

def run_feature_engineering_pipeline():
    conn = sqlite3.connect("product.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category, visiting FROM products")
    products = cursor.fetchall()

    all_features = {}
    price_changes = []
    views_changes = []

    for prod in products:
        p_id = prod[0]

        cursor.execute("""
            SELECT prices, view, time
            FROM products_snapshot
            WHERE product_id = ?
            ORDER BY time DESC
            LIMIT 3
        """, (p_id,))
        snapshots = cursor.fetchall()

        snapshots_last3 = snapshots[::-1]

        if not snapshots_last3:
            continue
        feats = build_feature_row(prod, snapshots_last3)
        all_features[p_id] = feats

        price_changes.append(feats["price_pct_change"])
        views_changes.append(feats["views_pct_change"])
    
    if price_changes and views_changes:
        mean_p_change, std_p_change = np.mean(price_changes), np.std(price_changes)
        mean_v_change, std_v_change = np.mean(views_changes), np.std(views_changes)

        THRESHOLD= 1.5

        for p_id, feats in all_features.items():
            z_p = zscore(feats["price_pct_change"], mean_p_change, std_p_change)
            z_v = zscore(feats["views_pct_change"], mean_v_change, std_v_change)

            if abs(z_p) > THRESHOLD:
                feats["is_price_shock"] = 1
            if z_v > THRESHOLD:
                feats["is_views_spike"] = 1
    
    insert_feature_sql = """
        INSERT INTO features (product_id, time, feature_json)
        VALUES (?,?,?)
    """

    from datetime import datetime
    computed_at = datetime.now().isoformat()

    for p_id, feats in all_features.items():
        feats_json_str = json.dumps(feats)

        cursor.execute("DELETE FROM features WHERE product_id = ?", (p_id,))
        cursor.execute(insert_feature_sql, (p_id, computed_at, feats_json_str))
    
    conn.commit()
    conn.close()

    anomalies = {p_id: f for p_id, f in all_features.items() if f["is_price_shock"] == 1 or f["is_views_spike"] == 1}
    return anomalies

if __name__ == "__main__":
    anomalies_summary = run_feature_engineering_pipeline()
    print(f"Tìm thấy {len(anomalies_summary)} sản phẩm có dấu hiệu dị biệt.")