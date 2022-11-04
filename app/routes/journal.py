#todo: make your returns a consistent style. (make_response(jsonify)) perhaps...

from textwrap import fill
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.journal import Journal

journal_bp = Blueprint("journal_bp" , __name__, url_prefix = "/journal")

#constants: (col names and defaults):
COL_NAMES = ["design", "sub_design", "cut", "complete", "size", "dye", "dye_gradient"]
COL_DEFAULTS = [None, "", True, True, 'A6', 'canyon tan', False]
COL_NAME_DEFAULT_DICT = dict(zip(COL_NAMES, COL_DEFAULTS))

@journal_bp.route("", methods = [ "POST"])
def create_journal():
    
    request_body = request.get_json()

    data_dict = fill_empties_with_defaults(request_body)
    
    new_journal = Journal.from_dict(data_dict)

    db.session.add(new_journal)
    db.session.commit()
    return {"id": new_journal.id}, 201
    

@journal_bp.route("", methods = ["GET"])
def read_all_journals():
    #goal: query whatever I want.
    #it's going to be a bunch of if checks. #OR can I make a variable for this????figure this out.
    #THIS IS DICTIONARY:
    #the keys of the dictionary are what design = DESIGN _QUERY below
    #look up DOUBLE SPLAT OPERATOR #dictionary splat. 
    # fake_dict = {
    #     "a": "stra"
    #     "b": "bstrb"
    # }

    design_query = request.args.get("design")
    
    if design_query:
        journals = Journal.query.filter_by(design = design_query) 
        #**fake_dict)  #this will splat out the dict!!!!
    else:
        journals = Journal.query.all()
    response = [journal.to_dict() for journal in journals]
    return jsonify(response), 200  

@journal_bp.route("/<journal_id>", methods = ["GET"])
def get_one_journal(journal_id):
    journal = validate_journal(journal_id)
    journal_dict = journal.to_dict()
    return journal_dict, 200

#make put or patch!
@journal_bp.route("/<journal_id>", methods = ["PUT", "PATCH"])
def update_journal(journal_id):
    journal = validate_journal(journal_id)
    request_body = request.get_json()
    journal = update_given_values(journal, request_body)
    db.session.commit()
    #the 200 might need to be inside the parens.
    return make_response(f"Journal #{journal_id} successfully updated"), 200
#make a side thing that will deal with 404s if it's not found!!


@journal_bp.route("/<journal_id>", methods = ["DELETE"])
def delete_journal(journal_id):
    journal = validate_journal(journal_id)
    db.session.delete(journal)
    db.session.commit()

    return make_response(f"Journal #{journal_id} successfully deleted"), 200

def validate_journal(journal_id):
    try:
        journal_id = int(journal_id)
    except:
        response_str = f"Journal {journal_id} invalid"
        abort(make_response({"message": response_str}, 400))
    journal = Journal.query.get(journal_id)
    if not journal:
        response_str = f"Journal {journal_id} not found"
        abort(make_response({"message":response_str}, 404))

    return journal



def fill_empties_with_defaults(request_body):
    """go through entered fields: if it has an entry, use that, if not, use the default."""
    
    journal_dict = {}
    for field, default in COL_NAME_DEFAULT_DICT.items():
        
        if field not in request_body:
            journal_dict[field] = default
        else:
            journal_dict[field] = request_body[field]

    return journal_dict

#can i make this a method for tasks?
def update_given_values(journal, request_body):
    """this updates the values given by request_body, and keeps the other values the same that aren't provided."""
    #is there a way to make this a loop?
    #if <field> in request_body, journal.field = request_body['field']

    # for field in COL_NAMES:
    #     if field in request_body:
    if "design" in request_body:
        journal.design = request_body["design"]

    if "sub_design" in request_body:
        journal.sub_design = request_body["sub_design"]

    if "cut" in request_body:
        journal.cut = request_body["cut"]

    if "complete" in request_body:
        journal.complete = request_body["complete"]

    if "size" in request_body:
        journal.size = request_body["size"]

    if "dye" in request_body:
        journal.dye = request_body["dye"]

    if "dye_gradient" in request_body:
        journal.dye_gradient = request_body["dye_gradient"]
    
    return journal

    
