import sqlite3
import hashlib
import secrets
import json
import os

def hash_password(password):
    """Hash-ul parolei cu salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def verify_password(password, hashed_password):
    """Verifică parola"""
    try:
        salt, hash_value = hashed_password.split('$')
        hash_obj = hashlib.sha256((password + salt).encode())
        return hash_obj.hexdigest() == hash_value
    except:
        return False

def register_user(data):
    """Înregistrează un utilizator nou"""
    try:
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        
        # Verifică dacă username-ul sau email-ul există deja
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', 
                      (data['username'], data['email']))
        if cursor.fetchone():
            conn.close()
            return {'success': False, 'error': 'Username-ul sau email-ul există deja'}
        
        # Hash parola și salvează utilizatorul
        password_hash = hash_password(data['password'])
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['username'], data['email'], password_hash, data['first_name'], 
              data['last_name'], data['phone'], data['address'], data['city']))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            'success': True, 
            'message': 'Cont creat cu succes!',
            'user': {
                'id': user_id,
                'username': data['username'],
                'email': data['email']
            }
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Eroare la înregistrare: {str(e)}'}

def login_user(username, password):
    """Autentifică un utilizator"""
    try:
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        
        # Găsește utilizatorul
        cursor.execute('SELECT id, username, email, password_hash FROM users WHERE username = ? OR email = ?', 
                      (username, username))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not verify_password(password, user[3]):
            return {'success': False, 'error': 'Username sau parolă incorectă'}
        
        return {
            'success': True,
            'message': 'Autentificare reușită!',
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[2]
            }
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Eroare la autentificare: {str(e)}'}

def save_cart_to_db(user_id, cart_data):
    """Salvează coșul în baza de date"""
    try:
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        
        # Șterge coșul vechi
        cursor.execute('DELETE FROM user_carts WHERE user_id = ?', (user_id,))
        
        # Adaugă produsele noi
        for item in cart_data:
            cursor.execute('''
                INSERT INTO user_carts (user_id, product_name, product_image, product_price, quantity)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, item['name'], item['image'], item['price'], item['quantity']))
        
        conn.commit()
        conn.close()
        return {'success': True, 'message': 'Coș salvat cu succes!'}
        
    except Exception as e:
        return {'success': False, 'error': f'Eroare la salvarea coșului: {str(e)}'}

def load_cart_from_db(user_id):
    """Încarcă coșul din baza de date"""
    try:
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT product_name, product_image, product_price, quantity 
            FROM user_carts 
            WHERE user_id = ?
        ''', (user_id,))
        
        cart_items = cursor.fetchall()
        conn.close()
        
        cart = []
        for item in cart_items:
            cart.append({
                'name': item[0],
                'image': item[1],
                'price': item[2],
                'quantity': item[3]
            })
        
        return {'success': True, 'cart': cart}
        
    except Exception as e:
        return {'success': False, 'error': f'Eroare la încărcarea coșului: {str(e)}'}

def create_order(user_id, order_data):
    """Creează o comandă nouă"""
    try:
        conn = sqlite3.connect('store.db')
        cursor = conn.cursor()
        
        # Creează comanda
        cursor.execute('''
            INSERT INTO orders (user_id, total_amount, payment_method, shipping_address, city, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, order_data['total_amount'], order_data['payment_method'], 
              order_data['shipping_address'], order_data['city'], order_data['phone']))
        
        order_id = cursor.lastrowid
        
        # Adaugă produsele din coș în comandă
        cursor.execute('''
            SELECT product_name, product_price, quantity 
            FROM user_carts 
            WHERE user_id = ?
        ''', (user_id,))
        
        cart_items = cursor.fetchall()
        
        for item in cart_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_name, product_price, quantity)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item[0], item[1], item[2]))
        
        # Golește coșul
        cursor.execute('DELETE FROM user_carts WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True, 
            'message': 'Comanda a fost creată cu succes!',
            'order_id': order_id
        }
        
    except Exception as e:
        return {'success': False, 'error': f'Eroare la crearea comenzii: {str(e)}'}

if __name__ == "__main__":
    # Test funcționalitate
    print("Sistem de autentificare simplu gata!")
    print("Funcții disponibile:")
    print("- register_user(data)")
    print("- login_user(username, password)")
    print("- save_cart_to_db(user_id, cart_data)")
    print("- load_cart_from_db(user_id)")
    print("- create_order(user_id, order_data)") 