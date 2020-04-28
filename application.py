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
                    {"name":"HEY!! Long Walk to freedom",
                    "author":"Nelson Mandela"
                    },
                    ]
                }
            }
@application.route("/<genre>")
def genre(genre):
    books= Book.query.filter_by(genre=genre).order_by(func.rand()).limit(10).all()
    booksList=[]

    for b in books:
        book = {"book_id": b.book_id, "goodreads_book_id": b.goodreads_book_id, "authors": b.authors, "isbn": b.isbn, "title": b.title,
        "average_rating": b.average_rating, "image_url": b.image_url, "genre": b.genre }
        booksList.append(book)

    booksDict={ "bookslist": booksList}

    return booksDict




if __name__ == '__main__':
    application.run()
