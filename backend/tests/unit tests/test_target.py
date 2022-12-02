
from Retailers.target.getProductInfo import Target
TEST_ZIPCODE = "47401"
TEST_PRODUCT = "milk"
LAT,LONG =None,None

##@pytest.mark.skip(reason="skipping to save api requests")

def test_target_store_endpoint():
    
    target = Target()
    

    response = target.getNearestStoreId(TEST_ZIPCODE,LAT,LONG)

    assert int(response) !=  -1

    pass



def test_target_product_endpoint():

    target = Target()

    response = target.getProductsInNearByStore(TEST_PRODUCT,TEST_ZIPCODE,LAT,LONG)
    
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict



