from marshmallow import Schema, fields, validate

class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    hubspot_id = fields.Str(required=True)
    email = fields.Email(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    phone = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class DealSchema(Schema):
    id = fields.Int(dump_only=True)
    hubspot_id = fields.Str(required=True)
    dealname = fields.Str(required=True)
    amount = fields.Float(required=True)
    dealstage = fields.Str(required=True)
    contact_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class TicketSchema(Schema):
    id = fields.Int(dump_only=True)
    hubspot_id = fields.Str(required=True)
    subject = fields.Str(required=True)
    description = fields.Str(required=True)
    category = fields.Str(required=True, validate=validate.OneOf(["general_inquiry", "technical_issue", "billing", "service_request", "meeting"]))
    pipeline = fields.Str(required=True)
    hs_ticket_priority = fields.Str(required=True)
    hs_pipeline_stage = fields.Str(required=True)
    contact_id = fields.Int(required=True)
    deal_ids = fields.List(fields.Int())
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)