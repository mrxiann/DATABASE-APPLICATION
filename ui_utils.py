# ui_utils.py
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class RoundedFrame:
    def __init__(self, parent, radius=20, **kwargs):
        self.radius = radius
        self.frame = tk.Frame(parent, **kwargs)
        self.canvas = tk.Canvas(self.frame, highlightthickness=0, **kwargs)
        self.canvas.pack(fill="both", expand=True)
        
    def create_rounded_rect(self, width, height, radius, fill):
        """Create a rounded rectangle"""
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw rounded rectangle
        draw.rounded_rectangle([(0, 0), (width-1, height-1)], radius, fill=fill)
        
        return ImageTk.PhotoImage(image)
    
    def configure(self, width=None, height=None, bg=None):
        if bg:
            self.frame.config(bg=bg)
            self.canvas.config(bg=bg)
        
        if width and height:
            img = self.create_rounded_rect(width, height, self.radius, bg)
            self.canvas.create_image(0, 0, image=img, anchor="nw")
            self.canvas.image = img
    
    def pack(self, **kwargs):
        return self.frame.pack(**kwargs)
    
    def place(self, **kwargs):
        return self.frame.place(**kwargs)
    
    def grid(self, **kwargs):
        return self.frame.grid(**kwargs)

def create_rounded_button(parent, text, command, radius=10, **kwargs):
    """Create a button with rounded corners"""
    btn = tk.Button(parent, text=text, command=command, 
                   relief='flat', cursor='hand2', **kwargs)
    btn.config(borderwidth=0, highlightthickness=0)
    return btn

def create_rounded_entry(parent, radius=8, **kwargs):
    """Create an entry with rounded corners"""
    entry = tk.Entry(parent, relief='flat', **kwargs)
    return entry