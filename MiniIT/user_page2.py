import customtkinter
import requests
import threading

customtkinter.set_appearance_mode("light")
customtkinter.set_appearance_mode("dark")

def run_user_page2():
    def fullscreen(window):
      screen_width = window.winfo_screenwidth()
      screen_height = window.winfo_screenheight()

      if screen_width / screen_height > 16/9:
            height = screen_height
            width = int(height *16/9)
      else:
            width = screen_width
            height = int(width * 9/16)

      window.geometry(f"{width}x{height}")
      window.attributes('-fullscreen', True)

    def sign_up():
        mmu_id = entry_id.get()
        name = entry_name.get()
        phone = entry_phone.get()
        password = entry_password.get()

        email = f"{mmu_id}@student.mmu.edu.my"
        print(f"Validating email: {email}")  # Debug statement

        def validate_and_sign_up():
            data = {
                "mmu_id": mmu_id,
                "name": name,
                "phone": phone,
                "password": password
            }

            try:
                response = requests.post("http://127.0.0.1:5001/signup", json=data)
                if response.status_code == 201:
                    label_message.configure(text="Sign-up successful", text_color="green")
                elif response.status_code == 409:
                    label_message.configure(text="User already exists", text_color="red")
                elif response.status_code == 400:
                    label_message.configure(text="Invalid MMU ID", text_color="red")
                else:
                    label_message.configure(text="Sign-up failed", text_color="red")
            except Exception as e:
                label_message.configure(text=f"An error occurred: {e}", text_color="red")

        threading.Thread(target=validate_and_sign_up).start()

    root = customtkinter.CTk() #Only create the CTk window
    root.title("Full Screen 16:9 Window")
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

    fullscreen(root)

    special_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')
    normal_font = customtkinter.CTkFont(family="Times New Roman", size=26)

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(fill="both", expand=True)

    label = customtkinter.CTkLabel(frame, text="Welcome to Pick Me Up for MMU!", font=special_font)
    label.pack(pady=20, padx=20)
    label.place(relx=0.5, rely=0.15, anchor="center")

    label1 = customtkinter.CTkLabel(frame, text="Please sign up for our app using your MMU Id, Name, and Phone Number. Next time you can just login using your ID and Password.")
    label1.pack(pady=20, padx=20)
    label1.place(relx=0.5, rely=0.25, anchor="center")

    entry_id = customtkinter.CTkEntry(frame, placeholder_text="MMU ID")
    entry_id.pack(pady=10)
    entry_id.place(relx=0.5, rely=0.35, anchor="center")

    entry_name = customtkinter.CTkEntry(frame, placeholder_text="Name")
    entry_name.pack(pady=10)
    entry_name.place(relx=0.5, rely=0.45, anchor="center")

    entry_phone = customtkinter.CTkEntry(frame, placeholder_text="Phone Number")
    entry_phone.pack(pady=10)
    entry_phone.place(relx=0.5, rely=0.55, anchor="center")

    entry_password = customtkinter.CTkEntry(frame, placeholder_text="Password", show='*')
    entry_password.pack(pady=10)
    entry_password.place(relx=0.5, rely=0.65, anchor="center")

    button_sign_up = customtkinter.CTkButton(frame, text="Sign Up", command=sign_up)
    button_sign_up.pack(pady=20)
    button_sign_up.place(relx=0.5, rely=0.75, anchor="center")

    label_message = customtkinter.CTkLabel(frame, text="")
    label_message.pack(pady=20)
    label_message.place(relx=0.5, rely=0.85, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    run_user_page2()
