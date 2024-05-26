import customtkinter

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
    label.place(relx=0.5, rely=0.25, anchor="center")

    label1 = customtkinter.CTkLabel(frame, text="Please sign up for our app using your MMU Id, Name, and Phone Number. Next time you can just login using your ID and Password.")
    label1.pack(pady=20, padx=20)
    label1.place(relx=0.5, rely=0.33, anchor="center")
    root.mainloop()

if __name__ == "__main__":
    run_user_page2()
