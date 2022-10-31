from time import time
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from backend.Retailers.walmart.getProductinfo import Walmart
from backend.Retailers.walgreens.getProductInfo import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask.json import jsonify
from sqlalchemy import select
import json

USER_NAME = "rollcartadmin"
PASSWORD = "!grocerybudget1"
SERVER_NAME = "rollcartdb.mysql.database.azure.com"
PORT_NUMBER = "3306"
DATABASE_NAME = "rollcarttest"

db_connect_string="mysql+pymysql://rollcartadmin:!grocerybudget1@rollcartdb.mysql.database.azure.com:3306/rollcarttest"
ssl_args = {'ssl': {'ca':'DigiCertGlobalRootCA.crt.pem'}}


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = db_connect_string
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(db_connect_string, connect_args=ssl_args)
SessionMaker = sessionmaker(bind=engine)
Session = SessionMaker()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
User = Base.classes.user
List = Base.classes.list
ItemDetails = Base.classes.itemdetails
ListDetails = Base.classes.listdetails
Price = Base.classes.price


## db endpoints
@app.route('/getUsers', methods=['GET'])
def getUsers():
    '''
    gets all users in the database
    '''
    try:
        results = Session.query(User).all()
        users = []
        for r in results:
            user = dict()
            user['name'] = r.user_name
            user['firstname'] = r.firstname
            user['lastname'] = r.lastname
            users.append(user)
        return make_response(users, 200)
    except Exception as e:
        print(e)
        return make_response('Error getting Users', 400)

    
@app.route('/getUserLists/<int:userId>', methods=['GET'])
def getUserLists(userId:int):
    '''
    Gets List Names created by user with userid provided in the request
    '''
    try:
        listIds = Session.query(List.list_id).filter(List.user_id == userId)
        lists = Session.query(ListDetails).join(List, ListDetails.item_id == List.list_id) \
        .filter(ListDetails.item_id.in_(listIds))
        listResults  = []
        for list in lists:
            listDict = dict()
            listDict['listname'] = list.listname
            listResults.append(listDict)
        return make_response(listResults, 200)
    except Exception as e:
        print(e)
        return make_response(e, 400)


@app.route('/getListItems/<int:listId>', methods=['GET'])
def getListItems(listId:int):
    '''
    Gets items in the list with listid provided in the query
    '''
    try:
        itemIds = Session.query(List.item_id).filter(List.list_id == listId)
        items = Session.query(ItemDetails).filter(ItemDetails.item_id.in_(itemIds))
        itemResults =[]
        for item in items:
            itemDict = dict()
            itemDict['itemName'] = item.itemname
            itemResults.append(itemDict)
        return make_response(itemResults, 200)
    except Exception as e:
        print(e)
        return make_response('Error retrieving items in list', 401)


@app.route('/addUser', methods=['POST'])
def addUser():
    user = request.get_json()
    newUser = User(user_id = user['user_id']
            , user_name = user['user_name']
            ,password = user['password']
            ,firstname = user['firstname']
            ,lastname = user['lastname'])
    try:
        Session.add(newUser)
        Session.commit()
        return make_response('User added successfully', 200)
    except Exception as e:
        print(e)
        return make_response('Error adding user', 400)


@app.route('/addItem', methods=['POST'])
def addItem():
    '''
    adds item to a list for a particular user
    '''
    body = request.get_json()
    # user_id = body['user_id']
    # list_id = body['list_id']
    item_id = body['item_id']
    newItem = ItemDetails(item_id = item_id
            ,itemname = body['itemname']
            )
    # newList = List(user_id = user_id
    #         ,list_id = list_id
    #         ,item_id = item_id)
    try:
        Session.add(newItem)
        Session.commit()
        return make_response('Item added successfully', 200)
    except Exception as e:
        print(e)
        return make_response('Error adding Item', 400)        
## 

@app.route('/intro')
def index():
    #print('Request for index page received')
    return {"welcomeMessage": "Hi there! We're currently getting things setup and should be ready for use in a few weeks!"}

# Only for testing


@app.route('/walmartTest', methods=['GET'])
def walmartTestEndPoint():
    args = request.args
    w = Walmart()
    return w.getProductsInNearByStore(args["q"], args["zipcode"])

# Only for testing


@app.route('/walgreensTest', methods=['GET'])
def walgreensTestEndPoint():
    args = request.args
    print(args['q'])
    print(args['zipcode'])
    w = Walgreens()
    return w.getProductsInNearByStore(args["q"], args["zipcode"])

# only for testing
# @app.route('/addUser', methods=['POST'])
# def add_user():
#     body = request.get_json()
#     user = (body.user.userName, body.user.password, body.user.firstName, body.user.lastName)
#     createUser(conn, user)
#     return make_response('User added', 200)


# # only for testing
# @app.route('/addList/<str:userName>', methods=['POST'])
# def add_list(userName:str):
#     body = request.get_json()
#     userId = getUserId(userName)
#     list = (body.list.name, userId)
#     create_list(conn, list)
#     return make_response('User added', 200)


if __name__ == '__main__':
    # u = User.query.all()
    # print(u)
    app.run(debug=True)
    # with app.app_context:
    #     db.reflect()
