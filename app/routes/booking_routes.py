from flask import Blueprint, request, jsonify
from sqlalchemy.exc import NoResultFound
from app.services.booking_service import (
    create_booking, depart_booking, arrive_booking, cancel_booking, get_booking_history, advanced_search_bookings, get_recent_bookings
)

bp = Blueprint("bookings", __name__, url_prefix="/bookings")

@bp.route("", methods=["POST"])
def create():
    data = request.get_json() or {}
    try:
        booking = create_booking(data)
        return jsonify({
            "ref_id": booking.ref_id,
            "status": booking.status.value
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/<ref_id>/depart", methods=["POST"])
def depart(ref_id):
    data = request.get_json() or {}
    try:
        booking = depart_booking(ref_id, data.get("location"), data.get("flight_id"))
        return jsonify({"ref_id": booking.ref_id, "status": booking.status.value})
    except NoResultFound:
        return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/<ref_id>/arrive", methods=["POST"])
def arrive(ref_id):
    data = request.get_json() or {}
    try:
        booking = arrive_booking(ref_id, data.get("location"))
        return jsonify({"ref_id": booking.ref_id, "status": booking.status.value})
    except NoResultFound:
        return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/<ref_id>/cancel", methods=["POST"])
def cancel(ref_id):
    try:
        booking = cancel_booking(ref_id)
        return jsonify({"ref_id": booking.ref_id, "status": booking.status.value})
    except NoResultFound:
        return jsonify({"error": "Booking not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route("/<ref_id>", methods=["GET"])
def history(ref_id):
    try:
        booking, events = get_booking_history(ref_id)
        return jsonify({
            "booking": {
                "ref_id": booking.ref_id,
                "origin": booking.origin,
                "destination": booking.destination,
                "pieces": booking.pieces,
                "weight_kg": booking.weight_kg,
                "status": booking.status.value,
                "created_at": booking.created_at.isoformat(),
                "updated_at": booking.updated_at.isoformat() if booking.updated_at else None,
            },
            "events": [
                {
                    "id": ev.id,
                    "event_type": ev.event_type.value,
                    "location": ev.location,
                    "flight_id": ev.flight_id,
                    "event_timestamp": ev.event_timestamp.isoformat()
                } for ev in events
            ]
        })
    except NoResultFound:
        return jsonify({"error": "Booking not found"}), 404

@bp.route("/advanced-search", methods=["POST"])
def advanced_search():
    data = request.get_json() or {}
    origin = data.get("origin")
    destination = data.get("destination")
    status = data.get("status")

    bookings = advanced_search_bookings(origin=origin, destination=destination, status=status)
    return jsonify([{
        "ref_id": booking.ref_id,
        "origin": booking.origin,
        "destination": booking.destination,
        "pieces": booking.pieces,
        "weight_kg": booking.weight_kg,
        "status": booking.status.value
    } for booking in bookings])

@bp.route("/recent", methods=["GET"])
def recent_bookings():
    limit = request.args.get("limit", default=10, type=int)
    bookings = get_recent_bookings(limit=limit)
    return jsonify([{
        "ref_id": booking.ref_id,
        "origin": booking.origin,
        "destination": booking.destination,
        "pieces": booking.pieces,
        "weight_kg": booking.weight_kg,
        "status": booking.status.value
    } for booking in bookings])