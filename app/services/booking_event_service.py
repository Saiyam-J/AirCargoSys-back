from datetime import datetime
from app.extensions import db
from app.models.booking_event import BookingEvent

def record_event(booking_id, event_type, location, flight_id=None):
    event = BookingEvent(
        booking_id=booking_id,
        event_type=event_type,
        location=location,
        flight_id=flight_id,
        timestamp=datetime.utcnow()
    )
    db.session.add(event)
    db.session.commit()
    return event
