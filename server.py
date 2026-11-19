print (" [+] Loading basics...")
import os
import json
import http.client
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen
if os.name == 'nt':
    os.system("color")
    os.system("title Social Empires Server")
else:
    import sys
    sys.stdout.write("\x1b]2;Social Empires Server\x07")

print (" [+] Loading game config...")
from get_game_config import get_game_config, patch_game_config

print (" [+] Loading players...")
from get_player_info import get_player_info, get_neighbor_info
from sessions import load_saved_villages, all_saves_userid, save_info, new_village, fb_friends_str
import accounts as legacy_accounts
import db as _db
_db.pull_villages()
load_saved_villages()

print (" [+] Loading server...")
from game_accounts import install_accounts
from flask import Flask, abort, g, render_template, send_from_directory, request, redirect
from flask.debughelpers import attach_enctype_error_multidict
from command import command
from engine import timestamp_now
from version import version_name
from constants import Constant
from quests import get_quest_map
from werkzeug.security import safe_join
from asset_cdn import asset_redirect
from bundle import ASSETS_DIR, STUB_DIR, TEMPLATES_DIR, BASE_DIR, DATA_DIR

host = '0.0.0.0' if os.environ.get('PORT') else '127.0.0.1'
port = 5050

app = Flask(__name__, template_folder=TEMPLATES_DIR)

print (" [+] Configuring server routes...")

##########
# ROUTES #
##########

## PAGES AND RESOURCES

current_save, protect_payload, game_lock = install_accounts(
    app, data_dir=DATA_DIR, slug="social-empires", title="Social Empires", theme="empires",
    play="/ruffle.html", create_save=lambda username: new_village(), legacy_accounts=legacy_accounts if legacy_accounts.enabled() else None, save_exists=lambda value: value in all_saves_userid(),
)


@app.before_request
def authorize_game_request():
    if request.path.startswith("/dynamic.flash1.dev.socialpoint.es/appsfb/socialempiresdev/srvempires/"):
        game_lock.acquire()
        g.game_locked = True
        save_id = protect_payload(request.values.get("USERID"))
        if save_id not in all_saves_userid():
            abort(503)


@app.teardown_request
def release_game_lock(error):
    if g.pop("game_locked", False):
        game_lock.release()


@app.route("/play.html")
@app.route("/ruffle.html")
def play():
    user_id = current_save()
    if user_id is None:
        return redirect("/login")
    with game_lock:
        if user_id not in all_saves_userid():
            abort(503, "La partida vinculada no está disponible.")
        return render_template(
            "ruffle.html", save_info=save_info(user_id), serverTime=timestamp_now(),
            friendsInfo=fb_friends_str(user_id), version=version_name,
            GAMEVERSION="SocialEmpires0926bsec.swf", SERVERIP=host, SERVERPORT=port,
        )


@app.route("/crossdomain.xml")
def crossdomain():
    return send_from_directory(STUB_DIR, "crossdomain.xml")

@app.route("/img/<path:path>")
def images(path):
    return send_from_directory(TEMPLATES_DIR + "/img", path, max_age=86400)

@app.route("/css/<path:path>")
def css(path):
    return send_from_directory(TEMPLATES_DIR + "/css", path)

## GAME STATIC


@app.route("/default01.static.socialpointgames.com/static/socialempires/swf/05122012_projectiles.swf")
def similar_05122012_projectiles():
    return send_from_directory(ASSETS_DIR + "/swf", "20130417_projectiles.swf", max_age=86400)

@app.route("/default01.static.socialpointgames.com/static/socialempires/swf/05122012_magicParticles.swf")
def similar_05122012_magicParticles():
    return send_from_directory(ASSETS_DIR + "/swf", "20131010_magicParticles.swf", max_age=86400)

@app.route("/default01.static.socialpointgames.com/static/socialempires/swf/05122012_dynamic.swf")
def similar_05122012_dynamic():
    return send_from_directory(ASSETS_DIR + "/swf", "120608_dynamic.swf", max_age=86400)

@app.route("/default01.static.socialpointgames.com/static/socialempires/<path:path>")
def static_assets_loader(path):
    cdn = asset_redirect(path)
    if cdn is not None:
        return cdn

    bundled = safe_join(ASSETS_DIR, path)
    if bundled is None:
        abort(404)
    if os.path.isfile(bundled):
        return send_from_directory(ASSETS_DIR, path, max_age=86400)

    downloads = Path(BASE_DIR) / "download_assets" / "assets"
    cached = Path(safe_join(str(downloads), path))
    if not cached.is_file():
        url = "https://static.socialpointgames.com/static/socialempires/assets/" + quote(path, safe="/")
        try:
            with urlopen(url, timeout=5) as response:
                data = response.read()
        except (URLError, TimeoutError, http.client.HTTPException):
            abort(404)
        cached.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=cached.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        try:
            temporary.replace(cached)
        finally:
            temporary.unlink(missing_ok=True)
    return send_from_directory(downloads, path, max_age=86400)

## GAME DYNAMIC

@app.route("/dynamic.flash1.dev.socialpoint.es/appsfb/socialempiresdev/srvempires/track_game_status.php", methods=['POST'])
def track_game_status_response():
    status = request.values['status']
    installId = request.values['installId']
    user_id = request.values['user_id']

    print(f"track_game_status: status={status}, installId={installId}, user_id={user_id}. --")
    return ("", 200)

@app.route("/dynamic.flash1.dev.socialpoint.es/appsfb/socialempiresdev/srvempires/get_game_config.php", methods=['GET','POST'])
def get_game_config_response():
    spdebug = None

    USERID = current_save()
    user_key = request.values['user_key']
    if 'spdebug' in request.values:
        spdebug = request.values['spdebug']
    language = request.values['language']

    print(f"get_game_config: USERID: {USERID}. --")
    return get_game_config()

@app.route("/dynamic.flash1.dev.socialpoint.es/appsfb/socialempiresdev/srvempires/get_player_info.php", methods=['POST'])
def get_player_info_response():

    USERID = current_save()
    user_key = request.values['user_key']
    spdebug = request.values['spdebug'] if 'spdebug' in request.values else None
    language = request.values['language']
    neighbors = request.values['neighbors'] if 'neighbors' in request.values else None
    client_id = request.values['client_id']
    user = request.values['user'] if 'user' in request.values else None
    map = int(request.values['map']) if 'map' in request.values else None

    print(f"get_player_info: USERID: {USERID}. user: {user} --")

    # Current Player
    if user is None:
        return (get_player_info(USERID), 200)
    # Arthur
    elif user == Constant.NEIGHBOUR_ARTHUR_GUINEVERE_1 \
    or user == Constant.NEIGHBOUR_ARTHUR_GUINEVERE_2 \
    or user == Constant.NEIGHBOUR_ARTHUR_GUINEVERE_3:
        return (get_neighbor_info(user, map), 200)
    # Quest
    elif user.startswith("100000"): # Dirty but quick
        return get_quest_map(user)
    # Neighbor
    else:
        return (get_neighbor_info(user, map), 200)

@app.route("/dynamic.flash1.dev.socialpoint.es/appsfb/socialempiresdev/srvempires/sync_error_track.php", methods=['POST'])
def sync_error_track_response():
    spdebug = None

    USERID = current_save()
    user_key = request.values['user_key']
    if 'spdebug' in request.values:
        spdebug = request.values['spdebug']
    language = request.values['language']
    error = request.values['error']
    current_failed = request.values['current_failed']
    tries = request.values['tries'] if 'tries' in request.values else None
    survival = request.values['survival']
    previous_failed = request.values['previous_failed']
    description = request.values['description']
    user_id = request.values['user_id']

    print(f"sync_error_track: USERID: {USERID}. [Error: {error}] tries: {tries}. --")
    return ("", 200)

@app.route("/null")
def flash_sync_error_response():
    sp_ref_cat = request.values['sp_ref_cat']

    if sp_ref_cat == "flash_sync_error":
        reason = "reload On Sync Error"
    elif sp_ref_cat == "flash_reload_quest":
        reason = "reload On End Quest"
    elif sp_ref_cat == "flash_reload_attack":
        reason = "reload On End Attack"

    print("flash_sync_error", reason, ". --")
    return redirect("/play.html")

@app.route("/dynamic.flash1.dev.socialpoint.es/appsfb/socialempiresdev/srvempires/command.php", methods=['POST'])
def command_response():
    spdebug = None

    USERID = current_save()
    user_key = request.values['user_key']
    if 'spdebug' in request.values:
        spdebug = request.values['spdebug']
    language = request.values['language']
    client_id = request.values['client_id']

    print(f"command: USERID: {USERID}. --")

    data_str = request.values.get("data", "")
    if len(data_str) < 66 or data_str[64] != ";":
        abort(400)
    try:
        data = json.loads(data_str[65:])
        if not isinstance(data, dict) or not isinstance(data.get("commands"), list):
            abort(400)
        command(USERID, data)
    except (KeyError, ValueError, TypeError, IndexError):
        abort(400)
    
    return ({"result": "success"}, 200)

@app.route("/dynamic.flash1.dev.socialpoint.es/appsfb/socialempiresdev/srvempires/get_continent_ranking.php")
def get_continent_ranking_response():

    USERID = current_save()
    worldChange = request.values['worldChange']
    if 'spdebug' in request.values:
        spdebug = request.values['spdebug']
    town_id = request.values['map']
    user_key = request.values['user_key']

    # TODO - stub
    response = {
        "world_id": 0,
        "continent": [
            {"posicion": 0, "nivel": 1, "user_id": 1111}, # villages/AcidCaos
            {"posicion": 1, "nivel": 0},
            {"posicion": 2, "nivel": 0},
            {"posicion": 3, "nivel": 0},
            {"posicion": 4, "nivel": 0},
            {"posicion": 5, "nivel": 0},
            {"posicion": 6, "nivel": 0},
            {"posicion": 7, "nivel": 0}
        ]
    }
    return(response)


########
# MAIN #
########

print (" [+] Running server...")

if __name__ == '__main__':
    app.run(host=host, port=int(os.environ.get('PORT', port)), debug=False)
