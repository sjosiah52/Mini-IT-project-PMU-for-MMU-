import customtkinter
import user_page2

def run_user_page():
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
    root = tkinter.Tk()
    root.title("Full Screen 16:9 Window")
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

    fullscreen(root)
        
    def login():
        print("test")

    def callback_up2():
        user_page2.run_user_page2()

    special_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(fill="both", expand=True)

    label = customtkinter.CTkLabel(root, text="Login System for Users", font=special_font)
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

    button1 = customtkinter.CTkButton(master=frame, text="Click here to sign up.", command=callback_up2)
    button1.place(relx=0.5, rely= 0.87, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    run_user_page()
