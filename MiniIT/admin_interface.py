import customtkinter

customtkinter.set_appearance_mode("light")
customtkinter.set_appearance_mode("dark")

import tkinter as tk

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

root = customtkinter.CTk() #Only create the CTk window
root.title("Full Screen 16:9 Window")
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

fullscreen(root)

special_font = customtkinter.CTkFont(family="Helvetica", size=32, weight="bold", underline=True, slant='italic')
normal_font = customtkinter.CTkFont(family="Times New Roman", size=26)

frame = customtkinter.CTkFrame(master=root)
frame.pack(fill="both", expand=True)

label = customtkinter.CTkLabel(frame, text="Welcome to Admin System!", font=special_font)
label.pack(pady=20, padx=20)
label.place(relx=0.5, rely=0.25, anchor="center")

label1 = customtkinter.CTkLabel(frame, text="Hi admin! Please choose a button to continue", font=normal_font)
label1.pack(pady=20, padx=20)
label1.place(relx=0.5, rely=0.38, anchor="center")

def view_users_data():
    print("Viewing Users' Data")

def view_users_history():
    print("Viewing Users' History")

def view_users_messages():
    print("Viewing User's Messages")

button1 = customtkinter.CTkButton(master=frame, fg_color="blue", text="View Users' Data", command=view_users_data)
button1.place(relx=0.5, rely=0.5, anchor="center")

button2 = customtkinter. CTkButton(master=frame, fg_color="white", text="View Users' History", command=view_users_history)
button2.place(relx=0.5, rely=0.63, anchor="center")

button3 = customtkinter.CTkButton(master=frame, fg_color="blue", text="View User's Messages", command=view_users_messages)
button3.place(relx=0.5, rely=0.75, anchor="center")

root.mainloop()



