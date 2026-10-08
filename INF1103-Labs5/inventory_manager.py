import json
import os

FILENAME = "inventory.json"

DEFAULT_inventory = {
    "P001": {"name": "Laptop", "price": 1200.00, "stock": 0},
    "P002": {"name": "Mouse", "price": 25.50, "stock": 0},
    "P003": {"name": "Keyboard", "price": 45.00, "stock": 0},
    "P004": {"name": "Monitor", "price": 299.99, "stock": 0},
}

LINE = "-" * 50

def load_inventory():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                inventory = json.load(file)
                print("Inventory loaded successfully.")
                return inventory
        except json.JSONDecodeError:
            print(f"{FILENAME} is not a valid JSON file. Starting with default inventory.")
    else:
        print(f"{FILENAME} not found. Starting with default inventory.")
    return {product_id: dict(item) for product_id, item in DEFAULT_inventory.items()}

def save_inventory(inventory, filename=FILENAME):
    with open(filename, "w") as file:
        json.dump(inventory, file, indent=4)

def display_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

def display_products(inventory):
    print("\nCurrent Inventory")
    print(LINE)
    for product_id, item in inventory.items():
        print(f"ID: {product_id} | Name: {item['name']} | "
              f"Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print(LINE)

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

def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id in inventory:
        print("Product ID already exists.")
        return
    name = input("Product Name: ").strip()
    price = read_input("Price: ", float)
    stock = read_input("Stock Quantity: ", int)
    inventory[product_id] = {"name": name, "price": price, "stock": stock}
    print("\nProduct added successfully!")

def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    item = inventory.get(product_id)
    if item is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {item['name']}")
    print(f"Current Stock: {item['stock']}")
    item["stock"] = read_input("\nNew Stock Quantity: ", int)
    print("\nStock updated successfully!")

def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    item = inventory.get(product_id)
    if item is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    print(f"ID: {product_id}")
    print(f"Name: {item['name']}")
    print(f"Price: ${item['price']:.2f}")
    print(f"Stock: {item['stock']}")
    print(LINE)

#Main Code
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
            display_products(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
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