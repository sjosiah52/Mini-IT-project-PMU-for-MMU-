import tkinter as tk
import customtkinter as ctk
from tkintermapview import TkinterMapView
import requests

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Your OpenRouteService API key
ORS_API_KEY = "your_openrouteservice_api_key"

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

        # Promo Code
        promo_label = ctk.CTkLabel(form_frame, text="Promo Code:")
        promo_label.pack(anchor="w", pady=5)

        self.promo_entry = ctk.CTkEntry(form_frame, width=300)
        self.promo_entry.pack(pady=5)

        # Book Now Button
        book_button = ctk.CTkButton(form_frame, text="Book Now", command=self.book_now, fg_color="#2600ff", hover_color="#555555")
        book_button.pack(pady=20)

        # Map Frame
        map_frame = ctk.CTkFrame(main_frame)
        map_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Create the map widget
        self.gmap_widget = TkinterMapView(map_frame, width=600, height=400)
        self.gmap_widget.pack(fill="both", expand=True)

        # Set the tile server
        self.gmap_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        # Set the address and add a marker
        self.gmap_widget.set_address("MMU CYBERJAYA", marker=True)

        # Route Info
        self.route_info_label = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(size=14))
        self.route_info_label.pack(pady=10)

        # Footer
        footer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#333")
        footer_frame.pack(side="bottom", fill="x")

        footer_label = ctk.CTkLabel(footer_frame, text="© 2024 Pick-Up For MMU. All rights reserved.", font=ctk.CTkFont(size=12), text_color="#ffffff")
        footer_label.pack(pady=10)

    def nav_command(self, text):
        print(f"Navigation button '{text}' clicked")

    def book_now(self):
        pickup = self.pickup_entry.get()
        destination = self.destination_entry.get()
        promo_code = self.promo_entry.get()

        print(f"Booking Details:\nPickup: {pickup}\nDestination: {destination}\nPromo Code: {promo_code}")

        # Get coordinates for pickup and destination
        pickup_coords = self.get_coordinates(pickup)
        destination_coords = self.get_coordinates(destination)

        if pickup_coords and destination_coords:
            # Display the route on the map
            self.gmap_widget.set_position(*pickup_coords)
            self.gmap_widget.set_marker(*pickup_coords, text="Pickup")
            self.gmap_widget.set_marker(*destination_coords, text="Destination")

            # Get route information and path coordinates
            route_info, path_coordinates = self.get_route_info(pickup_coords, destination_coords)

            if path_coordinates:
                self.gmap_widget.set_path(path_coordinates)

            self.route_info_label.configure(text=route_info)

    def get_coordinates(self, address):
        try:
            response = requests.get(
                f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
            )
            response_json = response.json()
            if response_json:
                return float(response_json[0]['lat']), float(response_json[0]['lon'])
            else:
                return None
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None

    def get_route_info(self, start_coords, end_coords):
        try:
            headers = {
                'Authorization': ORS_API_KEY,
                'Content-Type': 'application/json'
            }
            body = {
                "coordinates": [list(start_coords), list(end_coords)],
                "format": "geojson"
            }
            print(f"Requesting route info with body: {body}")
            
            response = requests.post(
                "https://api.openrouteservice.org/v2/directions/driving-car",
                json=body,
                headers=headers
            )
            
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")

            # Check if the response status code is 200 (OK)
            if response.status_code != 200:
                print(f"HTTP Error: {response.status_code} - {response.reason}")
                return "Unable to retrieve route info", None
            
            response_json = response.json()
            
            print(f"Response JSON: {response_json}")

            # Check if the response JSON contains the expected data
            if 'features' not in response_json or not response_json['features']:
                print(f"Unexpected response structure: {response_json}")
                return "Unable to retrieve route info", None

            # Extract distance and duration
            distance = response_json['features'][0]['properties']['segments'][0]['distance'] / 1000  # in km
            duration = response_json['features'][0]['properties']['segments'][0]['duration'] / 60  # in minutes

            # Extract path coordinates
            path_coordinates = [
                (coord[1], coord[0]) for coord in response_json['features'][0]['geometry']['coordinates']
            ]

            # Calculate total time based on average speed
            average_speed_kmh = 40  # km/h
            estimated_time_minutes = (distance / average_speed_kmh) * 60  # in minutes

            route_info = f"Distance: {distance:.2f} km\nDuration: {duration:.2f} min\nEstimated Total Time: {estimated_time_minutes:.2f} min"

            return route_info, path_coordinates
        except requests.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return "Unable to retrieve route info", None
        except ValueError as e:
            print(f"JSON Parsing failed: {e}")
            return "Unable to retrieve route info", None
        except KeyError as e:
            print(f"Expected data not found in response: {e}")
            return "Unable to retrieve route info", None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return "Unable to retrieve route info", None

if __name__ == "__main__":
    app = App()
    app.mainloop()
