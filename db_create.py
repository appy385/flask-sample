from application import db
from application.models import BookTags,Books

db.create_all()
print("DB created.")
