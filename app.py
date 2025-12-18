from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Simple file storage
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

# New Home Page (Root /)
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RoLink - Roblox Verification</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f8f9fa; }
            .header { background: #dc3545; color: white; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
            .header h1 { margin: 0; font-size: 28px; }
            .nav { }
            .nav a { color: white; background: rgba(255,255,255,0.2); padding: 10px 20px; margin-left: 10px; border-radius: 20px; text-decoration: none; font-weight: bold; }
            .nav a:hover { background: rgba(255,255,255,0.4); }
            .container { max-width: 1200px; margin: 40px auto; text-align: center; }
            .welcome { font-size: 36px; margin-bottom: 20px; }
            .trusted { font-size: 24px; color: #555; margin-bottom: 40px; }
            .pink-box { background: #f8d7da; border-radius: 15px; height: 200px; margin: 40px auto; max-width: 800px; display: flex; align-items: center; justify-content: center; color: #721c24; font-size: 20px; }
            .green-btn { background: #28a745; color: white; padding: 15px 40px; font-size: 20px; border: none; border-radius: 50px; cursor: pointer; text-decoration: none; display: inline-block; margin: 20px 0; }
            .green-btn:hover { background: #218838; }
            .footer { background: #007bff; height: 100px; margin-top: 100px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>RoLink</h1>
            <div class="nav">
                <a href="#">Dashboard</a>
                <a href="#">Invite</a>
                <a href="#">Support</a>
            </div>
        </div>
        <div class="container">
            <div class="welcome">Welcome to RoLink</div>
            <div class="trusted">Trusted by servers</div>
            <div class="pink-box">Placeholder for stats / image</div>
            <a href="YOUR_BOT_INVITE_LINK_HERE" class="green-btn">Invite to your server</a>
        </div>
        <div class="footer"></div> <!-- Empty blue footer -->
    </body>
    </html>
    """

# Keep your existing routes
@app.route("/verify")
def verify_page():
    discord_id = request.args.get("discord_id")
    if not discord_id:
        return "Error: No Discord ID", 400
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
    <br><a href="/">← Back to Home</a>
    """

@app.route("/submit", methods=["POST"])
def submit():
    discord_id = request.form["discord_id"]
    roblox_username = request.form["roblox_username"].strip()
    data = load_data()
    data[discord_id] = {"username": roblox_username, "verified": True}
    save_data(data)
    return """
    <h1>✅ Success!</h1>
    <p>Verified as <strong>{}</strong></p>
    <p>Return to Discord and click <strong>Check Verification</strong> in your DMs.</p>
    <br><a href="/">← Back to Home</a>
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)