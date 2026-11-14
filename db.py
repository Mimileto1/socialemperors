import json
import os

import requests

from bundle import SAVES_DIR

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


def push_village(userid, data):
    """Sube/actualiza una aldea en Supabase (se_villages)."""
    if not enabled() or not userid or data is None:
        return False
    try:
        resp = requests.put(
            URL + "/rest/v1/se_villages",
            headers=_headers(),
            json={"userid": str(userid), "data": data},
            timeout=15,
        )
        if resp.status_code >= 400:
            print("[DB] push HTTP", resp.status_code, resp.text[:200])
            return False
        return True
    except Exception as e:
        print("[DB] push error:", e)
        return False


def pull_villages():
    """Descarga todas las aldeas de Supabase al disco local (saves/)."""
    if not enabled():
        return 0
    try:
        resp = requests.get(
            URL + "/rest/v1/se_villages?select=userid,data",
            headers=_headers(),
            timeout=25,
        )
        if resp.status_code >= 400:
            print("[DB] pull HTTP", resp.status_code, resp.text[:200])
            return 0
        rows = resp.json()
        os.makedirs(SAVES_DIR, exist_ok=True)
        n = 0
        for row in rows:
            vid = str(row.get("userid") or "")
            data = row.get("data")
            if not vid or data is None:
                continue
            path = os.path.join(SAVES_DIR, vid + ".save.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            n += 1
        return n
    except Exception as e:
        print("[DB] pull error:", e)
        return 0