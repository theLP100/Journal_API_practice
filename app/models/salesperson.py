from app import db
from flask import Blueprint

#book is inheriting from db.Model, 
class Salesperson(db.Model): 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    journals = db.relationship("Journal", back_populates="salesperson")

    def to_dict(self):
        """given a salesperson, return a dictionary with their info."""
        journals_list = [journal.to_dict for journal in Salesperson.journals]
        journal_dict = {
                "id" : self.id,
                "name": self.name,
                "journal": journals_list
            }
        return journal_dict

    @classmethod  
    def from_dict(cls, data_dict):   
        if "name" in data_dict:
            new_obj = cls(name = data_dict["name"])
            return new_obj
        

