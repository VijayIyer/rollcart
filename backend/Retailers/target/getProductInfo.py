from backend.Retailers.util import read_ini
import requests


params = read_ini()
api_key = params["TARGET"]["rapidapi_key"]
api_host = params["TARGET"]["rapidapi_host"]

class Target:

    def __init__(self, zipcode, upc):
        self.zipcode = zipcode
        self.upc = upc
        print("Initializing target data retrieval...")

    def get_target_data(self):
        price = self.get_price_by_upc()
        response = {
            "vendor": "target",
            "price": price
        }

        return response

    def get_store_id_by_zip(self):
        url = "https://target1.p.rapidapi.com/stores/list"

        querystring = {"zipcode":self.zipcode}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        storeId = response.json()[0]["locations"][0]["location_id"]

        #print(storeId)
        return storeId

    def get_price_by_upc(self):
        url = "https://target1.p.rapidapi.com/products/search-by-barcode"

        storeId = self.get_store_id_by_zip()

        querystring = {"store_id":storeId,"barcode":self.upc}

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        price = str(response.json()["data"]["product_by_barcode"]["price"]["current_retail"])
        
        #print(price)
        return price