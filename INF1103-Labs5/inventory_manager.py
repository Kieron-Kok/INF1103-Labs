import json

def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            product_list = json.load(file)
            return json.loads(json.dumps(product_list))
    except FileNotFoundError:
        return 0, 0, 0, 0

def save_inventory(id, name, price, quantity):
    product_list={
        "id": id,
        "name": name,
        "price": price,
        "quantity": quantity
    }
    with open("inventory.json", "w") as file:
        json.dump(product_list, file)

product_list = [
    {
        "id": "P001",
        "name": "Laptop",
        "price": 1200.00,
        "quantity": 0
    },
    {
        "id": "P002",
        "name": "Mouse",
        "price": 25.50,
        "quantity": 0
    },
    {
        "id": "P003",
        "name": "Keyboard",
        "price": 45.00,
        "quantity": 0
    },
    {
        "id": "P004",
        "name": "Monitor",
        "price": 299.99,
        "quantity": 0
    }
]

#Main Code

print("===============================")
print("Inventory Management System")
print("===============================")

product_list = load_inventory()
print(f"Loaded Inventory: {product_list}")

while True:

    if load_inventory() is None:
        print("inventory.json not found.")
        save_inventory("P001", "Laptop", 1200.00, 0)
        save_inventory("P002", "Mouse", 25.50, 0)
        save_inventory("P003", "Keyboard", 45.00, 0)
        save_inventory("P004", "Monitor", 299.99, 0)
        product_list = load_inventory()
        print(f"Initialized Inventory: {product_list}")

    user_input = input("Enter Option: ").strip()

    if user_input.lower() == "quit":
        print("Exiting the Inventory Management System.")
        break
    
    if user_input.lstrip('-').isdigit():
         quantity=int(user_input)
         if quantity < 0:
            print("Error: Negative numbers are not allowed.")

    with open("inventory.json", "w") as f:
        json.dump(product_list, f)