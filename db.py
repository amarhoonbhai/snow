from tinydb import TinyDB, Query

DB_PATH = "user_data.json"
db = TinyDB(DB_PATH)
user_table = db.table("users")

def get_user_data(user_id):
    User = Query()
    data = user_table.get(User.user_id == user_id)
    if not data:
        data = {
            "user_id": user_id,
            "accounts": [],  # list of session_names
            "ads": {},       # session_name -> ad message
            "groups": {},    # session_name -> list of group IDs
            "intervals": {}  # session_name -> interval (20, 40, 60)
        }
        user_table.insert(data)
    return data

def save_user_data(user_id, data):
    User = Query()
    user_table.upsert(data, User.user_id == user_id)

def update_user_session(user_id, session_name):
    data = get_user_data(user_id)
    if session_name not in data["accounts"]:
        if len(data["accounts"]) < 3:
            data["accounts"].append(session_name)
        else:
            # Already 3 accounts
            return False
    save_user_data(user_id, data)
    return True
