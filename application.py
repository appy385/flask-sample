from flask import Flask, request
from application import *
from application.models import Book
from flask_cors import CORS, cross_origin
from  sqlalchemy.sql.expression import func
from flask_mail import Mail, Message
# Elastic Beanstalk initalization
#application = Flask(__name__)
application.debug=True
CORS(application)
mail = Mail()

application.config['MAIL_SERVER']='smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'contactbookaholics@gmail.com'
application.config['MAIL_PASSWORD'] = 'bookaholics@123'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
mail.init_app(application)


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


@application.route('/contact',methods = ['POST'])
def contact():
        print(request);
        send_message(request.json)
        return {
            "status": {"code": 200}
        }

def send_message(message):
    print(message['email'])
    msg = Message(subject="feedback for bookaholics", sender='contactbookaholics@gmail.com', recipients=['contactbookaholics@gmail.com'])
    msg.body = """
          From: %s <%s>
          %s
          """ % (message['name'], message['email'], message['message'])
    mail.send(msg)


if __name__ == '__main__':
    application.run()
