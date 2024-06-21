import customtkinter
import requests
import threading
import time
import driver_signup
import subprocess

def run_driver_page():
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
root.geometry("500x500")
root.title("Full Screen 16:9 Window")
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

fullscreen(root)

def login():
    mmu_id = entry1.get()
    password = entry2.get()

    data = {
        "mmu_id": mmu_id,
        "password": password
    }

     def send_requests():
          try:
              response = requests.post("http://127.0.0.1:5002/driver_login", json=data)
              print("Status Code:", response.status_code) # Debugging line
              print("Response Body:", response.text) # Debugging line
              if response.status_code ==200:
                  label_message.configure(text="Login succesful", text_color="green")
                  time.sleep(1) # Ensure there's a slight delay before closing
                  root.withdraw() # Hide the login window
                  print("user interface for accepting rides")
              elif response.status_code == 401:
                  label_message.configure(text="Invalid credentials", text_color="red")
              else:
                  label_message.configure(text="Login failed", text_clor="red")
          except Exception as e:
              label_message.configure(text=f"An error occured: {e}", text_color="red")
              print(f"An error occured: {e}") # Debugging line

      threading.Thread(target=send_request).start()

    def callback_dp2():
    driver_signup.run_driver_signup()

    special_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(fill="both", expand=True)

    label = customtkinter.CTkLabel(root, text="Login System for Drivers", font=special_font)
    label.pack(pady=0, padx=0)
    label.place(relx=0.5, rely=0.25, anchor="center")

    entry1 = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="MMU Id")
    entry1.pack(pady=12, padx=10)
    entry1.place(relx=0.5, rely=0.38, anchor='center')

    entry2 = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="Password", show="*") 
    entry2.place(relx=0.5, rely=0.5, anchor="center")

    button = customtkinter.CTkButton(master=frame, fg_color="red", text="Login", command=login)
    button.place(relx=0.5, rely=0.63, anchor="center")

    checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
    checkbox.place(relx=0.5, rely=0.75, anchor="center")

    button1 = customtkinter.CTkButton(master=frame, text="Click here to sign up.", command=callback_dp2) 
    button1.place(relx=0.5, rely= 0.87, anchor="center")

    label_message = customtkinter.CTkLabel(frame, text="")
    label_message.pack(pady=20)
    label_message.place(relx=0.5, rely=0.95, anchor="center")
    
    root.mainloop()

if __name__ == "_main_":
    run_driver_page()
