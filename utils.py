import os
from tinydb import TinyDB, Query

DB_PATH = os.path.join(os.path.dirname(__file__), "spinauth", "accounts.json")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

accounts_db = TinyDB(DB_PATH)

def get_user_sessions(user_id: int):
    """Fetch sessions for a given user id"""
    User = Query()
    return accounts_db.search(User.user_id == user_id)

def update_user_session(user_id: int, account_name: str, username: str):
    """Insert/Update user session"""
    User = Query()
    accounts_db.upsert(
        {"user_id": user_id, "account_name": account_name, "username": username},
        User.user_id == user_id
    )
