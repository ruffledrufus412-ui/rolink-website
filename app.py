from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Simple file storage (replace with real database for millions of users)
DATA_FILE = "verified.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/verify")
def verify_page():
    discord_id = request.args.get("discord_id")
    if not discord_id:
        return "Error: No Discord ID", 400

    # === YOUR CUSTOM LOGIN SYSTEM GOES HERE ===
    # Example placeholder page — replace with your real form/checks
    return f"""
    <h1>RoLink Verification</h1>
    <p>Discord Account ID: {discord_id}</p>
    <p>Log in or verify your Roblox account below using our system:</p>
    
    <form method="post" action="/submit">
        <input type="hidden" name="discord_id" value="{discord_id}">
        <input type="text" name="roblox_username" placeholder="Exact Roblox Username" required>
        <button type="submit">Verify Me</button>
    </form>
    
    <p>(Replace this form with your actual login/verification method)</p>
    """

@app.route("/submit", methods=["POST"])
def submit():
    discord_id = request.form["discord_id"]
    roblox_username = request.form["roblox_username"].strip()

    # === YOUR REAL VERIFICATION LOGIC HERE ===
    # Example: Just accept it (replace with actual checks!)
    data = load_data()
    data[discord_id] = {"username": roblox_username, "verified": True}
    save_data(data)

    return """
    <h1>✅ Success!</h1>
    <p>Verified as <strong>{}</strong></p>
    <p>Return to Discord and click <strong>Check Verification</strong> in your DMs.</p>
    """.format(roblox_username)

@app.route("/api/verify-status")
def api_status():
    discord_id = request.args.get("discord_id")
    if not discord_id:
        return jsonify({"verified": False}), 400

    data = load_data()
    user = data.get(discord_id, {})
    return jsonify({
        "verified": user.get("verified", False),
        "username": user.get("username")
    })

# This is the key part for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)