import dns.resolver
import smtplib
from flask import Flask, request, jsonify, Response, render_template, redirect, url_for
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
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = mx_records[0].exchange.to_text()
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(server.local_hostname)  # server.local_hostname(Get local server hostname)
        server.mail('me@domain.com')  # This should be a dummy email address
        code, message = server.rcpt(email)
        server.quit()
        if code == 250:
            return True
    except Exception as e:
        print(f"Failed to verify email: {e}")
    return False

# Hardcoded email address for testing
test_email = "1221109534@student.mmu.edu.my"

# Call the verify_email function with the test email address
if verify_email(test_email):
    print("Email is valid")
else:
    print("Email is invalid")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    mmu_id = data.get("mmu_id")
    name = data.get("name")
    phone = data.get("phone")
    password = hash_password(data.get("password"))

    email = f"{mmu_id}@student.mmu.edu.my"
    print(f"Validating email: {email}")  # Debug statement
    if not verify_email(email):
        print("Invalid MMU ID email")
        return jsonify({"message": "Invalid MMU ID"}), 400

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (mmu_id, name, phone, password) VALUES (?, ?, ?, ?)",
                           (mmu_id, name, phone, password))
            conn.commit()
            print("User added successfully")
            return jsonify({"message": "Sign-up successful"}), 201
        except sqlite3.IntegrityError:
            print("User already exists")
            return jsonify({"message": "User already exists"}), 409

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    mmu_id = data.get("mmu_id")
    password = hash_password(data.get("password"))

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE mmu_id=? AND password=?", (mmu_id, password))
        user = cursor.fetchone()
        if user:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

@app.route("/admin/users", methods=["GET"])
def get_users():
    auth = request.authorization
    if not auth or not check_admin_auth(auth.username, auth.password):
        return Response('Could not verify your access level for that URL.\n'
                        'You have to login with proper credentials', 401,
                        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT mmu_id, name, phone FROM users")
        users = cursor.fetchall()
        user_list = [{"mmu_id": user[0], "name": user[1], "phone": user[2]} for user in users]
        return jsonify(user_list)

@app.route("/admin/delete_user", methods=["POST"])
def delete_user():
    username = request.form.get("username")
    password = request.form.get("password")
    mmu_id = request.form.get("mmu_id")

    if not check_admin_auth(username, password):
        return Response('Could not verify your access level for that URL.\n'
                        'You have to login with proper credentials', 401,
                        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE mmu_id=?", (mmu_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        else:
            return jsonify({"message": "User deleted successfully"}), 200

@app.route("/admin/delete_form")
def delete_form():
    return render_template('delete_form.html')

@app.route("/validate_email/<email>", methods=["GET"])
def validate_email(email):
    valid = verify_email(email)
    return jsonify({"valid": valid}), 200 if valid else 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)
