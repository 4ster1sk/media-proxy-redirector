import os
import sys
import pathlib
from dotenv import load_dotenv

parent_dir = pathlib.Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(parent_dir, ".env")
if not os.path.exists(dotenv_path):
    print("not found: ", dotenv_path)
    sys.exit(1)

load_dotenv(dotenv_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

IS_ALLOW_SENSITIVE_FILE: bool = bool(os.getenv("IS_ALLOW_SENSITIVE_FILE", False))
IS_ALLOW_REMOTE_FILE: bool = bool(os.getenv("IS_ALLOW_REMOTE_FILE", False))
ALLOWED_DOMAINS: list[str] = os.getenv("ALLOWED_DOMAINS", "").split(",")
