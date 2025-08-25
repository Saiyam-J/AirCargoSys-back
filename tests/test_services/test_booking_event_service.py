from app.services.booking_event_service import record_event
from app.models.booking import Booking

def test_departure(db_session):
    booking = Booking(ref_id="REF200", passenger_name="Test", passenger_email="t@example.com", status="BOOKED", flight_id=1)
    db_session.add(booking)
    db_session.commit()

    event = record_event(booking.id, "DEPARTED", "DEL")
    assert event.event_type == "DEPARTED"
    assert event.location == "DEL"

def test_arrival(db_session):
    booking = Booking(ref_id="REF201", passenger_name="Test", passenger_email="t@example.com", status="BOOKED", flight_id=1)
    db_session.add(booking)
    db_session.commit()

    event = record_event(booking.id, "ARRIVED", "BLR")
    assert event.event_type == "ARRIVED"
    assert event.location == "BLR"
