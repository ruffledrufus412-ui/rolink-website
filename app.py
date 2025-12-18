from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# --- DATA HANDLING (KEEP THIS) ---
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

# --- ROUTES (KEEP THESE, BUT SIMPLIFIED) ---

@app.route("/")
def home():
    # This now pulls from templates/index.html
    return render_template("index.html")

@app.route("/verify")
def verify_page():
    discord_id = request.args.get("discord_id")
    if not discord_id:
        return "Error: No Discord ID provided", 400
    
    # For now, we are keeping this HTML string here 
    # until you are ready to make verify.html
    return f"""
    <html>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h1>Verify for Discord ID: {discord_id}</h1>
            <form method="post" action="/submit">
                <input type="hidden" name="discord_id" value="{discord_id}">
                <input type="text" name="roblox_username" placeholder="Roblox Username" required>
                <button type="submit">Verify Me</button>
            </form>
        </body>
    </html>
    """

@app.route("/submit", methods=["POST"])
def submit():
    discord_id = request.form["discord_id"]
    roblox_username = request.form["roblox_username"].strip()

    data = load_data()
    data[discord_id] = {"username": roblox_username, "verified": True}
    save_data(data)

    return f"<h1>Success!</h1><p>You verified as {roblox_username}.</p><a href='/'>Go Home</a>"

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)