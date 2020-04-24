from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

application = Flask(__name__)
CORS(application)
#db = SQLAlchemy(application)



@application.route("/")
def hello():
    return "hello world!!"



if __name__ == '__main__':
    application.run()
