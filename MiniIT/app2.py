import sqlite3
import hashlib
from flask import Flask, request, jsonify, g
import subprocess

DATABASE = 'rides.db'

app2 = Flask(__name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = hash_password("adminpassword")

def check_admin_auth(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    get_db().commit()
    return (rv[0] if rv else None) if one else rv

@app2.route('/book_ride', methods=['POST'])
def book_ride():
    try:
        data = request.json
        pickup = data.get('pickup')
        destination = data.get('destination')
        price = data.get('price')
        name = data.get('name')
        phone = data.get('phone')

        if not name:
            return jsonify({'message': 'User name not provided in JSON data'}), 400

        # Insert ride into the database
        with app2.app_context():
            db = get_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO ride (pickup, destination, price, user_name, phone_number) VALUES (?, ?, ?, ?, ?)',
                           (pickup, destination, price, name, phone))
            db.commit()

        return jsonify({'message': 'Ride booked successfully'}), 200

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return jsonify({'message': 'Failed to save data to the database'}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500

@app2.route('/rides', methods=['GET'])
def get_rides():
    try:
        rides = query_db('SELECT id, pickup, destination, price, user_name FROM ride')
        return jsonify([{'id': row[0], 'pickup': row[1], 'destination': row[2], 'price': row[3], 'name': row[4]} for row in rides])
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return jsonify({'message': 'Failed to fetch rides from the database'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500

@app2.route('/accept_ride', methods=['POST'])
def accept_ride():
    data = request.get_json()
    ride_id = data.get('id')
    
    if ride_id is None:
        return jsonify({"error": "Ride ID not provided"}), 400

    try:
        conn = sqlite3.connect('rides.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM ride WHERE id = ?', (ride_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Ride accepted and removed from the database"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app2.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    # Initialize the database
    subprocess.run(["python", "init2_db.py"])
    app2.run(debug=True, port=5003)
