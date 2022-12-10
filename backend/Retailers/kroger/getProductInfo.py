

import json

import os,base64
import requests
import logging
from Retailers import config
from geopy.distance import geodesic
import pgeocode

import requests


from getProductPrices import Retailer


params = config.Config.KROGER_PARAMS
BASE_URL = params["BASE_URL"]
payload='grant_type=client_credentials&scope=product.compact'
STORESEARCHURL = params['STORESEARCH_URL']
PRODUCTSEARCHURL = params['PRODUCTSEARCH_URL']
AUTH_TOKEN = params['AUTH_TOKEN']

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
      
      self.dist = pgeocode.Nominatim("us")

        
  def __str__(self):
        return 'Kroger'

  def getProductsInNearByStore(self, product: str, zipcode: str,lat,long):
      try:
        storeId = self.getNearestStoreId(zipcode,lat,long)
        if storeId == -1:
          return []
      
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
      except Exception as e:
        logging.exception("getProducInNearbyStores failed in Kroger with following exception")
        return []

  def getNearestStores(self,zipcode : str,lat,long):
    apiurl = STORESEARCHURL
    
    try:
      # exact_response = requests.get(apiurl,params={'filter.zipCode.near':int(zipcode),'filter.chain':'Kroger','filter.limit':1},headers=self.__header)
      # if lat and long:
      # response = requests.get(apiurl,params={'filter.zipCode.near':int(zipcode),'filter.chain':'Kroger','filter.limit':1},headers=self.__header)
      exact_response = requests.get(apiurl,params={'filter.lat.near':float(lat),'filter.lon.near':float(long),'filter.chain':'Kroger','filter.limit':1},headers=self.__header)
  
        

      stores_lat_long = exact_response.json()

      return stores_lat_long['data']
    except Exception as e:
      logging.exception("getNearestStores failed in Kroger with following exception")
      return -1

  def getNearestStore(self,zipcode : str,lat,long):
    try:
      if not(lat and long):
        userData = self.dist.query_postal_code(zipcode)
        lat = userData.latitude
        long = userData.longitude
      stores = self.getNearestStores(zipcode,lat,long)
      if stores != -1:
        nearestStore = stores[0]
        storeGeolocation = nearestStore['geolocation']
        nearestDistance = geodesic((storeGeolocation['latitude'], storeGeolocation['longitude']), (lat,long)).miles

        for store in stores:
          store_location = store['geolocation']
          curDistance = geodesic((store_location['latitude'], store_location['longitude']), (lat,long)).miles
          store['curDistance'] = curDistance
          if curDistance < nearestDistance:
            nearestStore = store
            nearestDistance = curDistance

        return nearestStore
    
      return -1
    except Exception as e:
      logging.exception("getNearestStore failed in Kroger with following exception")
      return -1

  def getNearestStoreId(self,zipcode,lat,long):
    store = self.getNearestStore(zipcode,lat,long)
    if store != -1:
      return store['locationId']

    return -1

  def getNearestStoreDistance(self,zipcode,lat,long):
    store = self.getNearestStore(zipcode,lat,long)
    if store != -1:
      return store['curDistance']


        






