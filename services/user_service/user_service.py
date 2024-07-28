from flask import Flask, jsonify, request
import sqlite3
import os
import consul

app = Flask(__name__)

CONSUL_HOST = os.environ.get('CONSUL_HOST', 'localhost')
c = consul.Consul(host=CONSUL_HOST)

SERVICE_NAME = "user-service"
SERVICE_ID = f"{SERVICE_NAME}-{os.environ.get('HOSTNAME', 'unknown')}"
SERVICE_PORT = int(os.environ.get('SERVICE_PORT', 5000))

c.agent.service.register(
    name=SERVICE_NAME,
    service_id=SERVICE_ID,
    address=os.environ.get('SERVICE_HOST', 'localhost'),
    port=SERVICE_PORT,
    check=consul.Check.http(f"http://{os.environ.get('SERVICE_HOST', 'localhost')}:{SERVICE_PORT}/health", interval="10s")
)

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = [{'id': row[0], 'username': row[1], 'email': row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, email) VALUES (?, ?)',
              (user_data['username'], user_data['email']))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return jsonify({'id': user_id, 'username': user_data['username'], 'email': user_data['email']}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({'id': user[0], 'username': user[1], 'email': user[2]})
    return jsonify({'error': 'User not found'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT 1')
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except:
        return jsonify({"status": "unhealthy"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=SERVICE_PORT)
