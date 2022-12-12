from Retailers import config
from getProductPrices import Item, Retailer
from typing import Dict, List, Tuple
import re
import pgeocode
import requests
from geopy.distance import geodesic
from Retailers.util import logExceptionInRetailerClass

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
    try:
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
        return requestResult(False, dict())
    except Exception as e:
        logExceptionInRetailerClass("getStoreLocatorRequestResults", "walgreens")
        return requestResult(False, dict())


def getProductSearchResults(url: str, search_term: str, store_number: str) -> requestResult:
    try:
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
        return requestResult(False, dict())
    except Exception as e:
        logExceptionInRetailerClass("getProductSearchResults", "walgreens")
        return requestResult(False, dict())


class Walgreens(Retailer):
    def __init__(self):
        self.dist = pgeocode.Nominatim("us")

    def __str__(self):
        return 'Walgreens'

    def getNearestStores(self,userLat,userLon):
        try:
            storeLocatorResults = getStoreLocatorRequestResults(userLat, userLon)
            if storeLocatorResults.success:
                return storeLocatorResults.data["results"]
        except Exception as e:
            logExceptionInRetailerClass("getNearestStores", str(self))
            return []

    def getNearestStore(self,userLocation,lat,long):
        try:
          if lat and long:
            userLat = lat
            userLon = long
          else:
            userData = self.dist.query_postal_code(userLocation)
            userLat = userData.latitude
            userLon = userData.longitude
          
          stores = self.getNearestStores(userLat,userLon)

          if len(stores) > 0:
              nearestStore = {
                      "storeName" : "",
                      "storeId" : "",
                      "currDistance" : "",
                      "Latitude" : "",
                      "Longitude" : ""
                  }
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
        except Exception as e:
          logExceptionInRetailerClass("getNearestStore", str(self))
          return -1

        
    def getCorrectPrice(self, priceString: str):
        lowestPrice = float("inf")
        try:
            results = re.findall(r"\$([0-9]*\.[0-9]*)", priceString)
            for group in results:
                if float(group) < lowestPrice:
                    lowestPrice = float(group)
            return lowestPrice
        except Exception as e:
            logExceptionInRetailerClass("getCorrectPrice", str(self))
            return -1

    def getProductsInNearByStore(self, product, zipcode,lat,long):
        try:
            storeNumber = self.getNearestStore(zipcode,lat,long)['storeId']
            # failed to find nearby store to this zipcode
            if storeNumber == -1:
                print("walgreens product search : store not found")
                return []
            else:
                resp = getProductSearchResults(url=WALGREENS_PRODUCTSEARCH_ENDPOINT,
                                            search_term=product,
                                            store_number=storeNumber)
                if not resp.success:
                    return []
                products = []
                for product in resp.data["products"]:
                    productInfo = product["productInfo"]
                    if "storeInv" not in productInfo.keys() and productInfo["storeInv"] != IN_STOCK:
                        print("request to {} failed".format(
                    WALGREENS_PRODUCTSEARCH_ENDPOINT))
                        return []
                    products.append(Item(itemName=productInfo["productName"],
                                                itemId=productInfo["upc"],
                                                itemPrice=self.getCorrectPrice(
                                productInfo["priceInfo"]["regularPrice"]),
                                itemThumbnail="http:" +
                                productInfo["imageUrl"],
                                productPageUrl=BASE_URL+productInfo["productURL"])
                            )
                return products
        except Exception as e:
            logExceptionInRetailerClass("getProductsInNearByStore", str(self))
            return []
