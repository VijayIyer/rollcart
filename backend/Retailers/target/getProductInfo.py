from backend.Retailers.util import read_ini
import requests


params = read_ini()
api_key = params["TARGET"]["rapidapi_key"]
api_host = params["TARGET"]["rapidapi_host"]
api_productName_host = params["TARGET"]["rapidapi_productName_host"]

class Target:

    def __init__(self, productName, zipcode):
        self.productName = productName
        self.zipcode = zipcode
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

    def get_price_by_product_name(self):
        url = "https://target-com-shopping-api.p.rapidapi.com/product_search"

        # get store ID based on user-zipcode
        storeId = self.get_store_id_by_zip()

        querystring = {
            "store_id":storeId,
            "keyword": self.productName,
            "offset": "0",
            "count": "25" #change depending on number of product matches needed
        }

        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_productName_host
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        # out = GoogleSearch(self.params).get_dictionary()
        # response = []
        # for item in out["organic_results"]:
        #     response.append(
        #         {
        #             "itemId": item["us_item_id"],
        #             "itemName": item["title"],
        #             "itemPrice": item["primary_offer"]["offer_price"],
        #             "itemThumbnail":item["thumbnail"],
        #             "productPageUrl":item["product_page_url"]
        #         }
        #     )
        # print("Store id using is",self.params["store_id"])
        # return response
        test_response = response.json()
        print(test_response)
        
        product_matches = response.json()["data"]["search"]["products"]

        result = []

        for i in range(len(product_matches)):
            result.append(
                {
                    "itemId": product_matches[i]["tcin"],
                    "itemName": product_matches[i]["item"]["product_description"]["title"],
                    "itemPrice": product_matches[i]["price"]["formatted_current_price"],
                    "itemThumbnail": product_matches[i]["item"]["enrichment"]["images"]["primary_image_url"],
                    "productPageUrl": product_matches[i]["item"]["enrichment"]["buy_url"]
                }
            )

        return result

    ### Below not used currently - leaving it as-is for UPC use-case
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