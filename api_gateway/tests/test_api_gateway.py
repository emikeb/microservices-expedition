import pytest
from microservices.api_gateway import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('microservices.api_gateway.get_service_url')
@patch('microservices.api_gateway.requests.get')
def test_get_users(mock_requests_get, mock_get_service_url, client):
    mock_get_service_url.return_value = 'http://user-service:5000'
    mock_requests_get.return_value.json.return_value = [{'id': 1, 'username': 'testuser', 'email': 'test@example.com'}]
    mock_requests_get.return_value.status_code = 200

    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1
    assert response.json[0]['username'] == 'testuser'

@patch('microservices.api_gateway.get_service_url')
@patch('microservices.api_gateway.requests.post')
def test_create_user(mock_requests_post, mock_get_service_url, client):
    mock_get_service_url.return_value = 'http://user-service:5000'
    mock_requests_post.return_value.json.return_value = {'id': 1, 'username': 'newuser', 'email': 'new@example.com'}
    mock_requests_post.return_value.status_code = 201

    user_data = {'username': 'newuser', 'email': 'new@example.com'}
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    assert response.json['username'] == user_data['username']
    assert response.json['email'] == user_data['email']

@patch('microservices.api_gateway.get_service_url')
@patch('microservices.api_gateway.requests.get')
def test_get_products(mock_requests_get, mock_get_service_url, client):
    mock_get_service_url.return_value = 'http://product-service:5001'
    mock_requests_get.return_value.json.return_value = [{'id': 1, 'name': 'Test Product', 'price': 9.99}]
    mock_requests_get.return_value.status_code = 200

    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Test Product'

@patch('microservices.api_gateway.get_service_url')
@patch('microservices.api_gateway.requests.post')
def test_create_product(mock_requests_post, mock_get_service_url, client):
    mock_get_service_url.return_value = 'http://product-service:5001'
    mock_requests_post.return_value.json.return_value = {'id': 1, 'name': 'New Product', 'price': 19.99}
    mock_requests_post.return_value.status_code = 201

    product_data = {'name': 'New Product', 'price': 19.99}
    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    assert response.json['name'] == product_data['name']
    assert response.json['price'] == product_data['price']

@patch('microservices.api_gateway.get_service_url')
@patch('microservices.api_gateway.requests.get')
def test_health_check(mock_requests_get, mock_get_service_url, client):
    mock_get_service_url.side_effect = ['http://user-service:5000', 'http://product-service:5001']
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {'status': 'healthy'}

    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
