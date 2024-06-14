import customtkinter
import requests
import threading

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("dark-blue")

def run_driver_signup():
    root = customtkinter.CTk()
    root.geometry("500x600")

    def signup():
        mmuid = entry_mmuid.get()
        icnumber = entry_icnumber.get()
        vehicleregistrationnumber = entry_vehicle_registration_number.get()
        password = entry_passowrd.get()

        email = f"{mmuid}@student.mmu.edu.my"
        print(f"Validating email: {email}")

        data = {
            "mmu_id": mmuid,
            "ic_number": icnumber,
            "vehicle_registration_number": vehicleregistrationnumber,
            "password": password
        }

         try:
             response = requests.post("http://127.0.0.1:5001/driver_signup", json=data)
             if reponse.status_code == 201:
                 label_message.configure(text="Sign-up sucessful", text_color="green")
             elif response.status_code == 409:
                 label_message.configure(text= "User already exists", text_color="red")
             elif response.status_code == 400:  
                 label.message.configure
          
        
