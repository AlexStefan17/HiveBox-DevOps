# utils.py
import requests

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
