import tkinter as tk
from tkinter import ttk

class ModernButton(tk.Canvas):
    """Modern button with hover effects and rounded corners"""
    def __init__(self, parent, text, command, width=200, height=45, 
                 bg="#4f46e5", fg="white", font=("Segoe UI", 12, "bold"), radius=10):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0)
        self.command = command
        self.bg = bg
        self.hover_bg = self.adjust_color(bg, -20)
        self.active_bg = self.adjust_color(bg, -30)
        self.fg = fg
        self.font = font
        self.radius = radius
        self.text = text
        self.is_active = False
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        self.draw_button(bg)
        self.create_text(width//2, height//2, text=text, fill=fg, font=font, tags="text")
        
    def adjust_color(self, color, amount):
        """Adjust hex color brightness"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
        return '#%02x%02x%02x' % rgb
    
    def draw_button(self, color):
        self.delete("all")
        
        # Draw subtle shadow - using a light gray instead of semi-transparent black
        shadow_color = '#e5e7eb'  # Light gray for shadow
        self.create_rounded_rect(2, 2, self.winfo_reqwidth()-1, self.winfo_reqheight()-1, 
                                self.radius, fill=shadow_color, outline='')
        
        # Draw main button
        self.create_rounded_rect(0, 0, self.winfo_reqwidth()-3, self.winfo_reqheight()-3, 
                                self.radius, fill=color, outline='')
        
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2, 
                        text=self.text, fill=self.fg, font=self.font, tags="text")
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create rounded rectangle using tkinter polygon"""
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
        
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def on_enter(self, e):
        if not self.is_active:
            self.draw_button(self.hover_bg)
    
    def on_leave(self, e):
        if not self.is_active:
            self.draw_button(self.bg)
    
    def on_click(self, e):
        self.is_active = True
        self.draw_button(self.active_bg)
    
    def on_release(self, e):
        self.is_active = False
        self.draw_button(self.hover_bg)
        self.command()

class ModernEntry(tk.Frame):
    """Modern input field with focus effects"""
    def __init__(self, parent, width=30, font=("Segoe UI", 11), show=None, placeholder="", **kwargs):
        super().__init__(parent, bg='#f1f5f9')
        self.width = width
        self.font = font
        self.show = show
        self.placeholder = placeholder
        self.has_placeholder = bool(placeholder)
        
        self.canvas = tk.Canvas(self, height=45, width=width*10, highlightthickness=0, bg='#f1f5f9')
        self.canvas.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Entry field
        self.entry = tk.Entry(self, font=font, relief='flat', bg='white', 
                             highlightthickness=0, show=show, fg='#374151')
        self.entry_window = self.canvas.create_window(12, 22, window=self.entry, 
                                                     anchor="w", width=width*10-24)
        
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.config(fg='#94a3b8')
        
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry.bind("<KeyRelease>", self.on_key_release)
        
        self.draw_border('#cbd5e1')
    
    def on_focus_in(self, e):
        self.draw_border('#4f46e5')
        if self.has_placeholder and self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg='#374151')
    
    def on_focus_out(self, e):
        self.draw_border('#cbd5e1')
        if self.has_placeholder and not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg='#94a3b8')
    
    def on_key_release(self, e):
        if self.entry.get() and self.entry.get() != self.placeholder:
            self.entry.config(fg='#374151')
    
    def create_rounded_rect(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Create rounded rectangle on canvas"""
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
        
        return canvas.create_polygon(points, **kwargs, smooth=True)
    
    def draw_border(self, color):
        self.canvas.delete("border")
        # Draw outer border
        self.create_rounded_rect(self.canvas, 0, 0, self.winfo_reqwidth(), 
                                self.winfo_reqheight(), 8, fill=color, outline="", tags="border")
        # Draw inner white area
        self.create_rounded_rect(self.canvas, 1, 1, self.winfo_reqwidth()-1, 
                                self.winfo_reqheight()-1, 7, fill='white', outline="", tags="border")
    
    def get(self):
        value = self.entry.get()
        if value == self.placeholder:
            return ""
        return value
    
    def insert(self, index, text):
        self.entry.insert(index, text)
        self.entry.config(fg='#374151')
        self.has_placeholder = False
    
    def delete(self, first, last=None):
        self.entry.delete(first, last)

class ModernCard(tk.Frame):
    """Modern card container with shadow and rounded corners"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg='white', **kwargs)
        self.config(highlightbackground='#e5e7eb', highlightthickness=1, 
                   relief='flat')
        
    def create_card(self, title="", content_frame=None):
        """Create a card with optional title and content"""
        if title:
            title_label = tk.Label(self, text=title, bg='white', 
                                  font=('Segoe UI', 14, 'bold'), fg='#1e293b')
            title_label.pack(anchor='w', padx=20, pady=(20, 10))
        
        if content_frame:
            content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

class ModernSidebarButton(tk.Frame):
    """Modern sidebar button with hover effects"""
    def __init__(self, parent, text, command, icon="", active=False, **kwargs):
        super().__init__(parent, bg='white' if not active else '#f3f4f6')
        self.command = command
        self.is_active = active
        
        self.btn = tk.Label(self, text=f"{icon} {text}", bg='white' if not active else '#f3f4f6',
                           fg='#374151' if not active else '#1e40af', font=('Segoe UI', 11),
                           cursor='hand2', anchor='w')
        self.btn.pack(fill='x', padx=20, pady=10)
        
        self.btn.bind("<Enter>", self.on_enter)
        self.btn.bind("<Leave>", self.on_leave)
        self.btn.bind("<Button-1>", self.on_click)
        
    def on_enter(self, e):
        if not self.is_active:
            self.btn.config(bg='#f8fafc')
    
    def on_leave(self, e):
        if not self.is_active:
            self.btn.config(bg='white')
    
    def on_click(self, e):
        self.command()
        # You can add active state management here

def create_modern_combobox(parent, values, width=20, default="", **kwargs):
    """Create a modern combobox with consistent styling"""
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Modern.TCombobox', 
                   borderwidth=1, 
                   relief='flat',
                   padding=8,
                   foreground='#374151',
                   background='white')
    
    style.map('Modern.TCombobox',
             fieldbackground=[('readonly', 'white')],
             selectbackground=[('readonly', '#f3f4f6')],
             selectforeground=[('readonly', '#1e293b')])
    
    combo = ttk.Combobox(parent, values=values, width=width, 
                         state='readonly', style='Modern.TCombobox', **kwargs)
    if default and default in values:
        combo.set(default)
    
    return combo

def create_stat_card(parent, title, value, color="#4f46e5", icon=""):
    """Create a modern statistics card"""
    card = tk.Frame(parent, bg='white', relief='flat', highlightbackground='#e5e7eb', 
                   highlightthickness=1, padx=20, pady=15)
    
    # Icon and value
    top_frame = tk.Frame(card, bg='white')
    top_frame.pack(fill='x', pady=(0, 5))
    
    if icon:
        tk.Label(top_frame, text=icon, bg='white', font=('Segoe UI', 14), 
                fg=color).pack(side='left', padx=(0, 10))
    
    tk.Label(top_frame, text=str(value), bg='white', font=('Segoe UI', 24, 'bold'), 
            fg=color).pack(side='right')
    
    # Title
    tk.Label(card, text=title, bg='white', font=('Segoe UI', 11), 
            fg='#64748b').pack(anchor='w')
    
    return card

# Monkey patch canvas to add rounded_rect method
def _create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
    """Add rounded_rect method to tkinter Canvas"""
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
    
    return self.create_polygon(points, **kwargs, smooth=True)

tk.Canvas.create_rounded_rect = _create_rounded_rect