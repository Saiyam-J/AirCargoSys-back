from app.models.booking import Booking

def test_create_booking(db_session):
    booking = Booking(
        ref_id="REF123",
        passenger_name="John Doe",
        passenger_email="john@example.com",
        status="BOOKED",
        flight_id=1
    )
    db_session.add(booking)
    db_session.commit()

    assert booking.id is not None
    assert booking.status == "BOOKED"
