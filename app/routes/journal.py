
from flask import Blueprint, jsonify, abort, make_response

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
        journal_dict = make_journal_dict(journal)
        response.append(journal_dict)
    
    return jsonify(response), 200  #this is the status code that will come back. 

def make_journal_dict(journal):
    """given a journal, return a dictionary with all the info for that journal."""
    journal_dict = {
            "id" : journal.id,
            "design" : journal.design,
            "dye color": journal.dye_color,
            "size": journal.size,
            "design_details": journal.design_details
        }
    
    return journal_dict


#now we'll make a route to return a journal with a specific id
@journal_bp.route("/<journal_id>", methods = ["GET"])
def get_journal_by_id(journal_id):
    journal = validate_journal(journal_id)
    journal_dict = make_journal_dict(journal)
    return jsonify(journal_dict), 200


def validate_journal(journal_id):
    #if journal_id entered is an int, keep going.  if not, return 400 code for invalid input.
    try:
        journal_id = int(journal_id)
    except:
        abort(make_response({"message": f"journal {journal_id} is invalid"}, 400))

    #if journal id isn't found, return 404 not found.
    for journal in journals:
        if journal.id == journal_id:
            return journal
    abort(make_response({"message": f"journal {journal_id} not found"}, 404))

    
