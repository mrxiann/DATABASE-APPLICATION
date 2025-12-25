import tkinter as tk
from tkinter import messagebox
import hashlib

class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, width=200, height=45, bg="#4f46e5", fg="white", font=("Segoe UI", 12, "bold"), radius=10):
        super().__init__(parent, width=width, height=height, highlightthickness=0, bd=0)
        self.command = command
        self.bg = bg
        self.hover_bg = self.adjust_color(bg, -20)
        self.fg = fg
        self.font = font
        self.radius = radius
        self.text = text
        
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
        # Draw shadow
        shadow_color = '#888888'  # Simplified shadow
        self.create_rounded_rect(2, 2, self.winfo_reqwidth()+1, self.winfo_reqheight()+1, 
                                self.radius, fill=shadow_color, outline="")
        
        # Draw main button
        self.create_rounded_rect(0, 0, self.winfo_reqwidth()-1, self.winfo_reqheight()-1, 
                                self.radius, fill=color, outline="")
        
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2, 
                        text=self.text, fill=self.fg, font=self.font, tags="text")
    
    def on_enter(self, e):
        self.draw_button(self.hover_bg)
    
    def on_leave(self, e):
        self.draw_button(self.bg)
    
    def on_click(self, e):
        self.draw_button(self.adjust_color(self.bg, -30))
    
    def on_release(self, e):
        self.draw_button(self.hover_bg)
        self.command()
    
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

class RoundedEntry(tk.Frame):
    def __init__(self, parent, width=30, font=("Segoe UI", 11), show=None, **kwargs):
        super().__init__(parent, bg='#f1f5f9')
        self.width = width
        self.font = font
        self.show = show
        
        self.canvas = tk.Canvas(self, height=45, width=width*10, highlightthickness=0, bg='#f1f5f9')
        self.canvas.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Entry field
        self.entry = tk.Entry(self, font=font, relief='flat', bg='white', 
                             highlightthickness=0, show=show)
        self.entry_window = self.canvas.create_window(10, 22, window=self.entry, 
                                                     anchor="w", width=width*10-20)
        
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        
        self.draw_border('#cbd5e1')
    
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
    
    def on_focus_in(self, e):
        self.draw_border('#4f46e5')
    
    def on_focus_out(self, e):
        self.draw_border('#cbd5e1')
    
    def get(self):
        return self.entry.get()
    
    def insert(self, index, text):
        self.entry.insert(index, text)
    
    def delete(self, first, last=None):
        self.entry.delete(first, last)

class LoginWindow:
    def __init__(self, app):
        self.app = app
        
        # Main container with gradient background
        container = tk.Frame(self.app.root, bg='#f8fafc')
        container.pack(fill='both', expand=True)
        
        # Left decorative panel
        left_panel = tk.Frame(container, bg='#4f46e5', width=400)
        left_panel.pack(side='left', fill='both', expand=False)
        left_panel.pack_propagate(False)
        
        # Decorative elements
        decor_canvas = tk.Canvas(left_panel, bg='#4f46e5', highlightthickness=0)
        decor_canvas.pack(fill='both', expand=True, padx=40, pady=60)
        
        # Get canvas dimensions
        canvas_width = 320  # 400 - 80 (40px padding on each side)
        canvas_height = decor_canvas.winfo_reqheight()
        
        # Calculate center positions
        center_x = canvas_width // 2  # 160 (in canvas coordinates)
        center_y = canvas_height // 2
        
        # Decorative circles
        colors = ['#e0e7ff', '#c7d2fe', '#a5b4fc']  # Light indigo shades
        
        # Position circles relative to center
        positions = [
            (center_x - 80, center_y - 80, 60),   # Top-left of center
            (center_x + 60, center_y - 40, 80),   # Top-right of center
            (center_x - 20, center_y + 60, 40)    # Bottom of center
        ]
        
        for (x, y, r), color in zip(positions, colors):
            decor_canvas.create_oval(x, y, x+r, y+r, fill=color, outline='')
        
        # Welcome text - perfectly centered
        # Start from center and work outwards
        text_start_y = center_y - 100  # Start above center
        
        decor_canvas.create_text(center_x, text_start_y, text="Welcome to", 
                                font=("Segoe UI", 18), fill='white', anchor='center')
        
        decor_canvas.create_text(center_x, text_start_y + 40, text="SK Youth", 
                                font=("Segoe UI", 26, 'bold'), fill='white', anchor='center')
        
        decor_canvas.create_text(center_x, text_start_y + 80, text="Management and", 
                                font=("Segoe UI", 22, 'bold'), fill='white', anchor='center')
        
        decor_canvas.create_text(center_x, text_start_y + 120, text="Information System", 
                                font=("Segoe UI", 22, 'bold'), fill='white', anchor='center')
        
        decor_canvas.create_text(center_x, text_start_y + 170, text="Empowering Youth, Building Futures", 
                                font=("Segoe UI", 14), fill='#e0e7ff', anchor='center')
        
        # Right panel - Login form
        right_panel = tk.Frame(container, bg='white')
        right_panel.pack(side='right', fill='both', expand=True, padx=80, pady=60)
        
        # Header
        header_frame = tk.Frame(right_panel, bg='white')
        header_frame.pack(fill='x', pady=(0, 40))
        
        tk.Label(header_frame, text="Welcome Back", bg='white', 
                font=('Segoe UI', 32, 'bold'), fg='#1e293b').pack(anchor='w')
        tk.Label(header_frame, text="Sign in to your account", bg='white', 
                font=('Segoe UI', 14), fg='#64748b').pack(anchor='w', pady=(5, 0))
        
        # Form container
        form_frame = tk.Frame(right_panel, bg='white')
        form_frame.pack(fill='x', pady=(0, 30))
        
        # Email
        tk.Label(form_frame, text="Email Address", bg='white', 
                font=('Segoe UI', 11), fg='#475569').pack(anchor='w', pady=(0, 8))
        self.email = RoundedEntry(form_frame, width=30, font=('Segoe UI', 12))
        self.email.pack(fill='x', pady=(0, 20))
        self.email.insert(0, "admin@sk.ph")
        
        # Password
        tk.Label(form_frame, text="Password", bg='white', 
                font=('Segoe UI', 11), fg='#475569').pack(anchor='w', pady=(0, 8))
        self.password = RoundedEntry(form_frame, width=30, font=('Segoe UI', 12), show="*")
        self.password.pack(fill='x', pady=(0, 25))
        self.password.insert(0, "admin123")
        
        # Role selection
        role_frame = tk.Frame(form_frame, bg='white')
        role_frame.pack(fill='x', pady=(0, 25))
        
        tk.Label(role_frame, text="Login as:", bg='white', 
                font=('Segoe UI', 11), fg='#475569').pack(side='left', padx=(0, 20))
        
        self.role = tk.StringVar(value="admin")
        
        # Modern radio buttons
        roles = [("Youth", "youth"), ("Admin", "admin")]
        for text, value in roles:
            rb_frame = tk.Frame(role_frame, bg='white')
            rb_frame.pack(side='left', padx=(0, 15))
            
            canvas = tk.Canvas(rb_frame, width=24, height=24, bg='white', highlightthickness=0)
            canvas.pack(side='left')
            
            # Create radio button indicator
            indicator = canvas.create_oval(4, 4, 20, 20, outline='#cbd5e1', width=2, fill='white')
            inner = canvas.create_oval(8, 8, 16, 16, outline='', fill='#4f46e5' if value == "admin" else 'white')
            
            def create_radio_cmd(val, canv=canvas, ind=inner, indicator_obj=indicator):
                return lambda: [self.role.set(val), 
                               canv.itemconfig(ind, fill='#4f46e5' if self.role.get() == val else 'white'),
                               canv.itemconfig(indicator_obj, outline='#4f46e5' if self.role.get() == val else '#cbd5e1')]
            
            canvas.bind("<Button-1>", lambda e, v=value, c=canvas, i=inner, ind=indicator: 
                       [self.role.set(v), c.itemconfig(i, fill='#4f46e5'), c.itemconfig(ind, outline='#4f46e5')])
            canvas.bind("<Enter>", lambda e, c=canvas, ind=indicator, v=value: 
                       c.itemconfig(ind, outline='#94a3b8' if self.role.get() != v else '#4f46e5'))
            canvas.bind("<Leave>", lambda e, c=canvas, ind=indicator, v=value: 
                       c.itemconfig(ind, outline='#4f46e5' if self.role.get() == v else '#cbd5e1'))
            
            tk.Label(rb_frame, text=text, bg='white', font=('Segoe UI', 11), 
                    fg='#475569').pack(side='left', padx=(8, 0))
            
            # Update the other radio button when one is clicked
            if value == "admin":
                canvas.bind("<Button-1>", lambda e, v=value: [self.update_radio_buttons(role_frame, v)])
            else:
                canvas.bind("<Button-1>", lambda e, v=value: [self.update_radio_buttons(role_frame, v)])
        
        # Login button - FIXED: Use lambda to defer the method call
        self.login_btn = ModernButton(form_frame, text="Sign In", 
                                     command=lambda: self.do_login(), 
                                     width=320, height=48, 
                                     bg='#4f46e5', fg='white',
                                     font=('Segoe UI', 13, 'bold'), radius=12)
        self.login_btn.pack(pady=(0, 25))
        
        # Register link
        link_frame = tk.Frame(form_frame, bg='white')
        link_frame.pack()
        
        tk.Label(link_frame, text="Don't have an account?", bg='white',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left')
        
        register_btn = tk.Label(link_frame, text="Register here", bg='white',
                              font=('Segoe UI', 11, 'underline'), fg='#4f46e5',
                              cursor='hand2')
        register_btn.pack(side='left', padx=(5, 0))
        register_btn.bind("<Button-1>", lambda e: self.register())
        register_btn.bind("<Enter>", lambda e: register_btn.config(fg='#3730a3'))
        register_btn.bind("<Leave>", lambda e: register_btn.config(fg='#4f46e5'))
        
        # Footer
        footer_frame = tk.Frame(right_panel, bg='white')
        footer_frame.pack(side='bottom', fill='x', pady=(20, 0))
        
        tk.Label(footer_frame, text="© 2025 SK Youth Management and Information System. All rights reserved.", 
                bg='white', font=('Segoe UI', 10), fg='#94a3b8').pack()
        
        self.app.root.bind('<Return>', lambda e: self.do_login())
        
        # Initial radio button state
        self.update_radio_buttons(role_frame, "admin")
    
    def update_radio_buttons(self, parent_frame, selected_value):
        """Update all radio button visual states"""
        for child in parent_frame.winfo_children():
            if isinstance(child, tk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, tk.Canvas):
                        # Get the value from the label next to this canvas
                        for sibling in child.winfo_children():
                            if isinstance(sibling, tk.Label):
                                value = "admin" if "Admin" in sibling.cget("text") else "youth"
                                # Find the oval shapes
                                items = widget.find_all()
                                if len(items) >= 2:
                                    indicator = items[0]  # Outer circle
                                    inner = items[1]     # Inner circle
                                    
                                    if value == selected_value:
                                        widget.itemconfig(inner, fill='#4f46e5')
                                        widget.itemconfig(indicator, outline='#4f46e5')
                                    else:
                                        widget.itemconfig(inner, fill='white')
                                        widget.itemconfig(indicator, outline='#cbd5e1')
    
    def do_login(self):
        email = self.email.get()
        pwd = self.password.get()
        role = self.role.get()
        
        if not email or not pwd:
            messagebox.showerror("Error", "Please fill all fields")
            return
        
        if not self.app.db:
            messagebox.showerror("Error", "Database not connected")
            return
        
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        
        cursor = self.app.db.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s AND role = %s AND status = 'active'",
            (email, hashed, role)
        )
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            if role == 'admin':
                self.app.show_admin_dashboard(user)
            else:
                self.app.show_youth_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid login credentials or account not active")
    
    def register(self):
        win = tk.Toplevel(self.app.root)
        win.title("Register Account")
        win.geometry("450x550")
        win.configure(bg='white')
        win.resizable(False, False)
        
        # Center the window
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header
        header = tk.Frame(win, bg='#4f46e5', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="Create Account", 
                font=('Segoe UI', 20, 'bold'), bg='#4f46e5', fg='white').pack(expand=True)
        
        close_btn = tk.Label(header, text="✕", font=('Segoe UI', 16), 
                           bg='#4f46e5', fg='white', cursor='hand2')
        close_btn.place(relx=0.95, rely=0.5, anchor='center')
        close_btn.bind("<Button-1>", lambda e: win.destroy())
        
        # Form container
        form_container = tk.Frame(win, bg='white')
        form_container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Form fields
        entries = {}
        field_configs = [
            ("Full Name", "name"),
            ("Email Address", "email"),
            ("Phone Number", "phone"),
            ("Barangay", "barangay"),
            ("Password", "password"),
            ("Confirm Password", "confirm")
        ]
        
        for i, (label, key) in enumerate(field_configs):
            tk.Label(form_container, text=label, bg='white', 
                    font=('Segoe UI', 11), fg='#475569').grid(row=i, column=0, sticky='w', pady=(10, 5))
            
            if "password" in key:
                entry = RoundedEntry(form_container, width=25, font=('Segoe UI', 11), show="*")
            else:
                entry = RoundedEntry(form_container, width=25, font=('Segoe UI', 11))
            
            entry.grid(row=i, column=0, pady=(0, 10), sticky='ew')
            entries[key] = entry
        
        def submit():
            data = {k: v.get().strip() for k, v in entries.items()}
            
            # Validation
            required_fields = ['name', 'email', 'password', 'confirm']
            for field in required_fields:
                if not data[field]:
                    messagebox.showerror("Error", f"{field.replace('_', ' ').title()} is required")
                    return
            
            if data['password'] != data['confirm']:
                messagebox.showerror("Error", "Passwords don't match")
                return
            
            hashed = hashlib.sha256(data['password'].encode()).hexdigest()
            
            cursor = self.app.db.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (name, email, password, phone, barangay, role, status) 
                    VALUES (%s, %s, %s, %s, %s, 'youth', 'pending')
                """, (data['name'], data['email'], hashed, data['phone'], data['barangay']))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "Account created! Wait for admin approval.")
                win.destroy()
            except Exception as e:
                if "Duplicate" in str(e):
                    messagebox.showerror("Error", "Email already exists")
                else:
                    messagebox.showerror("Error", f"Registration failed: {e}")
            finally:
                cursor.close()
        
        # Submit button
        submit_btn = ModernButton(form_container, text="Create Account", 
                                 command=submit, width=200, height=42, 
                                 bg='#10b981', fg='white',
                                 font=('Segoe UI', 12, 'bold'), radius=10)
        submit_btn.grid(row=len(field_configs), column=0, pady=(20, 10))