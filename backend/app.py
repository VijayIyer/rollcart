from distutils.log import debug
from multiprocessing import Pool, get_context, cpu_count
import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from Retailers import config
from flask import Flask, request, make_response
from Retailers.util import getUniqueItems
from Retailers.kroger.getProductInfo import Kroger
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
import datetime
import logging
from flask.logging import default_handler
from logging.config import dictConfig
import os

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
             "file": {
                "class": "logging.FileHandler",
                "filename": os.path.join("logs", "flask.log"),
                "formatter": "default",
            },
             "size-rotate": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join("logs", "rotate.log"),
                "maxBytes": 1000000,
                "backupCount": 5,
                "formatter": "default",
            },
        },
        "root":{
                "level":"WARNING",
                "handlers":["console", "size-rotate"]
            }
    }
)

app = Flask(__name__)

# Using a production configuration
#app.config.from_object('config.ProdConfig')

# Using a development configuration
app.config.from_object(config.DevConfig)
CORS(app)
app.logger.removeHandler(default_handler)

DB_PARAMS = app.config['DATABASE_PARAMS']
db_connect_string="mysql+pymysql://{}:{}@{}:{}/{}".format(DB_PARAMS['USER_NAME'], DB_PARAMS['PASSWORD'], DB_PARAMS['SERVER_NAME'], DB_PARAMS['PORT_NUMBER'], DB_PARAMS['NAME'])
ssl_args = {'ssl': {'ca':'DigiCertGlobalRootCA.crt.pem'}}


engine = create_engine(db_connect_string, connect_args=ssl_args)
Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(engine, reflect=True)
User = Base.classes.user
List = Base.classes.list
UserList = Base.classes.userlist
Item = Base.classes.item
UserListItem = Base.classes.userlistitem
Store = Base.classes.store
Price = Base.classes.price



retailers = [Target(), Walmart(), Walgreens(), Kroger()]

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
            if check_password_hash(existingUser.password, auth.password):
                token = jwt.encode({'user_id':existingUser.user_id, 'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=2)},app.config['SECRET_KEY'])
                return jsonify({'message':'login successful', 'token':token, 'favorite_list_id':existingUser.favorite_list_id, 'cart_list_id':existingUser.cart_list_id
                                }), 201                
            else:
                return make_response({'message':'Invalid Credentials'}, 403)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'Unknown Error, check logs'}, 400)


@app.route('/register', methods=['POST'])
def register():
    
    try:
        with Session() as session:
            user = request.get_json()
            existingUserCount = session.query(User).filter(User.user_name == user['username']).count()
            if existingUserCount > 0:
                return make_response({'message':'User already exists'}, 409)
            hashed_password = generate_password_hash(user['password'], method='sha256')
            newUser = User(user_name = user['username']
                        , password = hashed_password
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
            app.logger.info('added user {} to users table'.format(newUser.user_id))
        return make_response(response, 201)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'Unknown Error, check logs'}, 400)


@app.route('/logout', methods=['POST'])
def logout():
    try:
        with Session() as session:
            body = request.get_json()
            if session.query(User).filter(User.user_name == body['userName']).count() == 0:
                return make_response({'message':'No such User {} found in database'.format(body['userName'])})
            else:
                
                loggedInUser = session.query(User).filter(User.user_name == body['userName']).one()
                app.logger.info('user {} loggedin'.format(User.user_name))
                return make_response({'message':'User logged out successfully'}, 200)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'Unknown Error, check logs'}, 500)


@app.route('/addList', methods=['POST'])
@token_required
def addList(user):
    try:
        returnListId = None
        with Session() as session:
            body = request.get_json()
            if session.query(User).filter(User.user_id == user.user_id).count() == 0:
                return make_response({'message':'User with id {} not found'.format(user.user_id)}, 400)
            newList = List(list_name = body['listname'])
            session.add(newList)
            session.flush()
            newUserList = UserList(user_id = user.user_id, list_id = newList.list_id)
            session.add(newUserList)
            session.flush()
            returnListId = newUserList.list_id
            session.commit()
            app.logger.info('added list {} to lists table'.format(newList.list_id))
        return make_response({'listId': returnListId}, 201)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'Unknown Error, check logs'}, 500)


@app.route('/getLists', methods=['GET'])
@token_required
def getLists(user):
    '''
    Gets List Names created by user with userid provided in the request
    '''
    try:
        with Session() as session:
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
        app.logger.error('{} failed with exception:{}'.format(request.path), exc_info=True)
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
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'get lists for item {} failed'.format(itemId)}, 500)


@app.after_request
def logAfterRequest(response):

    app.logger.info(
        "path: %s | method: %s | status: %s >>> %s",
        request.path,
        request.method,
        response.status,
        response
    )

    return response


@app.route('/getListItems/<int:listId>', methods=['GET'])
@token_required
def getListItems(user, listId:int):
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
                itemDict['itemThumbnail'] = item.item_thumbnail
                itemResults.append(itemDict)
        return make_response(itemResults, 200)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
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
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
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
                        first()
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
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response('Error adding Item', 400)


@app.route('/<int:listId>', methods=['DELETE'])
@token_required
def removeList(user, listId:int):
    '''
    remove list specified by listid parameter
    '''
    try:
        with Session() as session:
            list = session.query(List).join(UserList, UserList.list_id == List.list_id)\
                .join(User, User.user_id == UserList.user_id)\
                .filter(and_(User.user_id == user.user_id, UserList.list_id==listId)).one()
            session.delete(list)
            session.commit()
        return make_response({'message':'List {} deleted successfully'.format(listId)}, 200)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'Error Deleting List'}, 500)

def getMinPriceForItem(retailerWithArgs):
    retailer, name, image, quantity, zip, lat, long = retailerWithArgs
   
    searchResults = retailer.getProductsInNearByStore(name, zip, lat,long)
    if len(searchResults) == 0:
        return {'store_name':str(retailer),'name':name, 'image':image , 'price':0, 'available':False}
    else:
        minPriceItem = min(searchResults, key=lambda x:x['itemPrice'])
        return {'store_name':str(retailer),'name':name, 'resultName':minPriceItem['itemName'], 'image':minPriceItem['itemThumbnail'] , 'productPageUrl':minPriceItem['productPageUrl'],  'price':minPriceItem['itemPrice']*quantity, 'available':True}

@app.route('/<int:listId>/getPrices', methods=['GET'])
@token_required
def getPrices(user, listId:int):
    try:
        with Session() as session:
            zip = request.args.get('zipcode')
            lat = request.args.get('lat')
            long = request.args.get('long')
            userListId = session.query(UserList.user_list_id).filter(and_(UserList.user_id == user.user_id, UserList.list_id == listId)).scalar()
            itemsWithQuantity = session.query(Item.item_name, Item.item_thumbnail, UserListItem.quantity).\
                join(UserListItem, Item.item_id == UserListItem.item_id).\
                    filter(UserListItem.user_list_id == userListId).all()
            retailerWithArgs = sum([[(retailer, item.item_name, item.item_thumbnail, item.quantity, zip, lat, long)\
                for item in itemsWithQuantity]\
                for retailer in retailers],\
                start=[])
            itemResults = []
            app.logger.info('processing on following list will be parallelized:{}'.format(retailerWithArgs))
            with Pool(cpu_count() - 1) as p:
                itemResults = [x for x in p.map(getMinPriceForItem, retailerWithArgs)]

            nearestStore = {}
            for retailer in retailers:
                nearestStore[str(retailer)] = retailer.getNearestStore(zip, lat, long)
            
            retailerPriceTotals = [{'store_name':str(retailer), 'total_price':0, 'unavailableItems':[], 'distanceInMiles':nearestStore[str(retailer)]['currDistance'], 'latitude' : nearestStore[str(retailer)]['latitude'],'longitude' : nearestStore[str(retailer)]['longitude']}\
                 for retailer in retailers]
            storeIds = {str(retailer):session.query(Store.store_id).filter(Store.store_name == str(retailer)).scalar() for retailer in retailers}
            for itemResult in itemResults:
                retailPriceTotal = [x for x in retailerPriceTotals if x['store_name'] == itemResult['store_name']][0]
                if itemResult['available']:
                    retailPriceTotal['total_price'] += itemResult['price']
                    userListItemId = session.query(UserListItem.user_list_item_id)\
                        .join(Item, Item.item_id == UserListItem.item_id)\
                        .filter(and_(UserListItem.user_list_id == userListId, Item.item_name == itemResult['name'])).scalar()
                    if session.query(Price).filter(and_(Price.user_list_item_id==userListItemId, Price.store_id == storeIds[retailPriceTotal['store_name']])).count() == 0:
                        newPrice = Price(user_list_item_id=userListItemId\
                                , price=itemResult['price']\
                                , store_id=storeIds[retailPriceTotal['store_name']]\
                                , item_url=itemResult['productPageUrl']\
                                , item_image=itemResult['image'])
                        session.add(newPrice)
                    else:
                        existingPrice = session.query(Price).filter(and_(Price.user_list_item_id==userListItemId, Price.store_id == storeIds[retailPriceTotal['store_name']]))
                        existingPrice.price=itemResult['price']
                        existingPrice.item_url=itemResult['productPageUrl']
                        existingPrice.item_image=itemResult['image']
                else:
                    retailPriceTotal['unavailableItems'].append({
                        'item_name':itemResult['name'],
                        'item_thumbnail':itemResult['image']
                    })
            session.commit()
            return make_response(retailerPriceTotals, 200)
    except Exception as e:      
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'Unable to get prices'}, 400)


@app.route('/<int:listId>/<string:storeName>/getPrices', methods=['GET'])
@token_required
def getStorePrices(user, listId:int, storeName:str):
    try:
        with Session() as session:
            storeId = session.query(Store.store_id).filter(Store.store_name == storeName).scalar()
            userListId = session.query(UserList.user_list_id).filter(and_(UserList.user_id == user.user_id, UserList.list_id == listId)).scalar()
            userListItemIds = session.query(UserListItem.user_list_item_id).filter(UserListItem.user_list_id == userListId)            
            itemStorePrices = session.query(Price).join(UserListItem, UserListItem.user_list_item_id == Price.user_list_item_id) \
            .filter(and_(Price.user_list_item_id.in_(userListItemIds), Price.store_id==storeId))
            
            results = []
            for price in itemStorePrices:
                itemStorePrice = dict()
                itemName = session.query(Item.item_name).join(UserListItem, Item.item_id == UserListItem.item_id)\
                    .filter(UserListItem.user_list_item_id == price.user_list_item_id).scalar()
            
                itemStorePrice['itemName'] = itemName
                itemStorePrice['storeId'] = price.store_id
                itemStorePrice['totalPrice'] = price.price
                itemStorePrice['item_image'] = price.item_image
                itemStorePrice['item_url'] = price.item_url
                results.append(itemStorePrice)
        return make_response(results, 200)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'Unable to get prices'}, 400)


@app.route('/<int:listId>/<int:itemId>', methods=['DELETE'])
@token_required
def removeItem(user, listId, itemId):
    try:
        with Session() as session:
            userListItem = session.query(UserListItem).join(UserList, UserList.user_list_id == UserListItem.user_list_id).\
                filter(and_(UserListItem.item_id==itemId,UserList.list_id == listId,UserList.user_id == user.user_id))\
                .one()
            session.delete(userListItem)
            session.commit()
        return make_response({'message': 'Item {} deleted successfully'\
            .format(userListItem.item_id)}, 200)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response('unable to remove item from list', 500)



@app.route('/intro')
def index():
    #print('Request for index page received')
    return {"welcomeMessage": "Hi there! We're currently getting things setup and should be ready for use in a few weeks!"}

def getProductsInStore(retailerAndArgs):
    retailer, q, zipcode, lat, long = retailerAndArgs
    return retailer.getProductsInNearByStore(q, zipcode, lat, long)

@app.route('/getProducts', methods=['GET'])
@token_required
def getProducts(user):
    try:
        args = request.args
        q, zipcode, lat, long = args.get('q'), args.get('zipcode'), args.get('lat'), args.get('long')
        with Pool(cpu_count()-1) as p:
            items:List[Retailer] = sum(p.map(getProductsInStore, [(retailer, q, zipcode, lat, long) for retailer in retailers]), start=[])
        items = getUniqueItems(items, k='itemName')
        return make_response(items, 200)
    except Exception as e:
        app.logger.error('{} failed with exception:{}'.format(request.path, e), exc_info=True)
        app.logger.exception('exception in {}'.format(request.path))
        return make_response({'message':'Error retrieving products'}, 400)


@app.route('/walmartTest', methods=['GET'])
def walmartTestEndPoint():
    args = request.args
    w = Walmart()
    return w.getProductsInNearByStore(args["q"], args["zipcode"], None, None)


@app.route('/walgreensTest', methods=['GET'])
def walgreensTestEndPoint():
    args = request.args
    w = Walgreens()
    return w.getProductsInNearByStore(args["q"], args["zipcode"],None, None)

@app.route('/targetTest')
def targetTestEndPoint():
   args = request.args
   t = Target()
   
   return t.getProductsInNearByStore(args["q"], args["zipcode"],None, None)

@app.route('/krogerTest',methods=['GET'])
def krogerTestEndpoint():
    k = Kroger()
    args = request.args
    return k.getProductsInNearByStore(args["q"], args["zipcode"],None, None)

if __name__ == '__main__':
    app.run()
