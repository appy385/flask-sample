from app import *
from app.models import Books, BookTags
from app.helper import *
from app.globals import *
from sqlalchemy.sql.expression import func
import os
import pandas as pd
import json




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
    return books(result)


@application.route('/contact',methods = ['POST'])
def contact():
        print(request);
        send_message(request.json,mail)
        return {
            "status": {"code": 200}
        }

@application.route('/title')
def bookTitle():
    path = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_csv(path +'/csv/books.csv')
    df.dropna(subset=['original_title'],inplace=True)
    book_titles = df['original_title'].tolist()
    #book_titles = json.dumps(book_titles)
    return {"titles":book_titles}








@application.route('/goodreads_id/<username>')
def goodreads(username):
    uri = goodreads_url + username
    response = sendRequest(uri,params)

    if response.status_code==200:
        return parseXML(response)

    elif response.status_code==401:
        error = { 'status': { 'code': response.status_code }, 'error_message' : 'Unauthorized access.Please Try again!' }
        return error

    else:
        error = { 'status': { 'code': response.status_code }, 'error_message' : 'Goodreads User ID does not exist' }
        return error


if __name__ == '__main__':

    application.run()
