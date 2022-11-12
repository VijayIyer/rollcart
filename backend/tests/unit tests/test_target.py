
from backend.Retailers.target.getProductInfo import Target

def test_target_store_endpoint():
    
    target = Target()
    

    response = target.getNearestStoreId(47401)

    assert int(response) !=  -1

    pass



def test_target_product_endpoint():

    target = Target()

    response = target.getProductsInNearByStore("milk",47401)
    
    assert type(response) == list
    assert len(response) != 0
    assert type(response[0]) == dict



