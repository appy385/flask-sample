from flask import Flask
from application import *
from application.models import Book
from flask_cors import CORS, cross_origin
from  sqlalchemy.sql.expression import func

# Elastic Beanstalk initalization
# application = Flask(__name__)
application.debug=True
CORS(application)



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
@application.route("/<genre>")
def genre(genre):
    books=db.session.query(Book).limit(10)
    for b in books:
        print(b.average_rating)
    # books= Book.query.order_by(func.rand()).limit(1)
    # print()
    return "hello world"




if __name__ == '__main__':
    application.run()
