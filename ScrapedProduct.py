class ScrapedProduct:
    def __init__(self, uid, average_rating: int, product_code: str, brand: str, name: str,
                 price: float, promotions, is_in_stock: bool,
                 default_sku: str, url: str, latest_price: float, variant_code: str, variant_info: str,
                 stock_level: int, ean: str):
        self.uid = uid
        self.average_rating = average_rating
        self.product_code = product_code
        self.brand = brand
        self.name = name
        self.price = price
        self.promotions = promotions
        self.is_in_stock = is_in_stock
        self.default_sku = default_sku
        self.url = url
        self.latest_price = latest_price
        self.variant_code = variant_code
        self.variant_info = variant_info
        self.stock_level = stock_level
        self.ean = ean

    def __repr__(self):
        return f"ScrapedProduct(uid={self.uid}, average_rating={self.average_rating}, product_code={self.product_code}, " \
               f"brand={self.brand}, name={self.name}, price={self.price}, promotions={self.promotions}, " \
               f"is_in_stock={self.is_in_stock}, default_sku={self.default_sku}, url={self.url}, " \
               f"latest_price={self.latest_price}, variant_code={self.variant_code}, variant_info={self.variant_info}, " \
               f"stock_level={self.stock_level}, ean={self.ean})"
