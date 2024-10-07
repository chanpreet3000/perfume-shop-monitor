import requests
import json
import re
import time
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from Logger import Logger
from ScrapedProduct import ScrapedProduct
from utils import getHeader


def parse_json_ld(html: str) -> Dict:
    soup = BeautifulSoup(html, 'html.parser')
    json_ld_script = soup.find('script', {'id': 'json-ld', 'type': 'application/ld+json'})
    if json_ld_script:
        json_ld_data = json.loads(json_ld_script.string)
        for item in json_ld_data:
            if item.get('@type') == 'Product':
                return item
    return {}


def extract_volume_and_price(html: str) -> Tuple[Optional[str], Optional[float]]:
    volume_match = re.search(r'<span class="product-add-to-cart(?:__)?price-size-depiction">\s*(\d+ML)\s*</span>', html)
    volume = volume_match.group(1) if volume_match else None

    price_match = re.search(r'<span class="price(?:__)?current">\s*£([\d.]+)', html)
    price = float(price_match.group(1)) if price_match else None

    return volume, price


def update_product_info(product, json_ld_data: Dict, html: str):
    if 'offers' in json_ld_data:
        product.is_in_stock = json_ld_data['offers'].get('availability') != 'OutOfStock'

    if 'name' in json_ld_data and 'description' in json_ld_data:
        description = json_ld_data['description']
        if isinstance(description, list) and len(description) > 0:
            product.name = f"{json_ld_data['name']} - {description[0]}"

    volume, price = extract_volume_and_price(html)
    product.variant_info = volume
    if price is not None:
        product.price = price
    return product


def fetch_product_html(product: ScrapedProduct) -> ScrapedProduct:
    try:
        headers = getHeader()
        response = requests.get(product.url, headers=headers)
        response.raise_for_status()
        html = response.text
        json_ld_data = parse_json_ld(html)
        updated_product = update_product_info(product, json_ld_data, html)
        Logger.info(f"Successfully scraped product: {product.url}")
        return updated_product
    except Exception as e:
        Logger.error(f"Error fetching {product.url}: {str(e)}")
        return product


def fetch_products_parallel(products: List[ScrapedProduct], threads: int = 10) -> List[ScrapedProduct]:
    Logger.info(f"Starting to fetch {len(products)} products with {threads} threads")
    start_time = time.time()

    results = []
    completed_count = 0
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_product = {executor.submit(fetch_product_html, product): product for product in products}
        for future in as_completed(future_to_product):
            product = future_to_product[future]
            try:
                result = future.result()
                results.append(result)
                completed_count += 1
                if completed_count % 10 == 0 or completed_count == len(products):
                    Logger.info(f"Progress: {completed_count}/{len(products)} products scraped")
            except Exception as exc:
                Logger.error(f"{product.url} generated an exception: {exc}")

    end_time = time.time()
    total_time = end_time - start_time
    Logger.info(f"Completed fetching {len(products)} products in {total_time:.2f} seconds")

    return results
