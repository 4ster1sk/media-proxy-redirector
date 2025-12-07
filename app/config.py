import os
import sys
import pathlib
from dotenv import load_dotenv


def getenv_bool(key: str, default: bool):
    val = os.getenv(key)
    if val is None:
        return default

    return val.strip().lower() in ("true", "1", "t")


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

if DB_HOST.startswith("unix:"):
    socket_dir = DB_HOST.removeprefix("unix:")
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}"
        f"?host={socket_dir}"
    )

else:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

IS_ALLOW_SENSITIVE_FILE: bool = getenv_bool("IS_ALLOW_SENSITIVE_FILE", False)
IS_ALLOW_REMOTE_FILE: bool = getenv_bool("IS_ALLOW_REMOTE_FILE", False)
IS_ALLOW_FEDERATED_DOMAIN: bool = getenv_bool("IS_ALLOW_FEDERATED_DOMAIN", False)
ALLOWED_DOMAINS: list[str] = os.getenv("ALLOWED_DOMAINS", "").split(",")
