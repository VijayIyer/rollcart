

import json
import os,base64
from this import d
from PIL import Image
import requests
import urllib.request

class KrogerApiHandler:

 
  def __init__(self):
    __sample_string = "grocery-budget-app-b70adbd5f6dabc039a2be71bf7e907655419924069399151519:PsI7IGO6S3viycNTIizsqHI5lwXq7YNUxq4UJtwe"
    __sample_string_bytes = __sample_string.encode("ascii")

    __base64_bytes = base64.b64encode(__sample_string_bytes)
    __base64_string = __base64_bytes.decode("ascii")


    token_command = "       curl -X POST \
              'https://api.kroger.com/v1/connect/oauth2/token' \
              -H 'Content-Type: application/x-www-form-urlencoded' \
              -H 'Authorization: Basic %s' \
              -d 'grant_type=client_credentials&scope=%s' > accesstoken.txt  "

    os.system(token_command %(__base64_string,"product.compact") )

    f = open('accesstoken.txt')
    readin = f.read()
    readin = json.loads(readin)



    self.__accesstoken = readin['access_token']
    print('*'*90)
    print(self.__accesstoken)
    print('*'*90)
    self.__header = {
      'Authorization': "Bearer %s" %(self.__accesstoken)
      }
    print(self.__header)


  def findNearestStore(self,zipcode):
      apiurl = "https://api.kroger.com/v1/locations"
      
      response = requests.get(apiurl,params={'filter.zipCode.near':zipcode,'filter.chain':'Kroger','filter.limit':1},headers=self.__header)
      #response = requests.request("GET",apiurl, headers=headers, data ={})
      
      
      if response.status_code == 200:
        responsevalue = response.json()
        print("\n LocationId of the store: ",responsevalue['data'][0]['locationId'])
        print("Address: " ,responsevalue['data'][0]['address'])

        return responsevalue['data'][0]['locationId']
      
      return  -1


  def findMatchingProducts(self,matchstring,storeId):


      apiurl =   'https://api.kroger.com/v1/products'
      params = {
        'filter.term': matchstring,
        'filter.locationId':storeId,
        'filter.limit': 3,
        'filter.fulfillment':'ais'
      }
      response = requests.get(apiurl,params=params,headers=self.__header)



      responsevalue = response.json()


      itemsretrived = {}




      for plist in responsevalue['data']:


        upc = plist['upc']
        desc = plist['description']
        price  = plist['items'][0]['price']['regular']
        promoprice = plist['items'][0]['price']['promo']
        size = plist['items'][0]['size']

        minprice = promoprice if (promoprice <= price and promoprice !=0)  else price

        urllib.request.urlretrieve(plist['images'][0]['sizes'][2]['url'],upc+".png")
        itemsretrived[upc]=[desc,minprice,size]



      print("upc\t\tdesc\t\t\t\t\t\tsize\t\t\ttprice")

      for key in itemsretrived.keys():
        img = Image.open(upc+".png")
        print('___'*40)
        print(key,'\t',itemsretrived[key][0],'\t\t\t',itemsretrived[key][2],'\t\t\t',itemsretrived[key][1])





kroger = KrogerApiHandler()


zipcode  = int(input("Enter Zipcode: "))
storeId = kroger.findNearestStore(zipcode)

if storeId == -1:
    print("No nearby stores found")
else:
    print('\n')
    m = input("Enter Product: ")
    print('\n')
    print("searching products in store ........................")


    kroger.findMatchingProducts(m,storeId)


