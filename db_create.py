from application import db
from application.models import Book

db.create_all()
print("DB created.")
