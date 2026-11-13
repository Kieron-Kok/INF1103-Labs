from products import Product

class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        return list(self.__products)   # a copy, so outside code can't change the real list

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.product_id) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)   # removes the reference only, the product still exists
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 50)
        for product in self.__products:
            product.display_information()
        print("-" * 50)

    def to_dict(self) -> dict:
        return {product.product_id: product.dict() for product in self.__products}