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
    assert data["version"] == "v0.2.0"
    
def test_temperature_endpoint(client, mocker):
    """Test the /temperature endpoint."""
    mock_data = [{'sensors': [{'unit': '°C', 'lastMeasurement': {'value': '22.5'}}]}]
    
    mocker.patch('app.fetch_data', return_value=mock_data)
    
    response = client.get('/temperature')
    assert response.status_code == 200
    data = response.get_json()
    assert "average_temperature" in data
    assert round(data["average_temperature"], 2) == 22.5
