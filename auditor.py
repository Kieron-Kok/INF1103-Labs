inventory = 0

while True:
    user_input = input("Enter stock quantity ( or 'quit' to finish): ")

    if user_input == "quit":
        break

    if user_input.isdigit():
        quantity = int(user_input)
        print(f"You Entered: {quantity}")
    else:
        print("Error: please enter a valid number.")