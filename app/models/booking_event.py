from sqlalchemy import Column, BigInteger, String, Enum, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.extensions import db
import enum

class EventType(enum.Enum):
    BOOKED = "BOOKED"
    DEPARTED = "DEPARTED"
    ARRIVED = "ARRIVED"
    CANCELLED = "CANCELLED"

class BookingEvent(db.Model):
    __tablename__ = "booking_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    booking_id = Column(BigInteger, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(Enum(EventType), nullable=False)
    location = Column(String(3), nullable=False)
    flight_id = Column(BigInteger, ForeignKey("flights.id"), nullable=True)
    event_timestamp = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking", backref="events")
    flight = relationship("Flight", backref="events")

    __table_args__ = (
        Index("idx_booking_event", "booking_id", "event_timestamp"),
    )

    def __repr__(self):
        return f"<BookingEvent {self.event_type} at {self.location}>"
