from backend.Retailers.walmart.getProductinfo import Walmart


def test_walmart_store_endpoint():
    
    walmart = Walmart()
    

    response = walmart.getNearestStoreId(47401)

    assert int(response) !=  -1

    pass


def test_walmart_product_endpoint():

    walmart = Walmart()

    response = walmart.getProductsInNearByStore("milk",47401)
    
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict
