import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "store.db")

def connect():
    return sqlite3.connect(DB_NAME)

def clean_categories():
    conn = connect()
    cursor = conn.cursor()
    
    # Categorii corecte (cele pe care le vrem)
    correct_categories = [
        'Procesoare (CPU)', 'Plăci de bază (Motherboard)', 'Plăci video (GPU)', 'Memorie RAM', 'SSD / HDD', 'Carcase PC', 'Surse de alimentare (PSU)', 'Sisteme de răcire', 'Plăci de sunet',
        'Monitoare', 'Tastaturi', 'Mouse-uri', 'Căști / Headset-uri', 'Boxe', 'Webcam-uri', 'Microfoane',
        'Mousepad-uri', 'Cabluri și adaptoare', 'Standuri / Suporturi', 'Iluminare RGB', 'Controlere ventilatoare',
        'Laptopuri', 'Sisteme PC preconfigurate',
        'Routere', 'Plăci de rețea', 'Adaptoare Wi-Fi', 'Cabluri de rețea',
        'Licențe Windows / Office', 'Software antivirus', 'Licențe pentru jocuri și platforme',
        'Console', 'Controller-e', 'Accesorii gaming', 'Scaune și birouri de gaming'
    ]
    
    # Mapări pentru a corecta categoriile duplicate
    category_mappings = {
        'Mouse': 'Mouse-uri',
        'Tastatură': 'Tastaturi',
        'PC gata făcut': 'Sisteme PC preconfigurate'
    }
    
    print("🧹 Curățare categorii...")
    
    # 1. Actualizează produsele cu categorii duplicate
    for old_name, new_name in category_mappings.items():
        if new_name in correct_categories:
            cursor.execute("""
                UPDATE products 
                SET category_id = (SELECT id FROM product_categories WHERE name = ?)
                WHERE category_id = (SELECT id FROM product_categories WHERE name = ?)
            """, (new_name, old_name))
            print(f"✅ Migrat produse din '{old_name}' în '{new_name}'")
    
    # 2. Șterge categoriile care nu mai sunt necesare
    cursor.execute("SELECT name FROM product_categories")
    all_categories = [row[0] for row in cursor.fetchall()]
    
    for cat_name in all_categories:
        if cat_name not in correct_categories and cat_name not in category_mappings.keys():
            # Verifică dacă există produse în această categorie
            cursor.execute("SELECT COUNT(*) FROM products WHERE category_id = (SELECT id FROM product_categories WHERE name = ?)", (cat_name,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute("DELETE FROM product_categories WHERE name = ?", (cat_name,))
                print(f"🗑️  Șters categoria '{cat_name}' (fără produse)")
            else:
                print(f"⚠️  Categoria '{cat_name}' are {count} produse - nu se șterge")
    
    conn.commit()
    conn.close()
    print("✅ Curățare completă!")

if __name__ == "__main__":
    clean_categories() 