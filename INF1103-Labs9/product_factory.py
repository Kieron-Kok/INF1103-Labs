from products import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, detail: float = 0.0) -> Product:
        # detail = weight (kg) for physical products, download size (MB) for digital products
        product_type = product_type.strip().lower()
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, detail)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, detail)
        else:
            raise ValueError(f"Unknown product type: {product_type}")