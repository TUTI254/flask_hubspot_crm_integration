from flask import Blueprint, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flasgger import swag_from
from docs.swagger_docs import NEW_CRM_OBJECTS_GET, CONTACTS_POST, DEALS_POST, TICKETS_POST
from services.hubspot_service import HubSpotService
import logging
import requests
import asyncio  # For non-blocking sleep

logging.basicConfig(level=logging.INFO)

routes_bp = Blueprint("routes", __name__, url_prefix='/api/v1')

# Initialize rate limiter inside the blueprint (only affects routes here)
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
limiter.init_app(routes_bp)

cache = Cache(config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache_directory"})
cache.init_app(routes_bp)

@routes_bp.route("/new-crm-objects", methods=["GET"])
@swag_from(NEW_CRM_OBJECTS_GET)
@cache.cached(timeout=300, query_string=True)  
def get_new_crm_objects():
    """Fetches new contacts, deals, and tickets with pagination."""
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        filter_by = request.args.get("filter_by")  # Optional filter

        # Call the service layer
        result = HubSpotService().get_new_crm_objects(page, limit, filter_by)

        logging.info(f"Fetched CRM objects successfully: {result}")
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error fetching CRM objects: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500


async def retry_request(func, max_retries=3, backoff_factor=2):
    """Retries a function with exponential backoff (non-blocking with asyncio)."""
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, "status_code", None)
            
            # Retry only on specific errors (429 Too Many Requests, 500+ Server Errors)
            if status_code in [429] or (status_code and status_code >= 500):
                wait_time = backoff_factor * (2 ** attempt)
                logging.warning(f"Request failed ({status_code}) (attempt {attempt+1}), retrying in {wait_time}s: {str(e)}")
                await asyncio.sleep(wait_time)  # Non-blocking sleep
            else:
                break  # Exit retry loop for other types of errors

    logging.error("Max retries reached. Request failed.")
    return None


@routes_bp.route("/contacts", methods=["POST"])
@swag_from(CONTACTS_POST)
@limiter.limit("5 per minute")
def create_update_contact():
    """Create or update a contact with retry mechanism."""
    try:
        data = request.json
        result = asyncio.run(retry_request(lambda: HubSpotService().create_or_update_contact(data)))

        if result:
            logging.info(f"Successfully created/updated contact: {result}")
            return jsonify(result), 201
        return jsonify({"error": "Failed to create/update contact"}), 500
    except Exception as e:
        logging.error(f"Error creating/updating contact: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500


@routes_bp.route("/deals", methods=["POST"])
@swag_from(DEALS_POST)
@limiter.limit("5 per minute")
def create_update_deal():
    """Create or update a deal with retry mechanism."""
    try:
        data = request.json
        result = asyncio.run(retry_request(lambda: HubSpotService().create_or_update_deal(data)))

        if result:
            logging.info(f"Successfully created/updated deal: {result}")
            return jsonify(result), 201
        return jsonify({"error": "Failed to create/update deal"}), 500
    except Exception as e:
        logging.error(f"Error creating/updating deal: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500


@routes_bp.route("/tickets", methods=["POST"])
@swag_from(TICKETS_POST)
@limiter.limit("5 per minute")
def create_ticket():
    """Create a support ticket with retry mechanism."""
    try:
        data = request.json
        result = asyncio.run(retry_request(lambda: HubSpotService().create_ticket(data)))

        if result:
            logging.info(f"Successfully created ticket: {result}")
            return jsonify(result), 201
        return jsonify({"error": "Failed to create support ticket"}), 500
    except Exception as e:
        logging.error(f"Error creating ticket: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500


@routes_bp.app_errorhandler(404)
def not_found(error):
    logging.error("Route not found")
    return jsonify({"error": "Route not found"}), 404
