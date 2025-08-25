from marshmallow import Schema, fields, validate, validates_schema, ValidationError

STATUS_VALUES = ["BOOKED", "DEPARTED", "ARRIVED", "DELIVERED", "CANCELLED"]

class BookingCreateSchema(Schema):
    origin = fields.Str(required=True, validate=validate.Length(equal=3))
    destination = fields.Str(required=True, validate=validate.Length(equal=3))
    pieces = fields.Int(required=True, validate=validate.Range(min=1))
    weight_kg = fields.Int(required=True, validate=validate.Range(min=1))

    @validates_schema
    def validate_route(self, data, **kwargs):
        if data.get("origin") == data.get("destination"):
            raise ValidationError("origin and destination must be different.")

class BookingPublicSchema(Schema):
    id = fields.Int(dump_only=True)
    ref_id = fields.Str(dump_only=True)
    origin = fields.Str()
    destination = fields.Str()
    pieces = fields.Int()
    weight_kg = fields.Int()
    status = fields.Str(validate=validate.OneOf(STATUS_VALUES))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
