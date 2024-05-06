import tkinter
import customtkinter
import admin_page
import user_page

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root = tkinter.Tk()

def callback_ap():
    admin_page.run_admin_page()

def callback_up():
    user_page.run_user_page()

admin_login = customtkinter.CTkButton(root, text="Admin", command=callback_ap)
admin_login.place(relx="0.5", rely="0.4", anchor="center")

user_login = customtkinter.CTkButton(root, text="User", command=callback_up)
user_login.place(relx="0.5", rely="0.8", anchor="center")

root.mainloop()