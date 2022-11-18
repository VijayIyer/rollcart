
from Retailers.walgreens.getProductInfo import Walgreens



TEST_ZIPCODE = "46219"
TEST_PRODUCT = "milk"

def test_walgreens_store_endpoint():
    
    walgreens = Walgreens()
    

    response = walgreens.getNearestStoreId(TEST_ZIPCODE)

    assert int(response) !=  -1

    pass


def test_walgreens_product_endpoint():

    walgreens = Walgreens()

    response = walgreens.getProductsInNearByStore(TEST_PRODUCT,TEST_ZIPCODE)
    
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict
