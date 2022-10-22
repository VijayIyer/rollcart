from cgitb import reset
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
import requests
import urllib3
import urllib
import json
import argparse
import pgeocode
import validators

WALGREENS_API_KEY = 'ZAvkGnCRXXuziCqrUGkvlvANLSZqvQYl'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
# exposed API endpoints
BASE_URL = "https://www.walgreens.com"
RESULTS_URL = BASE_URL+"/search/results.jsp?"
BASE_API_STORE_LOCATOR_URL = "https://services.walgreens.com/api/stores/search/v2"

# endpoints as seen in developer tools while scraping
WALGREENS_STORESEARCH_ENDPOINT = 'https://www.walgreens.com/locator/v1/stores/search'
WALGREENS_PRODUCTSEARCH_ENDPOINT = 'https://www.walgreens.com/retailsearch/products/search'
DEFAULT_STORE_RADIUS = 10


class requestResult:
    def __init__(self, success: bool, data: Dict) -> None:
        self.success = success
        self.data = data


class Product:
    def __init__(self, name: str, upc: str, price: str, url: str = '') -> None:
        self.name = name
        self.upc = upc
        self.price = price
        self.url = url


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
        "apiKey": WALGREENS_API_KEY,
        "affId": "storesapi",
        "zip": "47408",
        "s": "5",
        "p": "1",
        "r": "5"
    }
    r = urllib.request.Request(BASE_API_STORE_LOCATOR_URL,
                               data=urllib.parse.urlencode(params).encode())
    r.add_header('User-Agent', USER_AGENT)
    r.add_header('apiKey', WALGREENS_API_KEY)
    try:
        resp = urllib.request.urlopen(r)
        print(resp.read().decode())
    except Exception as e:
        print(e)

    # data = urllib3.parse.urlencode(params).encode()
    # print(data)
    # req = urllib3.request.Request(url=BASE_API_STORE_LOCATOR_URL)
    # req.add_header()
    # resp = urllib3.request.urlopen(req, data=data)
    # print(resp.read().decode())
    # print(r.data.decode('utf-8'))
    pass


def get_latlong_from_zipcode(zipcode: str) -> Tuple[str, str]:
    nomi = pgeocode.Nominatim('us')
    try:
        result = nomi.query_postal_code(zipcode)
    # in case zipcode is ill-formed
    except:
        return (-1, -1)
    return (result.latitude, result.longitude)


def get_store_locator_request_results(url: str, lat: str, long: str, radius: int = 10) -> requestResult:
    if validators.url(url):
        data = {
            "lat": lat,
            "lng": long,
            "p": "1",
            "r": radius,
            "requestType": "header",
            "requestor": "headerui",
            "sameday": "true",
        }
        resp = requests.post(url=url, data=data)
        if resp.status_code == 200:
            return requestResult(True, resp.json())
        else:
            return requestResult(False, dict())
    else:
        return requestResult(False, dict())


def get_product_search_results(url: str, search_term: str, store_number: str) -> requestResult:
    if validators.url(url):
        data = {
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
        }
        resp = requests.post(WALGREENS_PRODUCTSEARCH_ENDPOINT,
                             json=data)
        if resp.status_code == 200:
            return requestResult(True, resp.json())
        else:
            return requestResult(False, dict())
    else:
        return requestResult(False, dict())


def get_walgreens_products(search_term: str,
                           lat: float,
                           long: float,
                           radius: int = DEFAULT_STORE_RADIUS) -> List[Product]:
    products: List[Product] = []
    resp = get_store_locator_request_results(url=WALGREENS_STORESEARCH_ENDPOINT,
                                             lat=lat,
                                             long=long,
                                             radius=radius)
    if resp.success:
        data = resp.data
        # replace with logger
        # print(data)
        # change with nearest store logic
        store_number = data['results'][0]['store']['storeNumber']
    else:
        return []
    # replace with logger
    print(store_number)
    resp = get_product_search_results(url=WALGREENS_PRODUCTSEARCH_ENDPOINT,
                                      search_term=search_term,
                                      store_number=store_number)
    if resp.success:
        data = resp.data
        # replace with logger
        # print(data.keys())
        print(len(data['products']))

        # print(data['products'])
        for product in data['products']:
            if 'productInfo' in product.keys():

                if 'storeInv' in product['productInfo'].keys():
                    if product['productInfo']['storeInv'] == 'outofstock':
                        continue

                    else:
                        # print(product['productInfo']['priceInfo'])
                        # this is where desired fields can be added
                        new_product = Product(product['productInfo']['productName'],
                                              product['productInfo']['upc'],
                                              product['productInfo']['priceInfo']['regularPrice'],
                                              BASE_URL+product['productInfo']['productURL'])
                        products.append(new_product)
                else:
                    continue
            else:
                return []
        return products
    else:
        return []


# to test the methods
# parser = argparse.ArgumentParser()
# parser.add_argument('--search_term', type=str, required=True)
# parser.add_argument('--lat', type=float, required=True)
# parser.add_argument('--long', type=float, required=True)
# parser.add_argument('--radius', type=int)
# args = parser.parse_args()
# search_term = args.search_term
# lat = args.lat
# long = args.long
# radius = args.radius
# products: List[Product] = get_walgreens_products(
#     search_term=search_term,
#     lat=lat,
#     long=long,
#     radius=radius)
# for product in products:
#     print('{},{},{},{}'.format(product.name,
#           product.price, product.upc, product.url))
