from flask import Flask, request, jsonify
from flask import render_template_string, render_template
from flask import send_from_directory
import os, json, time, shutil, threading
import pathlib

app = Flask(__name__)

# Detects the folder where the script is located
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
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_save(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route("/api/status", methods=["GET"])
def status():
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
        return jsonify({"[x]error": "No active save detected"}), 404
    payload = request.get_json()
    if not payload or "amount" not in payload:
        return jsonify({"[x]error": "Missing 'amount' field"}), 400

    new_amount = int(payload["amount"])
    data = read_save(ACTIVE_SAVE)
    old_amount = data["playerInfo"]["cash"]

    # Backup and write
    backup_save(ACTIVE_SAVE)
    data["playerInfo"]["cash"] = new_amount
    write_save(ACTIVE_SAVE, data)

    return jsonify({
        "success": True,
        "player": ACTIVE_PLAYER,
        "old_cash": old_amount,
        "new_cash": new_amount,
        "message": f"[/]Cash updated successfully for {ACTIVE_PLAYER}. Restart the game by logging out to apply changes."
    })


def auto_detect_thread():
    """Continuously monitor for new saves every few seconds."""
    while True:
        find_latest_save()
        time.sleep(5)

@app.route("/control")
def control_panel():
    return render_template("SWCRAPI_test.html")

@app.route('/templates/img/<path:filename>')
def serve_template_images(filename):
    return send_from_directory('templates/img', filename)

if __name__ == "__main__":
    print("[+] Starting SWCRAPI...")
    print("[+] Open http://127.0.0.1:5056/control to start cash modifiying")
    threading.Thread(target=auto_detect_thread, daemon=True).start()
    app.run(host="127.0.0.1", port=5056, debug=False)
