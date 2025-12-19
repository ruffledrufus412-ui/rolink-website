from flask import Flask, request, jsonify, render_template, redirect, url_for
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
    # Automatically sends the user from "/" to "/home"
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("index.html")

# NEW: This handles the "Connect Roblox Account" button from your homepage
@app.route("/verify")
def verify_page():
    # Check if this is coming from the homepage (username) or Discord (discord_id)
    username = request.args.get("username")
    discord_id = request.args.get("discord_id")
    
    # If a username was provided on the homepage, show the Roblox Login Style page
    if username:
        return render_template("login.html", username=username)
    
    # If no Discord ID is provided for the legacy verify flow, show error
    if not discord_id:
        return "Error: No ID provided", 400
    
    # Standard legacy verification fallback
    return render_template("login.html", username="User")

@app.route("/submit", methods=["POST"])
def submit():
    # Get data from the new login form
    roblox_username = request.form.get("roblox_username", "Unknown").strip()
    # We use a dummy ID or capture the discord_id if it was passed through
    discord_id = request.form.get("discord_id", "web_user")

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
    return jsonify({
        "verified": user.get("verified", False),
        "username": user.get("username")
    })

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)