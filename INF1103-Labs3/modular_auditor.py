inventory = 0
delivery_processed = 0
failed_entries = 0
delivery_tax = 1.5

def get_valid_input():
    """Prompt once. Return an int (>=0), "quit," or "invalid"."""
    user_input=input("Enter stock quantity ( or 'quit' to finish): ").strip()

    if user_input() == "quit":
        return "quit"

    if user_input.lstrip('-').isdigit():
        quantity = int(user_input)
        if quantity<0:
            print("Error: Negative numbers are not allowed.")
            return "invalid"
        return quantity

    print("Error: Please enter a valid number")
    return "invalid"

while True:
    user_input = input("Enter stock quantity ( or 'quit' to finish): ")

    if user_input == "quit":
        break

    if user_input.lstrip('-').isdigit():
        quantity = int(user_input)
        if quantity < 0:
            print("Error: Negative numbers are not allowed")
            failed_entries += 1
        else:
            inventory = inventory + quantity
            print(f"You Entered: {quantity}. Total inventory: {inventory}")
            delivery_processed += 1
            if inventory > 500:
                print("OVERSTOCK!, Total inventory has exceeded 500 units.")
                break

    else:
        print("Error: please enter a valid number.")
        failed_entries += 1

print(f"Total Units Processed: {inventory}")
print(f"Total Deliveries: {delivery_processed}")
print(f"Total Delivery Amount: ${delivery_processed*delivery_tax}")
print(f"Number of Failed entries: {failed_entries}")