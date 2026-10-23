
from pathlib import Path
import os
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_PATH = PROJECT_ROOT / "data" / "cricbuzz.db"

CRICBUZZ_API_KEY = os.getenv("CRICBUZZ_API_KEY", "")
CRICBUZZ_API_HOST = os.getenv("CRICBUZZ_API_HOST", "")

APP_TITLE = "Cricbuzz LiveStats"
APP_ICON = "🏏"
