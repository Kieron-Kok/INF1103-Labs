import json

INVENTORY_FILE = "inventory.json"

inventory = 0
delivery_processed = 0
failed_entries = 0
delivery_tax = 0.1
total_tax = 0

def load_inventory():
     try:
         with open(INVENTORY_FILE, "r") as file:
             data = json.load(file)
             return data.get("inventory", 0), int(data.get("delivery_processed", 0)), float(data.get("total_tax", 0))
     except FileNotFoundError:
         return 0,0,0.0
     except (json.JSONDecodeError, ValueError, TypeError, AttributeError):
         print("Error: Inventory file is corrupted. Starting with default values.")
         return 0,0,0.0

def save_inventory(inventory, delivery_processed, total_tax):
    data = {
        "inventory": inventory,
        "delivery_processed": delivery_processed,
        "total_tax": total_tax
    }
    with open(INVENTORY_FILE, "w") as file:
        json.dump({"inventory": inventory, "delivery_processed": delivery_processed, "total_tax": total_tax}, file)

def get_valid_input():
    user_input = input("Enter stock quantity (or 'quit' to finish): ").strip()

    if user_input == "quit":
        return "quit"

    if user_input.lstrip('-').isdigit():
        quantity = int(user_input)
        if quantity<0:
            print("Error: Negative numbers are not allowed.")
            return "invalid"
        return quantity

    print("Error: Please enter a valid number")
    return "invalid"

def process_delivery(current_total,new_value):
    return current_total + new_value

def calculate_tax(amount):
     return amount * delivery_tax

def generate_report(total_deliveries, total_units):
    print(f"Total Units Processed: {total_units}")
    print(f"Total Deliveries: {total_deliveries}")

inventory, delivery_processed, total_tax = load_inventory()
print(f"Loaded Inventory: {inventory}, Deliveries Processed: {delivery_processed}, Total Tax Collected: ${total_tax:.2f}")

while True:
    user_input = get_valid_input()

    if user_input == "quit":
        break
    if user_input == "invalid":
            failed_entries += 1
            continue
    else:
            inventory = process_delivery(inventory, user_input)
            print(f"You Entered: {user_input}. Total inventory: {inventory}")
            tax = calculate_tax(user_input)
            total_tax += tax
            delivery_processed += 1

            save_inventory(inventory, delivery_processed, total_tax)

            if inventory > 500:
                print("OVERSTOCK!, Total inventory has exceeded 500 units.")
                break

generate_report(delivery_processed, inventory)
print(f"Total Tax Collected: ${total_tax:.2f}")