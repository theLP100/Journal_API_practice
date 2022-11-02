

from textwrap import fill
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.journal import Journal

journal_bp = Blueprint("journal_bp" , __name__, url_prefix = "/journal")


@journal_bp.route("", methods = [ "POST"])
def create_journal():
    
    request_body = request.get_json()

    lst_of_field_values = fill_empties_with_defaults(request_body)
    
    new_journal = make_new_journal(lst_of_field_values)

    db.session.add(new_journal)
    db.session.commit()
    return {"id": new_journal.id}, 201
    

@journal_bp.route("", methods = ["GET"])
def read_all_journals():
    
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


@journal_bp.route("/<journal_id>", methods = ["PUT"])
def update_journal(journal_id):
    journal = validate_journal(journal_id)
    request_body = request.get_json()

    #how can we make this so that the request body doesn't need to be the entire entry?? 
    #I'll try looking up things about PATCH.
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

def make_new_journal(lst_of_field_values):
    #refactor this so it uses a for loop!  (also so it works in any order.  MAKE A DICT INSTEAD.)
    new_journal = Journal(
        design = lst_of_field_values[0],
        sub_design = lst_of_field_values[1],
        cut = lst_of_field_values[2],
        complete = lst_of_field_values[3],
        size = lst_of_field_values[4],
        dye = lst_of_field_values[5],
        dye_gradient = lst_of_field_values[6]
    )
    return new_journal


def fill_empties_with_defaults(request_body):
    #go through entered fields: if it has an entry, use that, if not, use the default.
    #
    #I KNOW there has to be a way to do this in a for loop.  we'll get it eventually. 
    #see end of function for  my notes on this.
    lst_of_field_values = [] 

    design = request_body["design"]
    lst_of_field_values.append(design)

    if "sub_design" not in request_body:
        sub_design = ""
    else:
        sub_design = request_body["sub_design"]
    lst_of_field_values.append(sub_design)

    if "cut" not in request_body:
        cut = True
    else:
        cut = request_body['cut']
    lst_of_field_values.append(cut)

    if "complete" not in request_body:
        complete = True
    else:
        complete = request_body['complete']
    lst_of_field_values.append(complete)

    if "size" not in request_body:
        size = 'A6'
    else:
        size = request_body['size']
    lst_of_field_values.append(size)
    
    if 'dye' not in request_body:
        dye = 'canyon tan'
    else:
        dye = request_body['dye']
    lst_of_field_values.append(dye)

    if "dye_gradient" not in request_body:
        dye_gradient = False
    else:
        dye_gradient = request_body["dye_gradient"]
    lst_of_field_values.append(dye_gradient)

    #return a list of values for each field that we'll put in a journal.  (each function should do ONE thing)
    #CONSIDER MAKING THIS A DICT INSTEAD, WITH KEY BEING THE NAME OF THE FIELD AND VALUE BEING THE VALUE.
    return lst_of_field_values

    #here's my notes trying to do this in a for loop with a dictionary.
    # 
    # col_names = [design, sub_design, cut, complete, size, dye, dye_gradient]
    # col_defaults = [None, "", True, True, 'A6', 'canyon tan', False]
    # col_names_defaults_dict = dict(zip(col_names, col_defaults))

    #unfortnuately I think this is modifying col_names_default_dict.  that's no good. 
    # for field, default in col_names_defaults_dict.items():
    #     if str(field) not in request_body:
    #         field = default
    #     else:
    #         field = request_body[str(field)]

    ##NOW, HOW CAN I USE WHAT I DID ABOVE HERE?
    # new_journal = Journal(
    #     design = col_names_defaults_dict[design],
    #     sub_design = col_names_defaults_dict[sub_design],
    #     cut = col_names_defaults_dict[cut]

    # )
    #-----------------------------------------------------------------
    #old way:

    # new_journal = Journal(
    #     design = request_body["design"],
    #     sub_design = request_body["sub_design"],
    #     cut = request_body["cut"],
    #     complete = request_body["complete"],
    #     size = request_body["size"],
    #     dye = request_body["dye"],
    #     dye_gradient = dye_gradient
    # )

    #old code from 'put':
    # if "design" not in request_body or \
    #     "sub_design" not in request_body or \
    #     "cut" not in request_body or \
    #     "complete" not in request_body or \
    #     "size" not in request_body or \
    #     "dye" not in request_body or \
    #     "dye_gradient" not in request_body:
    #         return jsonify({"message": "Request must include design, sub_design, cut, complete, size, dye, and dye_gradient"}), 400
