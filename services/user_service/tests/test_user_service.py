import pytest
from user_service import app, init_db
import sqlite3

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_user(client):
    user_data = {'username': 'testuser', 'email': 'test@example.com'}
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    assert response.json['username'] == user_data['username']
    assert response.json['email'] == user_data['email']

def test_get_user(client):
    user_data = {'username': 'testuser2', 'email': 'test2@example.com'}
    create_response = client.post('/users', json=user_data)
    user_id = create_response.json['id']

    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json['username'] == user_data['username']
    assert response.json['email'] == user_data['email']

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
