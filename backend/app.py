from distutils.log import debug
from time import time
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from backend.Retailers.walmart.getProductinfo import Walmart
from backend.Retailers.walgreens.getProductInfo import *
# from sqlite_test import create_connection, create_list, createUser, getUserId
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
import sqlalchemy
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://rollcartadmin:!grocerybudget1@rollcartdb.mysql.database.azure.com:3306/rollcarttest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

#################################################
# Database Setup
#################################################
sqlUrl = sqlalchemy.engine.url.URL(
    drivername="mysql+pymysql",
    username='rollcartadmin',
    password='!grocerybudget1',
    host='rollcartdb.mysql.database.azure.com',
    port=3306,
    database='rollcarttest',
    query={"ssl_ca": "DigiCertGlobalRootCA.crt.pem"},
)
engine = create_engine(sqlUrl)
# engine = create_engine("mysql+pymysql://rollcartadmin:!grocerybudget1@rollcartdb.mysql.database.azure.com:3306/rollcarttest"
Session = sessionmaker(bind=engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
User = Base.classes.user
List = Base.classes.list
ItemDetails = Base.classes.itemdetails
ListDetails = Base.classes.listdetails
Price = Base.classes.price

# with app.app_context:
#     db.Model.metadata.reflect(bind=db.engine,schema='rollcarttest')

# with app.app_context():
#     db.reflect()


# class ListDetails(db.Model):
#     '''deal with an existing table'''
#     __tablename__ = 'listdetails'
#     # id = db.Column('')


@app.route('/getUsers', methods=['GET'])
def getUsers():
    results = Session.query(User).all()
    for r in results:
        print(r.user_name)
    return 'Users queried'

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
