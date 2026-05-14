"""
Tests for the Churn Prediction API.

Run with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
"""

from litestar.status_codes import HTTP_201_CREATED, HTTP_200_OK
from litestar.testing import TestClient
from main import app
from app.model_utils import predict_churn

# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------


# TODO 1: Write a test that calls predict_churn() directly with sample features
#         and asserts the result is 0 or 1
#         Hint: import predict_churn from app.model_utils
def test_predict_churn():
    sample = [619.0, 42.0, 2.0, 0.0, 1.0, 1.0, 1.0, 101348.88, 0, 0, 0]
    result = predict_churn(sample)
    assert result in [0, 1]


# TODO 2 (bonus): Write another function test with edge-case inputs
def test_predict_churn_edge_case():
    """
    Unit test for an edge case (e.g., all zeros or very high values).
    """
    high_values = [1000.0, 100.0, 20.0, 500000.0, 10.0, 1.0, 1.0, 200000.0, 1, 1, 1]
    result = predict_churn(high_values)
    assert result in [0, 1]


# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------


# TODO 3: Write a test that POSTs to /predict with valid JSON
#         and checks the status code and response body
#         Hint: Litestar POST returns 201, not 200
#         Hint: use `with TestClient(app=app) as client:`
def test_predict_endpoint_valid_json():
    """Test POST /predict with valid JSON"""
    valid_payload = {
        "CreditScore": 619.0,
        "Age": 42.0,
        "Tenure": 2.0,
        "Balance": 0.0,
        "NumOfProducts": 1.0,
        "HasCrCard": 1.0,
        "IsActiveMember": 1.0,
        "EstimatedSalary": 101348.88,
        "Geography_Germany": 0,
        "Geography_Spain": 0,
        "Gender_Male": 0,
    }

    with TestClient(app=app) as client:
        response = client.post("/predict", json=valid_payload)
        assert response.status_code == HTTP_201_CREATED
        assert "prediction" in response.json()
        assert response.json()["prediction"] in [0, 1]


# TODO 4: Write a test for GET /health
def test_health_endpoint():
    """Test GET /health"""
    with TestClient(app=app) as client:
        response = client.get("/health")
        assert response.status_code == HTTP_200_OK
        assert response.json() == {"status": "healthy"}


# TODO 5: Write a test for GET /
def test_home_endpoint():
    """Test GET /"""
    with TestClient(app=app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK
        assert "message" in response.json()


# TODO 6 (bonus): Test that invalid input returns status 400
def test_predict_endpoint_invalid_input():
    """Test POST /predict with missing fields (should return 400 or 422)"""
    invalid_payload = {"CreditScore": 619.0}

    with TestClient(app=app) as client:
        response = client.post("/predict", json=invalid_payload)
        assert response.status_code >= 400
