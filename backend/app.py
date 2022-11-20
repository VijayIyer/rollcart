from distutils.log import debug
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from Retailers import config
from flask import Flask, request, make_response
from Retailers.util import getUniqueItems
from Retailers.Kroger.getProductInfo import Kroger
from Retailers.walmart.getProductinfo import Walmart
from Retailers.walgreens.getProductInfo import *
from Retailers.target.getProductInfo import Target
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask.json import jsonify
from functools import wraps
import random

app = Flask(__name__)

# Using a production configuration
#app.config.from_object('config.ProdConfig')

# Using a development configuration
app.config.from_object(config.DevConfig)

CORS(app)

DB_PARAMS = app.config['DATABASE_PARAMS']
db_connect_string="mysql+pymysql://{}:{}@{}:{}/{}".format(DB_PARAMS['USER_NAME'], DB_PARAMS['PASSWORD'], DB_PARAMS['SERVER_NAME'], DB_PARAMS['PORT_NUMBER'], DB_PARAMS['NAME'])
ssl_args = {'ssl': {'ca':'DigiCertGlobalRootCA.crt.pem'}}

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
UserList = Base.classes.userlist
Item = Base.classes.item
UserListItem = Base.classes.userlistitem
Store = Base.classes.store
Price = Base.classes.price


# retailers
retailers = [Target(), Walgreens(), Kroger(), Walmart()]

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return jsonify({'message':'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms='HS256')
            with Session() as session:
                currentUser = session.query(User).filter(User.user_id == data['user_id']).first()
        except:            
            return jsonify({'message':'Token is invalid'}), 401
        
        return f(currentUser, *args, **kwargs)
    return decorated


## db endpoints
@app.route('/login', methods=['POST'])
def login():
    try:
        with Session() as session:
            auth = request.authorization
            if auth is None or auth.username is None or auth.password is None:
                return make_response({'message':'No authorization headers'}, 403)
            
            existingUser = session.query(User).filter(User.user_name == auth.username and User.password == auth.password).first()
            if not existingUser:
                return make_response({'message':'No such user in database'}, 409)
            if existingUser.password == auth.password:
                token = jwt.encode({'user_id':existingUser.user_id}, app.config['SECRET_KEY'])
                return jsonify({'message':'login successful', 'token':token}), 201
            else:
                return make_response({'message':'Invalid Credentials'}, 403)
    except Exception as e:
        print(e)
        return make_response({'message':'Unknown Error, check logs'}, 400)


@app.route('/register', methods=['POST'])
def register():
    
    try:
        with Session() as session:
            user = request.get_json()
            # hashedPassword = generate_password_hash(user['password'], method='sha256')
            existingUserCount = session.query(User).filter(User.user_name == user['username']).count()
            if existingUserCount > 0:
                return make_response({'message':'User already exists'}, 409)

            newUser = User(user_name = user['username']
                        , password = user['password']
                        , first_name = user['firstname']
                        , last_name = user['lastname'])
            session.add(newUser)
            session.commit()
            response = {'message':'Registration Successful'}
        return make_response(response, 201)
    except Exception as e:
        print(e)
        return make_response('Error adding user', 400)


@app.route('/logout', methods=['POST'])
def logout():
    try:
        with Session() as session:
            body = request.get_json()
            if session.query(User).filter(User.user_name == body['userName']).count() == 0:
                return make_response({'message':'No such User {} found in database'.format(body['userName'])})
            else:
                loggedInUser = session.query(User).filter(User.user_name == body['userName']).one()
                ## turn below into logged out update statement
                print(loggedInUser)
                return make_response({'message':'User logged out successfully'}, 200)
    except Exception as e:
        print(e)
        return make_response({'message':'error logging out user'}, 400)


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


@app.route('/addList', methods=['POST'])
@token_required
def addList(user):
    try:
        returnListId = None
        with Session() as session:
            body = request.get_json()
            # checking user exists
            if session.query(User).filter(User.user_id == user.user_id).count() == 0:
                return make_response({'message':'User with id {} not found'.format(user.user_id)}, 400)
            # adding to list table
            newList = List(list_name = body['listname'])
            session.add(newList)
            # flush() will allow to return id of inserted row
            session.flush()
            # adding to user list relationship table
            newUserList = UserList(user_id = user.user_id, list_id = newList.list_id)
            session.add(newUserList)
            # flush() will allow to return id of inserted row
            session.flush()
            returnListId = newUserList.list_id
            session.commit()
        return make_response({'listId': returnListId}, 201)
    except Exception as e:
        print(e)
        return make_response({'message':'Unable to add list'}, 500)


@app.route('/getLists', methods=['GET'])
@token_required
def getLists(user):
    '''
    Gets List Names created by user with userid provided in the request
    '''
    try:
        with Session() as session:
            # checking user exists
            if session.query(User).filter(User.user_id == user.user_id).count() == 0:
                return make_response({'message':'User with id {} not found'.format(user.user_id)}, 400)
            listIds = session.query(UserList.list_id).filter(UserList.user_id == user.user_id)
            lists = session.query(List).join(UserList, UserList.list_id == List.list_id) \
            .filter(List.list_id.in_(listIds))
            listResults  = []
            for list in lists:
                listDict = dict()
                listDict['listId'] = list.list_id
                listDict['listname'] = list.list_name
                listResults.append(listDict)
        return make_response(listResults, 200)
    except Exception as e:
        print(e)
        return make_response(e, 400)


@app.route('/getListItems/<int:listId>', methods=['GET'])
@token_required
def getListItems(user, listId:int):
    '''
    Gets items in the list with listid provided in the query
    '''
    try:
        with Session() as session:
            userListId = session.query(UserList.user_list_id).filter(UserList.list_id == listId).one()
            itemIds = session.query(UserListItem.item_id).filter(UserListItem.user_list_id == userListId)
            items = session.query(Item).filter(Item.item_id.in_(itemIds))
            itemResults =[]
            for item in items:
                itemDict = dict()
                itemDict['itemId'] = item.item_id
                itemDict['itemName'] = item.item_name
                itemDict['quantity'] = item.quantity
                itemResults.append(itemDict)
        return make_response(itemResults, 200)
    except Exception as e:
        print(e)
        return make_response('Error retrieving items in list', 401)


@app.route('/getItems', methods=['GET'])
@token_required
def getItems(user):
    try:
        with Session() as session:
            q = request.args['q']
            items = session.query(Item).filter(Item.itemname.contains(q))
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


@app.route('/<int:listId>/addItem', methods=['POST'])
@token_required
def addItem(user, listId:int):
    '''
    adds item to a list for a particular user
    '''
    try:
        returnItemId = None
        with Session() as session:
            # checking user exists
            if session.query(User).filter(User.user_id == user.user_id).count() == 0:
                return make_response({'message':'User with id {} not found'.format(user.user_id)}, 400)
            if session.query(List).filter(List.list_id == listId).count() == 0:
                return make_response({'message':'List with id {} not found'.format(listId)}, 400)
            body = request.get_json()
            newItem = Item(item_name = body['itemName'])
            session.add(newItem)
            session.flush()
            userListId = session.query(UserList.user_list_id).filter(UserList.user_id == user.user_id and UserList.list_id == listId).first() # create issue, weird code
            newUserListItem = UserListItem(user_list_id = userListId[0], item_id = newItem.item_id, quantity = body['quantity'])
            session.add(newUserListItem)
            session.flush()
            returnItemId = newItem.item_id
            session.commit()
        return make_response('Item {} added successfully to {}'.format(returnItemId, listId), 200)
    except Exception as e:
        print(e)
        return make_response('Error adding Item', 400)


@app.route('/<int:listId>/getPrices', methods=['GET'])
@token_required
def getPrices(user, listId:int):
    
    try:
        with Session() as session:
            zip = request.args.get('zipcode')
            userListId = session.query(UserList.user_list_id).filter(UserList.user_id == user.user_id and UserList.list_id == listId).scalar()
            print(userListId)
            userListItems = session.query(UserListItem).filter(UserListItem.user_list_id == userListId).all()
            print(userListItems)
            results = []
            for retailer in retailers:
                storeId = retailer.getNearestStoreId(zip)
                prices = dict()
                prices['store_name'] = str(retailer)
                prices['total_price'] = 0
                prices['storeId'] = storeId
                prices['distanceInMiles'] = random.randint(0, 20) # needs to be replaced with actual service getting distance
                prices['allItemsAvailable'] = True
                for userListItem in userListItems:
                    item = session.query(Item).join(UserListItem, Item.item_id == UserListItem.item_id).\
                    filter(UserListItem.item_id == userListItem.item_id).scalar()
                    searchResults =  retailer.getProductsInNearByStore(item.item_name, zip)
                    if len(searchResults) > 0:
                        minPriceItem = min(searchResults, key=lambda x:x['itemPrice'])
                        prices['total_price'] += minPriceItem['itemPrice']*userListItem.quantity
                    else:
                        prices['allItemsAvailable'] = False
                results.append(prices)                               
            return make_response(results, 200)
    except Exception as e:
        print(e)
        return make_response({'message':'Unable to get prices'}, 400)


@app.route('/<int:listId>/<int:storeId>/getPrices', methods=['GET'])
@token_required
def getStorePrices(user, listId:int, storeId:int):
    try:
        with Session() as session:
            userListId = session.query(UserList.user_list_id).filter(UserList.user_id == user.user_id and UserList.list_id == listId).one()
            itemIds = session.query(Item.item_id).filter(Item.user_list_id == userListId)
            itemStorePrices = session.query(Price).join(Item, Item.user_list_item_id == Price.user_list_item_id) \
            .filter(Price.item_id.in_(itemIds) and Price.store_id == storeId)
            results = []
            for price in itemStorePrices:
                ItemStorePrice = dict()
                ItemStorePrice['itemName'] = price.item_name
                ItemStorePrice['storeId'] = price.store_id
                ItemStorePrice['totalPrice'] = price.rec_product_price
                results.append(ItemStorePrice)
        return make_response(results, 200)
    except Exception as e:
        print(e)
        return make_response({'message':'Unable to get prices'}, 400)


@app.route('/<int:listId>/<int:itemId>', methods=['DELETE'])
@token_required
def removeItem(user, listId, itemId):
    try:
        with Session() as session:
            item = session.query(Item).filter(Item.item_id == itemId).one()
            # listItems = session.query(List).filter(List.user_id == userId and List.list_id == listId and List.item_id == itemId).all()
            # for listItem in listItems:
            #     session.delete(listItem)
            session.delete(item)
            session.commit()
        return make_response({'message': 'Item {} deleted successfully'\
            .format(item.item_id)}, 200)
    except Exception as e:
        print(e)
        return make_response('unable to remove item from list', 500)

@app.route('/intro')
def index():
    #print('Request for index page received')
    return {"welcomeMessage": "Hi there! We're currently getting things setup and should be ready for use in a few weeks!"}

# Only for testing


@app.route('/getProducts', methods=['GET'])
def getProducts():
    try:
        args = request.args
        items:List[Retailer] = sum([retailer.getProductsInNearByStore(args['q'], args['zipcode']) for retailer in retailers], start =[])
        print(len(items))
        items = getUniqueItems(items, k='itemName')
        print(len(items))
        return make_response(items, 200)
    except:
        return make_response({'message:Error retrieving products'}, 400)


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

@app.route('/targetTest')
def targetTestEndPoint():
   args = request.args
   t = Target()
   
   return t.getProductsInNearByStore(args["q"], args["zipcode"])

@app.route('/krogerTest',methods=['GET'])
def krogerTestEndpoint():
    k = Kroger()
    args = request.args
    return k.getProductsInNearByStore(args["q"], args["zipcode"])

    
# TODO: Need to remove the below endpoint. Only used for mocking frontend.
@app.route('/getItems')
def test():
    with open('./data.json', 'r') as j:     
        out = json.loads(j.read())
    return out 

# TODO: Need to remove the below endpoint. Only used for mocking frontend.
@app.route('/getStoreItems')
def test2():
    with open('./data.json', 'r') as j:     
        out = json.loads(j.read())
    return out 

# TODO: Need to remove the below endpoint. Only used for mocking frontend.
@app.route("/getPrices/<int:listId>")
def test1(listId: int):
    print("List id requested is",listId)
    return [
        {
            "store":"walmart",
            "price": 20
        },
        {
            "store": "target",
            "price": 21.21
        },
        {
            "store": "walgreens",
            "price": 11.21
        },
        {
            "store": "kroger",
            "price": 11.21
        },
        
    ]

if __name__ == '__main__':
    app.run()

