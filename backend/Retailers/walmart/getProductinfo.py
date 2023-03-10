from Retailers import config
from getProductPrices import Retailer
import pandas as pd
from serpapi import GoogleSearch
import pgeocode
from geopy.distance import geodesic
import csv
from Retailers.util import logExceptionInRetailerClass

params = config.Config.WALMART_PARAMS
api_key = params["API_KEY"]
device = params["DEVICE"]
engine = params["ENGINE"]
dict_reader = csv.DictReader(open("Retailers/walmart/walmartStoreData.csv"))


class Walmart(Retailer):
    def __str__(self):
        return 'Walmart'

    def __init__(self):
        # self.walmartStoreData = pd.read_csv("Retailers/walmart/walmartStoreData.csv")
        # self.dict_reader = csv.DictReader(open("Retailers/walmart/walmartStoreData.csv"))
        self.walmartStoreData = list(dict_reader)
        self.dist = pgeocode.Nominatim("us")
        self.params = {
            "api_key": api_key,
            "device": device,
            "engine": engine
        } 

    def getNearestStore(self,zipcode, lat, long):
        try:
            if not(lat and long):
                userData = self.dist.query_postal_code(zipcode)
                lat = userData.latitude
                long = userData.longitude


            nearestStore = {
                        "storeName" : str(self),
                        "storeId" : -1,
                        "currDistance" : -1,
                        "latitude" : -1,
                        "longitude" : -1
                    }
            nearestDistance = float("inf")


            for store in self.walmartStoreData:
                # storeLon, storeLat, storeId, storeName, storePostalCode = store
                new_store = {
                    "latitude" : store['Y'],
                    "longitude" : store['X'],
                    "storeId" : store['businessunit_number'],
                    "storeName" : store['businessunit_name'],
                    "storePostalCode" : store['postal_code']
                }
                if zipcode[0:2] == str(new_store['storePostalCode'])[0:2]:
                    curDistance = geodesic((new_store['latitude'], new_store['longitude']), (lat, long)).miles
                    if curDistance < nearestDistance:
                        nearestDistance = curDistance
                        nearestStore = new_store
                        nearestStore['currDistance'] = nearestDistance

            return nearestStore
        except Exception as e:
            logExceptionInRetailerClass("getNearestStore", str(self))
            return -1

    def getProductsInNearByStore(self, product, zipcode,lat,long):
        try:
            self.params["query"] = product
            self.params["store_id"] = self.getNearestStore(zipcode,lat,long)['storeId']
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
            logExceptionInRetailerClass("getProductsInNearByStore", str(self))
            return []

