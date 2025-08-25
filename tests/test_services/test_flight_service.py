from app.services.flight_service import search_direct_flights
from app.models.flight import Flight

def test_get_direct_flights(db_session):
    flight = Flight(
        flight_number="AI202",
        airline_name="IndiGo",
        origin="DEL",
        destination="BLR",
        departure_datetime="2025-08-24 06:00:00",
        arrival_datetime="2025-08-24 09:00:00",
    )
    db_session.add(flight)
    db_session.commit()

    flights = search_direct_flights("DEL", "BLR", "2025-08-24")
    assert len(flights) == 1
    assert flights[0].flight_number == "AI202"
