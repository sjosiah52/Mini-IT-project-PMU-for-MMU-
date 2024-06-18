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
          width = int(height * 16/9)
        else:
          width = screen_width
          height = int(width * 9 / 16)

         window.geometry(f"{width}x{height}")
         window.attributes('-fullscreen', True)
