inventory = 0

while True:
    inventory = int(input("Stock Quantity: "))
    if inventory == "quit":
        break 
    print("Inventory: ", inventory)