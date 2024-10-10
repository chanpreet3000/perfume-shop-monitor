import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from Logger import Logger
from ScrapedProduct import ScrapedProduct
from network import fetch_with_proxy, get_proxies_from_webshare


def fetch_products(proxies, category_code, page):
    params = {
        'fields': 'FULL',
        'searchType': 'PRODUCT',
        'categoryCode': category_code,
        'currentPage': page,
        'lang': 'en_GB',
        'curr': 'GBP',
        'pageSize': 200
    }

    response = fetch_with_proxy(proxies, 'https://api.theperfumeshop.com/api/v2/tpsgb/search', method='GET',
                                params=params, timeout=20, max_retries=5)
    if response.status_code == 200:
        return response.json()
    else:
        Logger.warn(f"Error fetching page {page} for category {category_code}: {response.status_code}", response)
        return None


def process_category(proxies, category_code):
    all_products = []
    page = 0
    total_pages = 1

    while page < total_pages:
        data = fetch_products(proxies, category_code, page)
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

    proxies = get_proxies_from_webshare()

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_category = {executor.submit(process_category, proxies, category): category for category in categories}
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
        average_rating = product.get('averageRating', -1)
        product_code = product['code']
        brand = product.get('masterBrand', {}).get('name', '')
        promotions = product.get('promotions', [])
        default_sku = product.get('defaultSku', 'N/A')
        url = f"https://www.theperfumeshop.com{product.get('url', '')}"

        scraped_product = ScrapedProduct(
            "N/A", average_rating, product_code, brand, 'N/A',
            -1, promotions, False,
            default_sku, url, -1, "N/A", "N/A", -1, "N/A")
        scraped_products.append(scraped_product)
    Logger.info("Finished Transforming scraped products")
    return scraped_products
