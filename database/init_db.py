
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATABASE_DIR / "cricbuzz.db"

SCHEMA_PATH = PROJECT_ROOT / "database" / "schema.sql"
SEED_PATH = PROJECT_ROOT / "database" / "seed.sql"


def initialize_database():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON;")

        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)

        seed = SEED_PATH.read_text(encoding="utf-8")
        connection.executescript(seed)

        connection.commit()
        print("Database initialized successfully!")
        print(f"Database location: {DATABASE_PATH}")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
