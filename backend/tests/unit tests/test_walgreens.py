from backend.Retailers.walgreens.getProductInfo import Walgreens


def test_target_store_endpoint():
    
    walgreens = Walgreens()
    

    response = walgreens.getNearestStoreId(47401)

    assert int(response) !=  -1

    pass


def test_walgreens_product_endpoint():

    walgreens = Walgreens()

    response = walgreens.getProductsInNearByStore("milk",47401)
    
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict
