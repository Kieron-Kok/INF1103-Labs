class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def stock(self):
        return self.__stock

    def update_stock(self, new_stock):
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = new_stock

    def display_info(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def dict(self):
        return {
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }