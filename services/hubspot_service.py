# Description: Service class for handling HubSpot API interactions and database operations.
import os
import logging
import requests
from dotenv import load_dotenv
from models import db, Contact, Deal, Ticket
from services.hubspot_auth import HubSpotAuth

load_dotenv()

HUBSPOT_API_BASE = os.getenv("HUBSPOT_API_BASE")

class HubSpotService:
    """Service class for handling HubSpot API interactions and database operations."""

    def __init__(self):
        self.token = HubSpotAuth.get_access_token()
        if not self.token:
            logging.error("Failed to retrieve access token.")

    def _get_headers(self):
        """Generates headers for API requests."""
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def create_or_update_contact(self, data):
        """Creates or updates a contact in HubSpot and saves it to the database."""
        url = f"{HUBSPOT_API_BASE}/contacts/v1/contact/createOrUpdate/email/{data['email']}"
        payload = {"properties": [{"property": k, "value": v} for k, v in data.items()]}
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            hubspot_data = response.json()

            contact = Contact(**data, hubspot_id=hubspot_data.get("vid"))
            db.session.merge(contact)
            db.session.commit()
            logging.info(f"Successfully created/updated contact: {contact}")
            return contact
        except requests.RequestException as e:
            logging.error(f"Failed to create/update contact: {str(e)}")
            return None
        except Exception as db_error:
            db.session.rollback()
            logging.error(f"Database error: {str(db_error)}")
            return None

    def create_or_update_deal(self, data):
        """Creates or updates a deal in HubSpot and saves it to the database."""
        url = f"{HUBSPOT_API_BASE}/deals/v1/deal"
        payload = {"properties": [{"name": k, "value": v} for k, v in data.items()]}
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            hubspot_data = response.json()

            deal = Deal(**data, hubspot_id=hubspot_data.get("dealId"))
            db.session.merge(deal)
            db.session.commit()
            logging.info(f"Successfully created/updated deal: {deal}")
            return deal
        except requests.RequestException as e:
            logging.error(f"Failed to create/update deal: {str(e)}")
            return None
        except Exception as db_error:
            db.session.rollback()
            logging.error(f"Database error: {str(db_error)}")
            return None

    def create_ticket(self, data):
        """Creates a new support ticket in HubSpot and saves it to the database."""
        url = f"{HUBSPOT_API_BASE}/crm-objects/v1/objects/tickets"
        payload = {"properties": [{"name": k, "value": v} for k, v in data.items()]}
        
        try:
            response = requests.post(url, headers=self._get_headers(), json=payload)
            response.raise_for_status()
            hubspot_data = response.json()

            ticket = Ticket(**data, hubspot_id=hubspot_data.get("id"))
            db.session.merge(ticket)
            db.session.commit()
            logging.info(f"Successfully created ticket: {ticket}")
            return ticket
        except requests.RequestException as e:
            logging.error(f"Failed to create support ticket: {str(e)}")
            return None
        except Exception as db_error:
            db.session.rollback()
            logging.error(f"Database error: {str(db_error)}")
            return None

    def get_new_crm_objects(self, page=1, limit=10, filter_by=None):
        """Fetches new contacts, deals, and tickets with pagination and filtering."""
        return {
            "contacts": self._fetch_hubspot_objects("contacts", page, limit, filter_by),
            "deals": self._fetch_hubspot_objects("deals", page, limit, filter_by),
            "tickets": self._fetch_hubspot_objects("tickets", page, limit, filter_by),
        }

    def _fetch_hubspot_objects(self, object_type, page, limit, filter_by):
        """Generic function to fetch HubSpot objects with proper pagination and filtering."""
        url = f"{HUBSPOT_API_BASE}/crm/v3/objects/{object_type}"
        params = {
            "limit": limit,
            "after": (page - 1) * limit  
        }
        
        if filter_by:
            params["properties"] = filter_by

        try:
            response = requests.get(url, headers=self._get_headers(), params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {object_type}: {str(e)}")
            return []
