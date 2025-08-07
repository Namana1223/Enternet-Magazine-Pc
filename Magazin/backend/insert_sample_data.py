import sqlite3
from faker import Faker
import random
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "store.db")
faker = Faker()

# ✅ URL-uri statice pentru testare
PRODUCT_IMAGE_URL = "https://i.pinimg.com/1200x/7b/30/6b/7b306bec5e7f33f4b16b214732459406.jpg"
PROFILE_PIC_URL = "https://i.pinimg.com/736x/ad/45/97/ad4597f4acb6498d11063f1fd00e5cd5.jpg"

def connect():
    return sqlite3.connect(DB_NAME)

def insert_sample_data():
    conn = connect()
    cursor = conn.cursor()

    # CATEGORII EXTINSE conform listei utilizatorului
    categories = [
        # 1. Componente PC
        ('Procesoare (CPU)', 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=400&h=300&fit=crop'),
        ('Plăci de bază (Motherboard)', 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&h=300&fit=crop'),
        ('Plăci video (GPU)', 'https://images.unsplash.com/photo-1591480555736-5e3fc9d8e5b4?w=400&h=300&fit=crop'),
        ('Memorie RAM', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('SSD / HDD', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Carcase PC', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Surse de alimentare (PSU)', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Sisteme de răcire', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Plăci de sunet', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Monitoare', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Tastaturi', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Mouse-uri', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTa3axAKVWzSIDN9FkdqDJcBhqpkvQm_dDFpw&s'),
        ('Căști / Headset-uri', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Boxe', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Webcam-uri', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Microfoane', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Mousepad-uri', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Cabluri și adaptoare', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Standuri / Suporturi', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Iluminare RGB', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Controlere ventilatoare', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Laptopuri', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Sisteme PC preconfigurate', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Routere', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Plăci de rețea', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Adaptoare Wi-Fi', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Cabluri de rețea', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Licențe Windows / Office', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Software antivirus', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Licențe pentru jocuri și platforme', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Console', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Controller-e', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Accesorii gaming', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop'),
        ('Scaune și birouri de gaming', 'https://images.unsplash.com/photo-1593642634315-48f5414c3ad9?w=400&h=300&fit=crop')
    ]
    category_map = {}

    for name, image_url in categories:
        cursor.execute("SELECT id FROM product_categories WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            category_map[name] = result[0]
            cursor.execute("UPDATE product_categories SET image_url = ? WHERE id = ?", (image_url, result[0]))
        else:
            cursor.execute("INSERT INTO product_categories (name, image_url) VALUES (?, ?)", (name, image_url))
            category_map[name] = cursor.lastrowid
    conn.commit()

    # 2. Atribute per categorie (exemple generice pentru test)
    attributes = {
        'Procesoare (CPU)': ['Frecvență', 'Număr nuclee', 'Socket', 'Cache', 'Proces de fabricație', 'TDP', 'Suport memorie'],
        'Plăci de bază (Motherboard)': ['Socket', 'Format', 'Chipset', 'Sloturi RAM', 'Sloturi PCIe', 'Porturi SATA', 'Porturi USB', 'Audio'],
        'Plăci video (GPU)': ['Memorie', 'Tip memorie', 'Producător', 'Frecvență GPU', 'Frecvență memorie', 'TDP', 'Porturi', 'Lungime'],
        'Memorie RAM': ['Capacitate', 'Frecvență', 'Tip memorie', 'Latency', 'Voltaj', 'Format', 'Compatibilitate'],
        'SSD / HDD': ['Capacitate', 'Tip', 'Interfață', 'Viteză citire', 'Viteză scriere', 'TBW', 'Garantie'],
        'Carcase PC': ['Format', 'Culoare', 'Material', 'Dimensiuni', 'Sloturi', 'Ventilatoare incluse', 'Filtre praf'],
        'Surse de alimentare (PSU)': ['Putere', 'Certificare', 'Modularitate', 'Eficiență', 'Conectoare', 'Garantie'],
        'Sisteme de răcire': ['Tip', 'Compatibilitate', 'Dimensiuni', 'Ventilatoare', 'Zgomot', 'Performanță'],
        'Plăci de sunet': ['Canale', 'Interfață', 'Frecvență', 'Bit depth', 'SNR', 'Compatibilitate'],
        'Monitoare': ['Diagonală', 'Rezoluție', 'Tip panou', 'Frecvență', 'Timp răspuns', 'Contrast', 'Luminozitate', 'Porturi'],
        'Tastaturi': ['Tip', 'Iluminare', 'Layout', 'Conexiune', 'Compatibilitate', 'Material', 'Switch-uri'],
        'Mouse-uri': ['DPI', 'Tip conexiune', 'Nr. butoane', 'Sensor', 'Accelerație', 'Polling rate', 'Greutate'],
        'Căști / Headset-uri': ['Tip', 'Microfon', 'Conexiune', 'Impedanță', 'Frecvență', 'Zgomot', 'Compatibilitate'],
        'Boxe': ['Putere', 'Număr boxe', 'Frecvență', 'Impedanță', 'Conexiune', 'Material'],
        'Webcam-uri': ['Rezoluție', 'Microfon integrat', 'FPS', 'Câmp vizual', 'Conexiune', 'Compatibilitate'],
        'Microfoane': ['Tip', 'Conexiune', 'Polaritate', 'Frecvență', 'Sensibilitate', 'Compatibilitate'],
        'Mousepad-uri': ['Dimensiune', 'Material', 'Grosime', 'Textură', 'Compatibilitate'],
        'Cabluri și adaptoare': ['Tip', 'Lungime', 'Material', 'Compatibilitate', 'Calitate'],
        'Standuri / Suporturi': ['Compatibilitate', 'Material', 'Dimensiuni', 'Ajustări', 'Greutate maximă'],
        'Iluminare RGB': ['Tip', 'Compatibilitate', 'Culori', 'Control', 'Putere', 'Dimensiuni'],
        'Controlere ventilatoare': ['Număr canale', 'Compatibilitate', 'Control', 'Putere', 'Conexiune'],
        'Laptopuri': ['Procesor', 'RAM', 'Stocare', 'Ecran', 'Placă video', 'Baterie', 'Greutate', 'Porturi'],
        'Sisteme PC preconfigurate': ['Procesor', 'RAM', 'Stocare', 'Placă video', 'Sursă', 'Carcasă', 'Sistem operare'],
        'Routere': ['Viteză', 'Standard Wi-Fi', 'Antene', 'Porturi', 'Securitate', 'Acoperire'],
        'Plăci de rețea': ['Tip', 'Viteză', 'Porturi', 'Compatibilitate', 'Conexiune'],
        'Adaptoare Wi-Fi': ['Standard', 'Viteză', 'Antene', 'Compatibilitate', 'Conexiune'],
        'Cabluri de rețea': ['Lungime', 'Categorie', 'Material', 'Compatibilitate', 'Calitate'],
        'Licențe Windows / Office': ['Tip licență', 'Valabilitate', 'Versiune', 'Compatibilitate', 'Suport'],
        'Software antivirus': ['Producător', 'Valabilitate', 'Versiune', 'Compatibilitate', 'Funcții'],
        'Licențe pentru jocuri și platforme': ['Platformă', 'Tip joc', 'Valabilitate', 'Compatibilitate'],
        'Console': ['Producător', 'Capacitate stocare', 'Versiune', 'Compatibilitate', 'Accesorii incluse'],
        'Controller-e': ['Compatibilitate', 'Tip conexiune', 'Baterie', 'Compatibilitate', 'Funcții'],
        'Accesorii gaming': ['Tip', 'Compatibilitate', 'Material', 'Dimensiuni', 'Funcții'],
        'Scaune și birouri de gaming': ['Tip', 'Material', 'Dimensiuni', 'Greutate maximă', 'Ajustări', 'Compatibilitate']
    }

    for cat, attr_list in attributes.items():
        cat_id = category_map[cat]
        for attr in attr_list:
            cursor.execute('''
                SELECT id FROM attributes WHERE name = ? AND category_id = ?
            ''', (attr, cat_id))
            if cursor.fetchone() is None:
                cursor.execute(
                    "INSERT INTO attributes (name, category_id) VALUES (?, ?)",
                    (attr, cat_id)
                )
    conn.commit()

    # 3. Utilizatori (se adaugă de fiecare dată)
    for _ in range(5):
        username = faker.unique.user_name()
        email = faker.unique.email()
        password_hash = faker.password()  # Simulăm hash-ul
        first_name = faker.first_name()
        last_name = faker.last_name()
        phone = faker.phone_number()
        address = faker.address().replace("\n", ", ")
        city = faker.city()

        cursor.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password_hash, first_name, last_name, phone, address, city))
    conn.commit()

    # 4. Produse
    products = []
    for cat_name in categories:
        for _ in range(4):  # 4 produse de test per categorie
            name = f"{cat_name} {faker.word().capitalize()}"
            price = round(random.uniform(50, 8000), 2)
            stock = random.randint(1, 50)
            image_url = PRODUCT_IMAGE_URL
            category_id = category_map[cat_name]
            cursor.execute('''
                INSERT INTO products (name, price, stock, image_url, category_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, price, stock, image_url, category_id))
            products.append(cursor.lastrowid)
    conn.commit()

    # 5. Atribute produse (doar pentru cele noi inserate)
    cursor.execute("SELECT id, name, category_id FROM attributes")
    attributes_all = cursor.fetchall()

    for prod_id in products:
        cursor.execute("SELECT category_id FROM products WHERE id = ?", (prod_id,))
        (cat_id,) = cursor.fetchone()

        for attr_id, attr_name, attr_cat_id in attributes_all:
            if attr_cat_id == cat_id:
                fake_value = faker.word().capitalize()
                cursor.execute('''
                    INSERT INTO product_attributes (product_id, attribute_id, value)
                    VALUES (?, ?, ?)
                ''', (prod_id, attr_id, fake_value))
    conn.commit()

    # 6. Coșuri (pentru userii existenți)
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]

    for user_id in user_ids[-5:]:  # doar pentru userii noi generați (ultimii 5)
        prod_id = random.choice(products)
        cursor.execute("SELECT name, price FROM products WHERE id = ?", (prod_id,))
        product_name, product_price = cursor.fetchone()
        
        cursor.execute('''
            INSERT INTO user_carts (user_id, product_name, product_price, quantity)
            VALUES (?, ?, ?, ?)
        ''', (user_id, product_name, str(product_price), random.randint(1, 3)))
    conn.commit()

    # 7. Comenzi + 8. Produse în comenzi (comentat pentru a evita problemele cu schema)
    # for user_id in user_ids[-5:]:
    #     if random.choice([True, False]):
    #         total_amount = round(random.uniform(100, 5000), 2)
    #         payment_method = random.choice(['Card', 'Cash', 'Transfer'])
    #         shipping_address = faker.address().replace("\n", ", ")
    #         city = faker.city()
    #         phone = faker.phone_number()

    #         cursor.execute('''
    #             INSERT INTO orders (user_id, total_amount, payment_method, shipping_address, city, phone)
    #             VALUES (?, ?, ?, ?, ?, ?)
    #         ''', (user_id, total_amount, payment_method, shipping_address, city, phone))
    #         order_id = cursor.lastrowid

    #         for _ in range(random.randint(1, 2)):
    #             prod_id = random.choice(products)
    #             cursor.execute("SELECT name, price FROM products WHERE id = ?", (prod_id,))
    #             product_name, product_price = cursor.fetchone()
    #             quantity = random.randint(1, 2)
                
    #             cursor.execute('''
    #                 INSERT INTO order_items (order_id, product_name, product_price, quantity)
    #                 VALUES (?, ?, ?, ?)
    #             ''', (order_id, product_name, str(product_price), quantity))
    # conn.commit()
    conn.close()
    print("✅ Date generate cu succes. URL-urile de test sunt acum fixe.")

if __name__ == "__main__":
    insert_sample_data()