from distutils.log import debug
from flask import Flask, render_template, request, redirect, url_for, send_from_directory


app = Flask(__name__)


@app.route('/intro')
def index():
   #print('Request for index page received')
   return {"welcomeMessage" : "Hi there! We're currently getting things setup and should be ready for use in a few weeks!"}

if __name__ == '__main__':
   app.run(debug=True)