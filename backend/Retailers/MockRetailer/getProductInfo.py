from getProductPrices import Item, Retailer
from typing import Dict, List, Tuple
import argparse
import random

THUMBNAILS = ['https://pics.drugstore.com/prodimg/533734/900.jpg'
, 'https://pics.drugstore.com/prodimg/572416/900.jpg'
, 'https://pics.drugstore.com/prodimg/418563/450.jpg'
, 'https://pics.drugstore.com/prodimg/633616/900.jpg']


PRODUCT_PAGES = ['https://www.walgreens.com/store/c/kroger-salted-butter,-sticks/ID=300412450-product', 
'https://www.walgreens.com/store/c/skippy-creamy/ID=prod6258062-product',
'https://www.walgreens.com/store/c/nature\'s-own-butterbread-butterbread/ID=prod6166509-product'
,'https://www.walgreens.com/store/c/nice!-eggs-large/ID=prod6179051-product']

class MockRetailer(Retailer):
    
    def __init__(self) -> None:
        super().__init__()
        self.storeId = random.randint(1000, 9999)

    def __str__(self):
        return 'MockStore'
    
    def getNearestStoreId(self, userLocation):
        return self.storeId
    
    
    def getRandomImageThumbnail(self):
        return THUMBNAILS[random.randint(0, len(THUMBNAILS) - 1)]
    
    def getRandomProductPage(self):
        return PRODUCT_PAGES[random.randint(0, len(PRODUCT_PAGES) - 1)]

    def getProductsInNearByStore(self, product: str, zipcode: str) -> List[Item]:
        numProducts = random.randint(3, 10)
        productNumber = random.randint(0, 9999)
        return [Item(itemName=product+str(i),
                        itemId=productNumber,
                        itemPrice=random.random()*random.randint(0,10),
                        itemThumbnail=self.getRandomImageThumbnail(),
                        productPageUrl=self.getRandomProductPage())
                        for i in range(numProducts)]
        


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_term', type=str, required=True)
    parser.add_argument('--zip', type=str, required=True)
    args = parser.parse_args()

    retailer = MockRetailer()
    products: List[Item] = retailer.getProductsInNearByStore(
        args.search_term, args.zip)
    print(len(products))
    for product in products:
        print('{}, {}, {}, {}, {}'.format(product['itemName'], product['itemPrice'],
            product['itemId'], product['itemThumbnail'], product['productPageUrl']))
