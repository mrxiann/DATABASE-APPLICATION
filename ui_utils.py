import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class RoundedFrame:
    def __init__(self, parent, radius=20, **kwargs):
        self.frame = tk.Frame(parent, **kwargs)
        self.canvas = tk.Canvas(self.frame, highlightthickness=0, bd=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.radius = radius
        self.fill = None
        self.corner_bg = None
        
    def create_rounded_rect(self, width, height, radius, fill):
        """Create a rounded rectangle"""
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw rounded rectangle
        draw.rounded_rectangle([(0, 0), (width-1, height-1)], radius, fill=fill)
        
        return ImageTk.PhotoImage(image)
    
    def configure(self, width=None, height=None, fill=None, corner_bg=None):
        if fill is not None:
            self.fill = fill
        if corner_bg is not None:
            self.corner_bg = corner_bg
            self.frame.config(bg=corner_bg)
            self.canvas.config(bg=corner_bg)
        
        if width and height and self.fill:
            img = self.create_rounded_rect(width, height, self.radius, self.fill)
            self.canvas.create_image(0, 0, image=img, anchor="nw")
            self.canvas.image = img
    
    def pack(self, **kwargs):
        return self.frame.pack(**kwargs)
    
    def place(self, **kwargs):
        return self.frame.place(**kwargs)
    
    def grid(self, **kwargs):
        return self.frame.grid(**kwargs)

def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def create_rounded_button(parent, text, command, radius=20, fill='#4f46e5', fg='white', font=('Helvetica', 12, 'bold'), **kwargs):
    canvas = tk.Canvas(parent, highlightthickness=0, bg=parent['bg'], cursor='hand2', **kwargs)
    
    # Create temporary text to measure
    temp_text = canvas.create_text(0, 0, text=text, font=font, fill=fg)
    bbox = canvas.bbox(temp_text)
    canvas.delete(temp_text)
    
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    pad_x = 30  # Increased padding for modern look
    pad_y = 15
    
    w = text_w + pad_x * 2
    h = text_h + pad_y * 2
    
    canvas.config(width=w, height=h)
    
    # Draw rounded rectangle
    draw_rounded_rect(canvas, 0, 0, w, h, radius, fill=fill, outline="")
    
    # Add text
    canvas.create_text(w/2, h/2, text=text, font=font, fill=fg)
    
    # Bind click
    canvas.bind("<Button-1>", lambda e: command())
    
    return canvas

def create_rounded_entry(parent, radius=8, fill='#f0f3f7', border_color='#d1d5db', width=30, font=('Helvetica', 12), **kwargs):
    frame = tk.Frame(parent, bg=parent['bg'])
    
    canvas = tk.Canvas(frame, highlightthickness=0, bd=0, bg=parent['bg'])
    canvas.pack(fill='both', expand=True)
    
    # Measure entry size
    temp_entry = tk.Entry(frame, width=width, font=font, **kwargs)
    req_w = temp_entry.winfo_reqwidth()
    req_h = temp_entry.winfo_reqheight() + 10  # Slight extra height for padding
    temp_entry.destroy()
    
    frame.config(width=req_w, height=req_h)
    canvas.config(width=req_w, height=req_h)
    
    # Draw rounded rectangle with border
    draw_rounded_rect(canvas, 0, 0, req_w, req_h, radius, fill=fill, outline=border_color, width=1)
    
    # Create entry on top
    entry = tk.Entry(frame, relief='flat', bd=0, bg=fill, highlightthickness=0, insertbackground='#64748b', font=font, **kwargs)
    entry.place(x=15, y=5, width=req_w - 30, height=req_h - 10)
    
    return entry, frame  # Return entry and its frame, so pack the frame