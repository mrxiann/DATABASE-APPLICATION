import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import math

class ModernTheme:
    """Modern UI theme configuration"""
    COLORS = {
        'primary': '#6366f1',
        'primary_dark': '#4f46e5',
        'primary_light': '#818cf8',
        'secondary': '#10b981',
        'secondary_dark': '#059669',
        'accent': '#f59e0b',
        'danger': '#ef4444',
        'warning': '#f59e0b',
        'success': '#10b981',
        'info': '#3b82f6',
        'dark': '#1e293b',
        'light': '#f8fafc',
        'gray': '#6b7280',
        'gray_light': '#e5e7eb',
        'white': '#ffffff',
        'sidebar': '#1e293b',
        'card': '#ffffff'
    }
    
    FONTS = {
        'h1': ('Segoe UI', 28, 'bold'),
        'h2': ('Segoe UI', 24, 'bold'),
        'h3': ('Segoe UI', 20, 'bold'),
        'h4': ('Segoe UI', 16, 'bold'),
        'body': ('Segoe UI', 11),
        'body_small': ('Segoe UI', 10),
        'button': ('Segoe UI', 11, 'bold'),
        'mono': ('Consolas', 10)
    }

class RoundedButton(tk.Canvas):
    """Modern rounded button with hover effects"""
    def __init__(self, parent, text, command=None, radius=10, **kwargs):
        width = kwargs.pop('width', 120)
        height = kwargs.pop('height', 40)
        bg_color = kwargs.pop('bg', ModernTheme.COLORS['primary'])
        fg_color = kwargs.pop('fg', ModernTheme.COLORS['white'])
        
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)
        self.text = text
        self.command = command
        self.radius = radius
        self.bg_color = bg_color
        self.text_color = fg_color
        
        # Calculate hover colors
        self.hover_bg = self._adjust_color(self.bg_color, -20)
        self.active_bg = self._adjust_color(self.bg_color, -40)
        
        # Bind events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        
        # Draw initial button
        self._draw_button()
        
        # Store for garbage collection
        self.image = None
    
    def _adjust_color(self, hex_color, amount):
        """Adjust color brightness"""
        if not hex_color.startswith('#'):
            return hex_color
            
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        new_rgb = []
        for value in rgb:
            new_value = max(0, min(255, value + amount))
            new_rgb.append(new_value)
            
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)
    
    def _draw_button(self):
        """Draw the rounded button with text"""
        self.delete("all")
        
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            width, height = 120, 40
        
        # Create rounded rectangle image
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Draw rounded rectangle
        draw.rounded_rectangle([(0, 0), (width-1, height-1)], 
                              radius=self.radius, 
                              fill=self.bg_color)
        
        # Convert to PhotoImage
        self.image = ImageTk.PhotoImage(image)
        self.create_image(0, 0, image=self.image, anchor='nw')
        
        # Add text
        self.create_text(width/2, height/2, 
                        text=self.text,
                        fill=self.text_color,
                        font=ModernTheme.FONTS['button'])
    
    def _on_enter(self, e):
        self.bg_color = self.hover_bg
        self._draw_button()
        self.config(cursor="hand2")
    
    def _on_leave(self, e):
        self.bg_color = self.config('bg')[4] if 'bg' in self.config() else ModernTheme.COLORS['primary']
        self._draw_button()
        self.config(cursor="")
    
    def _on_press(self, e):
        self.bg_color = self.active_bg
        self._draw_button()
    
    def _on_release(self, e):
        self.bg_color = self.hover_bg
        self._draw_button()
        if self.command:
            self.command()

class ModernCard(tk.Frame):
    """Modern card with shadow effect and rounded corners"""
    def __init__(self, parent, **kwargs):
        padding = kwargs.pop('padding', 20)
        bg_color = kwargs.pop('bg', ModernTheme.COLORS['card'])
        
        super().__init__(parent, **kwargs)
        self.configure(
            bg=bg_color,
            highlightbackground=ModernTheme.COLORS['gray_light'],
            highlightthickness=1,
            relief='flat'
        )
        
        # Inner frame for content
        self.inner = tk.Frame(self, bg=bg_color)
        self.inner.pack(fill='both', expand=True, padx=padding, pady=padding)

class GradientFrame(tk.Canvas):
    """Frame with gradient background"""
    def __init__(self, parent, color1=None, color2=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1 or ModernTheme.COLORS['light']
        self.color2 = color2 or ModernTheme.COLORS['white']
        self.bind("<Configure>", self._draw_gradient)
    
    def _draw_gradient(self, event=None):
        """Draw gradient background"""
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Calculate gradient
        limit = height
        for i in range(height):
            ratio = i / height
            r = int((1 - ratio) * int(self.color1[1:3], 16) + ratio * int(self.color2[1:3], 16))
            g = int((1 - ratio) * int(self.color1[3:5], 16) + ratio * int(self.color2[3:5], 16))
            b = int((1 - ratio) * int(self.color1[5:7], 16) + ratio * int(self.color2[5:7], 16))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
        self.tag_lower("gradient")

class Badge(tk.Frame):
    """Modern badge for status indicators"""
    def __init__(self, parent, text, color='primary', **kwargs):
        bg_color = ModernTheme.COLORS.get(color, color)
        fg_color = ModernTheme.COLORS['white']
        
        super().__init__(parent, **kwargs)
        self.configure(bg=bg_color)
        
        self.label = tk.Label(self, 
                             text=text.upper(),
                             bg=bg_color,
                             fg=fg_color,
                             font=('Segoe UI', 8, 'bold'),
                             padx=8,
                             pady=2)
        self.label.pack()
    
    def config(self, **kwargs):
        if 'text' in kwargs:
            self.label.config(text=kwargs['text'].upper())
        if 'bg' in kwargs:
            self.configure(bg=kwargs['bg'])
            self.label.configure(bg=kwargs['bg'])
        if 'fg' in kwargs:
            self.label.configure(fg=kwargs['fg'])

class ModernEntry(tk.Frame):
    """Modern styled entry field with floating label"""
    def __init__(self, parent, label="", **kwargs):
        super().__init__(parent, bg=ModernTheme.COLORS['white'])
        
        self.label = tk.Label(self, 
                             text=label,
                             bg=ModernTheme.COLORS['white'],
                             fg=ModernTheme.COLORS['gray'],
                             font=ModernTheme.FONTS['body_small'])
        self.label.pack(anchor='w', pady=(0, 2))
        
        entry_frame = tk.Frame(self, 
                              bg=ModernTheme.COLORS['gray_light'],
                              highlightbackground=ModernTheme.COLORS['gray_light'],
                              highlightthickness=1)
        entry_frame.pack(fill='x')
        
        self.entry = tk.Entry(entry_frame, 
                             bg=ModernTheme.COLORS['white'],
                             fg=ModernTheme.COLORS['dark'],
                             font=ModernTheme.FONTS['body'],
                             relief='flat',
                             bd=0)
        self.entry.pack(fill='x', padx=10, pady=8)
        
        # Focus effects
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        
        # Store original colors
        self.normal_bg = ModernTheme.COLORS['gray_light']
        self.focus_bg = ModernTheme.COLORS['primary']
    
    def _on_focus_in(self, event):
        self.label.config(fg=ModernTheme.COLORS['primary'])
        self.master.children['!frame'].config(
            highlightbackground=self.focus_bg,
            highlightcolor=self.focus_bg
        )
    
    def _on_focus_out(self, event):
        if not self.entry.get():
            self.label.config(fg=ModernTheme.COLORS['gray'])
        self.master.children['!frame'].config(
            highlightbackground=self.normal_bg,
            highlightcolor=self.normal_bg
        )
    
    def get(self):
        return self.entry.get()
    
    def insert(self, index, string):
        self.entry.insert(index, string)
    
    def delete(self, first, last=None):
        self.entry.delete(first, last)
    
    def config(self, **kwargs):
        if 'show' in kwargs:
            self.entry.config(show=kwargs['show'])

def create_menu_item(parent, icon, text, command=None, **kwargs):
    """Create a modern menu item"""
    item_frame = tk.Frame(parent, 
                         bg=kwargs.get('bg', ModernTheme.COLORS['sidebar']),
                         height=kwargs.get('height', 50))
    item_frame.pack(fill='x', pady=kwargs.get('pady', 2))
    item_frame.pack_propagate(False)
    
    # Store original colors
    original_bg = item_frame.cget('bg')
    hover_bg = ModernTheme.COLORS['primary']
    
    # Hover effect
    def on_enter(e):
        item_frame.configure(bg=hover_bg)
        for widget in item_frame.winfo_children():
            widget.configure(bg=hover_bg)
    
    def on_leave(e):
        item_frame.configure(bg=original_bg)
        for widget in item_frame.winfo_children():
            widget.configure(bg=original_bg)
    
    # Icon
    icon_label = tk.Label(item_frame, 
                         text=icon,
                         font=('Segoe UI', 14),
                         fg=ModernTheme.COLORS['white'],
                         bg=original_bg)
    icon_label.pack(side='left', padx=(20, 15))
    
    # Text
    text_label = tk.Label(item_frame, 
                         text=text,
                         font=ModernTheme.FONTS['body'],
                         fg=ModernTheme.COLORS['white'],
                         bg=original_bg,
                         anchor='w')
    text_label.pack(side='left', fill='x', expand=True)
    
    # Bind events
    if command:
        for widget in [item_frame, icon_label, text_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e, cmd=command: cmd())
            widget.configure(cursor='hand2')
    
    return item_frame