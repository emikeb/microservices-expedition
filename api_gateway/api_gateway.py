# api_gateway.py
from flask import Flask, jsonify, request
import requests
import os
import consul

app = Flask(__name__)

CONSUL_HOST = os.environ.get('CONSUL_HOST', 'localhost')
c = consul.Consul(host=CONSUL_HOST)

def get_service_url(service_name):
    _, services = c.health.service(service_name, passing=True)
    if services:
        address = services[0]['Service']['Address']
        port = services[0]['Service']['Port']
        return f"http://{address}:{port}"
    return None

@app.route('/users', methods=['GET', 'POST'])
def users():
    user_service_url = get_service_url('user-service')
    if not user_service_url:
        return jsonify({"error": "User service unavailable"}), 503
    
    if request.method == 'GET':
        response = requests.get(f"{user_service_url}/users")
    elif request.method == 'POST':
        response = requests.post(f"{user_service_url}/users", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/users/<int:user_id>', methods=['GET'])
def user(user_id):
    user_service_url = get_service_url('user-service')
    if not user_service_url:
        return jsonify({"error": "User service unavailable"}), 503
    
    response = requests.get(f"{user_service_url}/users/{user_id}")
    return jsonify(response.json()), response.status_code

@app.route('/products', methods=['GET', 'POST'])
def products():
    product_service_url = get_service_url('product-service')
    if not product_service_url:
        return jsonify({"error": "Product service unavailable"}), 503
    
    if request.method == 'GET':
        response = requests.get(f"{product_service_url}/products")
    elif request.method == 'POST':
        response = requests.post(f"{product_service_url}/products", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/products/<int:product_id>', methods=['GET'])
def product(product_id):
    product_service_url = get_service_url('product-service')
    if not product_service_url:
        return jsonify({"error": "Product service unavailable"}), 503
    
    response = requests.get(f"{product_service_url}/products/{product_id}")
    return jsonify(response.json()), response.status_code

@app.route('/health', methods=['GET'])
def health_check():
    user_service_url = get_service_url('user-service')
    product_service_url = get_service_url('product-service')
    
    if user_service_url and product_service_url:
        user_health = requests.get(f"{user_service_url}/health").status_code == 200
        product_health = requests.get(f"{product_service_url}/health").status_code == 200
        
        if user_health and product_health:
            return jsonify({"status": "healthy"}), 200
    
    return jsonify({"status": "unhealthy"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVICE_PORT', 8000)))
