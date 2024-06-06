import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pick-Up For MMU")
        self.geometry("400x600")

        self.frames = {}

        # Create frames for login and main application
        self.create_login_frame()
        self.create_main_app_frame()

        self.show_frame("LoginFrame")

    def create_login_frame(self):
        login_frame = ctk.CTkFrame(self)
        self.frames["LoginFrame"] = login_frame

        special_font = ctk.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')

        label = ctk.CTkLabel(login_frame, text="Login System for Users", font=special_font)
        label.place(relx=0.5, rely=0.25, anchor="center")

        self.username_entry = ctk.CTkEntry(login_frame, justify='center', placeholder_text="Username")
        self.username_entry.place(relx=0.5, rely=0.38, anchor='center')

        self.password_entry = ctk.CTkEntry(login_frame, justify='center', placeholder_text="Password", show="*")
        self.password_entry.place(relx=0.5, rely=0.5, anchor="center")

        login_button = ctk.CTkButton(login_frame, fg_color="red", text="Login", command=self.login)
        login_button.place(relx=0.5, rely=0.63, anchor="center")

        checkbox = ctk.CTkCheckBox(login_frame, text="Remember Me")
        checkbox.place(relx=0.5, rely=0.75, anchor="center")

    def create_main_app_frame(self):
        main_frame = ctk.CTkFrame(self)
        self.frames["MainAppFrame"] = main_frame

        # Header
        header_frame = ctk.CTkFrame(main_frame, corner_radius=0, fg_color="#ff0000")
        header_frame.pack(fill="x")

        header_label = ctk.CTkLabel(header_frame, text="Pick Me Up For MMU", font=ctk.CTkFont(size=24, weight="bold"), text_color="#ffffff")
        header_label.pack(pady=10)

        # Navigation
        nav_frame = ctk.CTkFrame(main_frame)
        nav_frame.pack(fill="x")

        nav_buttons = ["Home", "About", "Services", "Contact"]
        for btn_text in nav_buttons:
            btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=lambda text=btn_text: self.nav_command(text), fg_color="#ff0000", hover_color="#555555")
            btn.pack(side="left", padx=5, pady=5)

        # Main Content
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        booking_label = ctk.CTkLabel(content_frame, text="Book a Ride", font=ctk.CTkFont(size=20))
        booking_label.pack(pady=10)

        # Form
        form_frame = ctk.CTkFrame(content_frame)
        form_frame.pack(pady=10, fill="x")

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

        # Footer
        footer_frame = ctk.CTkFrame(main_frame, corner_radius=0, fg_color="#333")
        footer_frame.pack(side="bottom", fill="x")

        footer_label = ctk.CTkLabel(footer_frame, text="© 2024 Pick-Up For MMU. All rights reserved.", font=ctk.CTkFont(size=12), text_color="#ffffff")
        footer_label.pack(pady=10)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)
        frame.tkraise()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Add authentication logic here
        # For demonstration, we assume any username and password is correct
        print(f"Logging in with Username: {username}, Password: {password}")
        self.show_frame("MainAppFrame")

    def nav_command(self, text):
        print(f"Navigation button '{text}' clicked")

    def book_now(self):
        pickup = self.pickup_entry.get()
        destination = self.destination_entry.get()
        promo_code = self.promo_entry.get()

        print(f"Booking Details:\nPickup: {pickup}\nDestination: {destination}\nPromo Code: {promo_code}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
