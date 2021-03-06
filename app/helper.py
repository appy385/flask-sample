import requests
import xml.etree.ElementTree as ElementTree
from flask_mail import Message
import json

def send_message(message,mail):
    print(message['email'])
    msg = Message(subject="feedback for bookaholics", sender='contactbookaholics@gmail.com', recipients=['contactbookaholics@gmail.com'])
    msg.body = """
          From: %s <%s>
          %s
          """ % (message['name'], message['email'], message['message'])
    mail.send(msg)


def parseXML(res):
    book_list={}
    root = ElementTree.fromstring(res.content)
    for child in root.iter('update'):
        r=child.find('action')
        if r is None:
            continue
        goodreads_id = ((((child.find('object')).find('book')).find('id')).text)
        rating = (r.find('rating').text)
        book_list[goodreads_id]=rating

    return book_list

def parseXML1(response):
    root = ElementTree.fromstring(response.content)
    booksList = []
    for child in root.iter('book'):
        book = {}
        book['isbn'] = child.find('isbn').text
        book['title'] = child.find('title').text
        book['average_rating'] = child.find('average_rating').text
        book['image_url'] = child.find('image_url').text
        book['goodreads_book_id'] = child.find('id').text
        book['authors'] =''
        for subchild in child.iter('authors'):
                 book['authors']  += (((subchild.find('author')).find('name')).text) + ', '
        booksList.append(book)
    json_string = json.dumps(booksList)
    return json_string

def sendRequest(uri,params):
        response = requests.get(uri,params)
        return response

def getbooks(result):
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
