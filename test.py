import requests

cookies = {
    '__pr.5d3oh4': 'DieGn3Va7C',
    'rxVisitorsc46wh8q': '172845721311950RHF7LB7L2NEQTHDVMFT5NJ3EFU2TB6',
    'PIM-SESSION-ID': 'uwbQmIm32r8PgbXn',
    '_abck': '48DCFDDA89C0DDF2D255966BA81C8CE4~0~YAAQNmw/F8gL2GeSAQAACgkUcAyJ4OWk/UJXvRSBtoRpNva4KtH4sgDtgTj50VN+xnRfI4TJHJgvzByBpjJELhAbTYJ/4Qf67Qlr3MQEl8Q8zjjs6r8qmBG/UKjKmsUJr7AZ9W99LxuPkIaa5PrYgtC3sRtSguYi61/KKp6fgy25ggY4qSyylj3cCIyKV/M0HxI9DbjBeZkLpAIH0Oqy3OZFriZ+dxitiVhsj0/1XUbPEYoxO9+aeqDNonmnQmyWJ8AbemOmu5JQam42ZKNkbmZgdocgzmPbRRMoRh9oIGfJzBJWBM9bqIm7kGGOR7ehJD/QTUw1NSVlEhLesKQ2iiIptjoiShC2K7Itxd6yVHaXIe8aaP4mWaDb3pfUl7vsvGoR5bSXSDkMHs6K/8grxFCK0l6IO6FITzjPVT+qD8ruSY7zPLsleke7QYcC5L9vCDvJ7xL8HVsuKgNj0ScXkfAAfXgjUU0nGHwEiJvZGUKfk5JVWm8JwA==~-1~-1~-1',
    'rxvtsc46wh8q': '1728459014341|1728457213121',
    'dtPCsc46wh8q': '-79$457213116_879h-vIBUQIFCPNLPFJLFUOTMDCFDISBAPLLMH-0e0',
    'ak_bmsc': 'E2FA6A146D40612FA7E80387AC603E7E~000000000000000000000000000000~YAAQNmw/F+YL2GeSAQAAmAsUcBlcFB56wRXy49YsguJkZoWPaz1ZZ5e0QN4DGWYMlZUviUu7Zj0Jmbjjt9ry/xJK6xbAMN/WzgvTC1GWf9huGAy6m6WrfA7x5niUgSTGMF/0O9ScnMKQkiHhKbyWjB7HTl7Xc6fKcuI9wFvQMRZvdLIPVmIkneLLjzjCy9fancENiuIGEmNzZOb6qbRwvGnGifJLZj8PVrRTZCx/pfMJygBUnPJIUIkm2eaU0IiwhUn4M5b2YFwBb4+uqjvt2aomvfT4ZYdWTz97GuJjHcuFNjhpU66bfx6TDhVnjcMpMdh4E3bFjF5V7WByW8fynePmHfpGvQiqHXeOpewYCCIhBbATS4ApxM2CXNO+Hew9DAUUzEqBh2oJ0+jOoNL2QCsmVPNx7OKysNoaDdObboOMZqKVJGepsnI6/m/Mblzz1g+ymaBK1NQIc0FktvxFPm9fldM=',
    'dtSasc46wh8q': 'true%7CC%7C-1%7CdTMasked_A%7C-%7C1728457214629%7C457213116_879%7Chttps%3A%2F%2Fwww.theperfumeshop.com%2Fdior%2Fsauvage%2Feau-de-toilette-spray%2Fp%2F65330EDTJU%7C%7C%7C%7C',
    'dtCookiesc46wh8q': 'v_4_srv_2_sn_AEAAQBRKTNV45HTA9B94JV4CTLEFHK3P_perc_100000_ol_0_mul_1_app-3A2cb6d09069590080_0',
    'ROUTE': '.api-7fb5dc6889-cdld7',
    'bm_sv': 'FB73950B0967B54DCD254B0F8A1C59A7~YAAQNmw/F3IN2GeSAQAA+CEUcBl0DvUib1WH6us6yrvVGUOyiDuX/p5Nha1dQO+Pid+N6bHA/uruw276ThM3hLyy19gpeDDB3LqKA5KWLJNcfq26MpLVLUZpg6QH9VCAidkVl6N2O0E7ONMRN6/b/6NMCWBrsuX7pOLmjSLVTA/6BuJvDM4snnc/HCrSMMK9A+l0aa+46+QxuKI+KWGenfYi2czui6wib8DEjaJq15gJFmmwUgE8T8e1PDTtt4hbwjzdVQca4aFg~1',
    'bm_sz': 'C6EFEE41E549EBFB6ABF14312B458B0D~YAAQNmw/F3MN2GeSAQAA+CEUcBnEpbe1nWuRMs7p6jk4Hq4ngObtekOLbdoxPSVv40fFDeDyKR+a+OgInhxKNkeVp51gb+n84fkHgk9BftSVJgkaDu8M4UcGV+NdAimc7CYO/NoqN+koEVlbOVl75Uy7I6XtrJghhnv1E8706kY8SzAmGY9dOnipzHm17tTW9WDs/km0OcIwFD4IReSmiPRiMpXsGB9pWL4PuSmBUpWBlD6jfoWLtuDZMKDTBh+lV2nNF4FmWBvhURPNi9KF18j/3oMOyeapCMY9PK2gDBzuHClDpMCIYExT/ZCOxUPihcUZUV/AxpW61M7xSltd2GMzR7ekfodWqFs15Xmvw+VrLDqk2P7kQohuDc5ajzmaJl9NUaLNM1z2sEhLw6S9wUK84en5pMdfGOFGZx5HLgNP~3294265~3422529',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.8',
    'occ-personalization-id': '00825c91-4354-45cc-b4f2-176ebe96e709',
    'occ-personalization-time': '1728457217462',
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
    'categoryCode': 'C102',
    'lang': 'en_GB',
    'curr': 'GBP',
}

response = requests.get('https://api.theperfumeshop.com/api/v2/tpsgb/search', params=params, cookies=cookies, headers=headers)
print(response.json())