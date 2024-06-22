import tkinter as tk
import sqlite3

def checkridedetails():
    # Create tkinter window
    root = tk.Tk()
    root.title("View Ride Details")
    root.geometry("600x400")

    # Function to fetch and display details
    def view_details():
        # Get input values
        ride_id = entry_ride_id.get().strip()
        user_name = entry_user_name.get().strip()

        if not ride_id or not user_name:
            details_text.delete(1.0, tk.END)
            details_text.insert(tk.END, "Please enter Ride ID and User Name.")
            return

        # Query database for ride details
        try:
            conn = sqlite3.connect('rides.db')
            c = conn.cursor()

            c.execute("SELECT * FROM rides WHERE id=? AND user_name=?", (ride_id, user_name))
            ride_details = c.fetchone()

            if ride_details:
                display_details(ride_details)
            else:
                details_text.delete(1.0, tk.END)
                details_text.insert(tk.END, "No ride found with provided ID and User Name.")
            
            conn.close()

        except sqlite3.Error as e:
            print(f"Error retrieving data from database: {e}")
            details_text.delete(1.0, tk.END)
            details_text.insert(tk.END, f"Error retrieving data from database: {e}")

    # Function to display details
    def display_details(ride_details):
        # Clear previous text
        details_text.delete(1.0, tk.END)

        # Format and display details
        details_str = (
            f"Ride ID: {ride_details[0]}\n"
            f"Pickup: {ride_details[1]}\n"
            f"Destination: {ride_details[2]}\n"
            f"Price: {ride_details[3]}\n"
            f"User Name: {ride_details[4]}\n"
            f"User Phone: {ride_details[5]}\n"
            f"Driver Name: {ride_details[6]}\n"
            f"Driver Phone: {ride_details[7]}\n"
            f"Status: {ride_details[8]}\n"
        )

        details_text.insert(tk.END, details_str)

    # GUI Elements
    label_ride_id = tk.Label(root, text="Enter Ride ID:")
    label_ride_id.pack(pady=10)
    entry_ride_id = tk.Entry(root, width=30)
    entry_ride_id.pack()

    label_user_name = tk.Label(root, text="Enter Name(please use the exact same characters as when you were booking the ride):")
    label_user_name.pack(pady=10)
    entry_user_name = tk.Entry(root, width=30)
    entry_user_name.pack()

    btn_view_details = tk.Button(root, text="View Details", command=view_details)
    btn_view_details.pack(pady=20)

    details_text = tk.Text(root, wrap=tk.WORD, width=60, height=10)
    details_text.pack()

    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    checkridedetails()
