import requests
from flask import Flask, request, jsonify, Response, render_template
import sqlite3
import hashlib

app = Flask(__name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = hash_password("adminpassword")

def check_admin_auth(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD

def verify_email(email):
    API_KEY = '1852a73007a78997b959aa5191853dcbf45a1a9c'  # Replace with your Hunter API key
    response = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={API_KEY}')
    data = response.json()
    return data['data']['status'] == 'valid'

@app.route("/driver_signup", methods=["POST"])
def driver_signup():
    data = request.json
    mmu_id = data.get("mmu_id")
    ic_number = data.get("ic_number")
    vehicle_registration_number = data.get("vehicle_registration_number")
    password = hash_password(data.get("password"))

    email = f"{mmu_id}@student.mmu.edu.my"
    if not verify_email(email):
        return jsonify({"message": "Invalid MMU ID"}), 400

    try:
        with sqlite3.connect("drivers.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO drivers (mmu_id, ic_number, vehicle_registration_number, password) VALUES (?, ?, ?, ?)",
                           (mmu_id, ic_number, vehicle_registration_number, password))
            conn.commit()
            return jsonify({"message": "Driver sign-up successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Driver already exists"}), 409
    except Exception as e:
        return jsonify({"message": f"Sign-up failed: {str(e)}"}), 500

@app.route("/driver_login", methods=["POST"])
def driver_login():
    data = request.json
    mmu_id = data.get("mmu_id")
    password = hash_password(data.get("password"))

    with sqlite3.connect("drivers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drivers WHERE mmu_id=? AND password=?", (mmu_id, password))
        driver = cursor.fetchone()
        if driver:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

@app.route("/admin/drivers", methods=["GET"])
def get_drivers():
    auth = request.authorization
    if not auth or not check_admin_auth(auth.username, auth.password):
        return Response('Could not verify your access level for that URL.\n'
                        'You have to login with proper credentials', 401,
                        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    with sqlite3.connect("drivers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT mmu_id, ic_number, vehicle_registration_number FROM drivers")
        drivers = cursor.fetchall()
        driver_list = [{"mmu_id": driver[0], "ic_number": driver[1], "vehicle_registration_number": driver[2]} for driver in drivers]
        return jsonify(driver_list)

@app.route("/admin/delete_drivers", methods=["POST"])
def delete_drivers():
    auth = request.authorization
    if not auth or not check_admin_auth(auth.username, auth.password):
        return Response('Could not verify your access level for that URL.\n'
                        'You have to login with proper credentials', 401,
                        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    mmu_id = request.form.get("mmu_id")

    with sqlite3.connect("drivers.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM drivers WHERE mmu_id=?", (mmu_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Driver not found"}), 404
        else:
            return jsonify({"message": "Driver deleted successfully"}), 200

@app.route("/admin/delete_form")
def delete_form():
    return render_template('delete_form2.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
