from app import db
#from sqlalchemy.sql import func

#book is inheriting from db.Model, 
class Journal(db.Model):
    #HOW CAN I GET THESE DAFAULTS TO WORK??????
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

    def make_journal_dict(self):
        """given a journal, return a dictionary with all the info for that journal."""
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


