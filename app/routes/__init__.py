from .flight_routes import bp as flights_bp
from .booking_routes import bp as bookings_bp
from .booking_event_routes import bp as booking_events_bp

def register_routes(app):
    app.register_blueprint(flights_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(booking_events_bp)
