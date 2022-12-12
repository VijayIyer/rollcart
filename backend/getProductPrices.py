from abc import ABC, abstractmethod
from typing import List, TypedDict

class Item(TypedDict):
    itemName: str
    itemPrice: str
    itemId:str
    itemThumbnail:str
    productPageUrl:str
    

class Retailer(ABC):
    # @abstractmethod
    # def getNearestStoreId(self, zipcode: str) -> str:
    #     pass
    @abstractmethod
    def getNearestStore(self, product: str, zipcode: str) -> List[Item]:
        pass
    
    @abstractmethod
    def getProductsInNearByStore(self, product: str, zipcode: str) -> List[Item]:
        # Sample response
        # [
            # {
            #     "itemName": "Happy Egg Organic Free Range Large Brown Eggs, 12 Count", "itemPrice":"8.38", 
            #          "itemId":"131231232", "imageUrl": "https://i5.walmart.com/123123/asd",
            # "productPageUrl": "https://www.walmart.com/ip/Happy-Egg-Organic-Free-Range-Large-Brown-Eggs-12-Count/134714692"

            # },
            # {
                # "itemName": "GreatValue Free Large white eggs, 36 Ct", "itemPrice":"9.54", "itemId":"13531312", 
                # "imageUrl": "https://i5.walmart.com/4123/sdf",
                # "productPageUrl": "https://www.walmart.com/ip/Great-Value-Large-White-Eggs-36-Count/142616435?athcpid=142616435
            # }            
        # ]
        pass

