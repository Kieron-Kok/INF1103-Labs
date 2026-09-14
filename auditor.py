inventory = 0

while True:
    user_input = input("Enter stock quantity ( or 'quit' to finish): ")

    if user_input == "quit":
        break

    if user_input.lstrip('-').isdigit():
        quantity = int(user_input)
        if quantity < 0:
            print("Error: Negative numbers are not allowed")
        else:
            inventory = inventory + quantity
            print(f"You Entered: {quantity}. Total inventory: {inventory}")

    else:
        print("Error: please enter a valid number.")