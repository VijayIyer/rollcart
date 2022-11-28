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
from Retailers.MockRetailer.getProductInfo import MockRetailer
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from flask.json import jsonify
from functools import wraps
import random
import traceback
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


## retailers list
retailers = [Target(), Walgreens(), Kroger(), Walmart()]
# retailers = [MockRetailer(), MockRetailer(), MockRetailer(), MockRetailer()]

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
                return jsonify({'message':'login successful', 'token':token, 'favorite_list_id':existingUser.favorite_list_id, 'cart_list_id':existingUser.cart_list_id
                                }), 201                
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
            newFavoriteList = List(list_name='Favorites')
            newCartList = List(list_name='Cart')
            
            session.add(newUser)
            session.add(newFavoriteList)
            session.add(newCartList)
            session.flush()
            newUserFavoriteList = UserList(user_id = newUser.user_id, list_id = newFavoriteList.list_id)
            newUserCartList = UserList(user_id = newUser.user_id, list_id = newCartList.list_id)
            session.add(newUserFavoriteList)
            session.add(newUserCartList)
            response = {'message':'Registration Successful'
            , 'favorite_list_id':newFavoriteList.list_id
            , 'cart_list_id':newCartList.list_id}
            newUser.favorite_list_id = newFavoriteList.list_id
            newUser.cart_list_id = newCartList.list_id
            session.commit()
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
            listIds = session.query(UserList.list_id).join(User, User.user_id == UserList.user_id).\
            filter(and_(UserList.user_id == user.user_id, UserList.list_id != User.favorite_list_id,  UserList.list_id != User.cart_list_id))
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


@app.route('/<int:itemId>/getLists', methods=['GET'])
@token_required
def getListsForItem(user, itemId):
    '''
    Gets List Names created by user with userid provided in the request
    '''
    try:
        with Session() as session:
            lists = session.query(List).join(UserList, UserList.list_id == List.list_id) \
            .join(UserListItem, UserListItem.user_list_id == UserList.user_list_id) \
            .filter(and_(UserList.user_id == user.user_id, UserListItem.item_id == itemId)).all()
            
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
def getListsForItem(user, itemId):
    '''
    Gets List Names created by user with userid provided in the request
    '''
    try:
        with Session() as session:
            lists = session.query(List).join(UserList, UserList.list_id == List.list_id) \
            .join(UserListItem, UserListItem.user_list_id == UserList.user_list_id) \
            .filter(and_(UserList.user_id == user.user_id, UserListItem.item_id == itemId)).all()
            
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
# @token_required
def getListItems(listId:int):
    '''
    Gets items in the list with listid provided in the query
    '''
    try:
        with Session() as session:
            userListId = session.query(UserList.user_list_id).filter(UserList.list_id == listId).scalar()
            itemIds = session.query(UserListItem.item_id).filter(UserListItem.user_list_id == userListId)
            items = session.query(Item).filter(Item.item_id.in_(itemIds)).all()
            itemResults =[]
            for item in items:
                userListItem = session.query(UserListItem).filter(and_(UserListItem.user_list_id == userListId, UserListItem.item_id == item.item_id)).scalar()
                itemDict = dict()
                itemDict['itemId'] = item.item_id
                itemDict['itemName'] = item.item_name
                itemDict['quantity'] = userListItem.quantity
                itemResults.append(itemDict)
        return make_response(itemResults, 200)
    except Exception as e:
        print("error is:",e)
        traceback.print_exc()
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
            body = request.get_json()
            userListId = session.query(UserList.user_list_id).\
                    filter(and_(UserList.user_id == user.user_id, UserList.list_id == listId)).\
                        first() # create issue, weird code
            # check if item exists
            if session.query(Item).filter(Item.item_name == body['item_name']).count() == 0:
                newItem = Item(item_name = body['item_name'])
                session.add(newItem)
                session.flush()
                returnItemId = newItem.item_id
                
                newUserListItem = UserListItem(user_list_id = userListId[0], item_id = returnItemId, quantity = body['quantity'])
                session.add(newUserListItem)
                session.flush()
                session.commit()
            else:
                returnItemId = session.query(Item.item_id).filter(Item.item_name == body['item_name']).scalar()
                # check if item exists in same list
                if session.query(UserListItem).join(UserList, UserList.user_list_id\
                     == UserListItem.user_list_id)\
                    .filter(and_(UserListItem.item_id == returnItemId\
                         ,UserList.user_id == user.user_id\
                         ,UserList.list_id == listId)).count() == 0:
                    newUserListItem = UserListItem(user_list_id = userListId[0], item_id = returnItemId, quantity = body['quantity'])
                    session.add(newUserListItem)
                    session.commit()
                else:
                    userListItem = session.query(UserListItem).join(UserList, UserList.user_list_id == UserListItem.user_list_id)\
                    .filter(and_(UserListItem.item_id == returnItemId
                    , UserList.user_id == user.user_id
                    , UserList.list_id == listId)).one()
                    userListItem.quantity = body['quantity']
                    session.commit()

        return make_response('Item {} added/updated in list {}'.format(returnItemId, listId), 201)
    except Exception as e:
        print(e.with_traceback(None))
        return make_response('Error adding Item', 400)


@app.route('/<int:listId>', methods=['DELETE'])
@token_required
def removeList(user, listId:int):
    '''
    remove list specified by listid parameter
    '''
    try:
        with Session() as session:
            list = session.query(List).filter(List.list_id==listId).one()
            session.delete(list)
            session.commit()
        return make_response({'message':'List {} deleted successfully'.format(listId)}, 200)
    except Exception as e:
        print(e)
        return make_response('Error Deleting List', 500)



@app.route('/<int:listId>/getPrices', methods=['GET'])
@token_required
def getPrices(user, listId:int):
    
    try:
        with Session() as session:
            zip = request.args.get('zipcode')
            lat = request.args.get('lat')
            long = request.args.get('long')
            userListId = session.query(UserList.user_list_id).filter(and_(UserList.user_id == user.user_id, UserList.list_id == listId)).scalar()
            userListItems = session.query(UserListItem).filter(UserListItem.user_list_id == userListId).all()
            results = []
            for retailer in retailers:
                try:
                    storeId = retailer.getNearestStoreId(zip,lat,long)
                    prices = dict()
                    prices['store_name'] = str(retailer)
                    prices['total_price'] = 0
                    prices['storeId'] = storeId
                    prices['distanceInMiles'] = retailer.getNearestStoreDistance(zip,lat,long) # needs to be replaced with actual service getting distance
                    prices['allItemsAvailable'] = True
                
                    
                    for userListItem in userListItems:
                        item = session.query(Item).join(UserListItem, Item.item_id == UserListItem.item_id).\
                        filter(UserListItem.item_id == userListItem.item_id).scalar()
                        searchResults =  retailer.getProductsInNearByStore(item.item_name, zip, lat,long)
                        if len(searchResults) > 0:
                            minPriceItem = min(searchResults, key=lambda x:x['itemPrice'])
                            prices['total_price'] += minPriceItem['itemPrice']*userListItem.quantity
                            # adding price information to table
                            storeId = session.query(Store.store_id).filter(Store.store_name == str(retailer))
                            # print(str(retailer))
                            # check if price information for item already exists in table
                            
                            if session.query(Price).filter(Price.user_list_item_id==userListItem.user_list_item_id, Price.store_id == storeId).count() == 0:
                                print('this item\'s price not yet added')
                                newPrice = Price(user_list_item_id=userListItem.user_list_item_id,\
                                    price=minPriceItem['itemPrice']*userListItem.quantity\
                                        ,store_id=storeId, item_url=minPriceItem['productPageUrl']\
                                            ,item_image=minPriceItem['itemThumbnail'])
                                
                                session.add(newPrice)
                            else:
                                existingPrice = session.query(Price).filter(Price.user_list_item_id==userListItem.user_list_item_id)
                                existingPrice.price=minPriceItem['itemPrice']*userListItem.quantity
                                existingPrice.item_url=minPriceItem['productPageUrl']
                                existingPrice.item_image=minPriceItem['itemThumbnail']
                            
                        else:
                            prices['allItemsAvailable'] = False
                    session.commit()
                    results.append(prices)
                    # adding results to database tables
                except Exception as e:
                    
                    print('retailer {} did not return any items:{}'.format(str(retailer), e))
                    continue

            return make_response(results, 200)
    except Exception as e:
        print(e)
        return make_response({'message':'Unable to get prices'}, 400)


@app.route('/<int:listId>/<string:storeName>/getPrices', methods=['GET'])
@token_required
def getStorePrices(user, listId:int, storeName:str):
    try:
        with Session() as session:
            storeId = session.query(Store.store_id).filter(Store.store_name == storeName)
            
            userListId = session.query(UserList.user_list_id).filter(and_(UserList.user_id == user.user_id, UserList.list_id == listId)).scalar()
            # print(userListId)
            userListItemIds = session.query(UserListItem.user_list_item_id).filter(UserListItem.user_list_id == userListId)
            # print(list(userListItemIds))
            itemStorePrices = session.query(Price).join(UserListItem, UserListItem.user_list_item_id == Price.user_list_item_id) \
            .filter(and_(Price.user_list_item_id.in_(userListItemIds), Price.store_id==storeId))
            
            # print(itemStorePrices)
            results = []
            for price in itemStorePrices:
                itemStorePrice = dict()
                itemName = session.query(Item.item_name).join(UserListItem, Item.item_id == UserListItem.item_id)\
                    .filter(UserListItem.user_list_item_id == price.user_list_item_id).scalar()
                # print(itemName)
                itemStorePrice['itemName'] = itemName
                itemStorePrice['storeId'] = price.store_id
                itemStorePrice['totalPrice'] = price.price
                itemStorePrice['item_image'] = price.item_image
                itemStorePrice['item_url'] = price.item_url
                results.append(itemStorePrice)
        return make_response(results, 200)
    except Exception as e:
        print(e)
        return make_response({'message':'Unable to get prices'}, 400)


@app.route('/<int:listId>/<int:itemId>', methods=['DELETE'])
@token_required
def removeItem(user, listId, itemId):
    try:
        with Session() as session:
            userListItem = session.query(UserListItem).join(UserList, UserList.user_list_id == UserListItem.user_list_id).\
                filter(UserListItem.item_id==itemId)\
                .one()
            session.delete(userListItem)
            session.commit()
        return make_response({'message': 'Item {} deleted successfully'\
            .format(userListItem.item_id)}, 200)
    except Exception as e:
        print(e)
        return make_response('unable to remove item from list', 500)



@app.route('/intro')
def index():
    #print('Request for index page received')
    return {"welcomeMessage": "Hi there! We're currently getting things setup and should be ready for use in a few weeks!"}

# Only for testing


@app.route('/getProducts', methods=['GET'])
@token_required
def getProducts(user):
    try:
        args = request.args
        items:List[Retailer] = sum([retailer.getProductsInNearByStore(args['q'], args['zipcode']) for retailer in retailers], start =[])
        print(len(items))
        items = getUniqueItems(items, k='itemName')
        print(len(items))
        return make_response(items, 200)
    except:
        return make_response({'message':'Error retrieving products'}, 400)


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

