import requests
import time
import Logger
from concurrent.futures import ThreadPoolExecutor, as_completed

from LatestPriceDataManager import LatestPriceDataManager
from Logger import Logger
from ScrapedProduct import ScrapedProduct
from utils import getHeader

latest_price_db = LatestPriceDataManager()

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

    response = requests.get(base_url, params=params, headers=getHeader())
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
        variants = product.get('variantsCode', [])
        for variant in variants:
            id = f"{product['code']}-{variant}"
            average_rating = product.get('averageRating', 0)
            product_code = product['code']
            brand = product.get('masterBrand', {}).get('name', '')
            name = product.get('name', 'N/A')
            promotions = product.get('promotions', [])
            is_in_stock = product.get('stock', {}).get('stockLevelStatus', 'N/A') != 'outOfStock'
            default_sku = product.get('defaultSku', 'N/A')
            url = f"https://www.theperfumeshop.com{product.get('url', '').split('?')[0]}?varSel={variant}" if len(
                variants) > 1 else f"https://www.theperfumeshop.com{product.get('url', '')}"
            price_data = product.get('price', {})
            formatted_price = price_data.get('formattedValue', 'N/A')
            latest_price = latest_price_db.get_value(id)

            scraped_product = ScrapedProduct(
                id, average_rating, product_code, brand, name,
                -1, formatted_price, promotions, is_in_stock,
                default_sku, url, latest_price, variant, "N/A", -1)
            scraped_products.append(scraped_product)
    Logger.info("Finished Transforming scraped products")
    return scraped_products
