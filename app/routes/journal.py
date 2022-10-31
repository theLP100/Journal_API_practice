
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.journal import Journal

journal_bp = Blueprint("journal_bp" , __name__, url_prefix = "/journal")

#THIS ISN'T WORKING YET'nonetype isn't scriptable'
@journal_bp.route("", methods = [ "POST"])
def create_journal():
    
    request_body = request.get_json()
    new_journal = Journal(
        design = request_body["design"],
        sub_design = request_body["sub_design"],
        cut = request_body["cut"],
        complete = request_body["complete"],
        size = request_body["size"],
        dye = request_body["dye"],
        dye_gradient = request_body["dye_gradient"]
    )

    db.session.add(new_journal)
    db.session.commit()
    return {"id": new_journal.id}, 201
    
@journal_bp.route("", methods = ["GET"])
def read_all_journals():
    journals = Journal.query.all()
    response = []
    for journal in journals:
        journal_dict = make_journal_dict(journal)
        response.append(journal_dict)
    return jsonify(response), 200  

@journal_bp.route("/<journal_id>", methods = ["GET"])
def get_one_journal(journal_id):
    journal = validate_journal(journal_id)
    journal_dict = make_journal_dict(journal)
    return journal_dict

def validate_journal(journal_id):
    try:
        journal_id = int(journal_id)
    except:
        abort(make_response({"message": f"Journal {journal_id} invalid"}, 400))
    journal = Journal.query.get(journal_id)
    if not journal:
        abort(make_response({"message":f"Journal {journal_id} not found"}, 404))

    return journal

def make_journal_dict(journal):
    """given a journal, return a dictionary with all the info for that journal."""
    journal_dict = {
            "id" : journal.id,
            "design" : journal.design,
            "sub_design" : journal.sub_design,
            "cut": journal.cut,
            "complete": journal.complete,
            "size": journal.size,
            "dye": journal.dye,
            "dye_gradient": journal.dye_gradient
        }
    return journal_dict



# no longer need the class.
# class Journal:
#     def __init__(self, id, design, dye_color = "canyon tan", size = "A6", design_details = None, cut = True, complete = True):
#         self.id = id
#         self.design = design
#         self.dye_color = dye_color
#         self.size = size
#         self.design_details = design_details
#         self.cut = cut
#         self.complete = complete

# journals= [
#     Journal(1, "tree of life"),
#     Journal(2, "trefoil"),
#     Journal(3, "dragon"),
#     Journal(4, "astrology", design_details= "aries"),
#     Journal(5, "constellation"),
#     Journal(6, "astrology", design_details = "virgo")
# ]

# #now we'll make a route to return a journal with a specific id
# @journal_bp.route("/<journal_id>", methods = ["GET"])
# def get_journal_by_id(journal_id):
#     journal = validate_journal(journal_id)
#     journal_dict = make_journal_dict(journal)
#     return jsonify(journal_dict), 200


# def validate_journal(journal_id):
#     #if journal_id entered is an int, keep going.  if not, return 400 code for invalid input.
#     try:
#         journal_id = int(journal_id)
#     except:
#         abort(make_response({"message": f"journal {journal_id} is invalid"}, 400))

#     #if journal id isn't found, return 404 not found.
#     for journal in journals:
#         if journal.id == journal_id:
#             return journal
#     abort(make_response({"message": f"journal {journal_id} not found"}, 404))

    
