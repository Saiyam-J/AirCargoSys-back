from sqlalchemy import Column, BigInteger, String, DateTime, Index
from app.extensions import db

class Flight(db.Model):
    __tablename__ = "flights"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    flight_number = Column(String(20), nullable=False)
    airline_name = Column(String(100), nullable=False)
    departure_datetime = Column(DateTime, nullable=False)
    arrival_datetime = Column(DateTime, nullable=False)
    origin = Column(String(3), nullable=False)
    destination = Column(String(3), nullable=False)

    __table_args__ = (
        Index("idx_flight_route", "origin", "destination", "departure_datetime"),
    )

    def __repr__(self):
        return f"<Flight {self.flight_number} {self.origin}->{self.destination}>"
