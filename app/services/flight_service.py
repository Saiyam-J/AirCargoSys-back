from datetime import timedelta
from sqlalchemy import and_
from app.extensions import db
from app.models.flight import Flight

def get_all_flights():
    return Flight.query.all()

def search_direct_flights(origin, destination, departure_date):
    return Flight.query.filter(
        Flight.origin == origin,
        Flight.destination == destination,
        Flight.departure_datetime == departure_date
    ).all()


def search_transit_flights(origin, destination, departure_date):
    """Return 1-stop routes"""
    first_legs = Flight.query.filter(
        Flight.origin == origin,
        Flight.departure_datetime == departure_date
    ).all()

    routes = []
    for leg1 in first_legs:
        leg2_candidates = Flight.query.filter(
            Flight.origin == leg1.destination,
            Flight.destination == destination,
            Flight.departure_datetime.in_([
                departure_date,
                departure_date + timedelta(days=1)
            ])
        ).all()
        for leg2 in leg2_candidates:
            routes.append((leg1, leg2))

    return routes

def get_origins():
    origins = db.session.query(Flight.origin).distinct().all()
    return [o[0] for o in origins]  

def get_destinations():
    destinations = db.session.query(Flight.destination).distinct().all()
    return [d[0] for d in destinations]
