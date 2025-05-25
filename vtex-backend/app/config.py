from dotenv import load_dotenv
import os

load_dotenv()

VTEX_ACCOUNT = os.getenv("VTEX_ACCOUNT")
VTEX_TOKEN = os.getenv("VTEX_TOKEN")
USE_LOCAL_JSON = os.getenv("USE_LOCAL_JSON", "false").lower() == "true" 

HEADERS = {
    "VtexIdclientAutCookie": VTEX_TOKEN,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, "..", "data")
RAW_ORDERS_PATH = os.path.join(DATA_PATH, "raw_orders")