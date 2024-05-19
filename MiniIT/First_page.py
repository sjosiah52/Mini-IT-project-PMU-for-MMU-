import customtkinter
from admin_page import run_admin_page
from user_page import run_user_page

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

root = customtkinter.CTk()
root.title("Full Screen 16:9 Window")
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

fullscreen(root)

def callback_ap():
    run_admin_page()

def callback_up():
    run_user_page()

admin_login = customtkinter.CTkButton(root, text="Admin", command=callback_ap)
admin_login.place(relx="0.5", rely="0.4", anchor="center")

user_login = customtkinter.CTkButton(root, text="User", command=callback_up)
user_login.place(relx="0.5", rely="0.8", anchor="center")

root.mainloop()
