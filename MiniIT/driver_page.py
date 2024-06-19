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
                  subprocess.Popen(["python", "driver_accepting_page.py"])
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

label = customtkinter.CTkLabel(root, text
