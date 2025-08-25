from marshmallow import Schema, fields

class FlightSchema(Schema):
    id = fields.Int(dump_only=True)
    flight_number = fields.Str(required=True)
    airline_name = fields.Str(required=True)
    origin = fields.Str(required=True)
    destination = fields.Str(required=True)
    departure_datetime = fields.DateTime(required=True)
    arrival_datetime = fields.DateTime(required=True)

flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)