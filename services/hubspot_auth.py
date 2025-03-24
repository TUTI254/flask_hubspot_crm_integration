import os
import requests
import logging
import time
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter, Retry

load_dotenv()

HUBSPOT_CLIENT_ID = os.getenv("HUBSPOT_CLIENT_ID")
HUBSPOT_CLIENT_SECRET = os.getenv("HUBSPOT_CLIENT_SECRET")
HUBSPOT_REFRESH_TOKEN = os.getenv("HUBSPOT_REFRESH_TOKEN")
HUBSPOT_TOKEN_URL = os.getenv("HUBSPOT_TOKEN_URL")
HUBSPOT_MAX_RETRIES = int(os.getenv("HUBSPOT_MAX_RETRIES", 3))
HUBSPOT_BACKOFF_FACTOR = float(os.getenv("HUBSPOT_BACKOFF_FACTOR", 2.0))
TOKEN_REFRESH_BUFFER = int(os.getenv("TOKEN_REFRESH_BUFFER", 60))

# Store the access token and expiry time
token_cache = {"access_token": None, "expires_at": 0}

logging.basicConfig(level=logging.INFO, filename="logs/hubspot_auth.log")

class HubSpotAuth:
    """Handles authentication and token retrieval for HubSpot API with caching and retries."""

    @staticmethod
    def _get_session():
        """Creates a requests session with retry logic."""
        session = requests.Session()
        retries = Retry(
            total=HUBSPOT_MAX_RETRIES,
            backoff_factor=HUBSPOT_BACKOFF_FACTOR,
            status_forcelist=[500, 502, 503, 504]
        )
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    @staticmethod
    def get_access_token() -> str | None:
        """Fetches a new access token using the refresh token with caching."""
        current_time = int(time.time())
        if token_cache["access_token"] and token_cache["expires_at"] - TOKEN_REFRESH_BUFFER > current_time:
            return token_cache["access_token"]

        try:
            session = HubSpotAuth._get_session()
            response = session.post(HUBSPOT_TOKEN_URL, data={
                "grant_type": "refresh_token",
                "client_id": HUBSPOT_CLIENT_ID,
                "client_secret": HUBSPOT_CLIENT_SECRET,
                "refresh_token": HUBSPOT_REFRESH_TOKEN
            })
            response.raise_for_status()
            token_data = response.json()

            token_cache["access_token"] = token_data.get("access_token")
            token_cache["expires_at"] = current_time + token_data.get("expires_in", 3600)
            logging.info("Successfully refreshed HubSpot token.")
            return token_cache["access_token"]
        except requests.RequestException as e:
            logging.error(f"HubSpot Auth Failed: {str(e)}", exc_info=True)
            return None
