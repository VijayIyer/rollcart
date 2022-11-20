import pytest
from Retailers.walmart.getProductinfo import Walmart
from tests.retailer_factory import RetailerFactory
import mocker

TEST_ZIPCODE = "47401"
TEST_PRODUCT = "milk"

def test_retailers_mock_response(mocker):
    expected =[{

            
                      "itemId": "100000000",
                      "itemName": "Test mock milk",
                      "itemPrice": "12",
                      "itemThumbnail":"Image",
                      "productPageUrl":"product url"
        
        }]

    Retailers = ['Kroger' , 'Target', 'Walgreens']

    def mock_response(self):

        mockresponse = [{

            
                      "itemId": "100000000",
                      "itemName": "Test mock milk",
                      "itemPrice": "12",
                      "itemThumbnail":"Image",
                      "productPageUrl":"product url"
        
        }]
        return mockresponse

    for retailer in Retailers:


        print('Testing mock '+ retailer)
        mocker.patch(
            'Retailers.'+retailer.lower()+'.getProductInfo.'+retailer+'.getProductsInNearByStore' ,mock_response
        )

        actual = RetailerFactory.getRetailer(retailer).getProductsInNearByStore()
    
        assert actual == expected
        print( retailer + ' passed ......')
