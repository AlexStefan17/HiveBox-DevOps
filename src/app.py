from flask import Flask, jsonify, request  # Import request from Flask
from app_version import VERSION
from datetime import datetime, timedelta, timezone
import requests

app = Flask(__name__)

OPEN_SENSE_MAP_API = "https://api.opensensemap.org/boxes"

def fetch_data(date):
    params = {
        'unit': '°C',
        'date': date,
    }
    response = requests.get(OPEN_SENSE_MAP_API, params=params)
    return response.json()

def calculate_average_temperature(data):
    total_temperature = 0
    count = 0

    try:
        for box in data:
            sensors = box['sensors']
            for sensor in sensors:
                if sensor['unit'] == '°C':
                    value = sensor['lastMeasurement']['value']
                    total_temperature += float(value)
                    count += 1

    except (KeyError, TypeError, ValueError):
        pass

    if count == 0:
        return None
    return round(total_temperature / count, 2)

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
        else:
            return jsonify({"error": "No valid temperature available."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
