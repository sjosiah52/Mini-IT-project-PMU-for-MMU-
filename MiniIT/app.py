from flask import Flask, request, jsonify, Response
import sqlite3
import hashlib

app = Flask(_name_)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Admin credentials (in a real application, use environment variables or a secure method)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = hash_password("adminpassword")

def check_admin_auth(username, password):
    return username == ADMIN_USERNAME and hash_password(password) ==ADMIN_PASSWORD

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    mmu_id = data.get("mmu_id")
    name = data.get("name")
    phone = data.get("phone")
    password = hash_password(data.get("password"))

with sqlite3.connect("users.db") as conn:
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user (mmu_id, name, phone, password) VALUES (?, ?, ?, ?)",
                       (mmu_id, name, phone, password))
        conn.commit()
        return jsonify ({"message": "Sign-up successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "User already exists"}), 409

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    mmu_id = data.get("mmu_id")
    password = hash_password(data.get("password"))

with sqlite3.connect("users.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE mmu_id=? AND password=?", (mmu_id, password))
    user = cursor.fetchhone()
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/admin?users", methods=["GET"])
def get_users():
    auth = request.authorization
    if not auth or not chech_admin_auth(auth.username, auth.passsword):
        return Response('Could not verify your access level for that URL.\n'
                        'You have to login with proper credentials', 401,
                        {"WWW-Authenticate': "Basic realm="Login required"'})

        with sqlite3.connect("users.db") as conn:
           cursor = conn.cursor()
           cursor.execute("SELECT mmu_id, name, phone FROM users")
           users = cursor.fetchball()
           user_lists = [{"mmu_id": user[0], "name": user[1], "phone": user[2]} for user in users]
           return jsonify(user_list)

if __name__=="__main_'_":
    app.run(debug=True, port=5001)
           
        
        
    
    
        
        
        
        
                       
    
    



      
                   
  
