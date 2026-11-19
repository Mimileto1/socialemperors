from sessions import session, neighbor_session, neighbors
from engine import timestamp_now

def get_player_info(USERID, neighbor_ids=()):
    # Update last logged in
    ts_now = timestamp_now()
    session(USERID)["playerInfo"]["last_logged_in"] = ts_now
    # player
    player_info = {
        "result": "ok",
        "processed_errors": 0,
        "timestamp": ts_now,
        "playerInfo": session(USERID)["playerInfo"],
        "map": session(USERID)["maps"][0],
        "privateState": session(USERID)["privateState"],
        "neighbors": neighbors(USERID, neighbor_ids)
    }
    return player_info

def get_neighbor_info(userid, map_number):
    village = neighbor_session(userid)
    index = 0 if map_number is None else map_number
    if not village or not 0 <= index < len(village["maps"]):
        return ""
    neighbor_info = {
        "result": "ok",
        "processed_errors": 0,
        "timestamp": timestamp_now(),
        "playerInfo": village["playerInfo"],
        "map": village["maps"][index],
        "privateState": {} if session(userid) is not None else village["privateState"],
        "neighbors": neighbors(userid)
    }
    return neighbor_info
