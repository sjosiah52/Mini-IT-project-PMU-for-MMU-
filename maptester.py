import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests
import math

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
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
            elif btn_text == "Services":
                btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=self.show_services, fg_color="#ff0000", hover_color="#555555")
            elif btn_text == "About":
                btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=self.show_about_info, fg_color="#ff0000", hover_color="#555555")
            else:
                btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=lambda text=btn_text: self.nav_command(text), fg_color="#ff0000", hover_color="#555555")
            btn.pack(side="left", padx=5, pady=5)

        # Main Content Frame
        self.main_content_frame = ctk.CTkFrame(self)
        self.main_content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Footer
        footer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#333")
        footer_frame.pack(side="bottom", fill="x")

        footer_label = ctk.CTkLabel(footer_frame, text="© 2024 Pick-Up For MMU. All rights reserved.", font=ctk.CTkFont(size=12), text_color="#ffffff")
        footer_label.pack(pady=10)

        # Initialize main content
        self.create_booking_form()

    def nav_command(self, text):
        print(f"Navigation button '{text}' clicked")

    def show_contact_info(self):
        # Clear previous content in main frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        contact_info = (
            "Contact Us:\n\n"
            "Support Email: support@pickupformmu.com\n"
            "Support Phone: +60 112-813-3770\n"
            "Office Address: Multimedia University , Cyberjaya, Malaysia\n"
            "Operating Hours: 10 AM - 6 PM, Monday - Friday"
        )

        # Display contact information
        contact_label = ctk.CTkLabel(self.main_content_frame, text=contact_info, font=ctk.CTkFont(size=14), justify="left")
        contact_label.pack(padx=20, pady=20)

        back_button = ctk.CTkButton(self.main_content_frame, text="Back", command=self.show_main_content, fg_color="#2600ff", hover_color="#555555")
        back_button.pack(pady=10)

    def show_about_info(self):
        # Clear previous content in main frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        about_info = (
            "About Pick-Up For MMU:\n\n"
            "Pick-Up For MMU is a ride-hailing service designed to provide convenient and affordable transportation "
            "for the Multimedia University community. Similar to the Grab app, our service allows you to book a ride "
            "with ease, track your driver, and reach your destination safely and efficiently. Whether you need a ride "
            "to class, the library, or anywhere within Cyberjaya, Pick-Up For MMU is here to serve you. With transparent "
            "pricing and reliable service, you can trust us for all your transportation needs.\n\n"
            "Features:\n"
            "- Easy ride booking with a user-friendly app\n"
            "- Real-time driver tracking\n"
            "- Transparent pricing with no hidden fees\n"
            "- Reliable and professional drivers\n"
            "- 24/7 customer support\n\n"
            "Experience a smooth and convenient journey with Pick-Up For MMU!"
        )

        # Display about information
        about_label = ctk.CTkLabel(self.main_content_frame, text=about_info, font=ctk.CTkFont(size=14), justify="left")
        about_label.pack(padx=20, pady=20)

        back_button = ctk.CTkButton(self.main_content_frame, text="Back", command=self.show_main_content, fg_color="#2600ff", hover_color="#555555")
        back_button.pack(pady=10)

    def show_main_content(self):
        # Clear previous content in main frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        # Re-display main content (booking form and map)
        self.create_booking_form()

    def show_services(self):
        # Clear previous content in main frame
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()

        services_label = ctk.CTkLabel(self.main_content_frame, text="Customer Services", font=ctk.CTkFont(size=20))
        services_label.pack(pady=10)

        complaint_label = ctk.CTkLabel(self.main_content_frame, text="Have a complaint or a question? Let us know:")
        complaint_label.pack(anchor="w", padx=20, pady=5)

        self.complaint_entry = ctk.CTkEntry(self.main_content_frame, width=600, height=200)
        self.complaint_entry.pack(padx=20, pady=5)

        submit_button = ctk.CTkButton(self.main_content_frame, text="Submit", command=self.submit_complaint, fg_color="#2600ff", hover_color="#555555")
        submit_button.pack(pady=20)

        back_button = ctk.CTkButton(self.main_content_frame, text="Back", command=self.show_main_content, fg_color="#2600ff", hover_color="#555555")
        back_button.pack(pady=10)

    def submit_complaint(self):
        complaint = self.complaint_entry.get()
        # Implement logic to handle the complaint here, e.g., send to support team
        print(f"Complaint Submitted: {complaint}")
        self.complaint_entry.delete(0, tk.END)

        submitted_label = ctk.CTkLabel(self.main_content_frame, text="Your complaint/question has been submitted. We will get back to you soon.", font=ctk.CTkFont(size=14), text_color="#00aa00")
        submitted_label.pack(pady=10)

    def create_booking_form(self):
        # Booking Form Frame
        form_frame = ctk.CTkFrame(self.main_content_frame)
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

        # Calculate Journey Button (formerly Book Now)
        calculate_button = ctk.CTkButton(form_frame, text="Calculate Journey", command=self.calculate_journey, fg_color="#2600ff", hover_color="#555555")
        calculate_button.pack(pady=20)

        # Confirm Order Button
        confirm_button = ctk.CTkButton(form_frame, text="Confirm Order", command=self.confirm_order, fg_color="#2600ff", hover_color="#555555")
        confirm_button.pack(pady=10)

        # Route Info
        self.route_info_frame = ctk.CTkFrame(form_frame)
        self.route_info_frame.pack(pady=10)

        self.route_info_label = ctk.CTkLabel(self.route_info_frame, text="", font=ctk.CTkFont(size=14))
        self.route_info_label.pack()

        self.time_info_label = ctk.CTkLabel(self.route_info_frame, text="", font=ctk.CTkFont(size=14))
        self.time_info_label.pack()

        # Order Info Frame
        self.order_info_frame = ctk.CTkFrame(form_frame)
        self.order_info_frame.pack(pady=10)

        # Map Frame
        map_frame = ctk.CTkFrame(self.main_content_frame)
        map_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Create the map widget
        self.gmap_widget = TkinterMapView(map_frame, width=600, height=400)
        self.gmap_widget.pack(fill="both", expand=True)

        # Set the tile server
        self.gmap_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # List to keep track of markers and paths
        self.markers = []
        self.paths = []

    def calculate_journey(self):
        pickup = self.pickup_entry.get()
        destination = self.destination_entry.get()

        print(f"Journey Details:\nPickup: {pickup}\nDestination: {destination}")

        # Get coordinates for pickup and destination
        pickup_coords = self.get_coordinates(pickup)
        destination_coords = self.get_coordinates(destination)

        if pickup_coords and destination_coords:
            # Clear previous markers and paths
            self.clear_markers_and_paths()

            # Display the route on the map
            self.gmap_widget.set_position(*pickup_coords)
            pickup_marker = self.gmap_widget.set_marker(*pickup_coords, text="Pickup")
            destination_marker = self.gmap_widget.set_marker(*destination_coords, text="Destination")

            # Draw the route path
            path = self.gmap_widget.set_path([pickup_coords, destination_coords])

            # Keep track of the markers and path
            self.markers.extend([pickup_marker, destination_marker])
            self.paths.append(path)

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

    def confirm_order(self):
        pickup = self.pickup_entry.get()
        destination = self.destination_entry.get()
        price = self.price_entry.get()

        # Implement order confirmation logic here, e.g., send confirmation email, update database, etc.
        print(f"Order Confirmed:\nPickup: {pickup}\nDestination: {destination}\nPrice: {price}")

        # Change the button to Cancel Order
        confirm_button = ctk.CTkButton(self.order_info_frame, text="Cancel Order", command=self.cancel_order, fg_color="#2600ff", hover_color="#555555")
        confirm_button.pack(pady=10)

        # Driver details (example data)
        driver_name = "John Doe"
        driver_phone = "+60 987-654-321"
        driver_car = "Toyota Camry"
        driver_plate = "ABC 1234"

        # Clear previous order info
        for widget in self.order_info_frame.winfo_children():
            if widget != confirm_button:  # Keep Cancel Order button
                widget.destroy()

        # Display order details
        order_label = ctk.CTkLabel(self.order_info_frame, text=f"Order Details:\n\n"
                                                               f"Pickup: {pickup}\n"
                                                               f"Destination: {destination}\n"
                                                               f"Price: {price}", font=ctk.CTkFont(size=14))
        order_label.pack(padx=20, pady=10)

        # Display estimated time for driver acceptance
        estimated_time_label = ctk.CTkLabel(self.order_info_frame, text="Estimated time for driver to accept: 5 minutes", font=ctk.CTkFont(size=14))
        estimated_time_label.pack(pady=5)

        # Display driver details
        driver_details_label = ctk.CTkLabel(self.order_info_frame, text=f"\nDriver Details:\n\n"
                                                                       f"Name: {driver_name}\n"
                                                                       f"Phone: {driver_phone}\n"
                                                                       f"Car: {driver_car}\n"
                                                                       f"License Plate: {driver_plate}", font=ctk.CTkFont(size=14))
        driver_details_label.pack(padx=20, pady=10)

    def cancel_order(self):
        # Ask for confirmation using messagebox
        result = messagebox.askquestion("Cancel Order", "Are you sure you want to cancel the order?", icon="warning")

        if result == 'yes':
            # Clear order info
            for widget in self.order_info_frame.winfo_children():
                widget.destroy()

            # Display cancellation message
            cancelled_label = ctk.CTkLabel(self.order_info_frame, text="Order cancelled successfully.", font=ctk.CTkFont(size=14), text_color="#00aa00")
            cancelled_label.pack(pady=10)

            # Change the button back to Confirm Order
            confirm_button = ctk.CTkButton(self.order_info_frame, text="Confirm Order", command=self.confirm_order, fg_color="#2600ff", hover_color="#555555")
            confirm_button.pack(pady=10)

    def clear_markers_and_paths(self):
        for marker in self.markers:
            marker.delete()
        self.markers = []

        for path in self.paths:
            path.delete()
        self.paths = []

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
