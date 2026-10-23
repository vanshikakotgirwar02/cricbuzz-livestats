
from pathlib import Path
import os
import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_PATH = PROJECT_ROOT / "data" / "cricbuzz.db"


def get_setting(name):
    # First try local environment variables / .env
    value = os.getenv(name, "")

    # On Streamlit Cloud, fall back to Streamlit Secrets
    if not value:
        try:
            value = st.secrets.get(name, "")
        except Exception:
            value = ""

    return str(value).strip()


CRICBUZZ_API_KEY = get_setting("CRICBUZZ_API_KEY")
CRICBUZZ_API_HOST = get_setting("CRICBUZZ_API_HOST")

APP_TITLE = "Cricbuzz LiveStats"
APP_ICON = "🏏"
