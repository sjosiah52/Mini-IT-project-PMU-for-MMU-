from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create the rides table if it doesn't exist
conn = sqlite3.connect('rides.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS rides
             (id INTEGER PRIMARY KEY, pickup TEXT, destination TEXT, price REAL, user_name TEXT, user_phone TEXT, driver_name TEXT, driver_phone TEXT, status TEXT)''')
conn.commit()
conn.close()

# Endpoint to book a ride by users
@app.route('/book_ride', methods=['POST'])
def book_ride():
    try:
        data = request.json
        pickup = data.get('pickup')
        destination = data.get('destination')
        price = data.get('price')
        user_name = data.get('name')
        user_phone = data.get('phone')

        # SQLite connection and insertion
        conn = sqlite3.connect('rides.db')
        c = conn.cursor()
        c.execute("INSERT INTO rides (pickup, destination, price, user_name, user_phone, status) VALUES (?,?,?,?,?,?)",
                  (pickup, destination, price, user_name, user_phone, 'pending'))
        ride_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({"message": "Ride booked successfully!", "ride_id": ride_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/rides", methods=["GET"])
def get_rides():
    try:
        conn = sqlite3.connect("rides.db")
        c = conn.cursor()
        c.execute("SELECT id, pickup, destination, price, user_name, user_phone FROM rides")
        rides = c.fetchall()
        conn.close()

        rides_list = []
        for ride in rides:
            ride_dict = {
                "id": ride[0],
                "pickup": ride[1],
                "destination": ride[2],
                "price": ride[3],
                "name": ride[4],
                "phone": ride[5]
            }
            rides_list.append(ride_dict)

        return jsonify({"rides": rides_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Endpoint for drivers to view available rides
@app.route('/available_rides', methods=['GET'])
def get_available_rides():
    try:
        conn = sqlite3.connect('rides.db')
        c = conn.cursor()
        c.execute("SELECT id, pickup, destination, price FROM rides WHERE driver_name IS NULL AND status = 'pending'")
        rides = c.fetchall()
        conn.close()
        
        rides_list = []
        for ride in rides:
            ride_data = {
                "id": ride[0],
                "pickup": ride[1],
                "destination": ride[2],
                "price": ride[3]
            }
            rides_list.append(ride_data)
        
        return jsonify({"rides": rides_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for drivers to accept a ride
@app.route('/accept_ride', methods=['POST'])
def accept_ride():
    try:
        data = request.json
        ride_id = data.get('ride_id')
        driver_name = data.get('driver_name')
        driver_phone = data.get('driver_phone')

        # Connect to SQLite database
        conn = sqlite3.connect('rides.db')
        c = conn.cursor()

        # Update the ride with driver information
        c.execute("UPDATE rides SET driver_name =?, driver_phone =?, status =? WHERE id =?",
                  (driver_name, driver_phone, 'accepted', ride_id))
        
        # Fetch ride details after updating
        c.execute("SELECT pickup, destination, price, user_name, user_phone FROM rides WHERE id =?", (ride_id,))
        ride_details = c.fetchone()

        conn.commit()
        conn.close()

        if ride_details:
            return jsonify({
                "pickup": ride_details[0],
                "destination": ride_details[1],
                "price": ride_details[2],
                "name": ride_details[3],
                "phone": ride_details[4]
            }), 200
        else:
            return jsonify({"error": "Ride not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for drivers to view details of an accepted ride
@app.route('/accepted_ride/<int:ride_id>', methods=['GET'])
def get_accepted_ride(ride_id):
    try:
        conn = sqlite3.connect('rides.db')
        c = conn.cursor()
        c.execute("SELECT * FROM rides WHERE id=?", (ride_id,))
        ride = c.fetchone()
        conn.close()

        if not ride:
            return jsonify({"error": "Ride not found"}), 404

        ride_details = {
            "id": ride[0],
            "pickup": ride[1],
            "destination": ride[2],
            "price": ride[3],
            "user_name": ride[4],
            "user_phone": ride[5],
            "driver_name": ride[6],
            "driver_phone": ride[7],
            "status": ride[8]
        }

        return jsonify({"ride_details": ride_details}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/ride_details/<int:ride_id>', methods=['GET'])
def get_ride_details(ride_id):
    try:
        conn = sqlite3.connect('rides.db')
        c = conn.cursor()
        c.execute("SELECT * FROM rides WHERE id=?", (ride_id,))
        ride = c.fetchone()
        conn.close()

        if not ride:
            return jsonify({"error": "Ride not found"}), 404

        ride_details = {
            "id": ride[0],
            "pickup": ride[1],
            "destination": ride[2],
            "price": ride[3],
            "driver_name": ride[6],
            "driver_phone": ride[7]
        }

        return jsonify({"ride_details": ride_details}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5003)
