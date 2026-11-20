import json
import os
from typing import TypeVar
from products import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory
from can_be_shipped import CanBeShipped
from supplier import Supplier

FILENAME = "inventory.json"
LINE = "-" * 50
Number = TypeVar("Number", int, float)

def create_default_inventory() -> Inventory:
    tech_supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example")
    soft_supplier = Supplier("S002", "SoftHub", "support@softhub.example")

    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P001", "Laptop", 1200.00, 15, tech_supplier, 2.5))
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, tech_supplier, 0.1))
    inventory.add_product(PhysicalProduct("P003", "Keyboard", 45.00, 25, tech_supplier, 0.8))
    inventory.add_product(PhysicalProduct("P004", "Monitor", 299.99, 10, tech_supplier, 5.0))
    inventory.add_product(DigitalProduct("D001", "Antivirus Software", 49.99, 100, soft_supplier, 850.0))
    return inventory

def get_supplier(data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    # Reuse the same Supplier object when several products share one supplier
    supplier_id = data["supplier_id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, data["name"], data["contact_email"])
    return suppliers[supplier_id]

def create_product_from_dict(product_id: str, item: dict,
                             suppliers: dict[str, Supplier]) -> Product:
    supplier = get_supplier(item["supplier"], suppliers)
    if item["type"] == "physical":
        return PhysicalProduct(product_id, item["name"], item["price"],
                               item["stock"], supplier, item["weight"])
    if item["type"] == "digital":
        return DigitalProduct(product_id, item["name"], item["price"],
                              item["stock"], supplier, item["download_size"])
    raise ValueError(f"Unknown product type: {item['type']}")

def load_inventory() -> Inventory:
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
            inventory = Inventory()
            suppliers: dict[str, Supplier] = {}
            for product_id, item in data.items():
                inventory.add_product(create_product_from_dict(product_id, item, suppliers))
            print("Inventory loaded successfully.")
            return inventory
        except (json.JSONDecodeError, KeyError, ValueError):
            print(f"{FILENAME} is invalid. Starting with default inventory.")
    else:
        print(f"{FILENAME} not found. Starting with default inventory.")
    return create_default_inventory()

def save_inventory(inventory: Inventory, filename: str = FILENAME) -> None:
    with open(filename, "w") as file:
        json.dump(inventory.to_dict(), file, indent=4)

def read_input(prompt: str, cast: type[Number]) -> Number:
    while True:
        try:
            value = cast(input(prompt))
            if value < 0:
                print("Value cannot be negative. Try again.")
                continue
            return value
        except ValueError:
            print("Invalid number. Try again.")

def ask_for_supplier(inventory: Inventory) -> Supplier:
    supplier_id = input("Supplier ID: ").strip().upper()
    for product in inventory.products:
        if product.supplier.supplier_id == supplier_id:
            print(f"Using existing supplier: {product.supplier.name}")
            return product.supplier
    name = input("Supplier Name: ").strip()
    contact_email = input("Supplier Email: ").strip()
    return Supplier(supplier_id, name, contact_email)

def add_product_menu(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose product type (1-2): ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = input("Product ID: ").strip().upper()
    name = input("Product Name: ").strip()
    price = read_input("Price: ", float)
    stock = read_input("Stock Quantity: ", int)
    supplier = ask_for_supplier(inventory)
    product: Product

    if product_type == "1":
        weight = read_input("Weight (kg): ", float)
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = read_input("Download Size (MB): ", float)
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)

    if inventory.add_product(product):
        print("\nProduct added successfully!")
    else:
        print("Product ID already exists.")

def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")
    product.update_stock(read_input("\nNew Stock Quantity: ", int))
    print("\nStock updated successfully!")

def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip().upper()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    product.display_information()
    product.supplier.display_information()
    print(product.get_fulfilment_info())
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print(LINE)

def display_menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

def main() -> None:
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