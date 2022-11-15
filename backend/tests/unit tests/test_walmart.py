from Retailers.walmart.getProductinfo import Walmart

TEST_ZIPCODE = "47401"
TEST_PRODUCT = "milk"
def test_walmart_store_endpoint():
    
    walmart = Walmart()
    

    response = walmart.getNearestStoreId(TEST_ZIPCODE)

    assert int(response) !=  -1

    pass


def test_walmart_product_endpoint():

    walmart = Walmart()

    response = walmart.getProductsInNearByStore(TEST_PRODUCT,TEST_ZIPCODE)
    
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict
