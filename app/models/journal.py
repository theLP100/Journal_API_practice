from app import db
from flask import Blueprint
#from sqlalchemy.sql import func

#book is inheriting from db.Model, 
class Journal(db.Model):
    #HOW CAN I GET THESE DAFAULTS TO WORK??????(they don't here, I do it in another place)
    #note: if you don't put a default, it'll go to null. 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    #time_created = db.Column(db.DateTime(timezone = True), server_default = func.now() )
    #time_updated = db.Column(db.DateTime(timezone = True), onupdate = func.now())
    design = db.Column(db.String, nullable = False)
    sub_design = db.Column(db.String, default = "")
    cut = db.Column(db.Boolean, default = True)
    complete = db.Column(db.Boolean, default = True)
    size = db.Column(db.String, default = "A6")
    dye = db.Column(db.String, default = "canyon tan")
    dye_gradient = db.Column(db.Boolean, default = False)

    def to_dict(self):
        """given a journal, return a dictionary with all the info for that journal."""
        #figure out how this works with not everything there. 
        #work out how to fill in empties with defaults HERE. in the class method. 
        journal_dict = {
                "id" : self.id,
                "design" : self.design,
                "sub_design" : self.sub_design,
                "cut": self.cut,
                "complete": self.complete,
                "size": self.size,
                "dye": self.dye,
                "dye_gradient": self.dye_gradient
            }
        return journal_dict

    @classmethod  #this tags it saying it's a class method. 
    def from_dict(cls, data_dict):   #we'll initialize a new class object.
        #add an if statement to handle empties, or INCLUDE FILL EMPTIES WITH DEFAULTS MAYBE call here.
        new_object = cls(design = data_dict["design"],
        sub_design = data_dict["sub_design"],
        cut = data_dict["cut"],
        complete = data_dict["complete"],
        size = data_dict["size"],
        dye = data_dict["dye"],
        dye_gradient = data_dict["dye_gradient"])
        return new_object
        #add an else statement to return 404 if not enough info is given.


