from flask import Blueprint, jsonify, request
from app import db
from app.models.bike import Bike


bike_bp = Blueprint("bike_bp", __name__, url_prefix="/bike")

@bike_bp.route("", methods=["POST"])
def add_bike():
    request_body = request.get_json()

    new_bike = Bike(
        name=request_body["name"],
        price=request_body["price"],
        size=request_body["size"],
        type=request_body["type"]
    )

    db.session.add(new_bike)
    db.session.commit()

    return {"id": new_bike.id}, 201

@bike_bp.route("", methods=["GET"])
def get_all_bikes():
    bikes = Bike.query.all()
    response = []
    for bike in bikes:
        bike_dict = {
            "id": bike.id,
            "name": bike.name,
            "price": bike.price,
            "size": bike.size,
            "type": bike.type
        }
        response.append(bike_dict)
    return jsonify(response), 200


# @bike_bp.route("/<bike_id>", methods=["GET"])
# def get_one_bike(bike_id):
#     #see if bike_id can be converted to an integer
#     #try-except: try to convert to an int, if error occurs, catch it and raise 400 error with message
#     try:
#         bike_id = int(bike_id)
#     except ValueError:
#         response_str = f"Invalid bike_id: `{bike_id}`. ID must be an integer"
#         return jsonify({"message": response_str}), 400
#     #after the try-except: bike_id will be a valid int

#     #looping through data to find a bike with matching bike_id
#     #if found: return that bike's data with 200 response code
#     for bike in bikes:
#         if bike.id == bike_id:
#             bike_dict = {
#                 "id": bike.id,
#                 "name": bike.name,
#                 "price": bike.price,
#                 "size": bike.size,
#                 "type": bike.type
#                 }
#             #return in the if block
#             return jsonify(bike_dict), 200
        
#     #after the loop: the bike with matching bike_id was not found, we will raise 404 error with message
#     response_message = f"Could not find bike with ID {bike_id}"
#     return jsonify({"message":response_message}), 404