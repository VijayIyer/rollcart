from Retailers import config
from getProductPrices import Retailer
import pandas as pd
from serpapi import GoogleSearch
import pgeocode
from geopy.distance import geodesic
import csv

params = config.Config.WALMART_PARAMS
api_key = params["API_KEY"]
device = params["DEVICE"]
engine = params["ENGINE"]


class Walmart(Retailer):
    def __str__(self):
        return 'Walmart'

    def __init__(self):
        # self.walmartStoreData = pd.read_csv("Retailers/walmart/walmartStoreData.csv")
        self.dict_reader = csv.DictReader(open("Retailers/walmart/walmartStoreData.csv"))
        self.walmartStoreData = list(self.dict_reader)
        self.dist = pgeocode.Nominatim("us")
        self.params = {
            "api_key": api_key,
            "device": device,
            "engine": engine
        } 

    def getNearestStore(self,zipcode, lat, long):
        if not(lat and long):
            userData = self.dist.query_postal_code(zipcode)
            lat = userData.latitude
            long = userData.longitude

        nearestStore = -1
        nearestDistance = float("inf")

        for store in self.walmartStoreData:
            # storeLon, storeLat, storeId, storeName, storePostalCode = store
            new_store = {
                "storeLat" : store['Y'],
                "storeLon" : store['X'],
                "storeId" : store['businessunit_number'],
                "storeName" : store['businessunit_name'],
                "storePostalCode" : store['postal_code']
            }
            if zipcode[0:2] == str(new_store['storePostalCode'])[0:2]:
                curDistance = geodesic((new_store['storeLat'], new_store['storeLon']), (lat, long)).miles
                if curDistance < nearestDistance:
                    nearestDistance = curDistance
                    nearestStore = new_store
                    nearestStore['nearestDistance'] = nearestDistance

        return nearestStore

    def getNearestStoreId(self, zipcode, lat, long ):
        store = self.getNearestStore(zipcode,lat,long)
        if store != -1:
            return store['storeId']

        return -1

    def getNearestStoreDistance(self,userLocation,lat,long):
        store = self.getNearestStore(userLocation,lat,long)
        if store != -1:
            return store['nearestDistance']

        return -1

    def getProductsInNearByStore(self, product, zipcode,lat,long):
        try:
            self.params["query"] = product
            self.params["store_id"] = self.getNearestStoreId(zipcode,lat,long)
            out = GoogleSearch(self.params).get_dictionary()
            response = []
            if "organic_results" not in out:
                print(out)
                return response
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
        except Exception as e:
            print(e)
            return []

