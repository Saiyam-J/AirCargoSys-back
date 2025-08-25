from flask import Blueprint, jsonify
from app.services import booking_event_service
from app.schema.booking_event_schema import BookingEventPublicSchema

bp = Blueprint("booking_events", __name__, url_prefix="/booking-events")

booking_event_schema = BookingEventPublicSchema()
booking_events_schema = BookingEventPublicSchema(many=True)


@bp.route("/<int:booking_id>", methods=["GET"])
def list_booking_events(booking_id):
    events = booking_event_service.get_events_for_booking(booking_id)
    return jsonify(booking_events_schema.dump(events))
