import sqlite3
import hashlib
import secrets
import sqlite3

def get_connection():
    return sqlite3.connect('store.db')

def hash_password(password):
    """Hash-ul parolei cu salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def create_demo_user():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verifică dacă utilizatorul demo există deja
    cursor.execute('SELECT id FROM users WHERE username = ?', ('demo',))
    if cursor.fetchone():
        print("Utilizatorul demo există deja!")
        conn.close()
        return
    
    # Creează utilizatorul demo
    password_hash = hash_password('demo123')
    cursor.execute('''
        INSERT INTO users (username, email, password_hash, first_name, last_name, phone, address, city)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('demo', 'demo@example.com', password_hash, 'Demo', 'User', '+37312345678', 'Strada Demo 123', 'Chișinău'))
    
    conn.commit()
    conn.close()
    print("Utilizatorul demo a fost creat cu succes!")
    print("Username: demo")
    print("Parolă: demo123")

if __name__ == "__main__":
    create_demo_user() 