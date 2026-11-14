import json
import os
import threading

from werkzeug.security import generate_password_hash, check_password_hash

_BASE = os.path.dirname(os.path.abspath(__file__))
_PATH = os.path.join(_BASE, "accounts.json")
_LOCK = threading.Lock()


def _load():
    try:
        with open(_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(data):
    tmp = _PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _PATH)


def create_user(username, password):
    username = username.strip().lower()
    with _LOCK:
        data = _load()
        if username in data:
            return False
        data[username] = {"pw": generate_password_hash(password), "villages": []}
        _save(data)
        return True


def verify_user(username, password):
    username = username.strip().lower()
    with _LOCK:
        data = _load()
        entry = data.get(username)
        if not entry:
            return None
        if not check_password_hash(entry.get("pw", ""), password):
            return None
        villages = entry.get("villages") or []
        return villages[0] if villages else None


def attach_village(username, village_id):
    username = username.strip().lower()
    with _LOCK:
        data = _load()
        entry = data.get(username)
        if not entry:
            return False
        if village_id not in entry.setdefault("villages", []):
            entry["villages"].append(village_id)
        _save(data)
        return True