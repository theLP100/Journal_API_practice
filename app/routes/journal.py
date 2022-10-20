
from flask import Blueprint, jsonify

class Journal:
    def __init__(self, id, design, dye_color = "canyon tan", size = "A6", design_details = None):
        self.id = id
        self.design = design
        self.dye_color = dye_color
        self.size = size
        self.design_details = design_details

journals= [
    Journal(1, "tree of life"),
    Journal(2, "trefoil"),
    Journal(3, "dragon"),
    Journal(4, "astrology", design_details= "aries"),
    Journal(5, "constellation"),
    Journal(6, "astrology", design_details = "virgo")

]

journal_bp = Blueprint("journal_bp" , __name__, url_prefix = "/journal")

#we have a little tag on this to tell flask when to do this function:
@journal_bp.route("", methods = ["GET"])   #"" will be added to the end of the URL.  it's empty, so this route will handle things for /bike.  the method argument must be a list. 
def get_all_journals():
    response = []
    for journal in journals:
        journal_dict = {
            "id" : journal.id,
            "design" : journal.design,
            "dye color": journal.dye_color,
            "size": journal.size,
            "design_details": journal.design_details
        }
        response.append(journal_dict)
    
    return jsonify(response), 200  #this is the status code that will come back. 