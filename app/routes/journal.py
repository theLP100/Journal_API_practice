#todo: make your returns a consistent style. (make_response(jsonify)) perhaps...

from textwrap import fill
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.journal import Journal

journal_bp = Blueprint("journal_bp" , __name__, url_prefix = "/journal")

#constants: (col names and defaults):
col_names = ["design", "sub_design", "cut", "complete", "size", "dye", "dye_gradient"]
col_defaults = [None, "", True, True, 'A6', 'canyon tan', False]
COL_NAME_DEFAULT_DICT = dict(zip(col_names, col_defaults))

@journal_bp.route("", methods = [ "POST"])
def create_journal():
    
    request_body = request.get_json()

    dict_of_field_values = fill_empties_with_defaults(request_body)
    
    new_journal = make_new_journal(dict_of_field_values)

    db.session.add(new_journal)
    db.session.commit()
    return {"id": new_journal.id}, 201
    

@journal_bp.route("", methods = ["GET"])
def read_all_journals():
    #goal: query whatever I want.
    #THIS IS DICTIONARY:
    #the keys of the dictionary are what design = DESIGN _QUERY below
    #look up DOUBLE SPLAT OPERATOR #dictionary splat. 
    # fake_dict = {
    #     "a": "stra"
    #     "b": "bstrb"
    # }

    design_query = request.args.get("design")
    #FIGURE OUT A WAY THAT I CAN QUERY FOR WHATEVER I WANT
    #it's going to be a bunch of if checks. #OR can I make a variable for this????figure this out.
    if design_query:
        journals = Journal.query.filter_by(design = design_query) 
        #**fake_dict)  #this will splat out the dict!!!!
    else:
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
    return jsonify(journal_dict), 200

#make put or patch!
@journal_bp.route("/<journal_id>", methods = ["PUT", "PATCH"])
def update_journal(journal_id):
    journal = validate_journal(journal_id)
    request_body = request.get_json()

    #LATER MAKE THIS A HELPER FUNCTION and a for loop (careful with mutable values).  JUST GET IT WORKING FOR NOW.
    #if <field> in request_body, journal.field = request_body['field']

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

    db.session.commit()
    #the 200 might need to be inside the parens.
    return make_response(f"Journal #{journal_id} successfully updated"), 200


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

#put this in model.journal as a method on the class.  Journal.make_new_journal
def make_new_journal(dict_of_field_values):
    new_journal = Journal(
        design = dict_of_field_values["design"],
        sub_design = dict_of_field_values["sub_design"],
        cut = dict_of_field_values["cut"],
        complete = dict_of_field_values["complete"],
        size = dict_of_field_values["size"],
        dye = dict_of_field_values["dye"],
        dye_gradient = dict_of_field_values["dye_gradient"]
    )
    return new_journal

def fill_empties_with_defaults(request_body):
    #go through entered fields: if it has an entry, use that, if not, use the default.
    #maybe we can put these as constants on the top that can be referenced by all the functions? 

    journal_dict = {}
    for field, default in COL_NAME_DEFAULT_DICT.items():
        
        if field not in request_body:
            journal_dict[field] = default
        else:
            journal_dict[field] = request_body[field]

    return journal_dict
    
