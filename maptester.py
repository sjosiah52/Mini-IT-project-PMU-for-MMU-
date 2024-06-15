import tkinter as tk
import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests
import math

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Your OpenCage API key
OPENCAGE_API_KEY = "8ff4cd18db4e436c90a5fc5e06574570"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pick-Up For MMU")
        self.geometry("1200x800")  # Adjusted to fit the map and form together

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

        # Price Label
        price_label = ctk.CTkLabel(form_frame, text="Price:")
        price_label.pack(anchor="w", pady=5)

        self.price_entry = ctk.CTkEntry(form_frame, width=300)
        self.price_entry.pack(pady=5)

        # Book Now Button
        book_button = ctk.CTkButton(form_frame, text="Book Now", command=self.book_now, fg_color="#2600ff", hover_color="#555555")
        book_button.pack(pady=20)

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
            a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
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

if __name__ == "__main__":
    app = App()
    app.mainloop()
