def test_create_booking(client, db_session):
    res = client.post("/bookings", json={
        "passenger_name": "Alice",
        "passenger_email": "alice@example.com",
        "flight_id": 1
    })
    assert res.status_code == 201
    assert res.json["status"] == "BOOKED"

def test_cancel_booking(client, db_session):
    res = client.post("/bookings", json={
        "passenger_name": "Bob",
        "passenger_email": "bob@example.com",
        "flight_id": 1
    })
    ref_id = res.json["ref_id"]

    cancel_res = client.post(f"/bookings/{ref_id}/cancel")
    assert cancel_res.status_code == 200
    assert cancel_res.json["status"] == "CANCELLED"
