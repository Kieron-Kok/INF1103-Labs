inventory = 0
delivery_processed = 0
failed_entries = 0
delivery_tax = 0.1
total_tax = 0

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
            if inventory > 500:
                print("OVERSTOCK!, Total inventory has exceeded 500 units.")
                break

print(f"Total Units Processed: {inventory}")
print(f"Total Deliveries: {delivery_processed}")
print(f"Total Delivery Amount: ${total_tax:.2f}")
print(f"Number of Failed entries: {failed_entries}")