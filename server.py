print (" [+] Loading basics...")
import os
import json
import urllib
import requests
import io
import pathlib
import time
import shutil
import threading

# Add threading lock for file operations
file_lock = threading.Lock()

if os.name == 'nt':
    os.system("color")
    os.system("title Social Wars Server")
else:
    import sys
    sys.stdout.write("\x1b]2;Social Wars Server\x07")

# Variables for cash modification functionality
ROOT_DIR = pathlib.Path(__file__).parent.resolve()
POSSIBLE_SAVE_DIRS = [
    ROOT_DIR,  # ✅ Root directory (where save file currently is)
    ROOT_DIR / "saves",  # also check the /saves/ folder if it exists
]

BACKUP_DIR = "save_backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Global variable to store currently active save file
ACTIVE_SAVE = None
ACTIVE_PLAYER = None

# Keep track of the last detected file
LAST_DETECTED = None
CURRENT_CASH = None  # Track last known cash value

def find_latest_save():
    """Automatically detect and switch to the latest modified save file."""
    global ACTIVE_SAVE, ACTIVE_PLAYER, LAST_DETECTED, CURRENT_CASH

    latest_path = None
    latest_name = None
    latest_cash = None
    latest_time = 0

    for directory in POSSIBLE_SAVE_DIRS:
        if not os.path.exists(directory):
            continue
        for file in os.listdir(directory):
            if not file.endswith(".json") and not file.endswith(".save"):
                continue
            path = os.path.join(directory, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                player_name = data.get("playerInfo", {}).get("name")
                player_cash = data.get("playerInfo", {}).get("cash")
                mod_time = os.path.getmtime(path)
                if player_name and mod_time > latest_time:
                    latest_time = mod_time
                    latest_path = path
                    latest_name = player_name
                    latest_cash = player_cash
            except Exception:
                continue

    # Switch only if a new save is detected
    if latest_path and latest_path != LAST_DETECTED:
        ACTIVE_SAVE = latest_path
        ACTIVE_PLAYER = latest_name
        CURRENT_CASH = latest_cash
        LAST_DETECTED = latest_path
        print(f"[+] Currently loading:")
        print(f"[+]{os.path.basename(ACTIVE_SAVE)} (Player: {ACTIVE_PLAYER})")
        print(f"[+] Current cash: {CURRENT_CASH}")

def backup_save(file_path):
    """Backup before writing changes."""
    ts = time.strftime("%Y%m%d-%H%M%S")
    name = os.path.basename(file_path)
    shutil.copy2(file_path, os.path.join(BACKUP_DIR, f"{ts}_{name}"))

def read_save(file_path):
    """Thread-safe read of save file."""
    with file_lock:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

def write_save(file_path, data):
    """Thread-safe write of save file."""
    with file_lock:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

def auto_detect_thread():
    """Continuously monitor for new saves every few seconds."""
    while True:
        find_latest_save()
        time.sleep(5)

# Start the auto detection thread
threading.Thread(target=auto_detect_thread, daemon=True).start()

print (" [+] Loading game config...")
from get_game_config import get_game_config

print (" [+] Loading players...")
from get_player_info import get_player_info, get_neighbor_info
from sessions import load_saves, load_static_villages, load_quests, all_saves_userid, all_saves_info, save_info, new_village, fb_friends_str
load_saves()
print (" [+] Loading static villages...")
load_static_villages()
print (" [+] Loading quests...")
load_quests()

# print (" [+] Loading auction house data...")
# from auctions import AuctionHouse
# auction_house = AuctionHouse()

print (" [+] Loading server...")
from flask import Flask, render_template, send_from_directory, request, redirect, session, send_file, jsonify
from flask.debughelpers import attach_enctype_error_multidict
from command import command
from engine import timestamp_now
from version import version_name
from bundle import ASSETS_DIR, STUB_DIR, TEMPLATES_DIR, BASE_DIR
from constants import Quests
import sessions

host = '127.0.0.1'
port = 5055

app = Flask(__name__, template_folder=TEMPLATES_DIR)

print (" [+] Configuring server routes...")

##########
# ROUTES #
##########

__STATIC_ROOT = "/static/socialwars"
__DYNAMIC_ROOT = "/dynamic/menvswomen/srvsexwars"

## PAGES AND RESOURCES

@app.route("/", methods=['GET', 'POST'])
def login():
    # Log out previous session
    session.pop('USERID', default=None)
    session.pop('GAMEVERSION', default=None)
    # Reload saves (not static villages nor quests). Allows saves modification without server reset
    load_saves()
    # If logging in, set session USERID, and go to play
    if request.method == 'POST':
        session['USERID'] = request.form['USERID']
        session['GAMEVERSION'] = request.form['GAMEVERSION']
        print("[LOGIN] USERID:", request.form['USERID'])
        print("[LOGIN] GAMEVERSION:", request.form['GAMEVERSION'])
        return redirect("/play.html")
    # Login page
    if request.method == 'GET':
        saves_info = all_saves_info()
        return render_template("login.html", saves_info=saves_info, version=version_name)

@app.route("/play.html")
def play():
    if 'USERID' not in session:
        return redirect("/")
    if 'GAMEVERSION' not in session:
        return redirect("/")

    if session['USERID'] not in all_saves_userid():
        return redirect("/")
    
    USERID = session['USERID']
    GAMEVERSION = session['GAMEVERSION']
    print("[PLAY] USERID:", USERID)
    print("[PLAY] GAMEVERSION:", GAMEVERSION)
    return render_template("play.html", save_info=save_info(USERID), serverTime=timestamp_now(), friendsInfo=fb_friends_str(USERID), version=version_name, GAMEVERSION=GAMEVERSION, SERVERIP=host, SERVERPORT=port)

@app.route("/new.html")
def new():
    session['USERID'] = new_village()
    session['GAMEVERSION'] = "Basesec_1.5.4.swf"
    return redirect("play.html")

@app.route("/crossdomain.xml")
def crossdomain():
    return send_from_directory(STUB_DIR, "crossdomain.xml")

@app.route("/img/<path:path>")
def images(path):
    return send_from_directory(TEMPLATES_DIR + "/img", path)


@app.route("/avatars/<path:path>")
def avatars(path):
    return send_from_directory(TEMPLATES_DIR + "/avatars", path)

@app.route("/css/<path:path>")
def css(path):
    return send_from_directory(TEMPLATES_DIR + "/css", path)

# API endpoints for cash modification
@app.route("/api/status", methods=["GET"])
def api_status():
    if not ACTIVE_SAVE:
        return jsonify({"status": "no_save_found"})
    return jsonify({"status": "ready", "player": ACTIVE_PLAYER, "path": ACTIVE_SAVE})

@app.route("/api/cash", methods=["GET"])
def get_cash():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    data = read_save(ACTIVE_SAVE)
    cash = data.get("playerInfo", {}).get("cash")
    return jsonify({"player": ACTIVE_PLAYER, "cash": cash})

@app.route("/api/set_cash", methods=["POST"])
def set_cash():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    payload = request.get_json()
    if not payload or "amount" not in payload:
        return jsonify({"error": "Missing 'amount' field"}), 400
    
    # Validate and convert amount to integer
    try:
        new_amount = int(payload["amount"])
        if new_amount < 0:
            return jsonify({"error": "Amount must be a positive value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount value"}), 400
    
    # Use file lock to prevent race conditions
    with file_lock:
        data = read_save(ACTIVE_SAVE)
        old_amount = data["playerInfo"]["cash"]
        
        # Backup and write
        backup_save(ACTIVE_SAVE)
        data["playerInfo"]["cash"] = new_amount
        write_save(ACTIVE_SAVE, data)
        
        # Also update the session data to reflect changes in real-time
        if ACTIVE_PLAYER:
            user_id = data["playerInfo"]["pid"]
            # Update the in-memory session data
            if user_id in sessions.__saves:
                # Update all player info, not just cash
                for key, value in data["playerInfo"].items():
                    sessions.__saves[user_id]["playerInfo"][key] = value
                # Save the session to disk as well to persist changes
                sessions.save_session(user_id)
    
    return jsonify({
        "success": True,
        "player": ACTIVE_PLAYER,
        "old_cash": old_amount,
        "new_cash": new_amount,
        "message": f"Cash updated successfully for {ACTIVE_PLAYER}. Changes applied in real-time."
    })

# API endpoints for resource modification
@app.route("/api/oil", methods=["GET"])
def get_oil():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    data = read_save(ACTIVE_SAVE)
    oil = data["maps"][0].get("oil", 0)
    return jsonify({"player": ACTIVE_PLAYER, "oil": oil})

@app.route("/api/set_oil", methods=["POST"])
def set_oil():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    payload = request.get_json()
    if not payload or "amount" not in payload:
        return jsonify({"error": "Missing 'amount' field"}), 400
    
    # Validate and convert amount to integer
    try:
        new_amount = int(payload["amount"])
        if new_amount < 0:
            return jsonify({"error": "Amount must be a positive value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount value"}), 400
    
    # Use file lock to prevent race conditions
    with file_lock:
        data = read_save(ACTIVE_SAVE)
        old_amount = data["maps"][0].get("oil", 0)
        
        # Backup and write
        backup_save(ACTIVE_SAVE)
        data["maps"][0]["oil"] = new_amount
        write_save(ACTIVE_SAVE, data)
        
        # Also update the session data to reflect changes in real-time
        if ACTIVE_PLAYER:
            user_id = data["playerInfo"]["pid"]
            # Update the in-memory session data
            if user_id in sessions.__saves:
                sessions.__saves[user_id]["maps"][0]["oil"] = new_amount
                # Save the session to disk as well to persist changes
                sessions.save_session(user_id)
    
    return jsonify({
        "success": True,
        "player": ACTIVE_PLAYER,
        "old_oil": old_amount,
        "new_oil": new_amount,
        "message": f"Oil updated successfully for {ACTIVE_PLAYER}. Changes applied in real-time."
    })

@app.route("/api/wood", methods=["GET"])
def get_wood():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    data = read_save(ACTIVE_SAVE)
    wood = data["maps"][0].get("wood", 0)
    return jsonify({"player": ACTIVE_PLAYER, "wood": wood})

@app.route("/api/set_wood", methods=["POST"])
def set_wood():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    payload = request.get_json()
    if not payload or "amount" not in payload:
        return jsonify({"error": "Missing 'amount' field"}), 400
    
    # Validate and convert amount to integer
    try:
        new_amount = int(payload["amount"])
        if new_amount < 0:
            return jsonify({"error": "Amount must be a positive value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount value"}), 400
    
    # Use file lock to prevent race conditions
    with file_lock:
        data = read_save(ACTIVE_SAVE)
        old_amount = data["maps"][0].get("wood", 0)
        
        # Backup and write
        backup_save(ACTIVE_SAVE)
        data["maps"][0]["wood"] = new_amount
        write_save(ACTIVE_SAVE, data)
        
        # Also update the session data to reflect changes in real-time
        if ACTIVE_PLAYER:
            user_id = data["playerInfo"]["pid"]
            # Update the in-memory session data
            if user_id in sessions.__saves:
                sessions.__saves[user_id]["maps"][0]["wood"] = new_amount
                # Save the session to disk as well to persist changes
                sessions.save_session(user_id)
    
    return jsonify({
        "success": True,
        "player": ACTIVE_PLAYER,
        "old_wood": old_amount,
        "new_wood": new_amount,
        "message": f"Wood updated successfully for {ACTIVE_PLAYER}. Changes applied in real-time."
    })

@app.route("/api/steel", methods=["GET"])
def get_steel():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    data = read_save(ACTIVE_SAVE)
    steel = data["maps"][0].get("steel", 0)
    return jsonify({"player": ACTIVE_PLAYER, "steel": steel})

@app.route("/api/set_steel", methods=["POST"])
def set_steel():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    payload = request.get_json()
    if not payload or "amount" not in payload:
        return jsonify({"error": "Missing 'amount' field"}), 400
    
    # Validate and convert amount to integer
    try:
        new_amount = int(payload["amount"])
        if new_amount < 0:
            return jsonify({"error": "Amount must be a positive value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount value"}), 400
    
    # Use file lock to prevent race conditions
    with file_lock:
        data = read_save(ACTIVE_SAVE)
        old_amount = data["maps"][0].get("steel", 0)
        
        # Backup and write
        backup_save(ACTIVE_SAVE)
        data["maps"][0]["steel"] = new_amount
        write_save(ACTIVE_SAVE, data)
        
        # Also update the session data to reflect changes in real-time
        if ACTIVE_PLAYER:
            user_id = data["playerInfo"]["pid"]
            # Update the in-memory session data
            if user_id in sessions.__saves:
                sessions.__saves[user_id]["maps"][0]["steel"] = new_amount
                # Save the session to disk as well to persist changes
                sessions.save_session(user_id)
    
    return jsonify({
        "success": True,
        "player": ACTIVE_PLAYER,
        "old_steel": old_amount,
        "new_steel": new_amount,
        "message": f"Steel updated successfully for {ACTIVE_PLAYER}. Changes applied in real-time."
    })

@app.route("/api/gold", methods=["GET"])
def get_gold():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    data = read_save(ACTIVE_SAVE)
    gold = data["maps"][0].get("gold", 0)
    return jsonify({"player": ACTIVE_PLAYER, "gold": gold})

@app.route("/api/set_gold", methods=["POST"])
def set_gold():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    payload = request.get_json()
    if not payload or "amount" not in payload:
        return jsonify({"error": "Missing 'amount' field"}), 400
    
    # Validate and convert amount to integer
    try:
        new_amount = int(payload["amount"])
        if new_amount < 0:
            return jsonify({"error": "Amount must be a positive value"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount value"}), 400
    
    # Use file lock to prevent race conditions
    with file_lock:
        data = read_save(ACTIVE_SAVE)
        old_amount = data["maps"][0].get("gold", 0)
        
        # Backup and write
        backup_save(ACTIVE_SAVE)
        data["maps"][0]["gold"] = new_amount
        write_save(ACTIVE_SAVE, data)
        
        # Also update the session data to reflect changes in real-time
        if ACTIVE_PLAYER:
            user_id = data["playerInfo"]["pid"]
            # Update the in-memory session data
            if user_id in sessions.__saves:
                sessions.__saves[user_id]["maps"][0]["gold"] = new_amount
                # Save the session to disk as well to persist changes
                sessions.save_session(user_id)
    
    return jsonify({
        "success": True,
        "player": ACTIVE_PLAYER,
        "old_gold": old_amount,
        "new_gold": new_amount,
        "message": f"Gold updated successfully for {ACTIVE_PLAYER}. Changes applied in real-time."
    })

@app.route("/control")
def control_panel():
    return render_template("SW_Mod_API.html")

@app.route('/templates/img/<path:filename>')
def serve_template_images(filename):
    return send_from_directory('templates/img', filename)

@app.route('/templates/fusion_units.json')
def serve_fusion_units():
    return send_from_directory('templates', 'fusion_units.json')


## GAME STATIC

@app.route(__STATIC_ROOT + "/<path:path>")
def static_assets_loader(path):
    # LITE-WEIGHT BUILD: ASSETS FROM GITHUB
    if False:
        cdn = "https://raw.githubusercontent.com/AcidCaos/socialwarriors/main/assets/"
        try:
            r = requests.get(cdn + path) # TODO timeout, retry
        except requests.exceptions:
            return ""
        m = io.BytesIO(r.content)
        m.seek(0)
        return send_file(m, download_name=path.split("/")[-1:][0])
    # OFFLINE BUILD
    return send_from_directory(ASSETS_DIR, path)

## GAME DYNAMIC

@app.route(__DYNAMIC_ROOT + "/track_game_status.php", methods=['POST'])
def track_game_status_response():
    status = request.values['status']
    installId = request.values['installId']
    user_id = request.values['user_id']

    # print(f"track_game_status: status={status}, installId={installId}, user_id={user_id}. --", request.values)
    print(f"[STATUS] USERID {user_id}: {status}")
    return ("", 200)

@app.route(__DYNAMIC_ROOT + "/get_game_config.php")
def get_game_config_response():
    USERID = request.values['USERID']
    user_key = request.values['user_key']
    language = request.values['language']

    # print(f"get_game_config: USERID: {USERID}. --", request.values)
    print(f"[CONFIG] USERID {USERID}.")
    return get_game_config()

@app.route(__DYNAMIC_ROOT + "/get_player_info.php", methods=['POST'])
def get_player_info_response():
    USERID = request.values['USERID']
    user_key = request.values['user_key']
    language = request.values['language']

    user = request.values['user'] if 'user' in request.values else None
    client_id = int(request.values['client_id']) if 'client_id' in request.values else None
    map = int(request.values['map']) if 'map' in request.values else None

    # print(f"get_player_info: USERID: {USERID}. --", request.values)

    # Current Player
    if user is None:
        print(f"[PLAYER INFO] USERID {USERID}.")
        # Get player info from the session
        player_info = get_player_info(USERID)
        
        # Check if we have an active save with updated cash
        if ACTIVE_SAVE and ACTIVE_PLAYER:
            save_data = read_save(ACTIVE_SAVE)
            save_user_id = save_data["playerInfo"]["pid"]
            if save_user_id == USERID:
                # Update the cash value in the response with the latest value
                player_info["playerInfo"]["cash"] = save_data["playerInfo"]["cash"]
                # Also update other player info that might have changed
                for key, value in save_data["playerInfo"].items():
                    player_info["playerInfo"][key] = value
        
        return (player_info, 200)
    # General Mike
    elif user in ["100000030","100000031"]:
        print(f"[VISIT] USERID {USERID} visiting General Mike ({user}).")
        return (get_neighbor_info("100000030", map), 200)
    # Quest Maps
    elif user.startswith("100000"):
        print(f"[QUEST] USERID {USERID} loading", Quests.QUEST[user] if user in Quests.QUEST else "?", f"({user}).")
        return (get_neighbor_info(user, map), 200)
    # Static Neighbours
    else:
        print(f"[VISIT] USERID {USERID} visiting user: {user}.")
        return (get_neighbor_info(user, map), 200)
    
## AUCTION HOUSE

# @app.route(__DYNAMIC_ROOT + "/bets/get_bets_list.php", methods=['POST'])
# def get_bets_list():
#     USERID = request.values['USERID']
#     user_key = request.values['user_key']
#     language = request.values['language']
#     data = request.values['data']
# 
#     if not data.startswith("{"):
#         data = data[65:]
#     
#     data = json.loads(data)
#     user_id = data["user_id"]
#     level = data["level"]
# 
#     bets = auction_house.get_auctions(user_id, level)
#     for bet in bets:
#         bet["isPrivate"] =  0
#         bet["isWinning"] =  0
#         bet["won"] =  0
#         bet["finished"] =  0
# 
#     r = {}
#     r["result"] = "success"
#     r["data"] = {"bets": bets}
# 
#     response = json.dumps(r)
#     # print("RESPONSE:")
#     # print(response)
# 
#     return (response, 200)
# 
# @app.route(__DYNAMIC_ROOT + "/bets/get_bet_detail.php", methods=['POST'])
# def get_bet_detail():
#     USERID = request.values['USERID']
#     user_key = request.values['user_key']
#     language = request.values['language']
#     data = request.values['data']
#     
#     if not data.startswith("{"):
#         data = data[65:]
#     
#     data = json.loads(data)
#     uuid = data["uuid"]
#     checkFinish = 0
#     if "checkFinish" in data:
#         checkFinish = data["checkFinish"]
# 
#     bet = auction_house.get_auction_detail(USERID, uuid, checkFinish)
# 
#     print(f"Get bet details for BET UUID {uuid}")
#     print(json.dumps(data, indent="\t"))
# 
#     r = {}
#     r["result"] = "success"
#     r["data"] = bet
# 
#     response = json.dumps(r, indent="\t")
#     print("RESPONSE:")
#     print(response)
# 
#     return (response, 200)
# 
# @app.route(__DYNAMIC_ROOT + "/bets/set_bet.php", methods=['POST'])
# def set_bet():
#     USERID = request.values['USERID']
#     user_key = request.values['user_key']
#     language = request.values['language']
#     data = request.values['data']
# 
#     if not data.startswith("{"):
#         data = data[65:]
#     
#     data = json.loads(data)
#     uuid = data["uuid"]
#     bet_amount = data["bet"]
#     bet_round = data["round"]
# 
#     print(json.dumps(data, indent="\t"))
# 
#     auction_house.set_bet(USERID, uuid, bet_amount, bet_round)
# 
#     r = {}
#     r["result"] = "success"
#     r["data"] = {
#         "betResult": "OK"
#     }
# 
#     response = json.dumps(r)
#     # print("RESPONSE:")
#     # print(response)
# 
#     return (response, 200)

@app.route(__DYNAMIC_ROOT + "/sync_error_track.php", methods=['POST'])
def sync_error_track_response():
    USERID = request.values['USERID']
    user_key = request.values['user_key']
    language = request.values['language']

    # print(f"sync_error_track: USERID: {USERID}. --", request.values)
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

    print("flash_sync_error", reason, ". --", request.values)
    return redirect("/play.html")

@app.route("/fusions")
def fusion_results():
    # Import the get_game_config function to get the patched config
    from get_game_config import get_game_config
    
    try:
        # Get the patched game configuration
        config_data = get_game_config()
    except Exception as e:
        return jsonify({"error": f"Failed to load config: {str(e)}"}), 500
    
    # Extract fusion-related items
    fusion_items = []
    
    # The config_data returned by get_game_config is a tuple, get the first element
    if isinstance(config_data, tuple):
        game_config = config_data[0] if config_data else {}
    else:
        game_config = config_data or {}
    
    # Extract items from the config
    items = game_config.get("items", [])
    
    for item in items:
        # Check if the item has breeding_order (indicating it's a fusion unit)
        if "breeding_order" in item:
            fusion_items.append({
                "id": item["id"],
                "name": item["name"],
                "breeding_order": item["breeding_order"],
                "sm_training_time": item.get("sm_training_time", "Unknown")
            })
    
    # Sort by breeding_order
    fusion_items.sort(key=lambda x: int(x["breeding_order"]))
    
    return render_template("fusion_results.html", fusion_items=fusion_items)

@app.route(__DYNAMIC_ROOT + "/command.php", methods=['POST'])
def command_response():
    USERID = request.values['USERID']
    user_key = request.values['user_key']
    language = request.values['language']

    # print(f"command: USERID: {USERID}. --", request.values)

    data_str = request.values['data']
    data_hash = data_str[:64]
    assert data_str[64] == ';'
    data_payload = data_str[65:]
    data = json.loads(data_payload)

    command(USERID, data)
    
    return ({"result": "success"}, 200)

# Used by Player's World and Alliance buttons
# I added this so the error message stops appearing
@app.route(__DYNAMIC_ROOT + "/alliance/", methods=['POST'])
def alliance():
    USERID = request.values['USERID']
    user_key = request.values['user_key']
    language = request.values['language']
    method = request.values['method']

    response = {}
    return(response, 200)

# API endpoint for skipping chapter timer
@app.route("/api/skip_chapter_timer", methods=["POST"])
def skip_chapter_timer():
    if not ACTIVE_SAVE:
        return jsonify({"error": "No active save detected"}), 404
    
    # Use file lock to prevent race conditions
    with file_lock:
        # Load the current save
        data = read_save(ACTIVE_SAVE)
        
        # Set the last chapter timestamp to 0 to skip the timer
        data["maps"][0]["timestampLastChapter"] = 0
        
        # Backup and write the updated save
        backup_save(ACTIVE_SAVE)
        write_save(ACTIVE_SAVE, data)
        
        # Also update the session data to reflect changes in real-time
        if ACTIVE_PLAYER:
            user_id = data["playerInfo"]["pid"]
            # Update the in-memory session data
            if user_id in sessions.__saves:
                sessions.__saves[user_id]["maps"][0]["timestampLastChapter"] = 0
                # Save the session to disk as well to persist changes
                sessions.save_session(user_id)
    
    return jsonify({
        "success": True,
        "message": "Chapter timer skipped successfully"
    })


########
# MAIN #
########

print (" [+] Running server...")

if __name__ == '__main__':
    app.secret_key = 'SECRET_KEY'
    app.run(host=host, port=port, debug=False)
