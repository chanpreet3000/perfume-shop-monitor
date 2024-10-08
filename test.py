import requests

cookies = {}

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

params = {
    'fields': 'FULL',
    'searchType': 'PRODUCT',
    'query': 'hrllo',
    'lang': 'en_GB',
    'curr': 'GBP',
}

response = requests.get('https://api.theperfumeshop.com/api/v2/tpsgb/search', params=params, cookies=cookies, headers=headers)
print(response.json())