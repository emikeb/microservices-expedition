from flask import Flask, jsonify, request
import sqlite3
import os
import consul

app = Flask(__name__)


CONSUL_HOST = os.environ.get('CONSUL_HOST', 'localhost')
c = consul.Consul(host=CONSUL_HOST)

SERVICE_NAME = "product-service"
SERVICE_ID = f"{SERVICE_NAME}-{os.environ.get('HOSTNAME', 'unknown')}"
SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 5001))

c.agent.service.register(
    name=SERVICE_NAME,
    service_id=SERVICE_ID,
    address=os.environ.get('SERVICE_HOST', 'localhost'),
    port=SERVICE_PORT,
    check=consul.Check.http(f"http://{os.environ.get('SERVICE_HOST', 'localhost')}:{SERVICE_PORT}/health", interval="10s")
)

def init_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  price REAL NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/products', methods=['GET'])
def get_products():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = [{'id': row[0], 'name': row[1], 'price': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    product_data = request.json
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, price) VALUES (?, ?)',
              (product_data['name'], product_data['price']))
    conn.commit()
    product_id = c.lastrowid
    conn.close()
    return jsonify({'id': product_id, 'name': product_data['name'], 'price': product_data['price']}), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    conn.close()
    if product:
        return jsonify({'id': product[0], 'name': product[1], 'price': product[2]})
    return jsonify({'error': 'Product not found'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute('SELECT 1')
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except:
        return jsonify({"status": "unhealthy"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVICE_PORT)
