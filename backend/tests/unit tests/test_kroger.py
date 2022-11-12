
from backend.Retailers.Kroger.getProductInfo import Kroger

def test_kroger_store_endpoint():
    
    k = Kroger()
    
    response = k.getNearestStoreId(47401)

    assert int(response) !=  -1

    pass



def test_kroger_product_endpoint():

    k = Kroger()

    response = k.getProductsInNearByStore("milk",47401)
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict



