import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@book-recommender-db.ckt9u6nlihrw.us-east-1.rds.amazonaws.com:3306/book-recommender-db'
db = SQLAlchemy(application)

# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

@application.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    application.run()
