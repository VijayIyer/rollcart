
import pytest
from Retailers.walgreens.getProductInfo import Walgreens



TEST_ZIPCODE = "47167"
TEST_PRODUCT = "buns"
LAT,LONG =None,None

#@pytest.mark.skip(reason="skipping to save api requests")

def test_walgreens_store_endpoint():
    
    walgreens = Walgreens()
    

    response = walgreens.getNearestStoreId(TEST_ZIPCODE,LAT,LONG)

    assert int(response) !=  -1

    pass

#@pytest.mark.skip(reason="skipping to save api requests")

def test_walgreens_product_endpoint():

    walgreens = Walgreens()

    response = walgreens.getProductsInNearByStore(TEST_PRODUCT,TEST_ZIPCODE,LAT,LONG)
    
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict
