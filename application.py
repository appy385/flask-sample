from flask import Flask
# from config import Config
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
CORS(application)
# application.config.from_object(Config)
db = SQLAlchemy(application)



@application.route("/")
def BooksList():
    return  {
                    "bookslist": [ {"name":"Wings of Fire",
                    "author":"A P J Abdul Kalam, Arun Tiwari"
                    },
                    {"name":"Harry Potter and the Half-Blood Prince",
                    "author":"J K Rowling"
                    },
                    {"name":"Long Walk to freedom",
                    "author":"Nelson Mandela"
                    },
                    {"name":"Harry Potter and the Half-Blood Prince",
                    "author":"J K Rowling"
                    } ]
                }



if __name__ == '__main__':
    application.run()
