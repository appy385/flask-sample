# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database
SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:admin123@book-recommender-db.clywrivu0ofa.ap-south-1.rds.amazonaws.com:3306/bookRecommender'
SQLALCHEMY_TRACK_MODIFICATIONS= False
