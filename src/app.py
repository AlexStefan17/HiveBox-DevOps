"""HiveBox DevOps project: Flask API with version, temperature, and metrics endpoints."""

from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request
import requests
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from app_version import VERSION
from helpers import fetch_data, calculate_average_temperature

app = Flask(__name__)


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
    except (requests.exceptions.RequestException, ValueError) as e:
        return jsonify({"error": str(e)}), 500

REQUESTS = Counter("app_requests_total", "Total number of requests to the application")

@app.route("/metrics", methods=["GET"])
def get_metrics():
    """Expose Prometheus metrics."""
    REQUESTS.inc()  # Increment the request count
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
