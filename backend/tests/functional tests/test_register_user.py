from app import app
from Retailers import config


def test_register_user():
    
    testapp = app.test_client()

    data = {        "user_name" : "ManasTester",
                 "password" : "testingpassword"
                        , 'first_name' : "Manas"
                        ,'last_name' : "Tester"
    }
    response = testapp.post('/register', json = data)

    print(response)
