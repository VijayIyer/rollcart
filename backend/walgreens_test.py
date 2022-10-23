import argparse
from Retailers.walgreens.getProductInfo import *

parser = argparse.ArgumentParser()
parser.add_argument('--search_term', type=str, required=True)
parser.add_argument('--zip', type=str, required=True)
args = parser.parse_args()

walgreens = Walgreens()
products: List[Item] = walgreens.getProductsInNearByStore(
    args.search_term, args.zip)
print(len(products))
for product in products:
    print('{}, {}, {}, {}, {}'.format(product['itemName'], product['itemPrice'],
          product['itemId'], product['itemThumbnail'], product['productPageUrl']))
