from products import PhysicalProduct, DigitalProduct

print("=== Test 1: PhysicalProduct ===")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.5)
laptop.display_information()

print("\n=== Test 2: DigitalProduct ===")
software = DigitalProduct("D001", "Antivirus Software", 49.99, 100, 850.0)
software.display_information()