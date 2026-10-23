
import requests
from config import CRICBUZZ_API_KEY, CRICBUZZ_API_HOST
from utils.logger import get_logger

logger = get_logger(__name__)


def fetch_api_data(endpoint, params=None):
    """Fetch JSON data from the Cricbuzz API through RapidAPI."""

    if not CRICBUZZ_API_KEY or not CRICBUZZ_API_HOST:
        logger.warning("RapidAPI credentials are missing from .env.")
        return None

    endpoint = "/" + endpoint.lstrip("/")
    url = f"https://{CRICBUZZ_API_HOST}{endpoint}"

    headers = {
        "X-RapidAPI-Key": CRICBUZZ_API_KEY,
        "X-RapidAPI-Host": CRICBUZZ_API_HOST,
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        logger.error("RapidAPI request failed: %s", error)
        return None

    except ValueError as error:
        logger.error("Invalid JSON response: %s", error)
        return None


def get_live_matches():
    """Retrieve live match data from Cricbuzz."""
    return fetch_api_data("/matches/v1/live")
