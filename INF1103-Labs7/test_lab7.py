from products import Product, PhysicalProduct, DigitalProduct

print("=== Test 1: PhysicalProduct ===")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5)
laptop.display_information()

print("\n=== Test 2: DigitalProduct ===")
software = DigitalProduct("D001", "Antivirus Software", 49.99, 100, 850.0)
software.display_information()

print("\n=== Test 3: get_fulfilment_info() ===")
print(laptop.get_fulfilment_info())
print(software.get_fulfilment_info())

print("\n=== Test 4: Product cannot be created directly ===")
try:
    Product("X001", "Generic Product", 10.00, 5)
    print("FAIL: a plain Product was created")
except TypeError as error:
    print(f"PASS: {error}")