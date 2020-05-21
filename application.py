from app import *
from app.models import Books, BookTags
from app.helper import *
from app.globals import *
from sqlalchemy.sql.expression import func
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation, cosine
import pandas as pd
import numpy as np
import pickle
import os
import json



pickle_in = open("cropped_results_pkl","rb")
model = pickle.load(pickle_in)

path = os.path.abspath(os.path.dirname(__file__))
books = pd.read_csv(path +'/csv/books.csv', index_col=False)

pickle_in1 = open("matrix.pkl","rb")
user_item_matrix = pickle.load(pickle_in1)

pickle_in2 = open("knn_model.sav","rb")
model_knn = pickle.load(pickle_in2)


@application.route("/")
def bookList():
    return "Welcome to book recommendation system"

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
    df = pd.read_csv(path +'/csv/books.csv')
    df.dropna(subset=['title'],inplace=True)
    book_titles = df['title'].tolist()
    return {"titles":book_titles}


@application.route('/popular')
def popularBooks():
    df = pd.read_csv(path +'/csv/books.csv')
    df.dropna(subset=['title'],inplace=True)
    df['weighted_rating'] = df['average_rating']*df['ratings_count']
    df.sort_values('weighted_rating',ascending=False,inplace=True)
    df = df[:24]
    df=df.sample(frac=0.5)
    df=df[['goodreads_book_id', 'authors', 'isbn', 'title', 'average_rating', 'image_url']]
    result= df.to_json(orient='records')
    return result


@application.route('/recommend/booktitle/<bookname>')
def corpus_recommendations(bookname):
  titles = books[['isbn','title','authors','average_rating','image_url','goodreads_book_id','book_id']]
  indices = pd.Series(books.index, index=books['title'])
  idx=indices[bookname]
  recs = model[idx][:10]
  return titles.iloc[recs].T.to_dict()


@application.route('/goodreads_id/<username>')
def goodreads(username):
    uri = goodreads_url + username
    response = sendRequest(uri,params)

    if response.status_code==200:
        booksDict = parseXML(response)
        new_list = [0]*1000
        for key, value in booksDict.items():
            goodreads_id = int(key)
            book = books[books['goodreads_book_id']== 4473 ]
            if not book.empty:
                n = int(book['book_id'])
                new_list[n-1]=value
        return goodreads_recommendation(new_list,10)

    elif response.status_code==401:
        error = { 'status': { 'code': response.status_code }, 'error_message' : 'Unauthorized access.Please Try again!' }
        return error

    else:
        error = { 'status': { 'code': response.status_code }, 'error_message' : 'Goodreads User ID does not exist' }
        return error

def goodreads_recommendation(new_list,n):
    np_data = np.asarray(user_item_matrix)
    new_user = pd.DataFrame(new_list).T


    # Finding books which user has already read
    book_not_read = new_user.iloc[0][new_user.iloc[0] == 0]
    book_not_read = book_not_read.index+1

    # Finding similar users to the new user
    similarities,indices = findksimilarusers(new_user,np_data, metric='correlation')
    index_list = indices[0]

    # Making new dataframe of similar users
    similar_user_df = pd.DataFrame()
    for i in index_list:
      similar_user_df = similar_user_df.append(user_item_matrix.iloc[i:i+1])

    # Finding sum of ratings of similar users for all the books
    arr = []
    for i in similar_user_df:
      arr.append(similar_user_df[i].sum())

    # Making dataframe of ratings
    rat = pd.DataFrame(arr).T

    # Making final dataframe
    final_rat = pd.DataFrame(rat.stack())
    final_rat = final_rat.reset_index(level=1)
    final_rat.rename(columns={final_rat.columns[0]:'book_id',final_rat.columns[1]:'rating'},inplace=True)
    final_rat.reset_index(drop=True,inplace=True)

    # Sorting the final ratings
    sorted_df = final_rat.sort_values(by='rating',axis=0,ascending=False)
    sorted_df.reset_index(drop=True,inplace=True)

    # As book_id are from 0 to 9999 therefore removing book_id = 1 instead of 2.
    sorted_df = sorted_df[sorted_df.apply(lambda x: x['book_id']+1 in book_not_read, axis=1)]

    # Making a list of books to be recommended
    book_rec = []
    for i in range(n):
      book_rec.append(sorted_df['book_id'].iloc[i]+1)

    # Making final result dataframe
    result_df = pd.DataFrame()
    for i in book_rec:
      result_df = result_df.append(books.iloc[i-1:i])

    result_df.reset_index(drop=True,inplace = True)
    full_result = result_df
    result_df.drop(result_df.columns.difference(['book_id','goodreads_book_id','isbn','title','authors','average_rating','image_url']),1, inplace=True)

    return result_df.T.to_dict()

def findksimilarusers(new_user, ratings, metric = correlation, k=2):
      similarities=[]
      indices=[]

      distances, indices = model_knn.kneighbors(new_user, n_neighbors = k+1)
      similarities = 1-distances.flatten()
      print('{0} most similar users for new User:\n'.format(k))
      for i in range(0, len(indices.flatten())):

              print('{0}: User {1}, with similarity of {2}'.format(i, indices.flatten()[i]+1, similarities.flatten()[i]))

      return similarities,indices


if __name__ == '__main__':

    application.run()
