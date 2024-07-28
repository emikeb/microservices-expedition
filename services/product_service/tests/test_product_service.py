import pytest
from microservices.services.product_service import app, init_db
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_product(client):
    product_data = {'name': 'Test Product', 'price': 9.99}
    response = client.post('/products', json=product_data)
    assert response.status_code == 201
    assert response.json['name'] == product_data['name']
    assert response.json['price'] == product_data['price']

def test_get_product(client):
    product_data = {'name': 'Test Product 2', 'price': 19.99}
    create_response = client.post('/products', json=product_data)
    product_id = create_response.json['id']

    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    assert response.json['name'] == product_data['name']
    assert response.json['price'] == product_data['price']

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
