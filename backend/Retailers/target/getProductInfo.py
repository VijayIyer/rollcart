from backend.Retailers import config
from backend.getProductPrices import Retailer
import requests
import decimal

params = config.Config.TARGET_PARAMS
api_key = params["RAPIDAPI_KEY"]
api_host = params["RAPIDAPI_HOST"]
api_productName_host = params["RAPIDAPI_PRODUCTNAME_HOST"]

class Target(Retailer):

    def __init__(self) -> None:
        super().__init__()

    def __str__(self):
        return 'Target'
    
    def getNearestStoreId(self, userLocation):
        url = "https://target1.p.rapidapi.com/stores/list"

        querystring = {"zipcode":userLocation}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        storeId = response.json()[0]["locations"][0]["location_id"]

        return storeId

    def getProductsInNearByStore(self, product, zipcode):
        try:
            url = "https://target-com-shopping-api.p.rapidapi.com/product_search"

            # get store ID based on user-zipcode
            storeId = self.getNearestStoreId(zipcode)

            querystring = {
                "store_id":storeId,
                "keyword": product,
                "offset": "0",
                "count": "25" #change depending on number of product matches needed
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
        except:
            return []
        return result