from application import db

class Book(db.Model):
    goodreads_book_id =  db.Column(db.Integer, primary_key = True)
    authors = db.Column(db.String(255), nullable = False)
    title = db.Column(db.String(255), nullable = False)
    isbn = db.Column(db.String(255), nullable = False)
    average_rating =  db.Column(db.Float, nullable = False)
    image_url = db.Column(db.String(255), nullable = False)
    genre = db.Column(db.String(50), nullable = False)


    def __repr__(self):
        return '<Book{}>'.format(self.title)
