# Third-Party
from decouple import config


# Postgres
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASS = config("DB_PASS")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# WhatsApp
WEBHOOK_VERIFY_TOKEN = config("WEBHOOK_VERIFY_TOKEN")
GRAPH_API_TOKEN = config("GRAPH_API_TOKEN")