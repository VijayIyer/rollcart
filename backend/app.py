from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from backend.Retailers.walmart.getProductinfo import Walmart


app = Flask(__name__)


@app.route('/intro')
def index():
   #print('Request for index page received')
   return {"welcomeMessage" : "Hi there! We're currently getting things setup and should be ready for use in a few weeks!"}

# Only for testing
@app.route('/walmartTest',methods=['GET'])
def walmartTestEndPoint():
   args = request.args
   w = Walmart()
   return w.getProductsInNearByStore(args["q"],args["zipcode"])

if __name__ == '__main__':
   app.run(debug=True)