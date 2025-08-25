from app.services.booking_service import create_booking, cancel_booking
from app.models.booking import Booking

def test_create_booking(db_session):
    data = {
        "origin": "DEL",
        "destination": "BLR",
        "pieces": 2,
        "weight_kg": 15
    }
    booking = create_booking(data)
    db_session.commit()  # optional if create_booking already commits

    assert booking.id is not None
    assert booking.origin == "DEL"
    assert booking.status == "BOOKED"

def test_cancel_booking(db_session):
    data = {
        "origin": "DEL",
        "destination": "BLR",
        "pieces": 2,
        "weight_kg": 15
    }
    booking = create_booking(data)
    db_session.commit()  # optional if create_booking already commits
    cancelled = cancel_booking(booking.ref_id)
    assert cancelled.status == "CANCELLED"
