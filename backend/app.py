from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, make_response
from backend.Retailers.walmart.getProductinfo import Walmart
from backend.Retailers.walgreens.getProductInfo import *
from sqlite_test import create_connection, create_list, createUser, getUserId

app = Flask(__name__)

# read path from config
conn = create_connection('pythonsqlitedb')

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
@app.route('/addUser', methods=['POST'])
def add_user():
    body = request.get_json()
    user = (body.user.userName, body.user.password, body.user.firstName, body.user.lastName)
    createUser(conn, user)
    return make_response('User added', 200)


# only for testing
@app.route('/addList/<str:userName>', methods=['POST'])
def add_list(userName:str):
    body = request.get_json()
    userId = getUserId(userName)
    list = (body.list.name, userId)
    create_list(conn, list)
    return make_response('User added', 200)


if __name__ == '__main__':
    app.run(debug=True)
