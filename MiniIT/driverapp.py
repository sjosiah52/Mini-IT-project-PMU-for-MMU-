import tkinter as tk
import requests
import os
import subprocess

class DriverPageApp(tk.Tk):
    def __init__(self, width=800, height=600):
        super().__init__()

        self.title("Driver Page - Accept Rides")
        self.geometry(f"{width}x{height}")

        # Header
        header_frame = tk.Frame(self, bg="#ff0000")
        header_frame.pack(fill="x")

        header_label = tk.Label(header_frame, text="Driver Page - Accept Rides", font=("Helvetica", 24, "bold"), fg="#ffffff", bg="#ff0000")
        header_label.pack(pady=10)

        # Main Frame
        main_frame = tk.Frame(self)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Frame for Listbox and Scrollbars
        listbox_frame = tk.Frame(main_frame)
        listbox_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Listbox to display ride requests
        self.ride_listbox = tk.Listbox(listbox_frame, font=("Helvetica", 14), selectmode="single")
        self.ride_listbox.pack(side="left", fill="both", expand=True)

        # Scrollbars for the Listbox
        vertical_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=self.ride_listbox.yview)
        vertical_scrollbar.pack(side="right", fill="y")
        self.ride_listbox.config(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = tk.Scrollbar(listbox_frame, orient="horizontal", command=self.ride_listbox.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")
        self.ride_listbox.config(xscrollcommand=horizontal_scrollbar.set)

        # Accept Ride Button
        accept_button = tk.Button(main_frame, text="Accept Ride", command=self.on_accept_ride_button_click)
        accept_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(main_frame, text="")
        self.status_label.pack(pady=10)

        # Driver Name and Phone Number Entry
        self.driver_name_label = tk.Label(main_frame, text="Driver Name:")
        self.driver_name_label.pack()
        self.driver_name_entry = tk.Entry(main_frame)
        self.driver_name_entry.pack()

        self.driver_phone_label = tk.Label(main_frame, text="Driver Phone Number:")
        self.driver_phone_label.pack()
        self.driver_phone_entry = tk.Entry(main_frame)
        self.driver_phone_entry.pack()

        check_detail_button = tk.Button(main_frame, text="Check Ride Details", command=self.open_ride_details)
        check_detail_button.pack(pady=10)

        # Fetch and display ride requests
        self.fetch_ride_requests()

    def open_ride_details(self):
        script_path = os.path.join(os.path.dirname(__file__), "user_ride_confirmation.py")
        subprocess.Popen(["python", script_path])

    def fetch_ride_requests(self):
        try:
            response = requests.get("http://127.0.0.1:5003/available_rides")

            if response.status_code == 200:
                ride_requests = response.json()["rides"]  # Access the "rides" key
                self.ride_listbox.delete(0, tk.END)
                self.rides = {}  # Dictionary to store ride_id and corresponding ride data
                for ride in ride_requests:
                    ride_str = f"ID: {ride['id']}, Pickup: {ride['pickup']}, Destination: {ride['destination']}, Price: {ride['price']}, Name:{ride['user_name']}"
                    self.ride_listbox.insert(tk.END, ride_str)
                    self.rides[ride_str] = ride['id']  # Map ride_str to ride_id
            else:
                print(f"Failed to fetch ride requests. Status code: {response.status_code}")
                self.status_label.configure(text="Failed to fetch ride requests", fg="red")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            self.status_label.configure(text=f"Request error: {e}", fg="red")
        except Exception as e:
            print(f"An error occurred: {e}")
            self.status_label.configure(text=f"An error occurred: {e}", fg="red")

    def on_accept_ride_button_click(self):
        selected_ride = self.ride_listbox.get(tk.ACTIVE)
        if selected_ride:
            ride_id = self.rides.get(selected_ride)
            if ride_id:
                driver_name = self.driver_name_entry.get()
                driver_phone = self.driver_phone_entry.get()
                if driver_name and driver_phone:
                    self.accept_ride(ride_id, driver_name, driver_phone)
                else:
                    self.status_label.configure(text="Please enter your name and phone number", fg="red")

    def accept_ride(self, ride_id, driver_name, driver_phone):
        try:
            response = requests.post("http://127.0.0.1:5003/accept_ride", json={
                "ride_id": ride_id,
                "driver_name": driver_name,
                "driver_phone": driver_phone
            })

            if response.status_code == 200:
                print("Ride accepted and updated in the database.")
                self.status_label.configure(text="Ride accepted. Please visit the Ride Details to view your whole ride details.", fg="green")
                self.fetch_ride_requests()  # Refresh the ride list

                # Show ride details window
                self.show_ride_details(ride_id)

            else:
                error_message = response.json().get("error")
                print(f"Failed to accept ride: {error_message}")
                self.status_label.configure(text=f"Failed to accept ride: {error_message}", fg="red")

        except Exception as e:
            print(f"Error accepting ride: {e}")
            self.status_label.configure(text=f"Error accepting ride: {e}", fg="red")

    def show_ride_details(self, ride_id):
        # Create a new window to display ride details
        ride_details_window = tk.Toplevel(self)
        ride_details_window.title("Ride Details")

        # Create a label to display ride details
        ride_details_label = tk.Label(ride_details_window, text="", font=("Helvetica", 12))
        ride_details_label.pack(pady=10)

        # Fetch ride details from server using the new endpoint
        try:
            response = requests.get(f"http://127.0.0.1:5003/ride_detail/{ride_id}")
            if response.status_code == 200:
                ride_details = response.json()

                # Ensure ride_details is a dictionary
                if isinstance(ride_details, dict):
                    ride_details_text = f"Ride ID: {ride_details.get('id')}\nPickup: {ride_details.get('pickup')}\nDestination: {ride_details.get('destination')}\nPrice: {ride_details.get('price')}\nUser Name: {ride_details.get('user_name')}\nUser Phone: {ride_details.get('user_phone')}"
                    ride_details_label.config(text=ride_details_text)
                else:
                    ride_details_label.config(text="Invalid ride details format", fg="red")
            else:
                ride_details_label.config(text="Error fetching ride details", fg="red")
        except Exception as e:
            ride_details_label.config(text=f"Error fetching ride details: {e}", fg="red")

if __name__ == "__main__":
    app = DriverPageApp()
    app.mainloop()
