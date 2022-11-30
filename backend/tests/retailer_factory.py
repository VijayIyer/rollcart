
from Retailers.kroger.getProductInfo import Kroger
from Retailers.target.getProductInfo import Target
from Retailers.walmart.getProductinfo import Walmart
from Retailers.walgreens.getProductInfo import Walgreens


class RetailerFactory():
    
    @staticmethod
    def getRetailer(retailer):
        # match needs python 3.10 + implementing with ifelse
        
        if retailer == 'Kroger':
            return Kroger()
        elif retailer == 'Target':
            return Target()
        elif retailer == 'Walmart':
            return Walmart()
        else:
            return Walgreens()


            