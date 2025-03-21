import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()

HUBSPOT_CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID")
HUBSPOT_CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET")
HUBSPOT_REFRESH_TOKEN = os.getenv("HUBSPOT_REFRESH_TOKEN")
HUBSPOT_TOKEN_URL = "https://api.hubapi.com/oauth/v1/token"

logging.basicConfig(filename="logs/hubspot_auth.log", level=logging.INFO)

def get_access_token():
    """Fetches a new access token using the refresh token."""
    try:
        response = requests.post(HUBSPOT_TOKEN_URL, data={
            "grant_type": "refresh_token",
            "client_id": HUBSPOT_CLIENT_ID,
            "client_secret": HUBSPOT_CLIENT_SECRET,
            "refresh_token": HUBSPOT_REFRESH_TOKEN
        })
        response.raise_for_status()
        token_data = response.json()
        return token_data.get("access_token")
    except requests.RequestException as e:
        logging.error(f"HubSpot Auth Failed: {str(e)}")
        return None
