from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import swag_from
from docs.swagger_docs import NEW_CRM_OBJECTS_GET, CONTACTS_POST, DEALS_POST, TICKETS_POST
from services.hubspot_data import get_new_contacts, get_new_deals, get_new_tickets
from services.hubspot_api import create_or_update_contact, create_or_update_deal, create_support_ticket
import logging

routes_bp = Blueprint("routes", __name__, url_prefix='/api/v1')

# Initialize Flask-Limiter
limiter = Limiter(
    key_func=get_remote_address,  # Rate limit by client IP address
    default_limits=["200 per day", "50 per hour"]  # Default rate limits
)

# Apply rate limiting to all routes in this Blueprint
routes_bp = limiter.limit("50 per hour")(routes_bp)

@routes_bp.route("/new-crm-objects", methods=["GET"])
@swag_from(NEW_CRM_OBJECTS_GET)
def get_new_crm_objects():
    """Fetches new contacts, deals, and tickets with pagination support."""
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    contacts = get_new_contacts()
    deals = get_new_deals()
    tickets = get_new_tickets()

    def paginate(data):
        start = (page - 1) * limit
        end = start + limit
        return data[start:end] if data else []

    return jsonify({
        "contacts": paginate(contacts),
        "deals": paginate(deals),
        "tickets": paginate(tickets),
        "pagination": {
            "page": page,
            "limit": limit,
            "total_contacts": len(contacts) if contacts else 0,
            "total_deals": len(deals) if deals else 0,
            "total_tickets": len(tickets) if tickets else 0,
        }
    }), 200

@routes_bp.route("/contacts", methods=["POST"])
@swag_from(CONTACTS_POST)
@limiter.limit("5 per minute") 
def create_update_contact():
    """Create or update a contact in HubSpot and save to the database."""
    data = request.json
    email = data.get("email")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    phone = data.get("phone")

    if not all([email, firstname, lastname, phone]):
        return jsonify({"error": "Missing required fields"}), 400

    result = create_or_update_contact(email, firstname, lastname, phone, **data)
    if not result:
        return jsonify({"error": "Failed to create/update contact"}), 500

    return jsonify(result), 201

@routes_bp.route("/deals", methods=["POST"])
@swag_from(DEALS_POST)
@limiter.limit("5 per minute") 
def create_update_deal():
    """Create or update a deal in HubSpot and save to the database."""
    data = request.json
    dealname = data.get("dealname")
    amount = data.get("amount")
    dealstage = data.get("dealstage")
    contact_id = data.get("contact_id")

    if not all([dealname, amount, dealstage, contact_id]):
        return jsonify({"error": "Missing required fields"}), 400

    result = create_or_update_deal(dealname, amount, dealstage, contact_id, **data)
    if not result:
        return jsonify({"error": "Failed to create/update deal"}), 500

    return jsonify(result), 201

@routes_bp.route("/tickets", methods=["POST"])
@swag_from(TICKETS_POST)
@limiter.limit("5 per minute") 
def create_ticket():
    """Create a new support ticket in HubSpot and save to the database."""
    data = request.json
    subject = data.get("subject")
    description = data.get("description")
    category = data.get("category")
    pipeline = data.get("pipeline")
    hs_ticket_priority = data.get("hs_ticket_priority")
    hs_pipeline_stage = data.get("hs_pipeline_stage")
    contact_id = data.get("contact_id")
    deal_ids = data.get("deal_ids", [])

    if not all([subject, description, category, pipeline, hs_ticket_priority, hs_pipeline_stage, contact_id]):
        return jsonify({"error": "Missing required fields"}), 400

    result = create_support_ticket(
        subject, description, category, pipeline, hs_ticket_priority, hs_pipeline_stage, contact_id, deal_ids, **data
    )
    if not result:
        return jsonify({"error": "Failed to create support ticket"}), 500

    return jsonify(result), 201


@routes_bp.app_errorhandler(404)
def not_found(error):
    logging.error("Route not found")
    return jsonify({"error": "Route not found"}), 404
