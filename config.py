# Statement for enabling the development environment
DEBUG = True

# Define the application directory


# Define the database
SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:admin123@book-recommender-db.clywrivu0ofa.ap-south-1.rds.amazonaws.com:3306/bookRecommender'
SQLALCHEMY_TRACK_MODIFICATIONS= False


MAIL_SERVER='smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'contactbookaholics@gmail.com'
MAIL_PASSWORD = 'bookaholics@123'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
