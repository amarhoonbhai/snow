import os
from tinydb import TinyDB

ACCOUNTS_DB_PATH = "../spinauth/accounts.json"

# Ensure directory exists
os.makedirs(os.path.dirname(ACCOUNTS_DB_PATH), exist_ok=True)

accounts_db = TinyDB(ACCOUNTS_DB_PATH)
