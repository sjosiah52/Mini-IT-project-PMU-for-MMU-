import customtkinter
import requests
import threading
import time
import user_signup
import subprocess
import os 

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

        def send_request():
            try:
                response = requests.post("http://127.0.0.1:5001/login", json=data)
                if response.status_code == 200:
                    label_message.configure(text="Login successful", text_color="green")
                    time.sleep(1)  # Ensure there's a slight delay before closing
                    root.withdraw()
                    script_path = os.path.join(os.path.dirname(__file__), "route_map_app.py")  
                    subprocess.Popen(["python", script_path])
                elif response.status_code == 401:
                    label_message.configure(text="Invalid credentials", text_color="red")
                else:
                    label_message.configure(text="Login failed", text_color="red")
            except Exception as e:
                label_message.configure(text=f"An error occurred: {e}", text_color="red")

        threading.Thread(target=send_request).start()

    def back_to_main():
            root.withdraw
            script_path = os.path.join(os.path.dirname(__file__), "First_page.py")
            subprocess.Popen(["python", script_path])

    def callback_up2():
        root.withdraw
        script_path2 = os.path.join(os.path.dirname(__file__), "user_signup.py")
        subprocess.Popen(["python", script_path2])
        
    special_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(fill="both", expand=True)

    header_frame = customtkinter.CTkFrame(frame, corner_radius=0, fg_color="#ff0000")
    header_frame.pack(fill="x")

    label = customtkinter.CTkLabel(root, text="Login System for Users", font=special_font,bg_color="#ff0000",text_color="#fffefc")
    label.pack(pady=0, padx=0)
    label.place(relx=0.5, rely=0.15, anchor="center")

    entry1 = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="MMU Id")
    entry1.pack(pady=12, padx=10)
    entry1.place(relx=0.5, rely=0.38, anchor='center')

    entry2 = customtkinter.CTkEntry(master=frame, justify='center', placeholder_text="Password", show="*")
    entry2.place(relx=0.5, rely=0.5, anchor="center")

    button = customtkinter.CTkButton(master=frame, fg_color="red", text="Login", command=login)
    button.place(relx=0.5, rely=0.63, anchor="center")

    back_button = customtkinter.CTkButton(master=frame, text="Back", command=back_to_main)
    back_button.place(relx=0.075, rely=0.95, anchor="center")

    button1 = customtkinter.CTkButton(master=frame, text="Click here to sign up.", command=callback_up2)
    button1.place(relx=0.5, rely= 0.87, anchor="center")

    label_message = customtkinter.CTkLabel(frame, text="")
    label_message.pack(pady=20)
    label_message.place(relx=0.5, rely=0.95, anchor="center")
    
    root.mainloop()

if __name__ == "__main__":
    run_user_page()
