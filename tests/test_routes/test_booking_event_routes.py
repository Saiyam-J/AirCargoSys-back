def test_depart_booking(client, db_session):
    res = client.post("/bookings", json={
        "passenger_name": "Charlie",
        "passenger_email": "charlie@example.com",
        "flight_id": 1
    })
    ref_id = res.json["ref_id"]

    depart_res = client.post(f"/bookings/{ref_id}/depart", json={"location": "DEL"})
    assert depart_res.status_code == 200
    assert depart_res.json["status"] == "DEPARTED"

def test_arrive_booking(client, db_session):
    res = client.post("/bookings", json={
        "passenger_name": "Dana",
        "passenger_email": "dana@example.com",
        "flight_id": 1
    })
    ref_id = res.json["ref_id"]

    arrive_res = client.post(f"/bookings/{ref_id}/arrive", json={"location": "BLR"})
    assert arrive_res.status_code == 200
    assert arrive_res.json["status"] == "ARRIVED"
