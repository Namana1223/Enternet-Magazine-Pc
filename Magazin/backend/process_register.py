import json
import os
import sys
from simple_auth import register_user, login_user, save_cart_to_db, load_cart_from_db

def process_registration():
    """Procesează înregistrările din fișierul JSON"""
    try:
        # Verifică dacă există fișierul de înregistrare
        if not os.path.exists('registration_data.json'):
            print("Nu există date de înregistrare.")
            return
        
        # Citește datele din fișier
        with open('registration_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Procesează înregistrarea
        result = register_user(data)
        
        # Salvează rezultatul
        with open('registration_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"Rezultat înregistrare: {result}")
        
        # Șterge fișierul de date după procesare
        os.remove('registration_data.json')
        
    except Exception as e:
        print(f"Eroare la procesarea înregistrării: {e}")
        # Salvează eroarea
        with open('registration_result.json', 'w', encoding='utf-8') as f:
            json.dump({'success': False, 'error': str(e)}, f, ensure_ascii=False, indent=2)

def process_login():
    """Procesează autentificările din fișierul JSON"""
    try:
        # Verifică dacă există fișierul de autentificare
        if not os.path.exists('login_data.json'):
            print("Nu există date de autentificare.")
            return
        
        # Citește datele din fișier
        with open('login_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Procesează autentificarea
        result = login_user(data['username'], data['password'])
        
        # Salvează rezultatul
        with open('login_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"Rezultat autentificare: {result}")
        
        # Șterge fișierul de date după procesare
        os.remove('login_data.json')
        
    except Exception as e:
        print(f"Eroare la procesarea autentificării: {e}")
        # Salvează eroarea
        with open('login_result.json', 'w', encoding='utf-8') as f:
            json.dump({'success': False, 'error': str(e)}, f, ensure_ascii=False, indent=2)

def process_cart_save():
    """Procesează salvarea coșului din fișierul JSON"""
    try:
        # Verifică dacă există fișierul de coș
        if not os.path.exists('cart_save_data.json'):
            print("Nu există date de coș pentru salvare.")
            return
        
        # Citește datele din fișier
        with open('cart_save_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Procesează salvarea coșului
        result = save_cart_to_db(data['user_id'], data['cart'])
        
        # Salvează rezultatul
        with open('cart_save_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"Rezultat salvare coș: {result}")
        
        # Șterge fișierul de date după procesare
        os.remove('cart_save_data.json')
        
    except Exception as e:
        print(f"Eroare la salvarea coșului: {e}")
        # Salvează eroarea
        with open('cart_save_result.json', 'w', encoding='utf-8') as f:
            json.dump({'success': False, 'error': str(e)}, f, ensure_ascii=False, indent=2)

def process_cart_load():
    """Procesează încărcarea coșului din fișierul JSON"""
    try:
        # Verifică dacă există fișierul de încărcare coș
        if not os.path.exists('cart_load_data.json'):
            print("Nu există date pentru încărcarea coșului.")
            return
        
        # Citește datele din fișier
        with open('cart_load_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Procesează încărcarea coșului
        result = load_cart_from_db(data['user_id'])
        
        # Salvează rezultatul
        with open('cart_load_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"Rezultat încărcare coș: {result}")
        
        # Șterge fișierul de date după procesare
        os.remove('cart_load_data.json')
        
    except Exception as e:
        print(f"Eroare la încărcarea coșului: {e}")
        # Salvează eroarea
        with open('cart_load_result.json', 'w', encoding='utf-8') as f:
            json.dump({'success': False, 'error': str(e)}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "register":
            process_registration()
        elif action == "login":
            process_login()
        elif action == "save_cart":
            process_cart_save()
        elif action == "load_cart":
            process_cart_load()
        else:
            print("Acțiuni disponibile: register, login, save_cart, load_cart")
    else:
        print("Folosește: python process_register.py [register|login|save_cart|load_cart]") 