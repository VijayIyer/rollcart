
from ast import List

import json
import os,base64
from PIL import Image
import requests
import urllib.request
from backend.Retailers.util import read_ini

from backend.getProductPrices import Retailer


params = read_ini()
BASE_URL = params["KROGER"]["base_url"]
payload='grant_type=client_credentials&scope=product.compact'
STORESEARCHURL = params["KROGER"]['storesearch_url']
PRODUCTSEARCHURL = params["KROGER"]['productsearch_url']
AUTH_TOKEN = params['KROGER']['auth_token']

header = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': AUTH_TOKEN
  }


class Kroger(Retailer):


  def __init__(self):
      #Generates access token for API auth.

      self.accessresponse = requests.request("POST", BASE_URL, headers=header, data=payload)
      actoken = json.loads(self.accessresponse.text)
      actoken = actoken['access_token']
      
      #Header used by other functions for different API calls
      self.__header = {
        'Authorization': "Bearer %s" %(actoken)
        }



  def getProductsInNearByStore(self, product: str, zipcode: str):


      storeId = self.getNearestStoreId(zipcode)
      if storeId == -1:
        return {"Message ":" Kroger store unavailable at given zipcode"}
    
      apiurl =   PRODUCTSEARCHURL
      params = {
        'filter.term': product,
        'filter.locationId':storeId,
        'filter.limit': 3,
        'filter.fulfillment':'ais'
      }
      response = requests.get(apiurl,params=params,headers=self.__header)

      if response.status_code == 200 :
        responsevalue = response.json()

        itemsretrived = []


        for plist in responsevalue['data']:


          upc = plist['upc']
          desc = plist['description']
          
          price  = plist['items'][0]['price']['regular']
          promoprice = plist['items'][0]['price']['promo']
          minprice = promoprice if (promoprice <= price and promoprice !=0)  else price


          image = plist['images'][0]['sizes'][0]['url']
          purl = "https://www.kroger.com/search?query="+ upc +"&searchType=default_search"
          item ={
                      "itemId": upc,
                      "itemName": desc,
                      "itemPrice": minprice,
                      "itemThumbnail":image,
                      "productPageUrl":purl

          }

          itemsretrived.append(item)
        return itemsretrived

      return []




  def getNearestStoreId(self, zipcode: str) :

      apiurl = STORESEARCHURL
      
      response = requests.get(apiurl,params={'filter.zipCode.near':int(zipcode),'filter.chain':'Kroger','filter.limit':1},headers=self.__header)
      
      if response.status_code == 200:
        responsevalue = response.json()
        return responsevalue['data'][0]['locationId']

      return  -1


        





