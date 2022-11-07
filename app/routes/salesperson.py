from textwrap import fill
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.salesperson import Salesperson
from app.models.journal import Journal
from .routes_helper import get_one_obj_or_abort

salesperson_bp = Blueprint("salesperson_bp" , __name__, url_prefix = "/salesperson")

@salesperson_bp.route("", methods = [ "POST"])
def create_salesperson():
    
    request_body = request.get_json()
    
    new_salesperson = Salesperson.from_dict(request_body)

    db.session.add(new_salesperson)
    db.session.commit()
    return {"id": new_salesperson.id}, 201

@salesperson_bp.route("", methods = ["POST"])
def read_all_salespersons():
    salespersons = Salesperson.query.all()
    response = [Salesperson.to_dict() for salesperson in salespersons]
    return jsonify(response), 200

@salesperson_bp.route("/<salesperson_id>/journal", methods=["GET"])
def get_all_journals_sold_by_a_salesperson(salesperson_id):
    salesperson = get_one_obj_or_abort(Salesperson, salesperson_id)
    journals_response = [ journal.to_dift() for journal in salesperson.journals]
    return jsonify(journals_response), 200

@salesperson_bp.route("/<salesperson_id>/journal", methods = ["POST"])
def post_journal_sold_by_a_salesperson(salesperson_id):
    parent_salesperson = get_one_obj_or_abort(Salesperson, salesperson_id)
    request_body = request.get_json()
    #youre going to have to deal with "fill empties with defaults"??
    new_journal = Journal.from_dict(request_body)
    new_journal.salesperson = parent_salesperson
    db.session.add(new_journal)
    db.session.commit()
    #will there be a way add a seller to the journal in inventory??? and a price??
    return jsonify({'message': f"Journal {new_journal.design} sold by {parent_salesperson} added"}), 201

    