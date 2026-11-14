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


def pull_villages():
    """Import historical saves while leaving newer local copies intact."""
    if not enabled():
        return
    import re
    from pathlib import Path
    from tempfile import NamedTemporaryFile

    directory = Path(SAVES_DIR)
    directory.mkdir(parents=True, exist_ok=True)
    offset = 0
    while True:
        response = requests.get(
            URL + "/rest/v1/se_villages", headers=_headers(),
            params={"select": "userid,data", "order": "userid.asc", "offset": offset, "limit": 100},
            timeout=25,
        )
        response.raise_for_status()
        rows = response.json()
        if not rows:
            return
        for row in rows:
            save_id = str(row["userid"])
            data = row["data"]
            if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", save_id) or not isinstance(data, dict):
                continue
            if str(data.get("playerInfo", {}).get("pid")) != save_id:
                continue
            target = directory / (save_id + ".save.json")
            if target.exists():
                continue
            temporary = None
            try:
                with NamedTemporaryFile(dir=directory, mode="w", encoding="utf-8", delete=False) as stream:
                    temporary = Path(stream.name)
                    json.dump(data, stream)
                    stream.flush()
                    os.fsync(stream.fileno())
                temporary.replace(target)
            finally:
                if temporary:
                    temporary.unlink(missing_ok=True)
        offset += len(rows)
