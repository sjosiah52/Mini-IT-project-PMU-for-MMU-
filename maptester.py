import customtkinter as ctk
import tkinter as tk

class RouteMapApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Route Map App")
        self.geometry("800x600")
        
        # Set up the main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Canvas for drawing the route map
        self.canvas = tk.Canvas(self.main_frame, bg="white", width=760, height=540)
        self.canvas.pack(pady=20)
        
        # Button to draw a route
        self.draw_button = ctk.CTkButton(self.main_frame, text="Draw Route", command=self.draw_route)
        self.draw_button.pack(pady=10)
    
    def draw_route(self):
        # Clear the canvas
        self.canvas.delete("all")
        
        # Example points and lines (coordinates)
        points = [(50, 50), (200, 80), (350, 150), (500, 200), (650, 250)]
        
        # Draw points
        for x, y in points:
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="blue")
        
        # Draw lines
        for i in range(len(points) - 1):
            self.canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1], fill="red", width=2)

if __name__ == "__main__":
    app = RouteMapApp()
    app.mainloop()