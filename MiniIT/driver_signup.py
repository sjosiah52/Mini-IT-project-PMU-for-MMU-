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
                 label.message.configure(text="Invalid MMU ID", text_color="red")
             else:
                 label_message.configure(text="Sign-up failed", text_color="red")
        except requests.exceptions.RequestExcept as e:
             label_message.configure(text=f"An error occured: {str(e)}", text_color="red")
            
    special_font = customtkinter.CTkfont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')

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

    label_message = customtkinter.CTkLabel(master=frame, text="")
    label_message.place(relx=0.5, rely=0.8, anchor="center")

    root.mainloop()

if __name__=="__main__":
    run_driver_signup()
    
          
        
