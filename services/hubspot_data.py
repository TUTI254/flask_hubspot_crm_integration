import requests
import logging
from services.hubspot_auth import get_access_token

HUBSPOT_API_BASE = "https://api.hubapi.com"

logging.basicConfig(filename="logs/hubspot_data.log", level=logging.INFO)

def get_new_contacts():
    """Fetches newly created contacts with associated deals from HubSpot."""
    token = get_access_token()
    if not token:
        logging.error("Failed to retrieve access token.")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{HUBSPOT_API_BASE}/contacts/v1/lists/recently_updated/contacts/recent"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        contacts = response.json().get("contacts", [])

        # Fetch deals for each contact
        for contact in contacts:
            contact_id = contact["vid"]
            deals_url = f"{HUBSPOT_API_BASE}/deals/v1/deal/associated/contact/{contact_id}"
            deals_response = requests.get(deals_url, headers=headers)
            deals_response.raise_for_status()
            contact["deals"] = deals_response.json().get("deals", [])

        return contacts
    except requests.RequestException as e:
        logging.error(f"Failed to fetch contacts: {str(e)}")
        return None

def get_new_deals():
    """Fetches newly created deals with associated contacts."""
    token = get_access_token()
    if not token:
        logging.error("Failed to retrieve access token.")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{HUBSPOT_API_BASE}/deals/v1/deal/recent/created"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        deals = response.json().get("deals", [])

        # Fetch associated contacts for each deal
        for deal in deals:
            deal_id = deal["dealId"]
            contacts_url = f"{HUBSPOT_API_BASE}/associations/v1/deal/{deal_id}/contacts"
            contacts_response = requests.get(contacts_url, headers=headers)
            contacts_response.raise_for_status()
            deal["contacts"] = contacts_response.json().get("contacts", [])

        return deals
    except requests.RequestException as e:
        logging.error(f"Failed to fetch deals: {str(e)}")
        return None

def get_new_tickets(days=7):
    """Fetches support tickets created within the last 'days' days."""
    token = get_access_token()
    if not token:
        logging.error("Failed to retrieve access token.")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{HUBSPOT_API_BASE}/crm-objects/v1/objects/tickets/paged"

    params = {"limit": 100, "since": get_unix_timestamp(days)}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("tickets", [])
    except requests.RequestException as e:
        logging.error(f"Failed to fetch tickets: {str(e)}")
        return None

def get_unix_timestamp(days):
    """Returns Unix timestamp for 'days' ago."""
    from datetime import datetime, timedelta
    return int((datetime.utcnow() - timedelta(days=days)).timestamp() * 1000)
