from flask import Flask, request
from models import Books, BookTags
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from flask_mail import Mail, Message

application = Flask(__name__)
application.config.from_object('config')
db = SQLAlchemy(application)
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
    book_tag = db.session.query(BookTags).filter_by(genre=genre).subquery()
    result = db.session.query(Books,book_tag.c.genre).join(book_tag,Books.goodreads_book_id == book_tag.c.goodreads_book_id).order_by(func.rand()).limit(10).all()

    booksList=[]

    for b in result:
        book={}
        book['genre'] =  b.genre
        book['book_id'] = b[0].book_id
        book['goodreads_book_id'] = b[0].goodreads_book_id
        book['authors'] = b[0].authors
        book['isbn'] = b[0].isbn
        book['title'] = b[0].title
        book['average_rating'] = b[0].average_rating
        book['image_url'] = b[0].image_url
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
