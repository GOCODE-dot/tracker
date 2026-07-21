"""
Consensual Location Sharing App
--------------------------------
IMPORTANT: This app is designed for MUTUAL, CONSENSUAL location sharing.
- The "sharer" must actively click "Yes, share my location" AND grant
  their browser's location permission (a second, separate consent step
  enforced by the browser itself).
- The sharer can stop sharing at any time with one click.
- Nothing is hidden — whoever is sharing sees clearly that sharing is on.

Do not repurpose this to track someone without their knowledge.
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone
import threading

app = Flask(__name__)

# In-memory storage (fine for personal use between two people).
# For anything more permanent, swap this for a small database.
_lock = threading.Lock()
state = {
    "sharing": False,
    "lat": None,
    "lng": None,
    "accuracy": None,
    "updated_at": None,
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/her")
def her_page():
    """Page she opens. Nothing happens until she clicks the button
    AND approves the browser's own location permission prompt."""
    return render_template("her.html")


@app.route("/dashboard")
def dashboard():
    """Page you open to view her shared location on a Google Map."""
    return render_template("dashboard.html")


@app.route("/api/start", methods=["POST"])
def start_sharing():
    with _lock:
        state["sharing"] = True
    return jsonify(ok=True)


@app.route("/api/stop", methods=["POST"])
def stop_sharing():
    with _lock:
        state["sharing"] = False
        state["lat"] = None
        state["lng"] = None
        state["accuracy"] = None
        state["updated_at"] = None
    return jsonify(ok=True)


@app.route("/api/update", methods=["POST"])
def update_location():
    data = request.get_json(force=True)
    with _lock:
        if not state["sharing"]:
            # Ignore updates if sharing was turned off server-side.
            return jsonify(ok=False, reason="sharing is off"), 409
        state["lat"] = data.get("lat")
        state["lng"] = data.get("lng")
        state["accuracy"] = data.get("accuracy")
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
    return jsonify(ok=True)


@app.route("/api/location")
def get_location():
    with _lock:
        return jsonify(dict(state))


if __name__ == "__main__":
    import os
    # Railway (and most hosts) inject PORT as an env var.
    port = int(os.environ.get("PORT", 5000))
    # host="0.0.0.0" so it's reachable from outside the container/machine.
    app.run(host="0.0.0.0", port=port, debug=False)
