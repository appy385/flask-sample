from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
CORS(application)
#db = SQLAlchemy(application)



@application.route("/")
def hello():
    return "hello world!!"



if __name__ == '__main__':
    application.run()
