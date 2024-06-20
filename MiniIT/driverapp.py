import tkinter as tk
import requests

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

        # Listbox to display ride requests
        self.ride_listbox = tk.Listbox(main_frame, font=("Helvetica", 14), selectmode="single")
        self.ride_listbox.pack(pady=20, padx=20, fill="both", expand=True)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(self.ride_listbox, orient="vertical", command=self.ride_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.ride_listbox.config(yscrollcommand=scrollbar.set)

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

        # Fetch and display ride requests
        self.fetch_ride_requests()

    def fetch_ride_requests(self):
        try:
            response = requests.get("http://127.0.0.1:5003/available_rides")

            if response.status_code == 200:
                ride_requests = response.json()["rides"]  # Access the "rides" key
                self.ride_listbox.delete(0, tk.END)
                self.rides = {}  # Dictionary to store ride_id and corresponding ride data
                for ride in ride_requests:
                    ride_str = f"ID: {ride['id']}, Pickup: {ride['pickup']}, Destination: {ride['destination']}, Price: {ride['price']}"
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
            response = requests.post("http://127.0.0.1:5003/accept_ride", json={"ride_id": ride_id, "driver_name": driver_name, "driver_phone": driver_phone})
            if response.status_code == 200:
                print("Ride accepted and removed from the database.")
                self.status_label.configure(text="Ride accepted", fg="green")
                self.fetch_ride_requests()  # Refresh the ride list
            else:
                print(f"Failed to accept ride: {response.json().get('error')}")
                self.status_label.configure(text="Failed to accept ride", fg="red")
        except Exception as e:
            print(f"Error accepting ride: {e}")
            self.status_label.configure(text=f"Error accepting ride: {e}", fg="red")


if __name__ == "__main__":
    app = DriverPageApp()
    app.mainloop()
