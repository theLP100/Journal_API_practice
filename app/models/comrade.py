#this is for comrades, or workers.  anyone who helps selling or making journals, basically.
#update returns for POST To make more informative message.

#for THIS VERSION of the app, we will implement a one-to-many relationship: each comrade will sell multiple journals.
#eventually I would like to make this a many-to-many relationship: each journal can be sold by multiple comrades
#and each comrade can sell multiple journals. 

from app import db
from flask import Blueprint

class Comrade(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    #journals = db.relationship("Journal", back_populates="comrade") #aka salesperson

    def to_dict(self):
        comrade_dict = {
            "id": self.id,
            "name": self.name
            #journals (update this!)
        }
        return comrade_dict

    @classmethod 
    def from_dict(cls, data_dict):
        new_object = cls(name = data_dict["name"])
        return new_object