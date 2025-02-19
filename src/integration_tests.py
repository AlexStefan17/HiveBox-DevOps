import requests

def test_homepage():
    """Test the homepage endpoint."""
    response = requests.get("http://localhost:5000/")
    assert response.status_code == 200
    assert response.text == "Welcome to the HiveBox DevOps project!"

def test_version_endpoint():
    """Test the /version endpoint."""
    response = requests.get("http://localhost:5000/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data

def test_temperature_endpoint():
    """Test the /temperature endpoint with a valid request."""
    response = requests.get("http://localhost:5000/temperature")
    assert response.status_code in [200, 404]  # 404 if no data is available
    
    if response.status_code == 200:
        data = response.json()
        assert "average_temperature" in data
        average_temperature = data["average_temperature"]
        
        if average_temperature is not None:
            if average_temperature < 10:
                assert data["status"] == "Too Cold"
            elif 11 <= average_temperature <= 36:
                assert data["status"] == "Good"
            else:
                assert data["status"] == "Too Hot"

def test_metrics_endpoint():
    """Test the /metrics endpoint to ensure Prometheus metrics are exposed."""
    response = requests.get("http://localhost:5000/metrics")
    assert response.status_code == 200
    assert b"app_requests_total" in response.content
