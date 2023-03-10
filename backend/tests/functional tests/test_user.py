
import json

import pytest
from app import app
from Retailers import config

TEST_USERNAME = "Tester1"
TEST_PASSWORD = "testingpassword"
TEST_TOKEN = ""
TEST_USERLIST = 'Testing list'

 
def test_register_user():
    
    testapp = app.test_client()

    data = {        "username" : TEST_USERNAME,
                 "password" : TEST_PASSWORD
                        , 'firstname' : "Functional"
                        ,'lastname' : "Tester"
    }
    response = testapp.post('/register', json = data)

    assert response.status_code == 201 or 409


def test_login():
    global TEST_TOKEN
    testapp = app.test_client()
    response = testapp.post('/login',auth=(TEST_USERNAME,TEST_PASSWORD))
    res= json.loads(response.text)


    assert response.status_code == 201
    assert res['message'] == 'login successful'
    assert res['token'] != ""
    TEST_TOKEN = res['token']



def test_logout():

    testapp = app.test_client()
    
    data ={
        'userName':TEST_USERNAME
    }
    
    response = testapp.post('/logout',json=data)
    
    assert response.status_code == 200
