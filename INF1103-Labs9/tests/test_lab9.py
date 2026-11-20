import inspect
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Let the tests import the project files from the folder above
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from discount import (DiscountStrategy, NoDiscount, PercentageDiscount,
                      BulkDiscount, StudentDiscount)
from inventory import Inventory
from main import get_positive_float, load_products
from order import Order, OrderLine
from product_factory import ProductFactory
from products import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


def make_supplier() -> Supplier:
    return Supplier("S001", "TechWorld Pte Ltd", "sales@techworld.example")


def make_order_of_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = make_supplier()
    lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 50.00, 10, supplier, 1.0)
    editor = ProductFactory.create("digital", "D001", "Photo Editor", 75.00, 100, supplier, 500.0)
    order = Order("O001", discount)
    order.add_order_line(lamp, 2)     # 100
    order.add_order_line(editor, 2)   # 150  -> total 250
    return order


class TestDiscountStrategy(unittest.TestCase):
    def test_default_is_no_discount(self):
        order = make_order_of_250()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertAlmostEqual(order.calculate_total(), 250.00)

    def test_bulk_discount(self):
        order = make_order_of_250(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.00)

    def test_bulk_discount_below_threshold(self):
        self.assertAlmostEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_set_discount_changes_strategy(self):
        order = make_order_of_250(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.00)

    def test_new_strategy_works_without_changing_order(self):
        order = make_order_of_250(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.50)

    def test_order_has_no_discount_if_elif(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("if", source)

    def test_cannot_create_abstract_strategy(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()


class TestProductFactory(unittest.TestCase):
    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, make_supplier(), 1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100, make_supplier(), 300.0)
        self.assertIsInstance(product, DigitalProduct)

    def test_unknown_type_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, make_supplier())
        self.assertIn("Unknown product type: service", str(context.exception))

    def test_main_does_not_create_products_directly(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "main.py")) as file:
            source = file.read()
        self.assertNotIn("PhysicalProduct(", source)
        self.assertNotIn("DigitalProduct(", source)


class TestValidation(unittest.TestCase):
    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -5):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P001", "Lamp", bad_price, 10, make_supplier())

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", 10.0, -1, make_supplier())

    def test_zero_stock_is_allowed(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 10.0, 0, make_supplier())
        self.assertEqual(product.stock, 0)

    def test_update_stock_cannot_be_negative(self):
        product = ProductFactory.create("digital", "D001", "Editor", 10.0, 5, make_supplier())
        with self.assertRaises(ValueError):
            product.update_stock(-1)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 10.0, 5, make_supplier())
        for bad_quantity in (0, -2):
            with self.assertRaises(ValueError):
                OrderLine(product, bad_quantity)


class TestUserInput(unittest.TestCase):
    def test_get_positive_float_asks_again(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), \
             patch("sys.stdout", new_callable=io.StringIO) as output:
            value = get_positive_float("Price: ")
        self.assertEqual(value, 12.50)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])


class TestLoadProducts(unittest.TestCase):
    CSV_TEXT = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,P001,Desk Lamp,25.00,10\n"
                "digital,D001,Photo Editor,49.90,100\n"
                "service,S001,Installation,30.00,5\n"
                "physical,P002,Office Chair,abc,3\n"
                "physical,P003,Monitor Stand,39.50,7\n")

    def run_load(self, path: str) -> tuple[Inventory, list[str]]:
        inventory = Inventory()
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            load_products(path, inventory, make_supplier())
        return inventory, output.getvalue().splitlines()

    def test_bad_rows_skipped_and_valid_rows_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as file:
                file.write(self.CSV_TEXT)
            inventory, lines = self.run_load(path)

        self.assertEqual([p.product_id for p in inventory.products], ["P001", "D001", "P003"])
        self.assertIn("Unknown product type: service", lines[0])
        self.assertIn("could not convert string to float: 'abc'", lines[1])
        self.assertEqual(lines[2], "3 products loaded.")
        self.assertEqual(lines[3], "Load attempt finished.")

    def test_missing_file_handled_gracefully(self):
        inventory, lines = self.run_load("does_not_exist.csv")
        self.assertEqual(inventory.products, [])
        self.assertEqual(lines, ["Products file not found: does_not_exist.csv",
                                 "Load attempt finished."])


if __name__ == "__main__":
    unittest.main()