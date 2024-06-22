import customtkinter
import requests
import threading
import subprocess
import os

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

def run_driver_signup():
    def fullscreen(window):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            if screen_width / screen_height > 16/9:
                height = screen_height
                width = int(height *16/9)
            else:
                width = screen_width
                height = int(width *9/16)

            window.geometry(f"{width}x{height}")
            window.attributes('-fullscreen', True)
        
    root = customtkinter.CTk()
    root.geometry("500x500")
    root.title("Full Screen 16:9 Window")
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

    fullscreen(root)
    
    def signup():
        mmuid = entry_mmuid.get()
        icnumber = entry_icnumber.get()
        vehicleregistrationnumber = entry_vehicle_registration_number.get()
        password = entry_password.get()

        email = f"{mmuid}@student.mmu.edu.my"
        print(f"Validating email: {email}")

        def validate_and_sign_up():
            data = {
            "mmu_id": mmuid,
            "ic_number": icnumber,
            "vehicle_registration_number": vehicleregistrationnumber,
            "password": password
            }

            try:
                response = requests.post("http://127.0.0.1:5002/driver_signup", json=data)
                if response.status_code == 201:
                    label_message.configure(text="Sign-up sucessful", text_color="green")
                elif response.status_code == 409:
                    label_message.configure(text= "User already exists", text_color="red")
                elif response.status_code == 400:  
                    label_message.configure(text="Invalid MMU ID", text_color="red")
                else:
                    label_message.configure(text="Sign-up failed", text_color="red")
            except Exception as e:
                label_message.configure(text=f"An error occured: {str(e)}", text_color="red")

        threading.Thread(target=validate_and_sign_up).start()

    def back_to_main():
            root.withdraw
            script_path = os.path.join(os.path.dirname(__file__), "driver_page.py")
            subprocess.Popen(["python", script_path])
       
    special_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(fill="both", expand=True)

    label = customtkinter.CTkLabel(frame, text="Driver Sign-Up", font=special_font)
    label.pack(pady=20, padx=10)
    label.place(relx=0.5, rely=0.1, anchor="center")

    entry_mmuid = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="MMU ID")
    entry_mmuid.pack(pady=12, padx=10)
    entry_mmuid.place(relx=0.5, rely=0.2, anchor='center')

    entry_icnumber = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="IC Number")
    entry_icnumber.pack(pady=12, padx=10)
    entry_icnumber.place(relx=0.5, rely=0.3, anchor='center')

    entry_vehicle_registration_number = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="Vehicle Registration Number")
    entry_vehicle_registration_number.pack(pady=12, padx=10)
    entry_vehicle_registration_number.place(relx=0.5, rely=0.4, anchor='center')

    entry_password = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="Password", show="*")
    entry_password.pack(pady=12, padx=10)
    entry_password.place(relx=0.5, rely=0.5, anchor="center")

    button = customtkinter.CTkButton(master=frame, fg_color="green", text="Sign Up", command=signup)
    button.place(relx=0.5, rely=0.6, anchor="center")

    back_button = customtkinter.CTkButton(master=frame, text="Back", command=back_to_main)
    back_button.place(relx=0.075, rely=0.95, anchor="center")

    label_message = customtkinter.CTkLabel(master=frame, text="")
    label_message.place(relx=0.5, rely=0.8, anchor="center")

    root.mainloop()

if __name__=="__main__":
    run_driver_signup()
    
          
        
