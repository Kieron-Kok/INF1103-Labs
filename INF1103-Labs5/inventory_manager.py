import json
import os

FILENAME = "inventory.json"

DEFAULT_PRODUCT_LIST = {
    "P001": {"name": "Laptop", "price": 1200.00, "stock": 0},
    "P002": {"name": "Mouse", "price": 25.50, "stock": 0},
    "P003": {"name": "Keyboard", "price": 45.00, "stock": 0},
    "P004": {"name": "Monitor", "price": 299.99, "stock": 0},
}

def load_inventory():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                product_list = json.load(file)
                print("Inventory loaded successfully.")
                return product_list
        except json.JSONDecodeError:
            print(f"{FILENAME} is not a valid JSON file. Starting with default inventory.")
    else:
        print(f"{FILENAME} not found. Starting with default inventory.")
    return {product_id: dict(item) for product_id, item in DEFAULT_PRODUCT_LIST.items()}

def save_inventory(product_list, filename=FILENAME):
    with open(filename, "w") as file:
        json.dump(product_list, file, indent=4)

def display_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

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

#Main Code
def main():
    print("================================")
    print("Welcome to the Inventory Management System")
    print("================================")
    print()

    product_list = load_inventory()
    print()
    display_menu()

product_list = load_inventory()
print(f"Loaded Inventory: {product_list}")

while True:
    user_input = input("Enter Option: ").strip()

    if user_input.lower() == "quit":
        print("Exiting the Inventory Management System.")
        break
    
    if user_input.lstrip('-').isdigit():
         quantity=int(user_input)
         if quantity < 0:
            print("Error: Negative numbers are not allowed.")
