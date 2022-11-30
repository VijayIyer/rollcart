import pytest
from Retailers.walmart.getProductinfo import Walmart
from tests.retailer_factory import RetailerFactory
import mocker

def test_all_store_finder_with_mock_response(mocker):
    expected = 1001
    Retailers = ['Kroger' , 'Target', 'Walgreens']
    
    def mock_response(self):
        mockresponse = 1001
        return mockresponse


    def test_retailer(retailer):
        mocker.patch(
            'Retailers.'+retailer.lower()+'.getProductInfo.'+retailer+'.getNearestStoreId' ,mock_response
        )

        actual = RetailerFactory.getRetailer(retailer).getNearestStoreId()
    
        assert actual == expected
        print( retailer + ' passed ......')


    for retailer in Retailers:
        print('Testing mock store finder on '+ retailer)
        test_retailer(retailer)


        


    pass







def test_all_retailers_with_mock_response(mocker):
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


    def test_retailer(retailer):
        mocker.patch(
            'Retailers.'+retailer.lower()+'.getProductInfo.'+retailer+'.getProductsInNearByStore' ,mock_response
        )

        actual = RetailerFactory.getRetailer(retailer).getProductsInNearByStore()
    
        assert actual == expected
        print( retailer + ' passed ......')


    for retailer in Retailers:
        print('Testing mock product finder on '+ retailer)
        test_retailer(retailer)


        