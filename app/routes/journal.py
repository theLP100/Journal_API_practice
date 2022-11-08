#todo: make your returns a consistent style. (make_response(jsonify)) perhaps...
#update returns for POST To make more informative message.

from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.journal import Journal
from .routes_helper import get_one_obj_or_abort, update_given_values, fill_empties_with_defaults

journal_bp = Blueprint("journal_bp" , __name__, url_prefix = "/journal")

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
    journal = get_one_obj_or_abort(Journal, journal_id)
    journal_dict = journal.to_dict()
    return journal_dict, 200

#make put or patch!
@journal_bp.route("/<journal_id>", methods = ["PUT", "PATCH"])
def update_journal(journal_id):
    journal = get_one_obj_or_abort(Journal, journal_id)
    request_body = request.get_json()
    journal = update_given_values(journal, request_body)
    db.session.commit()
    #the 200 might need to be inside the parens.
    return make_response(f"Journal #{journal_id} successfully updated"), 200
#make a side thing that will deal with 404s if it's not found!!


@journal_bp.route("/<journal_id>", methods = ["DELETE"])
def delete_journal(journal_id):
    journal = get_one_obj_or_abort(Journal, journal_id)
    db.session.delete(journal)
    db.session.commit()

    return make_response(f"Journal #{journal_id} successfully deleted"), 200

    
