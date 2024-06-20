import customtkinter
import tkinter

def run_admin_page():
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    root = tkinter.Tk()
    root.geometry("500x500")

    def login():
        print("test")

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
