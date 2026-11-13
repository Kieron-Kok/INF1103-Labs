from supplier import Supplier
from products import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory
from order import Order

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

# ---------- Section 3: Aggregation (Inventory and Product) ----------
print("\n=== Test 2: Aggregation - Inventory and Product ===")
tech_supplier = Supplier("S002", "GadgetCo", "hello@gadgetco.example")
mouse = PhysicalProduct("P002", "Mouse", 25.50, 40, tech_supplier, 0.1)   # created BEFORE any inventory

inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(mouse)
print(f"Mouse in Inventory A? {inventory_a.find_product('P002') is not None}")

inventory_a.remove_product("P002")   # Predict first: does the mouse still work?
print(f"Mouse in Inventory A after removing? {inventory_a.find_product('P002') is not None}")
print("Mouse still works after removal:")
mouse.display_information()

inventory_b.add_product(mouse)
print(f"Mouse in Inventory B? {inventory_b.find_product('P002') is not None}")
print(f"Same Mouse object in B? {inventory_b.find_product('P002') is mouse}")


# ---------- Section 4: Composition (Order and OrderLine) ----------
print("\n=== Test 3: Composition - Order and OrderLine ===")
order_1 = Order("O001")
order_1.add_order_line(laptop, 2)
order_1.add_order_line(software, 3)
order_1.display_order()

order_2 = Order("O002")
order_2.add_order_line(laptop, 1)   # Predict first: how many OrderLines / Products now?

line_in_order_1 = order_1.order_lines[0]
line_in_order_2 = order_2.order_lines[0]
print(f"\nSame OrderLine object in both orders? {line_in_order_1 is line_in_order_2}")
print(f"Same Product object in both order lines? {line_in_order_1.product is line_in_order_2.product}")
print(f"OrderLine ids: {id(line_in_order_1)} vs {id(line_in_order_2)}")
print(f"Product ids:   {id(line_in_order_1.product)} vs {id(line_in_order_2.product)}")

order_1.remove_order_line("D001")
print("\nAfter removing the software line from Order O001:")
order_1.display_order()
print("Software product still exists:")
software.display_information()

# ---------- Section 6 & 7: LSP and Polymorphism ----------
def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


print("\n=== Test 4: LSP - one function works for both product types ===")
show_product_details(laptop)
show_product_details(software)

print("\n=== Test 5: LSP - update_stock() means the same for both ===")
laptop.update_stock(20)
software.update_stock(500)
print(f"Laptop stock: {laptop.stock} | Software stock: {software.stock}")

print("\n=== Test 6: Polymorphism - one loop, no isinstance() ===")
mixed_inventory = Inventory()
mixed_inventory.add_product(laptop)
mixed_inventory.add_product(software)
for product in mixed_inventory.products:   # Predict first: what will each print?
    product.display_information()
    print(product.get_fulfilment_info())