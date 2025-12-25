import tkinter as tk

class RoundedFrame:
    def __init__(self, parent, radius=20, **kwargs):
        self.radius = radius
        self.frame = tk.Frame(parent, **kwargs)
        self.canvas = tk.Canvas(self.frame, highlightthickness=0, **kwargs)
        self.canvas.pack(fill="both", expand=True)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create rounded rectangle using tkinter polygon (no PIL)"""
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        
        return self.canvas.create_polygon(points, **kwargs, smooth=True)
    
    def configure(self, width=None, height=None, bg=None):
        if bg:
            self.frame.config(bg=bg)
            self.canvas.config(bg=bg)
        
        if width and height:
            self.canvas.delete("all")
            self.create_rounded_rect(0, 0, width, height, self.radius, fill=bg, outline="")
    
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