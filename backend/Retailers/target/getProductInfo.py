from Retailers import config
from getProductPrices import Retailer
import requests
import decimal
import geopy
from geopy.distance import geodesic
import pgeocode

params = config.Config.TARGET_PARAMS
api_key = params["RAPIDAPI_KEY"]
api_host = params["RAPIDAPI_HOST"]
api_productName_host = params["RAPIDAPI_PRODUCTNAME_HOST"]

geo_locator = geopy.Nominatim(user_agent='1234')

class Target(Retailer):

    def __init__(self) -> None:
        self.dist = pgeocode.Nominatim("us")
        super().__init__()

    def __str__(self):
        return 'Target'

    def getNearestStore(self,userLocation,lat,long):
        try:
            if not(lat and long):
                userData = self.dist.query_postal_code(userLocation)
                lat = userData.latitude
                long = userData.longitude
            # r = geo_locator.reverse((lat, long))
            # userLocation = r.raw['address']['postcode']
            stores = self.getNearestStores(userLocation,lat,long)
            if len(stores) > 0 and len(stores[0]['locations']) > 0:
                nearestStore = {
                    "storeName" : "",
                    "storeId" : "",
                    "currDistance" : "",
                    "Latitude" : "",
                    "Longitude" : ""
                }
                # nearestStore = stores[0]["locations"][0]
                # nearestStore_geographic = nearestStore['geographic_specifications']
                # nearestDistance = geodesic((nearestStore_geographic['latitude'],nearestStore_geographic['longitude']),(lat,long)).miles
                nearestDistance = float("inf")

                for store in stores[0]['locations']:
                    geographic = store['geographic_specifications']
                    curDistance = geodesic((geographic['latitude'], geographic['longitude']), (lat,long)).miles
                    store['curDistance'] = curDistance
                    if curDistance < nearestDistance:
                        nearestDistance = curDistance
                        nearestStore = {
                            "storeName" : "",
                            "storeId" : store['location_id'],
                            "currDistance" : nearestDistance,
                            "latitude" : geographic['latitude'],
                            "longitude" : geographic['longitude']
                        }


                return nearestStore
        except Exception as e:
            print(e)
            return -1
    
        

    def getNearestStores(self,userLocation,lat,long):
        zipcode = userLocation
        url = "https://target1.p.rapidapi.com/stores/list"
        
        querystring = {"zipcode":zipcode}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
        }

        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
        except Exception as e:
            print(e)

        return response.json()


    def getProductsInNearByStore(self, product, zipcode,lat,long):
        try:
            url = "https://target-com-shopping-api.p.rapidapi.com/product_search"
            # get store ID based on user-zipcode
            storeId = self.getNearestStore(zipcode,lat,long)['storeId']

            querystring = {
                "store_id":storeId,
                "keyword": product,
                "offset": "0",
                "count": "5" #change depending on number of product matches needed
            }

            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": api_productName_host
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            
            product_matches = response.json()["data"]["search"]["products"]

            result = []

            for i in range(len(product_matches)):
                result.append(
                    {
                        "itemId": product_matches[i]["tcin"],
                        "itemName": product_matches[i]["item"]["product_description"]["title"],
                        "itemPrice": decimal.Decimal(product_matches[i]["price"]["formatted_current_price"][1:]),
                        "itemThumbnail": product_matches[i]["item"]["enrichment"]["images"]["primary_image_url"],
                        "productPageUrl": product_matches[i]["item"]["enrichment"]["buy_url"]
                    }
                )
        except Exception as e:
            print(e)
            return []
        return result