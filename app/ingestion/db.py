import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

# Project root: Enterprise-Knowledge-Intelligence/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)



import os
import psycopg


def get_connection():
    required_vars = ["PGHOST", "PGPORT", "PGDATABASE", "PGUSER", "PGPASSWORD"]
    missing = [name for name in required_vars if not os.getenv(name)]

    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    connection_params = {
        "host": os.getenv("PGHOST"),
        "port": int(os.getenv("PGPORT")),
        "dbname": os.getenv("PGDATABASE"),
        "user": os.getenv("PGUSER"),
        "password": os.getenv("PGPASSWORD"),
        "connect_timeout": 5,
    }

    return psycopg.connect(**connection_params)


def test_connection():
    params = get_connection()

    print("Environment file found:", ENV_FILE.exists())
    print("Database host:", params["host"])
    print("Database:", params["dbname"])
    print("Database user:", params["user"])
    print("Password loaded:", bool(params["password"]))

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            print("Connection successful:", cur.fetchone())


if __name__ == "__main__":
    test_connection()