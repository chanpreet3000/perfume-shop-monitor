class ScrapedProduct:
    def __init__(self, uid, average_rating: int, product_code: str, brand: str, name: str,
                 price: float, formatted_price: str, promotions, is_in_stock: bool,
                 default_sku: str, url: str, latest_price: float, variant_code: str, variant_info: str):
        self.uid = uid
        self.average_rating = average_rating
        self.product_code = product_code
        self.brand = brand
        self.name = name
        self.price = price
        self.formatted_price = formatted_price
        self.promotions = promotions
        self.is_in_stock = is_in_stock
        self.default_sku = default_sku
        self.url = url
        self.latest_price = latest_price
        self.variant_code = variant_code
        self.variant_info = variant_info

    def __repr__(self):
        return f"ScrapedProduct({self.uid}, {self.average_rating}, {self.product_code}, {self.brand}, {self.name}, {self.price}, {self.formatted_price}, {self.promotions}, {self.is_in_stock}, {self.default_sku}, {self.url}, {self.latest_price}, {self.variant_code}, {self.variant_info})"
