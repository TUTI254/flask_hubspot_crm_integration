# swagger_docs.py

# Swagger documentation for GET /new-crm-objects
NEW_CRM_OBJECTS_GET = {
    "tags": ["CRM Objects"],
    "description": "Fetches new contacts, deals, and tickets with pagination support.",
    "parameters": [
        {
            "name": "page",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 1,
            "description": "Page number for pagination."
        },
        {
            "name": "limit",
            "in": "query",
            "type": "integer",
            "required": False,
            "default": 10,
            "description": "Number of items per page."
        }
    ],
    "responses": {
        200: {
            "description": "A list of new contacts, deals, and tickets.",
            "schema": {
                "type": "object",
                "properties": {
                    "contacts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "email": {"type": "string"},
                                "firstname": {"type": "string"},
                                "lastname": {"type": "string"},
                                "phone": {"type": "string"},
                                "deals": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "dealname": {"type": "string"},
                                            "amount": {"type": "number"},
                                            "dealstage": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "deals": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "dealname": {"type": "string"},
                                "amount": {"type": "number"},
                                "dealstage": {"type": "string"},
                                "contacts": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "email": {"type": "string"},
                                            "firstname": {"type": "string"},
                                            "lastname": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "tickets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "subject": {"type": "string"},
                                "description": {"type": "string"},
                                "category": {"type": "string"},
                                "pipeline": {"type": "string"},
                                "hs_ticket_priority": {"type": "string"},
                                "hs_pipeline_stage": {"type": "string"}
                            }
                        }
                    },
                    "pagination": {
                        "type": "object",
                        "properties": {
                            "page": {"type": "integer"},
                            "limit": {"type": "integer"},
                            "total_contacts": {"type": "integer"},
                            "total_deals": {"type": "integer"},
                            "total_tickets": {"type": "integer"}
                        }
                    }
                }
            }
        }
    }
}

# Swagger documentation for POST /contacts
CONTACTS_POST = {
    "tags": ["Contacts"],
    "description": "Creates or updates a contact in HubSpot and saves it to the database.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "firstname": {"type": "string"},
                    "lastname": {"type": "string"},
                    "phone": {"type": "string"}
                },
                "required": ["email", "firstname", "lastname", "phone"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Contact created or updated successfully.",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "email": {"type": "string"},
                    "firstname": {"type": "string"},
                    "lastname": {"type": "string"},
                    "phone": {"type": "string"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        400: {
            "description": "Missing required fields."
        },
        500: {
            "description": "Failed to create/update contact."
        }
    }
}

# Swagger documentation for POST /deals
DEALS_POST = {
    "tags": ["Deals"],
    "description": "Creates or updates a deal in HubSpot and saves it to the database.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "dealname": {"type": "string"},
                    "amount": {"type": "number"},
                    "dealstage": {"type": "string"},
                    "contact_id": {"type": "integer"}
                },
                "required": ["dealname", "amount", "dealstage", "contact_id"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Deal created or updated successfully.",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "dealname": {"type": "string"},
                    "amount": {"type": "number"},
                    "dealstage": {"type": "string"},
                    "contact_id": {"type": "integer"},
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        400: {
            "description": "Missing required fields."
        },
        500: {
            "description": "Failed to create/update deal."
        }
    }
}

# Swagger documentation for POST /tickets
TICKETS_POST = {
    "tags": ["Tickets"],
    "description": "Creates a new support ticket in HubSpot and saves it to the database.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "description": {"type": "string"},
                    "category": {"type": "string"},
                    "pipeline": {"type": "string"},
                    "hs_ticket_priority": {"type": "string"},
                    "hs_pipeline_stage": {"type": "string"},
                    "contact_id": {"type": "integer"},
                    "deal_ids": {
                        "type": "array",
                        "items": {"type": "integer"}
                    }
                },
                "required": [
                    "subject", "description", "category", "pipeline",
                    "hs_ticket_priority", "hs_pipeline_stage", "contact_id"
                ]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Ticket created successfully.",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "subject": {"type": "string"},
                    "description": {"type": "string"},
                    "category": {"type": "string"},
                    "pipeline": {"type": "string"},
                    "hs_ticket_priority": {"type": "string"},
                    "hs_pipeline_stage": {"type": "string"},
                    "contact_id": {"type": "integer"},
                    "deal_ids": {
                        "type": "array",
                        "items": {"type": "integer"}
                    },
                    "created_at": {"type": "string", "format": "date-time"},
                    "updated_at": {"type": "string", "format": "date-time"}
                }
            }
        },
        400: {
            "description": "Missing required fields."
        },
        500: {
            "description": "Failed to create ticket."
        }
    }
}