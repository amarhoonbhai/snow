from tinydb import TinyDB, Query

ACCOUNTS_DB_PATH = "../spinauth/accounts.json"
accounts_db = TinyDB(ACCOUNTS_DB_PATH)

def get_user_sessions(user_id: int):
    """
    Retrieve all sessions/accounts linked to this user_id.
    Returns a list of dicts (TinyDB rows).
    """
    User = Query()
    results = accounts_db.search(User.user_id == user_id)
    return results or []
