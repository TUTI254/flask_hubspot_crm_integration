import requests
import logging
from services.hubspot_auth import get_access_token
from models.models import db, Contact, Deal, Ticket
from schemas.schemas import ContactSchema, DealSchema, TicketSchema


HUBSPOT_API_BASE = "https://api.hubapi.com"
def create_or_update_contact(email, firstname, lastname, phone, **kwargs):
    """Create or update a contact in HubSpot and save to the database."""
    token = get_access_token()
    if not token:
        logging.error("Failed to retrieve access token.")
        return None

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{HUBSPOT_API_BASE}/contacts/v1/contact/createOrUpdate/email/{email}"

    data = {
        "properties": [
            {"property": "email", "value": email},
            {"property": "firstname", "value": firstname},
            {"property": "lastname", "value": lastname},
            {"property": "phone", "value": phone},
        ]
    }

    # Add additional fields dynamically
    for key, value in kwargs.items():
        data["properties"].append({"property": key, "value": value})

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        hubspot_data = response.json()

        # Save to database
        contact = Contact(
            hubspot_id=hubspot_data.get("vid"),
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            **kwargs
        )
        db.session.add(contact)
        db.session.commit()

        return ContactSchema().dump(contact)
    except requests.RequestException as e:
        logging.error(f"Failed to create/update contact: {str(e)}")
        return None
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database error: {str(e)}")
        return None

def create_or_update_deal(dealname, amount, dealstage, contact_id, **kwargs):
    """Create or update a deal in HubSpot and save to the database."""
    token = get_access_token()
    if not token:
        logging.error("Failed to retrieve access token.")
        return None

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{HUBSPOT_API_BASE}/deals/v1/deal"

    data = {
        "properties": [
            {"name": "dealname", "value": dealname},
            {"name": "amount", "value": amount},
            {"name": "dealstage", "value": dealstage},
        ],
        "associations": {
            "associatedVids": [contact_id]
        }
    }

    # Add additional fields dynamically
    for key, value in kwargs.items():
        data["properties"].append({"name": key, "value": value})

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        hubspot_data = response.json()

        # Save to database
        deal = Deal(
            hubspot_id=hubspot_data.get("dealId"),
            dealname=dealname,
            amount=amount,
            dealstage=dealstage,
            contact_id=contact_id,
            **kwargs
        )
        db.session.add(deal)
        db.session.commit()

        return DealSchema().dump(deal)
    except requests.RequestException as e:
        logging.error(f"Failed to create/update deal: {str(e)}")
        return None
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database error: {str(e)}")
        return None

def create_support_ticket(subject, description, category, pipeline, hs_ticket_priority, hs_pipeline_stage, contact_id, deal_ids, **kwargs):
    """Create a new support ticket in HubSpot and save to the database."""
    token = get_access_token()
    if not token:
        logging.error("Failed to retrieve access token.")
        return None

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{HUBSPOT_API_BASE}/crm-objects/v1/objects/tickets"

    data = {
        "properties": [
            {"name": "subject", "value": subject},
            {"name": "description", "value": description},
            {"name": "category", "value": category},
            {"name": "pipeline", "value": pipeline},
            {"name": "hs_ticket_priority", "value": hs_ticket_priority},
            {"name": "hs_pipeline_stage", "value": hs_pipeline_stage},
        ],
        "associations": {
            "associatedVids": [contact_id],
            "associatedDealIds": deal_ids
        }
    }

    # Add additional fields dynamically
    for key, value in kwargs.items():
        data["properties"].append({"name": key, "value": value})

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        hubspot_data = response.json()

        # Save to database
        ticket = Ticket(
            hubspot_id=hubspot_data.get("id"),
            subject=subject,
            description=description,
            category=category,
            pipeline=pipeline,
            hs_ticket_priority=hs_ticket_priority,
            hs_pipeline_stage=hs_pipeline_stage,
            contact_id=contact_id,
            deal_ids=deal_ids,
            **kwargs
        )
        db.session.add(ticket)
        db.session.commit()

        return TicketSchema().dump(ticket)
    except requests.RequestException as e:
        logging.error(f"Failed to create support ticket: {str(e)}")
        return None
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database error: {str(e)}")
        return None
