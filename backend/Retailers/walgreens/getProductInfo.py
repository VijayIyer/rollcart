from backend.Retailers.util import read_ini
from backend.getProductPrices import Item, Retailer
from typing import Dict, List, Tuple
import re
import validators
import pgeocode
import requests
from geopy.distance import geodesic

params = read_ini()
BASE_URL = params["WALGREENS"]["base_url"]
WALGREENS_STORESEARCH_ENDPOINT = params["WALGREENS"]["api_key"]
WALGREENS_PRODUCTSEARCH_ENDPOINT = params["WALGREENS"]["device"]
DEFAULT_STORE_RADIUS = params["WALGREENS"]["default_radius"]


class requestResult:
    def __init__(self, success: bool, data: Dict) -> None:
        self.success = success
        self.data = data


def getStoreLocatorRequestResults(lat: str, long: str, radius: int = 10) -> requestResult:
    if validators.url(WALGREENS_STORESEARCH_ENDPOINT):
        data = {
            "lat": lat,
            "lng": long,
            "p": "1",
            "r": radius,
            "requestType": "header",
            "requestor": "headerui",
            "sameday": "true",
        }
        resp = requests.post(url=WALGREENS_STORESEARCH_ENDPOINT, data=data)
        if resp.status_code == 200:
            return requestResult(True, resp.json())
        else:
            return requestResult(False, dict())
    else:
        return requestResult(False, dict())


def getProductSearchResults(url: str, search_term: str, store_number: str) -> requestResult:
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


class Walgreens(Retailer):
    def __init__(self):
        self.dist = pgeocode.Nominatim("us")

    def getNearestStoreId(self, userLocation):
        nearestStoreId = -1
        nearestDistance = float("inf")
        userData = self.dist.query_postal_code(userLocation)
        userLat = userData.latitude
        userLon = userData.longitude
        storeLocatorResults = getStoreLocatorRequestResults(userLat, userLon)
        if storeLocatorResults.success:
            for store in storeLocatorResults.data["results"]:
                storeLon = store["longitude"]
                storeLat = store["latitude"]
                storeId = store["store"]["storeNumber"]
                curDistance = geodesic(
                    (storeLat, storeLon), (userLat, userLon)).miles
                if curDistance < nearestDistance:
                    nearestDistance = curDistance
                    nearestStoreId = storeId
        else:
            return nearestStoreId

    def getCorrectPrice(self, priceString: str):
        lowestPrice = float("inf")
        try:
            results = re.findall(r"\$([0-9]*\.[0-9]*)", priceString)
            for group in results:
                if float(group) < lowestPrice:
                    lowestPrice = float(group)
        except:
            # replace with logger
            print("no price string found")
        return lowestPrice

    def getProductsInNearByStore(self, product, zipcode):
        storeNumber = self.getNearestStoreId(zipcode)
        # failed to find nearby store to this zipcode
        if storeNumber == -1:
            return []
        else:
            resp = getProductSearchResults(url=WALGREENS_PRODUCTSEARCH_ENDPOINT,
                                           search_term=product,
                                           store_number=storeNumber)
            if resp.success:
                # list in which resulting products will be appended
                products = []
                data = resp.data
                # replace with logger
                # print(data.keys())
                print(len(data["products"]))
                # print(data["products"])
                for product in data["products"]:
                    if "productInfo" in product.keys():

                        if "storeInv" in product["productInfo"].keys():
                            if product["productInfo"]["storeInv"] == "outofstock":
                                continue

                            else:
                                # print(product["productInfo"]["priceInfo"])
                                # this is where desired fields can be added
                                lowestOfferedPrice = self.getCorrectPrice(
                                    product["productInfo"]["priceInfo"]["regularPrice"])
                                if lowestOfferedPrice == float("inf"):
                                    lowestOfferedPrice = -1
                                products.append(Item(itemName=product["productInfo"]["productName"],
                                                     itemId=product["productInfo"]["upc"],
                                                     itemPrice=lowestOfferedPrice,
                                                     itemThumbnail=BASE_URL +
                                                     product["productInfo"]["productURL"],
                                                     productPageUrl=BASE_URL+product["productInfo"]["productURL"])
                                                )
                        else:
                            continue
                    else:
                        return []
                return products
            else:
                return []
