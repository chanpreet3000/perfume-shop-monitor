import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import Logger
from Logger import Logger


class ScrapedProduct:
    def __init__(self, average_rating: int, code: str, image: str, brand: str, name: str,
                 price: float, formatted_price: str, promotions, is_in_stock: bool,
                 default_sku: str, url: str):
        self.average_rating = average_rating
        self.code = code
        self.image = image
        self.brand = brand
        self.name = name
        self.price = price
        self.formatted_price = formatted_price
        self.promotions = promotions
        self.is_in_stock = is_in_stock
        self.default_sku = default_sku
        self.url = url

    def __repr__(self):
        return (f"ScrapedProduct({self.code}, {self.name}, {self.price}, "
                f"{self.formatted_price}, {self.is_in_stock}, {self.url}, {self.brand}, "
                f"{self.image}, {self.average_rating}, {self.promotions}, {self.default_sku})")


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'occ-personalization-id': 'cf7088c4-b393-41b1-94d4-0ad108d5fb72',
    'occ-personalization-time': '1728113833620',
    'origin': 'https://www.theperfumeshop.com',
    'priority': 'u=1, i',
    'referer': 'https://www.theperfumeshop.com/',
    'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'x-anonymous-consents': '%5B%5D',
}

base_url = 'https://api.theperfumeshop.com/api/v2/tpsgb/search'


def fetch_products(category_code, page):
    params = {
        'fields': 'FULL',
        'searchType': 'PRODUCT',
        'categoryCode': category_code,
        'currentPage': page,
        'lang': 'en_GB',
        'curr': 'GBP',
        'pageSize': 200
    }

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        Logger.warn(f"Error fetching page {page} for category {category_code}: {response.status_code}")
        return None


def process_category(category_code):
    all_products = []
    page = 0
    total_pages = 1

    while page < total_pages:
        data = fetch_products(category_code, page)
        if data and 'products' in data:
            all_products.extend(data['products'])
            total_pages = data['pagination']['totalPages']
            page += 1
            Logger.info(f'Fetched page {page}/{total_pages} for category {category_code}')
        else:
            break
        time.sleep(1)

    return all_products


def scrape_products(links: set[str]) -> list[ScrapedProduct]:
    categories = [link.split('/')[-1] for link in links]
    all_products = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_category = {executor.submit(process_category, category): category for category in categories}
        for future in as_completed(future_to_category):
            category = future_to_category[future]
            try:
                products = future.result()
                all_products.extend(products)
                Logger.info(f"Completed fetching all products for category {category}")
            except Exception as exc:
                Logger.error(f"Category {category} generated an exception", exc)

    Logger.info(f'Total products fetched: {len(all_products)}')

    return transform_scraped_products(all_products)


def transform_scraped_products(products: list[dict]) -> list[ScrapedProduct]:
    Logger.info("Started Transforming scraped products")
    scraped_products = []
    for product in products:
        average_rating = product.get('averageRating', 0)
        code = product.get('code', 'N/A')
        image = f"https://media.theperfumeshop.com/medias{product.get('images')[0]['url']}"
        brand = product.get('masterBrand', {}).get('name', '')
        name = product.get('name', 'N/A')
        promotions = product.get('promotions', [])
        is_in_stock = product.get('stock', {}).get('stockLevelStatus', 'N/A') != 'outOfStock'
        default_sku = product.get('defaultSku', 'N/A')
        url = f"https://www.theperfumeshop.com{product.get('url', '')}"
        price_data = product.get('price', {})
        price = price_data.get('value', -1)
        formatted_price = price_data.get('formattedValue', 'N/A')

        scraped_product = ScrapedProduct(
            average_rating, code, image, brand, name,
            price, formatted_price, promotions, is_in_stock,
            default_sku, url
        )
        scraped_products.append(scraped_product)
    Logger.info("Finished Transforming scraped products")
    return scraped_products
