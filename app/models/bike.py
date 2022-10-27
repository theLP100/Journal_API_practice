from app import db

class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    size = db.Column(db.Integer)
    type = db.Column(db.String)

