import os
import json

import requests
from werkzeug.security import check_password_hash

URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")


def enabled():
    return bool(URL and KEY)


def _headers():
    return {
        "apikey": KEY,
        "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json",
    }


def _table():
    return URL + "/rest/v1/se_accounts"


def _rows(filters):
    response = requests.get(_table(), headers=_headers(), params=filters, timeout=15)
    response.raise_for_status()
    return response.json()


def exists(username):
    return bool(_rows({"select": "username", "username": "eq." + username.lower()}))


def owns_save(save_id):
    return bool(_rows({"select": "username", "villages": "cs." + json.dumps([save_id]), "limit": 1}))


def verify_user(username, password):
    rows = _rows({"select": "pw_hash,villages", "username": "eq." + username.lower()})
    if not rows or not check_password_hash(rows[0]["pw_hash"], password):
        return None
    villages = rows[0].get("villages") or []
    return str(villages[0]) if villages else None
