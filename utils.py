import os
from tinydb import TinyDB, Query

ACCOUNTS_DB_PATH = os.getenv("ACCOUNTS_DB_PATH", "../spinauth/accounts.json")
accounts_db = TinyDB(ACCOUNTS_DB_PATH)
accounts_table = accounts_db.table("accounts")

def get_user_sessions(user_id):
    Account = Query()
    return accounts_table.search(Account.user_id == user_id)
