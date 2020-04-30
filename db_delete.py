from application import db
from application.models import BookTags,Books

db.drop_all()
print("DB deleted.")
