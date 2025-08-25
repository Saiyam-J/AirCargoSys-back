import uuid
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from app.extensions import db
from app.models.booking import Booking, BookingStatus
from app.models.booking_event import BookingEvent, EventType
from app.utils.lock import redis_lock

def _generate_ref() -> str:
    return uuid.uuid4().hex[:10].upper()

def _get_locked_booking_by_ref(ref_id: str):
    stmt = select(Booking).where(Booking.ref_id == ref_id).with_for_update()
    result = db.session.execute(stmt).scalars().first()
    if not result:
        raise NoResultFound("Booking not found")
    return result

def _add_event(booking_id: int, event_type: EventType, location: str, flight_id: int | None = None):
    ev = BookingEvent(
        booking_id=booking_id,
        event_type=event_type,
        location=location,
        flight_id=flight_id
    )
    db.session.add(ev)
    return ev

def create_booking(data: dict) -> Booking:
    # Expecting: origin, destination, pieces, weight_kg
    ref_id = _generate_ref()
    booking = Booking(
        ref_id=ref_id,
        origin=data["origin"],
        destination=data["destination"],
        pieces=data["pieces"],
        weight_kg=data["weight_kg"],
        status=BookingStatus.BOOKED
    )
    with db.session.begin():
        db.session.add(booking)
        db.session.flush()
        _add_event(booking.id, EventType.BOOKED, location=booking.origin, flight_id=None)
    return booking

def depart_booking(ref_id: str, location: str, flight_id: int | None = None) -> Booking:
    lock_key = f"lock:booking:{ref_id}"
    with redis_lock(lock_key, ttl_ms=8000, wait_ms=3000):
        with db.session.begin():
            booking = _get_locked_booking_by_ref(ref_id)

            # Idempotency / state guard
            if booking.status in (BookingStatus.DEPARTED, BookingStatus.ARRIVED, BookingStatus.DELIVERED):
                return booking
            if booking.status == BookingStatus.CANCELLED:
                raise ValueError("Cannot depart a cancelled booking.")

            booking.status = BookingStatus.DEPARTED
            _add_event(booking.id, EventType.DEPARTED, location=location, flight_id=flight_id)
    return booking

def arrive_booking(ref_id: str, location: str) -> Booking:
    lock_key = f"lock:booking:{ref_id}"
    with redis_lock(lock_key, ttl_ms=8000, wait_ms=3000):
        with db.session.begin():
            booking = _get_locked_booking_by_ref(ref_id)

            if booking.status in (BookingStatus.ARRIVED, BookingStatus.DELIVERED):
                return booking
            if booking.status == BookingStatus.CANCELLED:
                raise ValueError("Cannot arrive a cancelled booking.")
            if booking.status == BookingStatus.BOOKED:
                raise ValueError("Cannot arrive before departure.")

            booking.status = BookingStatus.ARRIVED
            _add_event(booking.id, EventType.ARRIVED, location=location, flight_id=None)
    return booking

def cancel_booking(ref_id: str) -> Booking:
    lock_key = f"lock:booking:{ref_id}"
    with redis_lock(lock_key, ttl_ms=8000, wait_ms=3000):
        with db.session.begin():
            print("Attempting to cancel booking:", ref_id)
            booking = _get_locked_booking_by_ref(ref_id)

            if booking.status in (BookingStatus.ARRIVED, BookingStatus.DELIVERED):
                raise ValueError("Cannot cancel after arrival/delivery.")
            if booking.status == BookingStatus.CANCELLED:
                return booking

            booking.status = BookingStatus.CANCELLED
            _add_event(booking.id, EventType.CANCELLED, location=booking.origin, flight_id=None)
    return booking

def get_booking_history(ref_id: str):
    booking = Booking.query.filter_by(ref_id=ref_id).first()
    if not booking:
        raise NoResultFound("Booking not found")
    events = sorted(booking.events, key=lambda e: e.event_timestamp)
    return booking, events

def get_recent_bookings(limit: int = 10):
    return Booking.query.order_by(Booking.created_at.desc()).limit(limit).all()

def advanced_search_bookings(origin: str | None = None, destination: str | None = None, status: BookingStatus | None = None):
    query = Booking.query
    if origin:
        query = query.filter(Booking.origin == origin)
    if destination:
        query = query.filter(Booking.destination == destination)
    if status:
        query = query.filter(Booking.status == status)
    return query.all()