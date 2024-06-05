from flask import Flask, request, jsonify
import sqlite3
import hashlib

app = Flask(_name_)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/signup", methods=["POST"])
def signup():
  data = request.json
  mmu_id = data.get("mmu_id")
  name = data.get("name")
  password = hash_password(data.get("password"))


with sqlite3.connect("users.db") as conn:
  cursor = conn.cursor()
  try:
    cursor.execute("INSERT INTO users (mmu_id, name, phone, password) VALUES (?, ?, 
  
