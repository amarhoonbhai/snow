from tinydb import TinyDB, Query

db = TinyDB('../spinauth/accounts.json')  # Adjust path if needed
accounts_table = db.table("accounts")

def get_user_accounts(user_id):
    return accounts_table.search(Query().user_id == user_id)
