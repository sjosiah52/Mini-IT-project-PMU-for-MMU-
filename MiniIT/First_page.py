import customtkinter as ctk
import subprocess
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

def fullscreen(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    if screen_width / screen_height > 16 / 9:
        height = screen_height
        width = int(height * 16 / 9)
    else:
        width = screen_width
        height = int(width * 9 / 16)

    window.geometry(f"{width}x{height}")
    window.attributes('-fullscreen', True)

root = ctk.CTk()
root.title("Full Screen 16:9 Window")
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

fullscreen(root)

def callback_ap():
    script_path = os.path.join(os.path.dirname(__file__), "admin_page.py")
    subprocess.Popen(["python", script_path])

def callback_up():
    script_path1 = os.path.join(os.path.dirname(__file__), "user_page.py")
    subprocess.Popen(["python", script_path1])

def callback_dp():
    script_path2 = os.path.join(os.path.dirname(__file__), "driver_page.py")
    subprocess.Popen(["python", script_path2])

def create_ui(root):
    # Header
    def show_contact_info():
        contact_info = (
            "Contact Us:\n\n"
            "Support Email: sjosiah52@gmail.com, azifffizrie2@gmail.com, liverneshk24@gmail.com\n"
            "Support Phone: +60149237392\n"
            "Office Address: Multimedia University, Cyberjaya, Malaysia\n"
            "Operating Hours: 9 AM - 6 PM, Monday to Friday"
        )
        contact_window = ctk.CTkToplevel()
        contact_window.title("Contact Information")
        contact_window.geometry("800x600")

        contact_label = ctk.CTkLabel(contact_window, text=contact_info, font=ctk.CTkFont(size=14), justify="left")
        contact_label.pack(padx=20, pady=20)
        contact_window.lift()

    def show_about_info():
        about_info = (
            "About Us:\n\n"
            "This is a ride booking application for MMU students.\n"
            "Our goal is to provide a convenient and affordable way for students to travel to and from campus."
        )
        about_window = ctk.CTkToplevel()
        about_window.title("About Us")
        about_window.geometry("800x600")

        about_label = ctk.CTkLabel(about_window, text=about_info, font=ctk.CTkFont(size=14), justify="left")
        about_label.pack(padx=20, pady=20)
        about_window.lift()

    def show_services_info():
        services_info = (
            "Our Services:\n\n"
            "We offer a range of services to make your travel experience convenient and comfortable.\n"
            "Our services include:\n"
            "- Competitive pricing"
        )
        services_window = ctk.CTkToplevel()
        services_window.title("Our Services")
        services_window.geometry("800x600")

        services_label = ctk.CTkLabel(services_window, text=services_info, font=ctk.CTkFont(size=14), justify="left")
        services_label.pack(padx=20, pady=20)
        services_window.lift()

    def show_home_info():
        home_info = (
            "Welcome to Pick-Up For MMU:\n\n"
            "This is a ride booking application designed specifically for MMU students.\n"
            "Book your ride now and experience the convenience of door-to-door pickup and dropoff."
        )
        
        home_window = ctk.CTkToplevel()
        home_window.title("Home")
        home_window.geometry("800x600")

        home_label = ctk.CTkLabel(home_window, text=home_info, font=ctk.CTkFont(size=14), justify="left")
        home_label.pack(padx=20, pady=20)
        home_window.lift()
    
    header_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#ff0000")
    header_frame.pack(fill="x")

    header_label = ctk.CTkLabel(header_frame, text="Pick Me Up For MMU", font=ctk.CTkFont(size=24, weight="bold"), text_color="#ffffff")
    header_label.pack(pady=10)

    # Navigation
    nav_frame = ctk.CTkFrame(root)
    nav_frame.pack(fill="x", pady=10)

    nav_buttons = ["Home", "About", "Services", "Contact"]
    for btn_text in nav_buttons:
        if btn_text == "Contact":
            btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=show_contact_info, fg_color="#ff0000", hover_color="#555555")
        elif btn_text == "About":
            btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=show_about_info, fg_color="#ff0000", hover_color="#555555")
        elif btn_text == "Services":
            btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=show_services_info, fg_color="#ff0000", hover_color="#555555")
        else:
            btn = ctk.CTkButton(nav_frame, text=btn_text, text_color="#ffffff", command=show_home_info, fg_color="#ff0000", hover_color="#555555")
        btn.pack(side="left", padx=5, pady=5)
    
    def nav_command(self, text):
        print(f"Navigation button '{text}' clicked")


    # Main Content
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Booking Form Frame
    form_frame = ctk.CTkFrame(main_frame)
    form_frame.pack(side="left", padx=20, pady=20, fill="y")

    # Route Info
    route_info_frame = ctk.CTkFrame(form_frame)
    route_info_frame.pack(pady=10)

    route_info_label = ctk.CTkLabel(route_info_frame, text="", font=ctk.CTkFont(size=14))
    route_info_label.pack()

    time_info_label = ctk.CTkLabel(route_info_frame, text="", font=ctk.CTkFont(size=14))
    time_info_label.pack()

    # Footer
    footer_frame = ctk.CTkFrame(root, corner_radius=0, fg_color="#333")
    footer_frame.pack(side="bottom", fill="x")

    footer_label = ctk.CTkLabel(footer_frame, text="© 2024 Pick-Up For MMU. All rights reserved.", font=ctk.CTkFont(size=12), text_color="#ffffff")
    footer_label.pack(pady=10)

    user_login = ctk.CTkButton(root, text="User", command=callback_up, bg_color="white")
    user_login.place(relx="0.5", rely="0.4", anchor="center")

    driver_login = ctk.CTkButton(root, text="Driver", command=callback_dp)
    driver_login.place(relx ="0.5", rely= "0.65", anchor="center")

    admin_login = ctk.CTkButton(root, text="Admin", command=callback_ap, fg_color="#ffffff")
    admin_login.place(relx="0.93", rely="0.9", anchor="center")


def nav_command(text):
    print(f"Navigation button '{text}' clicked")

def show_contact_info():
    contact_info = (
        "Contact Us:\n\n"
        "Support Email: support@pickupformmu.com\n"
        "Support Phone: +60 123-456-789\n"
        "Office Address: 123 MMU Street, Cyberjaya, Malaysia\n"
        "Operating Hours: 9 AM - 6 PM, Monday to Friday"
    )
    contact_window = ctk.CTkToplevel(root)
    contact_window.title("Contact Information")
    contact_window.geometry("400x300")

    contact_label = ctk.CTkLabel(contact_window, text=contact_info, font=ctk.CTkFont(size=14), justify="left")
    contact_label.pack(padx=20, pady=20)

    back_button = ctk.CTkButton(contact_window, text="Back", command=contact_window.destroy, fg_color="#2600ff", hover_color="#555555")
    back_button.pack(pady=10)

# Call create_ui to set up the UI
create_ui(root)

root.mainloop()
