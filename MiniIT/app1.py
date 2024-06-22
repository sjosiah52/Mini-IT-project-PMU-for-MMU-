import sqlite3
import hashlib
import requests
from flask import Flask, request, jsonify, Response, render_template
from init1_db import initialize_database

app1 = Flask(__name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = hash_password("adminpassword")

def check_admin_auth(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD

def verify_email(email):
    API_KEY = '1852a73007a78997b959aa5191853dcbf45a1a9c'
    response = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={API_KEY}')
    data = response.json()
    return data['data']['status'] == 'valid'

initialize_database()

@app1.route("/driver_signup", methods=["POST"])
def driver_signup():
    data = request.json
    mmu_id = data.get("mmu_id")
    ic_number = data.get("ic_number")
    vehicle_registration_number = data.get("vehicle_registration_number")
    password = hash_password(data.get("password"))

    email = f"{mmu_id}@student.mmu.edu.my"
    if not verify_email(email):
        return jsonify({"message": "Invalid MMU ID"}), 400

    with sqlite3.connect("drivers.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO drivers (mmu_id, ic_number, vehicle_registration_number, password) VALUES (?, ?, ?, ?)",
                           (mmu_id, ic_number, vehicle_registration_number, password))
            conn.commit()
            return jsonify({"message": "Driver sign-up successful"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"message": "Driver already exists"}), 409
    
@app1.route("/driver_login", methods=["POST"])
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

@app1.route("/admin/drivers", methods=["GET"])
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
        return render_template('admin_driver.html', users=drivers)

@app1.route("/admin/delete_drivers", methods=["POST"])
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

@app1.route("/admin/delete_form")
def delete_form():
    return render_template('delete_form2.html')

if __name__ == "__main__":
    app1.run(debug=True, port=5002)
