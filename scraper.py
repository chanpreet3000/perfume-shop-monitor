import json
import re
import time
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape

from Logger import Logger
from ScrapedProduct import ScrapedProduct
from network import fetch_with_proxy, get_proxies_from_webshare


def get_all_variants(product: ScrapedProduct, html: str) -> List[ScrapedProduct]:
    try:
        script_content = re.search(r'<script id="spartacus-app-state" type="application/json">(.*?)</script>', html,
                                   re.DOTALL)
        json_string = script_content.group(1)
        json_string = unescape(json_string.replace('&q;', '"'))

        data = json.loads(json_string)
        entries = data['cx-state']['product']['details']['entities']
        product_key = list(entries.keys())[0]
        variant_matrix = entries[product_key]['variants']['value']['variantMatrix']
        name = entries[product_key]['details']['value']['name']
        range_name = entries[product_key]['details']['value']['rangeName']
        name = f"{range_name} - {name}"

        products = []
        for variant_m in variant_matrix:
            variant_option = variant_m['variantOption']
            variant = variant_option['code']
            ean = variant_option['ean']
            uid = f"{product.product_code}-{variant}"
            price = variant_option['priceData']['value']
            is_in_stock = variant_option['stock']['stockLevelStatus'] != 'outOfStock'
            stock_level = variant_option['stock']['stockLevel']
            url = f"https://www.theperfumeshop.com/{variant_option['url']}"
            variant_info = variant_m['variantValueCategory']['name']

            products.append(
                ScrapedProduct(uid, product.average_rating, product.product_code, product.brand, name, price,
                               product.promotions,
                               is_in_stock, product.default_sku, url, -1, variant, variant_info, stock_level,
                               ean))
        return products
    except Exception as e:
        raise e


def fetch_product_html(proxies: List[Dict[str, str]], product: ScrapedProduct) -> List[ScrapedProduct] | None:
    try:
        response = fetch_with_proxy(proxies, product.url, method='GET', timeout=20, max_retries=3)
        html = response.text
        updated_product = get_all_variants(product, html)
        Logger.info(f"Successfully scraped product: {product.url}")
        return updated_product
    except Exception as e:
        Logger.error(f"Error fetching {product.url}", e)
        return None


def fetch_products_parallel(products: List[ScrapedProduct], threads: int = 10) -> List[ScrapedProduct]:
    Logger.info(f"Starting to fetch {len(products)} products with {threads} threads")
    start_time = time.time()

    proxies = get_proxies_from_webshare()

    results = []
    completed_count = 0
    batch_size = 50
    delay_seconds = 60

    for i in range(0, len(products), batch_size):
        batch = products[i:i + batch_size]

        Logger.info(f"Processing batch {i // batch_size + 1} of products")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_product = {executor.submit(fetch_product_html, proxies, product): product for product in batch}
            for future in as_completed(future_to_product):
                product = future_to_product[future]
                try:
                    result = future.result()
                    if result is not None:
                        results.extend(result)
                    completed_count += 1
                    if completed_count % 10 == 0 or completed_count == len(batch):
                        Logger.info(f"Progress: {completed_count}/{len(products)} products scraped")
                except Exception as exc:
                    Logger.error(f"{product.url} generated an exception: {exc}")

        if i + batch_size < len(products):
            Logger.info(f"Batch complete. Waiting for {delay_seconds} seconds before next batch...")
            time.sleep(delay_seconds)

    end_time = time.time()
    total_time = end_time - start_time
    Logger.info(f"Completed fetching {len(products)} products in {total_time:.2f} seconds")

    return results
