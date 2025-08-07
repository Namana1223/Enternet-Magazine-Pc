from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime
from db import get_connection

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # În producție, folosește o cheie sigură
CORS(app, supports_credentials=True)

# Funcții helper
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

def get_user_id_from_session():
    """Obține user_id din sesiune"""
    return session.get('user_id')

# Rute pentru autentificare
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        phone = data.get('phone', '')
        address = data.get('address', '')
        city = data.get('city', '')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Toate câmpurile obligatorii trebuie completate'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verifică dacă username-ul sau email-ul există deja
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Username-ul sau email-ul există deja'}), 400
        
        # Hash parola și salvează utilizatorul
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password_hash, first_name, last_name, phone, address, city))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Creează sesiunea
        session['user_id'] = user_id
        session['username'] = username
        
        return jsonify({
            'success': True,
            'message': 'Cont creat cu succes!',
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Eroare la înregistrare: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username și parola sunt obligatorii'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Găsește utilizatorul
        cursor.execute('SELECT id, username, email, password_hash FROM users WHERE username = ? OR email = ?', (username, username))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not verify_password(password, user[3]):
            return jsonify({'error': 'Username sau parolă incorectă'}), 401
        
        # Creează sesiunea
        session['user_id'] = user[0]
        session['username'] = user[1]
        
        return jsonify({
            'success': True,
            'message': 'Autentificare reușită!',
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[2]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Eroare la autentificare: {str(e)}'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Deconectare reușită!'}), 200

@app.route('/api/user', methods=['GET'])
def get_user():
    user_id = get_user_id_from_session()
    if not user_id:
        return jsonify({'error': 'Nu ești autentificat'}), 401
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, email, first_name, last_name, phone, address, city FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Utilizatorul nu a fost găsit'}), 404
        
        return jsonify({
            'user': {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'first_name': user[3],
                'last_name': user[4],
                'phone': user[5],
                'address': user[6],
                'city': user[7]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Eroare la obținerea datelor: {str(e)}'}), 500

# Rute pentru coș
@app.route('/api/cart', methods=['GET'])
def get_cart():
    user_id = get_user_id_from_session()
    if not user_id:
        return jsonify({'error': 'Nu ești autentificat'}), 401
    
    try:
        conn = get_connection()
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
        
        return jsonify({'cart': cart}), 200
        
    except Exception as e:
        return jsonify({'error': f'Eroare la obținerea coșului: {str(e)}'}), 500

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    user_id = get_user_id_from_session()
    if not user_id:
        return jsonify({'error': 'Nu ești autentificat'}), 401
    
    try:
        data = request.get_json()
        product_name = data.get('name')
        product_image = data.get('image', '')
        product_price = data.get('price')
        quantity = data.get('quantity', 1)
        
        if not all([product_name, product_price]):
            return jsonify({'error': 'Numele și prețul produsului sunt obligatorii'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verifică dacă produsul există deja în coș
        cursor.execute('''
            SELECT id, quantity FROM user_carts 
            WHERE user_id = ? AND product_name = ?
        ''', (user_id, product_name))
        
        existing_item = cursor.fetchone()
        
        if existing_item:
            # Actualizează cantitatea
            new_quantity = existing_item[1] + quantity
            cursor.execute('''
                UPDATE user_carts 
                SET quantity = ? 
                WHERE id = ?
            ''', (new_quantity, existing_item[0]))
        else:
            # Adaugă produs nou
            cursor.execute('''
                INSERT INTO user_carts (user_id, product_name, product_image, product_price, quantity)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, product_name, product_image, product_price, quantity))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Produs adăugat în coș!'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Eroare la adăugarea în coș: {str(e)}'}), 500

@app.route('/api/cart/update', methods=['PUT'])
def update_cart_item():
    user_id = get_user_id_from_session()
    if not user_id:
        return jsonify({'error': 'Nu ești autentificat'}), 401
    
    try:
        data = request.get_json()
        product_name = data.get('name')
        quantity = data.get('quantity')
        
        if not product_name or quantity is None:
            return jsonify({'error': 'Numele produsului și cantitatea sunt obligatorii'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        if quantity <= 0:
            # Șterge produsul
            cursor.execute('''
                DELETE FROM user_carts 
                WHERE user_id = ? AND product_name = ?
            ''', (user_id, product_name))
        else:
            # Actualizează cantitatea
            cursor.execute('''
                UPDATE user_carts 
                SET quantity = ? 
                WHERE user_id = ? AND product_name = ?
            ''', (quantity, user_id, product_name))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Coș actualizat!'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Eroare la actualizarea coșului: {str(e)}'}), 500

@app.route('/api/cart/remove', methods=['DELETE'])
def remove_from_cart():
    user_id = get_user_id_from_session()
    if not user_id:
        return jsonify({'error': 'Nu ești autentificat'}), 401
    
    try:
        data = request.get_json()
        product_name = data.get('name')
        
        if not product_name:
            return jsonify({'error': 'Numele produsului este obligatoriu'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM user_carts 
            WHERE user_id = ? AND product_name = ?
        ''', (user_id, product_name))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Produs șters din coș!'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Eroare la ștergerea din coș: {str(e)}'}), 500

@app.route('/api/cart/clear', methods=['DELETE'])
def clear_cart():
    user_id = get_user_id_from_session()
    if not user_id:
        return jsonify({'error': 'Nu ești autentificat'}), 401
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM user_carts WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Coș golit!'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Eroare la golirea coșului: {str(e)}'}), 500

# Rute pentru comenzi
@app.route('/api/orders', methods=['POST'])
def create_order():
    user_id = get_user_id_from_session()
    if not user_id:
        return jsonify({'error': 'Nu ești autentificat'}), 401
    
    try:
        data = request.get_json()
        total_amount = data.get('total_amount')
        payment_method = data.get('payment_method')
        shipping_address = data.get('shipping_address')
        city = data.get('city')
        phone = data.get('phone')
        
        if not all([total_amount, payment_method, shipping_address, city, phone]):
            return jsonify({'error': 'Toate câmpurile sunt obligatorii'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Creează comanda
        cursor.execute('''
            INSERT INTO orders (user_id, total_amount, payment_method, shipping_address, city, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, total_amount, payment_method, shipping_address, city, phone))
        
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
        
        return jsonify({
            'success': True, 
            'message': 'Comanda a fost creată cu succes!',
            'order_id': order_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Eroare la crearea comenzii: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 