# tests/test_models/test_flight.py
from app.models.flight import Flight

def test_create_flight(db_session, app):  
    flight = Flight(
        flight_number="AI101",
        airline_name="Air India Express",
        origin="DEL",
        destination="BOM",
        departure_date="2025-08-25",
        capacity=180,
        price=5000.0
    )
    db_session.add(flight)
    db_session.commit()

    assert flight.id is not None
    assert flight.origin == "DEL"
    assert flight.airline_name == "Air India Express"
