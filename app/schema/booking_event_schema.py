from marshmallow import Schema, fields, validate

EVENT_VALUES = ["BOOKED", "DEPARTED", "ARRIVED", "CANCELLED"]

class BookingEventCreateSchema(Schema):
    # for depart/arrive calls
    location = fields.Str(required=True, validate=validate.Length(equal=3))
    event_type = fields.Str(required=True, validate=validate.OneOf(EVENT_VALUES))
    flight_id = fields.Int(allow_none=True)

class BookingEventPublicSchema(Schema):
    id = fields.Int(dump_only=True)
    booking_id = fields.Int()
    event_type = fields.Str(validate=validate.OneOf(EVENT_VALUES))
    location = fields.Str()
    flight_id = fields.Int(allow_none=True)
    event_timestamp = fields.DateTime()
