import os
import threading

import requests
from werkzeug.security import generate_password_hash, check_password_hash

URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
_LOCK = threading.Lock()


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


def create_user(username, password):
    username = username.strip().lower()
    with _LOCK:
        try:
            r = requests.get(
                _table() + "?username=eq." + username + "&select=username",
                headers=_headers(),
                timeout=15,
            )
            if r.status_code >= 400:
                print("[DB] create check HTTP", r.status_code)
                return False
            if r.json():
                return False
            resp = requests.post(
                _table(),
                headers=_headers(),
                json={
                    "username": username,
                    "pw_hash": generate_password_hash(password),
                    "villages": [],
                },
                timeout=15,
            )
            if resp.status_code >= 400:
                print("[DB] create HTTP", resp.status_code, resp.text[:200])
                return False
            return True
        except Exception as e:
            print("[DB] create error:", e)
            return False


def verify_user(username, password):
    username = username.strip().lower()
    try:
        r = requests.get(
            _table() + "?username=eq." + username + "&select=pw_hash,villages",
            headers=_headers(),
            timeout=15,
        )
        if r.status_code >= 400:
            print("[DB] verify HTTP", r.status_code)
            return None
        rows = r.json()
        if not rows:
            return None
        row = rows[0]
        if not check_password_hash(row.get("pw_hash") or "", password):
            return None
        villages = row.get("villages") or []
        return villages[0] if villages else None
    except Exception as e:
        print("[DB] verify error:", e)
        return None


def attach_village(username, village_id):
    username = username.strip().lower()
    try:
        r = requests.get(
            _table() + "?username=eq." + username + "&select=villages",
            headers=_headers(),
            timeout=15,
        )
        if r.status_code >= 400 or not r.json():
            return False
        villages = r.json()[0].get("villages") or []
        if village_id not in villages:
            villages.append(village_id)
        resp = requests.patch(
            _table() + "?username=eq." + username,
            headers=_headers(),
            json={"villages": villages},
            timeout=15,
        )
        return resp.status_code < 400
    except Exception as e:
        print("[DB] attach error:", e)
        return False