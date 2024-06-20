import customtkinter
import admin_page2
from tkinter import messagebox
from argon2 import PasswordHasher, exceptions

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

def run_admin_page():
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root.title("Full Screen 16:9 Window")
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

    fullscreen(root)

    ph = PasswordHasher()
    allowed_users = {
        "samthedon": ph.hash("test"),
        "Liveradmin": ph.hash("admin2109"),
        "aziffadmin": ph.hash("admin1602"),
        "lecturersuhaini": ph.hash("mmuisyou")
    }

    login_attempts = {}

    def callback_ap2():
        admin_page2.open_admin_page()

    def login():
        username = entry1.get()
        password = entry2.get()

        if username in allowed_users:
            try:
                ph.verify(allowed_users[username], password)
                callback_ap2()
                return
            except exceptions.VerifyMismatchError:
                pass

        if username not in login_attempts:
            login_attempts[username] = 0
        login_attempts[username] += 1

        if login_attempts[username] > 3:
            messagebox.showerror("Error", "Too many failed attempts. Try again later.")
        else:
            messagebox.showerror("Error", "Invalid username or password")

    special_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(fill="both", expand=True)

    label = customtkinter.CTkLabel(root, text="Login System for Admin", font=special_font)
    label.pack(pady=0, padx=0)
    label.place(relx=0.5, rely=0.25, anchor="center")

    entry1 = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="Username")
    entry1.pack(pady=12, padx=10)
    entry1.place(relx=0.5, rely=0.38, anchor='center')

    entry2 = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="Password", show="*")
    entry2.place(relx=0.5, rely=0.5, anchor="center")

    button = customtkinter.CTkButton(master=frame, fg_color="red", text="Login", command=login)
    button.place(relx=0.5, rely=0.63, anchor="center")

    checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.place(relx=0.5, rely=0.75, anchor="center")

    root.mainloop()

run_admin_page()
