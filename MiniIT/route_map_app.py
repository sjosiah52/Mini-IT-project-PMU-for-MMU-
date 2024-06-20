import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests
import math
from user_ride_confirmation import RideDetailsApp
import tkinter as tk

# Your OpenCage API key
OPENCAGE_API_KEY = "8ff4cd18db4e436c90a5fc5e06574570"

class RouteMapApp(ctk.CTk):
    def __init__(self, width=1200, height=800):
        super().__init__()

        self.title("Pick-Up For MMU")
        self.geometry(f"{width}x{height}")
        # Header
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#ff0000")
        header_frame.pack(fill="x")

        header_label = ctk.CTkLabel(header_frame, text="Pick Me Up For MMU", font=ctk.CTkFont(size=24, weight="bold"), text_color="#ffffff")
        header_label.pack(pady=10)

        # Navigation
        nav_frame = ctk.CTkFrame(self)
        nav_frame.pack(fill="x")

        nav_buttons = ["Home", "About", "Services", "Contact"]
        for btn_text in nav_buttons:
            if btn_text == "Contact":
                btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=self.show_contact_info, fg_color="#ff0000", hover_color="#555555")
            else:
                btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=lambda text=btn_text: self.nav_command(text), fg_color="#ff0000", hover_color="#555555")
            btn.pack(side="left", padx=5, pady=5)

        # Main Content
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Booking Form Frame
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(side="left", padx=20, pady=20, fill="y")

        booking_label = ctk.CTkLabel(form_frame, text="Book a Ride", font=ctk.CTkFont(size=20))
        booking_label.pack(pady=10)

        # Pickup Location
        pickup_label = ctk.CTkLabel(form_frame, text="Pickup Location:")
        pickup_label.pack(anchor="w", pady=5)

        self.pickup_entry = ctk.CTkEntry(form_frame, width=300)
        self.pickup_entry.pack(pady=5)

        # Destination
        destination_label = ctk.CTkLabel(form_frame, text="Destination:")
        destination_label.pack(anchor="w", pady=5)

        self.destination_entry = ctk.CTkEntry(form_frame, width=300)
        self.destination_entry.pack(pady=5)

        # User Name
        user_label = ctk.CTkLabel(form_frame, text="User Name:")
        user_label.pack(anchor="w", pady=5)

        self.user_entry = ctk.CTkEntry(form_frame, width=300)
        self.user_entry.pack(pady=5)  

        # Price Label
        price_label = ctk.CTkLabel(form_frame, text="Price:")
        price_label.pack(anchor="w", pady=5)

        self.price_entry = ctk.CTkEntry(form_frame, width=300)
        self.price_entry.pack(pady=5)
        
        #Phone number
        phone_label = ctk.CTkLabel(form_frame, text="Phone Number:")
        phone_label.pack(anchor="w", pady=5)

        self.phone_entry = ctk.CTkEntry(form_frame, width=300)
        self.phone_entry.pack(pady=5)
        
        # Book Now Button
        book_button = ctk.CTkButton(form_frame, text="Check Price", command=self.book_now, fg_color="#2600ff", hover_color="#555555")
        book_button.pack(pady=20)

        confirm_button = ctk.CTkButton(form_frame, text="Confirm Ride", command=self.confirm_ride, fg_color="#2600ff", hover_color="#555555")
        confirm_button.pack(pady=10)

        # Route Info
        self.route_info_frame = ctk.CTkFrame(form_frame)
        self.route_info_frame.pack(pady=10)

        self.route_info_label = ctk.CTkLabel(self.route_info_frame, text="", font=ctk.CTkFont(size=14))
        self.route_info_label.pack()

        self.time_info_label = ctk.CTkLabel(self.route_info_frame, text="", font=ctk.CTkFont(size=14))
        self.time_info_label.pack()

        # Map Frame
        map_frame = ctk.CTkFrame(main_frame)
        map_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Create the map widget
        self.gmap_widget = TkinterMapView(map_frame, width=600, height=400)
        self.gmap_widget.pack(fill="both", expand=True)

        # Set the tile server
        self.gmap_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # List to keep track of markers
        self.markers = []

        # Footer
        footer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#333")
        footer_frame.pack(side="bottom", fill="x")

        footer_label = ctk.CTkLabel(footer_frame, text="© 2024 Pick-Up For MMU. All rights reserved.", font=ctk.CTkFont(size=12), text_color="#ffffff")
        footer_label.pack(pady=10)

        # Initialize fullscreen mode
        self.is_fullscreen = False
        self.fullscreen()

        # Bind Escape key to toggle fullscreen
        self.bind("<Escape>", lambda e: self.toggle_fullscreen())

    def confirm_ride(self):
        pickup = self.pickup_entry.get()
        destination = self.destination_entry.get()
        price = self.price_entry.get()
        name = self.user_entry.get()
        phone = self.phone_entry.get()

        data = {
            "pickup": pickup,
            "destination": destination,
            "price": price,
            "name": name,
            "phone": phone
        }

        try:
            response = requests.post("http://127.0.0.1:5003/book_ride", json=data)
            if response.status_code == 200:
                print("Ride confirmed and data saved to the database.")
            else:
                print("Failed to save data to the database.")
        except Exception as e:
            print(f"Error confirming ride: {e}")

    def nav_command(self, text):
        print(f"Navigation button '{text}' clicked")

    def show_contact_info(self):
        contact_info = (
            "Contact Us:\n\n"
            "Support Email: support@pickupformmu.com\n"
            "Support Phone: +60 123-456-789\n"
            "Office Address: 123 MMU Street, Cyberjaya, Malaysia\n"
            "Operating Hours: 9 AM - 6 PM, Monday to Friday"
        )
        contact_window = ctk.CTkToplevel(self)
        contact_window.title("Contact Information")
        contact_window.geometry("400x300")

        contact_label = ctk.CTkLabel(contact_window, text=contact_info, font=ctk.CTkFont(size=14), justify="left")
        contact_label.pack(padx=20, pady=20)

        back_button = ctk.CTkButton(contact_window, text="Back", command=contact_window.destroy, fg_color="#2600ff", hover_color="#555555")
        back_button.pack(pady=10)

    def book_now(self):
        pickup = self.pickup_entry.get()
        destination = self.destination_entry.get()

        print(f"Booking Details:\nPickup: {pickup}\nDestination: {destination}")

        # Get coordinates for pickup and destination
        pickup_coords = self.get_coordinates(pickup)
        destination_coords = self.get_coordinates(destination)

        if pickup_coords and destination_coords:
            # Clear previous markers
            self.clear_markers()

            # Display the route on the map
            self.gmap_widget.set_position(*pickup_coords)
            pickup_marker = self.gmap_widget.set_marker(*pickup_coords, text="Pickup")
            destination_marker = self.gmap_widget.set_marker(*destination_coords, text="Destination")

            # Keep track of the markers
            self.markers.extend([pickup_marker, destination_marker])

            # Calculate and display total distance
            total_distance = self.calculate_total_distance(pickup_coords, destination_coords)
            if total_distance is not None:
                self.route_info_label.configure(text=f"Total Distance: {total_distance:.2f} km")

                # Calculate and display total time
                average_speed = 30  # Assuming an average speed of 30 km/h
                total_time_hours = total_distance / average_speed
                total_time_minutes = total_time_hours * 60
                self.time_info_label.configure(text=f"Estimated Time: {total_time_minutes:.2f} minutes")

                # Calculate and display price
                price = self.calculate_price(total_distance)
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, f"RM {price:.2f}")

    def clear_markers(self):
        for marker in self.markers:
            marker.delete()
        self.markers = []

    def get_coordinates(self, address):
        try:
            # Construct the geocoding API request URL
            url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={OPENCAGE_API_KEY}&language=en&pretty=1"

            # Send the request
            response = requests.get(url)
            response_json = response.json()

            # Extract latitude and longitude from the response
            if response_json['results']:
                lat = response_json['results'][0]['geometry']['lat']
                lng = response_json['results'][0]['geometry']['lng']
                return lat, lng
            else:
                print(f"Geocoding failed for {address}")
                return None
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None

    def calculate_total_distance(self, start_coords, end_coords):
        try:
            # Calculate distance using Haversine formula
            lat1, lon1 = start_coords
            lat2, lon2 = end_coords

            # Radius of the Earth in km
            R = 6371.0

            # Convert latitude and longitude from degrees to radians
            lat1_rad = math.radians(lat1)
            lon1_rad = math.radians(lon1)
            lat2_rad = math.radians(lat2)
            lon2_rad = math.radians(lon2)

            # Calculate differences in latitude and longitude
            dlon = lon2_rad - lon1_rad
            dlat = lat2_rad - lat1_rad

            # Haversine formula to calculate distance
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c

            return distance
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return None

    def calculate_price(self, distance):
        base_fare = 5.0  # Base fare in Ringgit Malaysia (RM)
        rate_per_km = 2.50  # Rate per kilometer in Ringgit Malaysia (RM)
        price = base_fare + (rate_per_km * distance)
        return price

    def confirm_ride(self):
        pickup = self.pickup_entry.get()
        destination = self.destination_entry.get()
        price = self.price_entry.get()
        name = self.user_entry.get()
        phone = self.phone_entry.get()

        data = {
            "pickup": pickup,
            "destination": destination,
            "price": price,
            "name": name,
            "phone": phone
        }
        try:
            response = requests.post("http://127.0.0.1:5003/book_ride", json=data)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            print("Ride booked successfully!")

            # Get the ride ID from the response
            ride_id = response.json().get("ride_id")

            # Create a new window to display ride details
            ride_details_window = tk.Toplevel(self)
            ride_details_window.title("Ride Details")

            # Create a label to display ride details
            ride_details_label = tk.Label(ride_details_window, text="", font=("Helvetica", 12))
            ride_details_label.pack(pady=10)

            # Fetch ride details from server
            response = requests.get(f"http://127.0.0.1:5003/ride_details/{ride_id}")
            if response.status_code == 200:
                ride_details = response.json()["ride_details"]
                ride_details_text = f"Ride ID: {ride_details['id']}\nPickup: {ride_details['pickup']}\nDestination: {ride_details['destination']}\nPrice: {ride_details['price']}"

                # Add a label to display driver information
                driver_info_label = tk.Label(ride_details_window, text="", font=("Helvetica", 12))
                driver_info_label.pack(pady=10)

                # Update the ride status and fetch driver information
                def update_ride_status():
                    response = requests.get(f"http://127.0.0.1:5003/accepted_ride/{ride_id}")
                    if response.status_code == 200:
                        ride_details = response.json()
                        if ride_details.get("driver_name") and ride_details.get("driver_phone"):
                            driver_info_text = f"Driver Name: {ride_details['driver_name']}\nPhone: {ride_details['driver_phone']}"
                            driver_info_label.config(text=driver_info_text)
                        else:
                            driver_info_label.config(text="Waiting for driver to accept...")
                    else:
                        print(f"Failed to fetch ride status: {response.json().get('error')}")
                        driver_info_label.config(text="Failed to fetch ride status", fg="red")
                    ride_details_window.after(5000, update_ride_status)  # Update every 5 seconds

                update_ride_status()  # Initial update

                ride_details_label.configure(text=ride_details_text)
            else:
                print(f"Failed to fetch ride details: {response.json().get('error')}")
                ride_details_label.configure(text="Failed to fetch ride details", fg="red")

        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong", err)

        # Clear the form fields
        self.pickup_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        def update_ride_status():
            response = requests.get(f"http://127.0.0.1:5003/accepted_ride/{ride_id}")
            if response.status_code == 200:
                ride_details = response.json()
                if ride_details.get("driver_name") and ride_details.get("driver_phone"):
                    driver_info_text = f"Driver Name: {ride_details['driver_name']}\nPhone: {ride_details['driver_phone']}"
                    driver_info_label.config(text=driver_info_text)
                else:
                    driver_info_label.config(text="Waiting for driver to accept...")
            else:
                print(f"Failed to fetch ride status: {response.json().get('error')}")
                driver_info_label.config(text="Failed to fetch ride status", fg="red")
            ride_details_window.after(5000, update_ride_status)  # Update every 5 seconds

        update_ride_status()
    
    def on_confirm_ride_button_click(self):
        pickup = self.pickup_entry.get()
        destination = self.destination_entry.get()
        price = self.price_entry.get()

        if not pickup or not destination or not price:
            self.status_label.configure(text="Please fill in all fields", fg="red")
            return

        try:
            price = float(price)
            if price <= 0:
                self.status_label.configure(text="Price must be greater than 0", fg="red")
                return
        except ValueError:
            self.status_label.configure(text="Invalid price", fg="red")
            return

        try:
            response = requests.post("http://127.0.0.1:5003/create_ride", json={"pickup": pickup, "destination": destination, "price": price})
            if response.status_code == 200:
                ride_id = response.json()["ride_id"]
                self.status_label.configure(text="Ride created successfully", fg="green")

                # Create an instance of the RideDetailsApp
                ride_details_app = RideDetailsApp(self,ride_id)
                ride_details_app.mainloop()

                # Clear the input fields
                self.pickup_entry.delete(0, tk.END)
                self.destination_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
            else:
                self.status_label.configure(text="Failed to create ride", fg="red")
        except Exception as e:
            self.status_label.configure(text=f"Error creating ride: {e}", fg="red")

    def fullscreen(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.attributes('-fullscreen', True)
        self.is_fullscreen = True

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.geometry("1200x800")
            self.attributes('-fullscreen', False)
            self.is_fullscreen = False
        else:
            self.fullscreen()

if __name__ == "__main__":
    app = RouteMapApp(1200, 800)
    app.mainloop()
