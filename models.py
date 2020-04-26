from application import db

class Tag(db.Model):
    tag_id =  db.Column(db.Integer, primary_key = True)
    tag_name = db.Column(db.String(255), nullable = False)

    def __repr__(self):
        return '<Tag {}>'.format(self.tag_name)
