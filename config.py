from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
PUBLIC_KEY = os.environ.get("PRIVATE_KEY")

EXPIRE_MINUTES_ACCESS = 1
EXPIRE_MINUTES_REFRESH = 3
