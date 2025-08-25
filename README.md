<<<<<<< HEAD
# AirCargoSys-back
=======
# Air Cargo System Backend

This is the backend service for the Air Cargo System, built using Flask. It provides APIs for managing flights, bookings, and booking events.

## List of APIs

- **Flight APIs**

  - `GET /flights`: Retrieve all flights.
  - `GET /flights/search`: Search for direct and transit flights based on origin, destination, and departure date.
  - `GET /flights/origins`: Retrieve a list of all unique flight origins.
  - `GET /flights/destinations`: Retrieve a list of all unique flight destinations.

- **Booking APIs**
  - `POST /bookings`: Create a new booking.
  - `GET /bookings/<ref_id>`: Retrieve booking details by reference ID.
  - `POST /bookings/<ref_id>/cancel`: Cancel a booking by reference ID.
  - `POST /bookings/<ref_id>/depart`: Mark a booking as departed.
  - `POST /bookings/<ref_id>/arrive`: Mark a booking as arrived.
  - `GET /bookings/<ref_id>/history`: Retrieve the event history for a specific booking.
  - `GET /bookings/search`: Advanced search for bookings based on multiple criteria.
  - `GET /bookings/recent`: Retrieve bookings made in the last 24 hours
- **Booking Event APIs**
  - `GET /booking-events/<booking_id>`: Retrieve all events for a specific booking
>>>>>>> 8ea811d (first commit)
