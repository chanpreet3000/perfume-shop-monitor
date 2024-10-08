import requests

cookies = {
    'bm_sz': '76A0CB763C2C74F0D71750C054993FE6~YAAQNAVaaEB/XDCSAQAAuGicWxlaxWc/G4PU2v2LCwONteMZJLD+E1yE9OhWzoQRrB2nzxJqh5Vm4MBAlNG4zCTYv1nPOhbhXYxDvfP+XLskbVKyamAJkI9e2gL2XsVr7XWajE0sLK2iZc2RL3jNXOWW3rhx6+ZamppdL/PBUM/L2pUQCuDWrZvJcJWMRvAq2LR1L1k+6YzyqokHwP2XltseaX35/XEpRAe0YLaNDomC0c8pJn5YQDp0hYMkKh1JxWhhRSltTKoxUh+5P26e7coSjkiK6IUc4PLkYHMoVLqbtckBXFbYN1YQOP4l4R6y1bepvpyHDalI8RSzxVHJuGqWD5IX54UEEU7PlGhuSRainhuLBL/J6Kw/yKEjjqrZXuP7cR5IV1JA0aZZCiNuuDDU6UbGCd4=~3159618~3421251',
    'rxVisitorsc46wh8q': '1728113826603L4A27H8C0VEOEKLEG2I7T1M9BB27PN3I',
    'PIM-SESSION-ID': 'km0MFszUtiTPZnDX',
    'dtSasc46wh8q': '-',
    'rxvtsc46wh8q': '1728115627901|1728113826604',
    'dtPCsc46wh8q': '-93$113826600_545h-vRUCKUSDJESUUCRFSPPFLTIAMSQQUEPDP-0e0',
    'ak_bmsc': '2297ABAAB1556CAD6629D7297F236C58~000000000000000000000000000000~YAAQNAVaaEl/XDCSAQAAqG6cWxlfiEMpW378ADtQ92QHxnoyCmp6uiBt0smXNo4hvV1P7h4/vACj7D4Z6JQcGI1rI5cX1sh0+k0qERjTxv1ZdwTHo28OkPyoOg77icHzi6BFMpTMOh3E48Kr4BNiYye0SQkZ7IxQHagiNaWIDD1ydAB/s79/+0AGAtlNa79n2Yme9X2DB/Oxt8Mvl8hYzp536HU6/xOYnnLCx5HibpOeGnPkSt+x3astAzQlafRHq6gh2TkJhCANGhA/HYRPEM2uCwRaZRqF/NwOVtnvgmQaigcVgn0BsppvHREBouro2zOyOFAKq/e9ZCiJ/oxvI/z3VwEtWL+hfn1sudt42pYxdts5UjsST2CYpR6oUWcM9R8DbkAmuPg/z/v1n29MQaVIQNKig4Nsmx7yV7Mb8i1MQfhXdqZUwHlcdXUWZ+QnxAedy/vGJUzsgU+x8UZjEPXUr3U=',
    '_abck': '48DCFDDA89C0DDF2D255966BA81C8CE4~0~YAAQNAVaaEt/XDCSAQAAiXGcWwzH715thuFnEmI93jppo1mb2r8Z52KdivQdJRe24ZoHz6b3OzuZL2YVfz6KffN88wJWve1nGhTNyds3FbNDOJyj2KGhqQr7H73x1SXIBIFUlyFSGB6SzHGP22VQZzw+zcRPdG2FUppxcu6XOCaBvIO5QgSFCa10MraWj9bIcjMk29NCaQDV5+xROhtNzoN7MAJ7teWM6QLIiGCxbNIr2PulhajjeAUnhIEE3I5jtSSDMdxx3PPIZS8kxOHKObkrlbbGqVnC8ZDENV6BjbyChsbJz9XOi4/b68TUm8n+7qguh921Eum5TXSbRTjeUrgp41wvRMFQhlgoV5odKeH/QSxE9SSxoZWphZUBsl1d8xW3jM+/0tISTvsEmABGCynZ7s1S9sul2A+el6Tbv1sufXL2E4JuSNdDnPfdTTCqAfMRUGXPdn4hBwhP1//hxemycZ1/yNo8HQv9oQBVo7AOBLMSCepHHQ==~-1~||0||~-1',
    'ROUTE': '.api-7fb5dc6889-cdld7',
    'dtCookiesc46wh8q': 'v_4_srv_2_sn_VTIB1129PAE7RMIGE1Q8EQRGJ7J6V8S2_perc_100000_ol_0_mul_1_app-3A2cb6d09069590080_0',
    'bm_sv': 'DD37519DD39F1FA3D609E48EDF764336~YAAQNAVaaL1/XDCSAQAADZycWxk6nrMglifAh93qpLvFCYnsiwead/mu9UsE16mMAYykijKEv6Ah68vPC8YkIX1L/poUFVpXGu5kawtwVuSsFVDlEnmfY6c4T0LTp4ioxoGzFs6JmcIqh7bG70S/vlqWYKxs2pedi1bUc+EfFj7YuuT9ETn53txggjw82hjd2T7HqANv90BEw3zoR1o3olxqjmSsKgdcQOJlAHIygm+fC7p3HRNRK838ynq5PGlnm5zycFBzUhc=~1',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
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