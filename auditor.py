inventory = 0
failed_entries = 0

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

            if inventory > 500:
                print("OVERSTOCK!, Total inventory has exceeded 500 units.")
                break

    else:
        print("Error: please enter a valid number.")
        failed_entries += 1

print(f"Total Units Processed: {inventory}")
print(f"Number of Failed entries: {failed_entries}")