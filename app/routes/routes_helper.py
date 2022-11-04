from flask import jsonify, abort, make_response

def get_one_obj_or_abort(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except:
        response_str = f"Journal {obj_id} invalid"
        abort(make_response({"message": response_str}, 400))

    matching_obj = cls.query.get(obj_id)

    if not matching_obj:
        response_str = f"Journal {obj_id} not found"
        abort(make_response({"message":response_str}, 404))

    return matching_obj

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

