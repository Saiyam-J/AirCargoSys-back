from app.models.booking_event import BookingEvent

def test_create_booking_event(db_session):
    event = BookingEvent(
        booking_id=1,
        event_type="DEPARTED",
        location="DEL",
        timestamp="2025-08-24 10:15:00"
    )
    db_session.add(event)
    db_session.commit()

    assert event.id is not None
    assert event.event_type == "DEPARTED"
