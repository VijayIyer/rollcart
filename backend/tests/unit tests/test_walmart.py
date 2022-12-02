import pytest
from Retailers.walmart.getProductinfo import Walmart


TEST_ZIPCODE = "47401"
TEST_PRODUCT = "milk"
LAT,LONG =None,None


#@pytest.mark.skip(reason="skipping to save api requests")

def test_walmart_store_endpoint():
    
    walmart = Walmart()
    

    response = walmart.getNearestStoreId(TEST_ZIPCODE,LAT,LONG)

    assert int(response) !=  -1

    pass

#@pytest.mark.skip(reason="skipping to save api requests")

def test_walmart_product_endpoint():

    walmart = Walmart()

    response = walmart.getProductsInNearByStore(TEST_PRODUCT,TEST_ZIPCODE,LAT,LONG)
    
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict
