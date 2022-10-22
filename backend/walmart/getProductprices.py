from serpapi import GoogleSearch
import pgeocode
from geopy.distance import geodesic
import pandas as pd

# TODO: Need to put these in an env file
params = {
    "api_key": "cb4579e10bb941b61ca774c9088b4e831df7e9714d917a36c301e5cc132e0e60",
    "device": "desktop",
    "engine": "walmart",
}


class Walmart:
    def __init__(self):
        self.walmartStoreData = pd.read_csv("backend/walmart/walmartStoreData.csv")
        self.dist = pgeocode.Nominatim("us")
        self.params = {
            "api_key": "cb4579e10bb941b61ca774c9088b4e831df7e9714d917a36c301e5cc132e0e60",
            "device": "desktop",
            "engine": "walmart",
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
                    "us_item_id": item["us_item_id"],
                    "title": item["title"],
                    "price": item["primary_offer"]["offer_price"],
                }
            )
        return response


# starter script
w = Walmart()
out = w.getProductsInNearByStore("eggs", "47408")
print(out[:2])
