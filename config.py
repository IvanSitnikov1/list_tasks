from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

with open('certs/jwt-public.pem', 'r') as f:
    PUBLIC_KEY = f.read()
with open('certs/jwt-private.pem', 'r') as f:
    PRIVATE_KEY = f.read()

EXPIRE_MINUTES_ACCESS = 5
EXPIRE_MINUTES_REFRESH = 1440
