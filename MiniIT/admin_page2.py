import customtkinter
import tkinter as tk
import webbrowser

def open_admin_page():
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("dark-blue")

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

    root = customtkinter.CTk()  # Only create the CTk window
    root.title("Full Screen 16:9 Window")
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

    fullscreen(root)

    special_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')
    normal_font = customtkinter.CTkFont(family="Times New Roman", size=26)

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(fill="both", expand=True)

    label = customtkinter.CTkLabel(frame, text="Welcome to Admin System!", font=special_font)
    label.pack(pady=20, padx=20)
    label.place(relx=0.5, rely=0.25, anchor="center")

    label1 = customtkinter.CTkLabel(frame, text="Hi admin! Please choose a button to continue", font=normal_font)
    label1.pack(pady=20, padx=20)
    label1.place(relx=0.5, rely=0.38, anchor="center")

    def view_users_data():
        webbrowser.open("http://127.0.0.1:5001/admin/users")
        print("Viewing Users' Data")

    def view_drivers_data():
        webbrowser.open("http://127.0.0.1:5002/admin/drivers")
        print("Viewing Drivers' Data")

    def delete_users_data():
        webbrowser.open("http://127.0.0.1:5001/admin/delete_form")
        print("Deleting Users' Data")

    def delete_drivers_data():
        webbrowser.open("http://127.0.0.1:5002/admin/delete_form")
        print("Deleting Drivers' Data")

    button1 = customtkinter.CTkButton(master=frame, fg_color="blue", text="View Users' Data", command=view_users_data)
    button1.place(relx=0.5, rely=0.5, anchor="center")

    button2 = customtkinter.CTkButton(master=frame, fg_color="blue", text="View Drivers' Data", command=view_drivers_data)
    button2.place(relx=0.5, rely=0.63, anchor="center")

    button3 = customtkinter.CTkButton(master=frame, fg_color="blue", text="Delete Users' Data", command=delete_users_data)
    button3.place(relx=0.5, rely=0.75, anchor="center")

    button4 = customtkinter.CTkButton(master=frame, fg_color="blue", text="Delete Drivers' Data", command=delete_drivers_data)
    button4.place(relx=0.5, rely=0.88, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    open_admin_page()
