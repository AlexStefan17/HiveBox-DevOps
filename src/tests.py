import pytest
from app import app

@pytest.fixture
def client():
    """Set up the test client for Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_version_endpoint(client):
    """Test the /version endpoint."""
    response = client.get('/version')
    assert response.status_code == 200
    data = response.get_json()
    assert "version" in data
    assert data["version"] == "v0.5.0"
    
def test_temperature_endpoint_cold(client, mocker):
    """Test the /temperature endpoint."""
    mock_data = [{'sensors': [{'unit': '°C', 'lastMeasurement': {'value': '0'}}]}]
    
    mocker.patch('app.fetch_data', return_value=mock_data)
    
    response = client.get('/temperature')
    assert response.status_code == 200
    data = response.get_json()
    assert "average_temperature" in data
    assert round(data["average_temperature"], 2) == 0
    assert data["status"] == "Too Cold"

def test_temperature_endpoint_good(client, mocker):
    """Test the /temperature endpoint."""
    mock_data = [{'sensors': [{'unit': '°C', 'lastMeasurement': {'value': '15'}}]}]
    
    mocker.patch('app.fetch_data', return_value=mock_data)
    
    response = client.get('/temperature')
    assert response.status_code == 200
    data = response.get_json()
    assert "average_temperature" in data
    assert round(data["average_temperature"], 2) == 15
    assert data["status"] == "Good"

def test_temperature_endpoint_good(client, mocker):
    """Test the /temperature endpoint."""
    mock_data = [{'sensors': [{'unit': '°C', 'lastMeasurement': {'value': '40'}}]}]
    
    mocker.patch('app.fetch_data', return_value=mock_data)
    
    response = client.get('/temperature')
    assert response.status_code == 200
    data = response.get_json()
    assert "average_temperature" in data
    assert round(data["average_temperature"], 2) == 40
    assert data["status"] == "Too Hot"