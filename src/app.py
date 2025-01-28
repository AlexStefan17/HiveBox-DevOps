from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request
from app_version import VERSION  # Corrected import
from helpers import fetch_data, calculate_average_temperature
import os

app = Flask(__name__)

# app.config['APP_NAME'] = os.getenv('APP_NAME', 'SenseBox')
# app.config['APP_V'] = os.getenv('APP_NAME', 'SenseBox')


@app.route("/", methods=["GET"])
def home():
    """Simple homepage."""
    return "Welcome to the HiveBox DevOps project!"


@app.route("/version", methods=["GET"])
def get_version():
    """Return the current app version."""
    return jsonify({"version": VERSION})


@app.route("/temperature", methods=["GET"])
def get_temperature():
    """Return current average temperature based on all senseBox data."""
    one_hour_ago = (
        (datetime.now(timezone.utc) - timedelta(hours=1))
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    date = request.args.get("date", one_hour_ago)

    try:
        data = fetch_data(date)
        average_temperature = calculate_average_temperature(data)

        if average_temperature is not None:
            if average_temperature < 10:
                status = "Too Cold"
            elif 11 <= average_temperature <= 36:
                status = "Good"
            else:
                status = "Too Hot"
                
            return jsonify({"average_temperature": average_temperature,
                            "status": status
                            })
        return jsonify({"error": "No valid temperature available."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
