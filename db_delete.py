from application import db
from application.models import Book

db.drop_all()
print("DB deleted.")
