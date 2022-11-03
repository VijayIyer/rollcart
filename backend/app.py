from distutils.log import debug
import json
from flask import Flask, request, make_response
from backend.Retailers.walmart.getProductinfo import Walmart
from backend.Retailers.walgreens.getProductInfo import *
from backend.Retailers.target.getProductInfo import Target
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask.json import jsonify
from sqlalchemy import select

USER_NAME = "rollcartadmin"
PASSWORD = "!grocerybudget1"
SERVER_NAME = "rollcartdb.mysql.database.azure.com"
PORT_NUMBER = "3306"
DATABASE_NAME = "rollcarttest"

db_connect_string="mysql+pymysql://rollcartadmin:!grocerybudget1@rollcartdb.mysql.database.azure.com:3306/rollcarttest"
ssl_args = {'ssl': {'ca':'DigiCertGlobalRootCA.crt.pem'}}


app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = db_connect_string
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine(db_connect_string, connect_args=ssl_args)
Session = sessionmaker(bind=engine)
# Session = SessionMaker()

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
@app.route('/login', methods=['POST'])
def login():
    return make_response('login unsuccessful', 403)


@app.route('/register', methods=['POST'])
def register():
    user = request.get_json()
    existingUserCount = Session.query(User).filter(User.user_name == user['user_name']).count()
    if existingUserCount > 0:
        return make_response({'message':'User already exists'}, 409)
    newUser = User(user_id = user['user_id']
            , user_name = user['user_name']
            ,password = user['password']
            ,firstname = user['firstname']
            ,lastname = user['lastname'])
    try:
        Session.add(newUser)
        Session.commit()
        response = {'message':'Registration Successful'}
        return make_response(response, 201)
    except Exception as e:
        print(e)
        return make_response('Error adding user', 400)
    return make_response('User already exists', 409)


@app.route('/logout', methods=['POST'])
def logout():
    return make_response({'message':'User logged out successfully'}, 200)


#  @app.route('/getUsers', methods=['GET']) # API endpoint not exposed / should only be for tests
def getUsers():
    '''
    gets all users in the database
    '''
    try:
        with Session() as session:
            results = session.query(User).all()
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


@app.route('/user/<int:userId>/addList', methods=['POST'])
def addList(userId:int):
    try:
        with Session() as session:
            body = request.get_json()
            listId = session.query(ListDetails).count() + 1
            newList = ListDetails(item_id = listId, listname = body['listname'])
            session.add(newList)
            session.commit()
        return make_response({'listId': listId}, 201)
    except Exception as e:
        print(e)
        return make_response({'message':'Unable to add list'}, 500)


@app.route('/user/<int:userId>/getLists', methods=['GET'])
def getLists(userId:int):
    '''
    Gets List Names created by user with userid provided in the request
    '''
    try:
        with Session() as session:
            listIds = session.query(List.list_id).filter(List.user_id == userId)
            lists = session.query(ListDetails).join(List, ListDetails.item_id == List.list_id) \
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
        with Session() as session:
            itemIds = session.query(List.item_id).filter(List.list_id == listId)
            items = session.query(ItemDetails).filter(ItemDetails.item_id.in_(itemIds))
            itemResults =[]
            for item in items:
                itemDict = dict()
                itemDict['itemName'] = item.itemname
                itemResults.append(itemDict)
        return make_response(itemResults, 200)
    except Exception as e:
        print(e)
        return make_response('Error retrieving items in list', 401)


@app.route('/getItems', methods=['GET'])
def getItems():
    try:
        with Session() as session:
            q = request.args['q']
            items = session.query(ItemDetails).filter(ItemDetails.itemname.contains(q))
            results = []
            for item in items:
                itemDict = dict()
                itemDict['item_id'] = item.item_id
                itemDict['itemname'] = item.itemname
                results.append(itemDict)
        return make_response(results, 200)
    except Exception as e:
        print(e)
        return make_response({'message':'unable to get items'}, 400)


@app.route('/<int:userId>/<int:listId>/addItem', methods=['POST'])
def addItem(userId:int, listId:int):
    '''
    adds item to a list for a particular user
    '''
    try:
        returnItemId = None
        returnListId = None
        with Session() as session:
            body = request.get_json()
            item_id = body['item_id']
            newItem = ItemDetails(item_id = item_id
                ,itemname = body['itemname'])
            session.add(newItem)
            newListItem = List(user_id = userId, list_id = listId, item_id = newItem.item_id)
            session.add(newListItem)
            session.commit()
            returnItemId = newListItem.item_id
            returnListId = newListItem.list_id
        return make_response('Item {} added successfully to {}'.format(returnItemId, returnListId), 200)
    except Exception as e:
        print(e)
        return make_response('Error adding Item', 400)


@app.route('/<int:userId>/<int:listId>/getPrices', methods=['GET'])
def getPrices(userId:int, listId:int):
    try:
        with Session() as session:
            itemIds = session.query(List.item_id).filter(List.user_id == userId and List.list_id == listId)
            prices = session.query(Price).filter(Price.item_id.in_(itemIds))
            results = []
            for price in prices:
                storePrice = dict()
                storePrice['storeId'] = price.store_id
                storePrice['totalPrice'] = price.rec_product_price
                results.append(storePrice)
            return make_response(results, 200)
    except Exception as e:
        print(e)
        return make_response({'message':'Unable to get prices'}, 400)


@app.route('/<int:userId>/<int:listId>/<int:storeId>/getPrices', methods=['GET'])
def getStorePrices(userId:int, listId:int, storeId:int):
    try:
        with Session() as session:
            itemIds = session.query(List).filter(List.user_id == userId and List.list_id == listId)
            prices = session.query(Price).filter(Price.item_id.in_(itemIds) and Price.store_id == storeId)
            results = []
            for price in prices:
                storePrice = dict()
                storePrice['storeId'] = price.store_id
                storePrice['totalPrice'] = price.rec_product_price
                results.append(storePrice)
            return make_response(results, 200)
    except Exception as e:
        print(e)
        return make_response({'message':'Unable to get prices'}, 400)
    return make_response([], 200)


@app.route('/<int:userId>/<int:listId>/<int:itemId>/removeItem', methods=['DELETE'])
def removeItem(userId, listId, itemId):
    try:
        with Session() as session:
            item = session.query(ItemDetails).filter(ItemDetails.item_id == itemId).one()
            listItems = session.query(List).filter(List.user_id == userId and List.list_id == listId and List.item_id == itemId).all()
            for listItem in listItems:
                session.delete(listItem)
            session.delete(item)
            session.commit()
        return make_response({'message': 'Item {} deleted successfully from {}'\
            .format(item.item_id, listId)}, 200)
    except Exception as e:
        print(e)
        return make_response('unable to remove item from list', 500)

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


## TODO: Update target class to take in Retailer format like the others.
@app.route('/targetTest')
def targetTestEndPoint():
   args = request.args

   t = Target(args['zip'], args['upc'])
   response = t.get_target_data()

   return response

@app.route('/getItems')
def test():
    with open('./data.json', 'r') as j:     
        out = json.loads(j.read())
    return out 

if __name__ == '__main__':
    app.run(debug=True)

