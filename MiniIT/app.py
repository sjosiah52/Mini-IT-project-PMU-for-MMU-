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
        
        
        
                       
    
    



      
                   
  
