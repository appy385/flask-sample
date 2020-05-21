import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
books = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/books.csv')
book_tags = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/book_tags.csv')
tags = pd.read_csv('https://raw.githubusercontent.com/zygmuntz/goodbooks-10k/master/tags.csv')
tags_join_DF = pd.merge(book_tags, tags, left_on='tag_id', right_on='tag_id', how='inner')
books_with_tags = pd.merge(books, tags_join_DF, left_on='goodreads_book_id', right_on='goodreads_book_id', how='inner')
temp_df = books_with_tags.groupby('book_id')['tag_name'].apply(' '.join).reset_index()
books = pd.merge(books, temp_df, left_on='book_id', right_on='book_id', how='inner')
books['corpus'] = (pd.Series(books[['authors', 'tag_name']]
                .fillna('')
                .values.tolist()
                ).str.join(' '))
bad_tags = {
    'to-read',
    'currently-reading',
    'books-i-own',
    'owned',
    'owned-books',
    'read',
    'favourites',
    'default',
    'kindle',
    'my-books',
    'to-buy',
    'all-time-favorites',
    're-read',
    'i-own',
    'ebook',
    'on-hold',
    'favorite',
    'favorites'
}
import nltk
import pickle
import bz2
import pickle
import _pickle as cPickle
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(bad_tags)
tf_corpus = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words=stopwords)
tfidf_matrix_corpus = tf_corpus.fit_transform(books['corpus'])
cosine_sim_corpus = linear_kernel(tfidf_matrix_corpus, tfidf_matrix_corpus)
results={}
for idx, row in books.iterrows():
    similar_indices = cosine_sim_corpus[idx].argsort()[:-11:-1]
    results[idx] = similar_indices
outfile = open("cropped_results_pkl",'wb')
pickle.dump(results,outfile)
outfile.close()
