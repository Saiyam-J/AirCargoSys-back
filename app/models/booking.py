from sqlalchemy import Column, BigInteger, String, Enum, Integer, DateTime, Index
from sqlalchemy.sql import func
from app.extensions import db
import enum

class BookingStatus(enum.Enum):
    BOOKED = "BOOKED"
    DEPARTED = "DEPARTED"
    ARRIVED = "ARRIVED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Booking(db.Model):
    __tablename__ = "bookings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ref_id = Column(String(50), unique=True, nullable=False)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)
    pieces = Column(Integer, nullable=False)
    weight_kg = Column(Integer, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.BOOKED, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_booking_ref", "ref_id"),
    )

    def __repr__(self):
        return f"<Booking {self.ref_id} {self.status}>"
