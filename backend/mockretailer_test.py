import argparse
from Retailers.MockRetailer.getProductInfo import *

parser = argparse.ArgumentParser()
parser.add_argument('--search_term', type=str, required=True)
parser.add_argument('--zip', type=str, required=True)
args = parser.parse_args()

retailer = MockRetailer()
products: List[Item] = retailer.getProductsInNearByStore(
    args.search_term, args.zip)
for product in products:
    print('{}, {}, {}, {}, {}'.format(product['itemName'], product['itemPrice'],
          product['itemId'], product['itemThumbnail'], product['productPageUrl']))
    print('\n\n')
