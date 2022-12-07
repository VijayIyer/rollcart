from Retailers import config
from getProductPrices import Item, Retailer
from typing import Dict, List, Tuple
import re
import pgeocode
import requests
from geopy.distance import geodesic

params = config.Config.WALGREENS_PARAMS
BASE_URL = params["BASE_URL"]
WALGREENS_STORESEARCH_ENDPOINT = params["STORESEARCH_URL"]
WALGREENS_PRODUCTSEARCH_ENDPOINT = params["PRODUCTSEARCH_URL"]
DEFAULT_STORE_RADIUS = params["DEFAULT_RADIUS"]
IN_STOCK = params["IN_STOCK_STRING"]


class requestResult:
    def __init__(self, success: bool, data: Dict) -> None:
        self.success = success
        self.data = data


def getStoreLocatorRequestResults(lat: str, long: str, radius: int = 10) -> requestResult:
    # print(WALGREENS_STORESEARCH_ENDPOINT)

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
    # print(resp.status_code)
    if resp.status_code == 200:
        return requestResult(True, resp.json())
    else:
        print("request to {} failed".format(WALGREENS_STORESEARCH_ENDPOINT))
        return requestResult(False, dict())


def getProductSearchResults(url: str, search_term: str, store_number: str) -> requestResult:
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


class Walgreens(Retailer):
    def __init__(self):
        self.dist = pgeocode.Nominatim("us")

    def __str__(self):
        return 'Walgreens'

    def getNearestStores(self,userLat,userLon):
        storeLocatorResults = getStoreLocatorRequestResults(userLat, userLon)
        if storeLocatorResults.success:
            return storeLocatorResults.data["results"]

        return []

    def getNearestStore(self,userLocation,lat,long):
        userData = self.dist.query_postal_code(userLocation)
        userLat = userData.latitude
        userLon = userData.longitude
        if lat and long:
            userLat = lat
            userLon = long
        stores = self.getNearestStores(userLat,userLon)
        
        if len(stores) > 0:
            nearestStore = {
                    "storeName" : "",
                    "storeId" : "",
                    "currDistance" : "",
                    "Latitude" : "",
                    "Longitude" : ""
                }
            # nearestDistance = geodesic((nearestStore['latitude'], nearestStore['longitude']), (userLat, userLon)).miles
            nearestDistance = float("inf")
            for store in stores:
                curDistance = geodesic((store['latitude'], store['longitude']), (userLat, userLon)).miles
                store['curDistance'] = curDistance
                if curDistance < nearestDistance:
                    nearestDistance = curDistance
                    nearestStore = {
                            "storeName" : "",
                            "storeId" : store["store"]["storeNumber"],
                            "currDistance" : nearestDistance,
                            "latitude" : store['latitude'],
                            "longitude" : store['longitude']
                        }

            return nearestStore
        
        return -1
        
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
        return -1 if lowestPrice == float("inf") else lowestPrice

    def getProductsInNearByStore(self, product, zipcode,lat,long):
        try:
            storeNumber = self.getNearestStore(zipcode,lat,long)['storeId']
            # failed to find nearby store to this zipcode
            if storeNumber == -1:
                print("unsuccessful store search request")
                return []
            else:
                resp = getProductSearchResults(url=WALGREENS_PRODUCTSEARCH_ENDPOINT,
                                            search_term=product,
                                            store_number=storeNumber)
                if resp.success:
                    # list in which resulting products will be appended
                    products = []

                    # replace with logger
                    # print(len(data["products"]))
                    # print(data["products"])
                    for product in resp.data["products"]:
                        productInfo = product["productInfo"]
                        if "storeInv" in productInfo.keys():
                            if productInfo["storeInv"] == IN_STOCK:
                                # this is where desired fields can be added
                                products.append(Item(itemName=productInfo["productName"],
                                                    itemId=productInfo["upc"],
                                                    itemPrice=self.getCorrectPrice(
                                    productInfo["priceInfo"]["regularPrice"]),
                                    itemThumbnail="http:" +
                                    productInfo["imageUrl"],
                                    productPageUrl=BASE_URL+productInfo["productURL"])
                                )
                    return products
                else:
                    print("request to {} failed".format(
                        WALGREENS_PRODUCTSEARCH_ENDPOINT))
                    return []
        except Exception as e:
            print(e)
            return []
