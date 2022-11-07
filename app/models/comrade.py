#this is for comrades, or workers.  anyone who helps selling or making journals, basically.

from app import db
from flask import Blueprint

class Comrade(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)

    def to_dict(self):
        comrade_dict = {
            "id": self.id,
            "name": self.name
        }
        return comrade_dict

    @classmethod 
    def from_dict(cls, data_dict):
        new_object = cls(name = data_dict["name"])
        return new_object