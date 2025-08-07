from db import create_tables
from models.product import add_product, get_all_products

def start():
    create_tables()

    #  Exemplu: adăugăm produse doar o dată
    if not get_all_products():
        add_product("Tastatură mecanică", 650.0, 20)
        add_product("Mouse gaming", 350.0, 30)
        add_product("Monitor 144Hz", 2500.0, 15)

    print("Produse existente în magazin:")
    for prod in get_all_products():
        print(f"ID: {prod[0]}, Nume: {prod[1]}, Preț: {prod[2]} MDL, Stoc: {prod[3]}")

if __name__ == "__main__":
    start()
