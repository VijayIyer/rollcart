from distutils.log import debug
from flask import Flask, request
from backend.Retailers.walmart.getProductinfo import Walmart
from backend.Retailers.walgreens.getProductInfo import *
from backend.Retailers.target.getProductInfo import Target

app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)
