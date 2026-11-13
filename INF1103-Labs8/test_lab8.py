from supplier import Supplier
from products import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory

# ---------- Section 2: Association (Supplier and Product) ----------
print("=== Test 1: Association - Supplier and Product ===")
supplier = Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.5)
software = DigitalProduct("D001", "Antivirus Software", 49.99, 100, supplier, 850.0)

laptop.supplier.display_information()
software.supplier.display_information()
print(f"Supplier and laptop are separate objects? {supplier is not laptop}")
print(f"Both products share the same Supplier object? {laptop.supplier is software.supplier}")

del supplier   # Predict first: can the products still show their supplier?
print("After 'del supplier':")
laptop.supplier.display_information()
software.supplier.display_information()