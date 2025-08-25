def test_get_direct_flights(client):
    response = client.get("/flights/search?origin=DEL&destination=BOM&departure_date=2025-08-25")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_create_booking(client):
    payload = {
        "flight_id": 1,
        "customer_name": "John Doe",
        "customer_email": "john@example.com"
    }
    response = client.post("/bookings", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "BOOKED"
