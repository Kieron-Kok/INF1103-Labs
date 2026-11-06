import json
import os
from products import Product
from inventory import Inventory

FILENAME = "inventory.json"
LINE = "-" * 50

def create_default_inventory():
    inventory = Inventory()
    inventory.add_product(Product("P001", "Laptop", 1200.00, 15))
    inventory.add_product(Product("P002", "Mouse", 25.50, 40))
    inventory.add_product(Product("P003", "Keyboard", 45.00, 25))
    inventory.add_product(Product("P004", "Monitor", 299.99, 10))
    return inventory

def load_inventory():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
            inventory = Inventory()
            for product_id, item in data.items():
                inventory.add_product(
                    Product(product_id, item["name"], item["price"], item["stock"])
                )
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, KeyError):
            print(f"{FILENAME} is invalid. Starting with default inventory.")
    else:
        print(f"{FILENAME} not found. Starting with default inventory.")
    return create_default_inventory()

def save_inventory(inventory, filename=FILENAME):
    with open(filename, "w") as file:
        json.dump(inventory.to_dict(), file, indent=4)

def read_input(prompt, cast):
    while True:
        try:
            value = cast(input(prompt))
            if value < 0:
                print("Value cannot be negative. Try again.")
                continue
            return value
        except ValueError:
            print("Invalid number. Try again.")

def add_product_menu(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    name = input("Product Name: ").strip()
    price = read_input("Price: ", float)
    stock = read_input("Stock Quantity: ", int)

    if inventory.add_product(Product(product_id, name, price, stock)):
        print("\nProduct added successfully!")
    else:
        print("Product ID already exists.")

def update_stock_menu(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    product.update_stock(read_input("\nNew Stock Quantity: ", int))
    print("\nStock updated successfully!")

def search_product_menu(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print(LINE)

def display_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

def main():
    print("================================")
    print("Welcome to the Inventory Management System")
    print("================================")
    print()

    inventory = load_inventory()
    print()
    display_menu()

    while True:
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_menu(inventory)
        elif choice == "3":
            update_stock_menu(inventory)
        elif choice == "4":
            search_product_menu(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print(f"Inventory saved successfully to {FILENAME}.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()