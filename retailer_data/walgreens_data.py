from math import prod
import re
from typing import List
from bs4 import BeautifulSoup
import requests
import urllib3
import json
import argparse

BASE_URL = "https://www.walgreens.com"
RESULTS_URL = BASE_URL+"/search/results.jsp?"
BASE_API_STORE_LOCATOR_URL = "https://services.walgreens.com/api/stores/search/v2"


class Product:
    def __init__(self, name: str, upc: str, price: str) -> None:
        self.name = name
        self.upc = upc
        self.price = price


def fetch_products(search_term: str) -> List[Product]:
    # parameterize body
    params = {"Ntt": search_term.strip(), "inStockOnly": "true",
              "inStore": "true"}
    url: str = RESULTS_URL + urllib.parse.urlencode(params)
    resp = urllib3.request.urlopen(url)
    try:
        body = resp.read().decode()
    except:
        pass
    print(body)
    soup = BeautifulSoup(body, "lxml")
    items = soup.find_all(class_="item")
    detail_links = [item.find("a").get('href') for item in items]
    for link in detail_links:
        print(BASE_URL+link)
    return []


def fetch_products_store_inventory_api(address: str):
    http = urllib3.PoolManager()
    params = {
        "apiKey": "ZAvkGnCRXXuziCqrUGkvlvANLSZqvQYl",
        "affId": "",
        "address": "4299 WINSTON AVE, Covington, KY",
        "s": 5,
        "p": 1,
        "r": 5
    }
    r = http.request('POST', BASE_API_STORE_LOCATOR_URL,
                     headers={
                         "apiKey": "ZAvkGnCRXXuziCqrUGkvlvANLSZqvQYl"
                     },
                     fields=params)
    print(r.data.decode())
    # data = urllib3.parse.urlencode(params).encode()
    # print(data)
    # req = urllib3.request.Request(url=BASE_API_STORE_LOCATOR_URL)
    # req.add_header()
    # resp = urllib3.request.urlopen(req, data=data)
    # print(resp.read().decode())
    print(r.data.decode('utf-8'))
    pass


WALGREENS_STORESEARCH_ENDPOINT = 'https://www.walgreens.com/locator/v1/stores/search'
WALGREENS_PRODUCTSEARCH_ENDPOINT = 'https://www.walgreens.com/retailsearch/products/search'
DEFAULT_STORE_RADIUS = 10


def get_walgreens_products(search_term: str,
                         lat: float,
                         long: float,
                         radius: int = DEFAULT_STORE_RADIUS) -> List[Product]:
    products: List[Product] = []
    resp = requests.post(WALGREENS_STORESEARCH_ENDPOINT,
                         data={
                             "lat": lat,
                             "lng": long,
                             "p": "1",
                             "r": radius,
                             "requestType": "header",
                             "requestor": "headerui",
                             "sameday": "true",
                         })

    if resp.status_code == 200:
        data = resp.json()
        store_number = data['results'][0]['store']['storeNumber']
    else:
        return []
    print(store_number)
    resp = requests.post(WALGREENS_PRODUCTSEARCH_ENDPOINT,
                         json={
                             "p": "1",
                             "s": "72",
                             "sort": "relevance",
                             "view": "allView",
                             "geoTargetEnabled": "true",
                             "q": str(search_term),
                             "requestType": "search",
                             "deviceType": "desktop",
                             "includeDrug": "true",
                             "inStore": "true",
                             "storeId": str(store_number),
                             "searchTerm": str(search_term)
                         })
    if resp.status_code == 200:
        data = resp.json()
        print(data.keys())
        for product in data['products']:
            if product['productInfo']['storeInv'] == 'outofstock':
                continue
            new_product = Product(product['productInfo']['productName'],
                                  product['productInfo']['upc'],
                                  product['productInfo']['priceInfo']['regularPrice'])
            products.append(new_product)
        return products
    else:
        return []


# to test the method
parser = argparse.ArgumentParser()
parser.add_argument('--search_term', type=str)
parser.add_argument('--lat', type=float)
parser.add_argument('--long', type=float)
parser.add_argument('--radius', type=int)
args = parser.parse_args()
search_term = args.search_term
lat = args.lat
long = args.long
radius = args.radius
products: List[Product] = get_walmart_products(
    search_term=search_term,
    lat=lat,
    long=long,
    radius=radius)
for product in products:
    print(product.name)
