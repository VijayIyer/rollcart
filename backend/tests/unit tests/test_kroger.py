
import pytest
import mocker
from Retailers.kroger.getProductInfo import Kroger

TEST_ZIPCODE = "47401"
TEST_PRODUCT = "milk"

#@pytest.mark.skip(reason="skipping to save api requests")
def test_kroger_store_endpoint():
    
    k = Kroger()
    
    response = k.getNearestStoreId(TEST_ZIPCODE)

    assert int(response) !=  -1

    pass


#@pytest.mark.skip(reason="skipping to save api requests")

def test_kroger_product_endpoint():

    k = Kroger()

    response = k.getProductsInNearByStore(TEST_PRODUCT,TEST_ZIPCODE)
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict






