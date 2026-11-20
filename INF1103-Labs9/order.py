from products import Product
from discount import DiscountStrategy, NoDiscount


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.name} x {self.__quantity} "
              f"@ ${self.__product.price:.2f} = ${self.calculate_subtotal():.2f}")


class Order:
    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    @property
    def order_id(self) -> str:
        return self.__order_id

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)   # the Order creates its own OrderLine
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.product.product_id == product_id:
                self.__order_lines.remove(order_line)
                return True
        return False

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 50)
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 50)
        print(f"Total: ${self.calculate_total():.2f}")