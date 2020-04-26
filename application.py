from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_cors import CORS, cross_origin

application = Flask(__name__)
application.debug=True
CORS(application)
application.config.from_object('config')
db = SQLAlchemy(application)


@application.route("/")
def bookList():
    return { "status": { "code": 200},
            "response": {
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
            }



if __name__ == '__main__':
    application.run()
