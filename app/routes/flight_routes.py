from flask import Blueprint, request, jsonify
from app.services import flight_service
from app.schema.flight_schema import FlightSchema

bp = Blueprint("flights", __name__, url_prefix="/flights")

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)


@bp.route("/", methods=["GET"])
def list_flights():
    flights = flight_service.get_all_flights()
    return jsonify(flights_schema.dump(flights))

#functionto search flights based on origin, destination, and departure date
@bp.route("/search", methods=["POST"])
def search_flights():
    data = request.get_json()
    origin = data.get("origin")
    destination = data.get("destination")
    departure_date = data.get("departure_date")

    direct_flights = flight_service.search_direct_flights(origin, destination, departure_date)
    transit_flights = flight_service.search_transit_flights(origin, destination, departure_date)

    return jsonify({
        "direct_flights": flights_schema.dump(direct_flights),
        "transit_flights": flights_schema.dump(transit_flights)
    })

@bp.route("/origins", methods=["GET"])
def get_origins():
    origins = flight_service.get_origins()
    return jsonify(origins)


@bp.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = flight_service.get_destinations()
    return jsonify(destinations)


@bp.route("/<int:flight_id>", methods=["GET"])
def get_flight(flight_id):
    flight = flight_service.get_flight_by_id(flight_id)
    if not flight:
        return jsonify({"error": "Flight not found"}), 404
    return flight_schema.jsonify(flight)


@bp.route("/", methods=["POST"])
def create_flight():
    data = request.get_json()
    flight = flight_service.create_flight(data)
    return flight_schema.jsonify(flight), 201
