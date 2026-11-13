from products import Product, PhysicalProduct, DigitalProduct
from can_be_shipped import CanBeShipped

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

print("\n=== Test 5: Shipping cost for different weights ===")
mouse = PhysicalProduct("P002", "Mouse", 25.50, 40, 0.1)
monitor = PhysicalProduct("P004", "Monitor", 299.99, 10, 5.0)
for item in (mouse, laptop, monitor):
    print(f"{item.name} ({item.weight} kg): ${item.calculate_shipping_cost():.2f}")

print("\n=== Test 6: Digital product does not need shipping ===")
print(f"Laptop can be shipped? {isinstance(laptop, CanBeShipped)}")
print(f"Software can be shipped? {isinstance(software, CanBeShipped)}")