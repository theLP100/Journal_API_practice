from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.comrade import Comrade

comrade_bp = Blueprint("comrade_bp", __name__, url_prefix = "/comrade")

@comrade_bp.route("", methods = ["POST"])
def create_comrade():
    request_body = request.get_json()
    new_comrade = Comrade.from_dict(request_body)
    db.session.add(new_comrade)
    db.session.commit()
    return {"id": new_comrade.id}, 201

@comrade_bp.route("", methods = ["GET"])
def read_all_comrades():
    comrades = Comrade.query.all()
    response = [comrade.to_dict() for comrade in comrades]
    return jsonify(response), 200
