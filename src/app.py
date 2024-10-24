from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request
from app_version import VERSION
from helpers import fetch_data, calculate_average_temperature

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    """Simple homepage."""
    return "Welcome to the HiveBox DevOps project!"

@app.route('/version', methods=['GET'])
def get_version():
    """Return the current app version."""
    return jsonify({"version": VERSION})

@app.route('/temperature', methods=['GET'])
def get_temperature():
    """Return current average temperature based on all senseBox data."""
    one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(timespec='seconds').replace("+00:00", "Z")
    date = request.args.get('date', one_hour_ago)
    
    try:
        data = fetch_data(date)
        average_temperatue = calculate_average_temperature(data)
    
        if average_temperatue is not None:
            return jsonify({"average_temperature": average_temperatue})
        return jsonify({"error": "No valid temperature available."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
