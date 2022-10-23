from backend.Retailers.util import read_ini
from backend.getProductPrices import Retailer
import pandas as pd
from serpapi import GoogleSearch
import pgeocode
from geopy.distance import geodesic


params = read_ini()
api_key = params["WALMART"]["api_key"]
device = params["WALMART"]["device"]
engine = params["WALMART"]["engine"]


class Walmart(Retailer):
    def __init__(self):
        self.walmartStoreData = pd.read_csv("Retailers/walmart/walmartStoreData.csv")
        self.dist = pgeocode.Nominatim("us")
        self.params = {
            "api_key": api_key,
            "device": device,
            "engine": engine
        } 

    def getNearestStoreId(self, userLocation):
        nearestStoreId = -1
        nearestDistance = float("inf")
        userData = self.dist.query_postal_code(userLocation)
        userLat = userData.latitude
        userLon = userData.longitude

        for store in self.walmartStoreData.iterrows():

            storeLon, storeLat, storeId, storeName, storePostalCode = store[1]
            if userLocation[0:2] == str(storePostalCode)[0:2]:
                curDistance = geodesic((storeLat, storeLon), (userLat, userLon)).miles
                if curDistance < nearestDistance:
                    nearestDistance = curDistance
                    nearestStoreId = storeId
        return nearestStoreId

    def getProductsInNearByStore(self, product, zipcode):
        self.params["query"] = product
        self.params["store_id"] = self.getNearestStoreId(zipcode)
        out = GoogleSearch(self.params).get_dictionary()
        response = []
        for item in out["organic_results"]:
            response.append(
                {
                    "itemId": item["us_item_id"],
                    "itemName": item["title"],
                    "itemPrice": item["primary_offer"]["offer_price"],
                    "itemThumbnail":item["thumbnail"],
                    "productPageUrl":item["product_page_url"]
                }
            )
        print("Store id using is",self.params["store_id"])
        return response

