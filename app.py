from flask import Flask, request, jsonify, render_template, redirect, url_for # Added redirect and url_for
import json
import os

app = Flask(__name__)

# --- DATA HANDLING ---
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

# --- ROUTES ---

@app.route("/")
def root():
    # This automatically sends the user from "/" to "/home"
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/verify")
def verify_page():
    discord_id = request.args.get("discord_id")
    if not discord_id:
        return "Error: No Discord ID provided", 400
    
    # Simple styled verify page to match
    return f"""
    <html>
        <head><title>RoLink | Verify</title></head>
        <body style="font-family: Arial; text-align: center; padding-top: 100px; background: #f8f9fa;">
            <div style="background: white; display: inline-block; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h1 style="color: #dc3545;">RoLink Verification</h1>
                <p>Discord ID: <strong>{discord_id}</strong></p>
                <form method="post" action="/submit">
                    <input type="hidden" name="discord_id" value="{discord_id}">
                    <input type="text" name="roblox_username" placeholder="Roblox Username" required 
                           style="padding: 10px; border-radius: 5px; border: 1px solid #ccc; width: 250px;"><br><br>
                    <button type="submit" style="background: #28a745; color: white; padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold;">Verify Me</button>
                </form>
            </div>
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

    # Branded Success Page
    return f"""
    <html>
        <body style="font-family: Arial; text-align: center; padding-top: 100px; background: #f8f9fa;">
            <div style="background: white; display: inline-block; padding: 40px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h1 style="color: #28a745;">✅ Success!</h1>
                <p>You have been verified as <strong>{roblox_username}</strong></p>
                <p>You can now return to Discord.</p>
                <a href="/home" style="color: #dc3545; text-decoration: none; font-weight: bold;">← Back to Home</a>
            </div>
        </body>
    </html>
    """

@app.route("/api/verify-status")
def api_status():
    discord_id = request.args.get("discord_id")
    if not discord_id:
        return jsonify({"verified": False}), 400

    data = load_data()
    user = data.get(discord_id, {})
    return jsonify({{
        "verified": user.get("verified", False),
        "username": user.get("username")
    }})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)