# login.py
import tkinter as tk
from tkinter import messagebox
import hashlib
from ui_utils import ModernTheme, RoundedButton, ModernCard, GradientFrame

class LoginWindow:
    def __init__(self, app):
        self.app = app
        
        # Modern gradient background
        self.container = GradientFrame(self.app.root, 
                                     color1=ModernTheme.COLORS['light'],
                                     color2=ModernTheme.COLORS['white'])
        self.container.pack(fill='both', expand=True)
        
        # Center card
        self.card = ModernCard(self.container, padding=30)
        self.card.place(relx=0.5, rely=0.5, anchor='center', width=420, height=520)
        
        # Logo and title
        logo_frame = tk.Frame(self.card.inner, bg=ModernTheme.COLORS['white'])
        logo_frame.pack(pady=(0, 30))
        
        # Logo with gradient
        logo_canvas = tk.Canvas(logo_frame, width=80, height=80, 
                               bg=ModernTheme.COLORS['white'], 
                               highlightthickness=0)
        logo_canvas.pack()
        
        # Draw SK logo
        logo_canvas.create_rectangle(20, 20, 60, 60, 
                                    fill=ModernTheme.COLORS['primary'],
                                    outline="")
        logo_canvas.create_text(40, 40, text="SK", 
                               font=('Segoe UI', 20, 'bold'),
                               fill=ModernTheme.COLORS['white'])
        
        tk.Label(logo_frame, text="SK Youth Portal", 
                font=ModernTheme.FONTS['h2'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(pady=(15, 5))
        
        tk.Label(logo_frame, text="Sign in to your account", 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['gray'],
                bg=ModernTheme.COLORS['white']).pack()
        
        # Login form
        form_frame = tk.Frame(self.card.inner, bg=ModernTheme.COLORS['white'])
        form_frame.pack(fill='x', pady=20)
        
        # Email field
        email_frame = tk.Frame(form_frame, bg=ModernTheme.COLORS['white'])
        email_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(email_frame, text="Email Address", 
                font=ModernTheme.FONTS['body_small'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(anchor='w')
        
        self.email = ModernEntry(email_frame, label="")
        self.email.pack(fill='x', pady=(5, 0))
        self.email.entry.insert(0, "admin@sk.ph")
        
        # Password field
        password_frame = tk.Frame(form_frame, bg=ModernTheme.COLORS['white'])
        password_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(password_frame, text="Password", 
                font=ModernTheme.FONTS['body_small'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(anchor='w')
        
        self.password = ModernEntry(password_frame, label="")
        self.password.pack(fill='x', pady=(5, 0))
        self.password.entry.insert(0, "admin123")
        self.password.entry.config(show="*")
        
        # Role selection
        role_frame = tk.Frame(form_frame, bg=ModernTheme.COLORS['white'])
        role_frame.pack(fill='x', pady=(0, 25))
        
        tk.Label(role_frame, text="Login as", 
                font=ModernTheme.FONTS['body_small'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(anchor='w', pady=(0, 8))
        
        self.role = tk.StringVar(value="admin")
        
        # Role buttons container
        role_buttons_frame = tk.Frame(role_frame, bg=ModernTheme.COLORS['white'])
        role_buttons_frame.pack(fill='x')
        
        def create_role_button(parent, text, value):
            btn_frame = tk.Frame(parent, 
                                bg=ModernTheme.COLORS['gray_light'],
                                highlightbackground=ModernTheme.COLORS['gray_light'],
                                highlightthickness=1)
            btn_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
            btn_frame.pack_propagate(False)
            
            def on_click():
                self.role.set(value)
                for child in parent.winfo_children():
                    child.configure(bg=ModernTheme.COLORS['gray_light'])
                    child.label.configure(fg=ModernTheme.COLORS['dark'])
                btn_frame.configure(bg=ModernTheme.COLORS['primary'])
                btn_frame.label.configure(fg=ModernTheme.COLORS['white'])
            
            btn_frame.label = tk.Label(btn_frame, 
                                      text=text,
                                      font=ModernTheme.FONTS['body'],
                                      bg=ModernTheme.COLORS['gray_light'],
                                      fg=ModernTheme.COLORS['dark'],
                                      padx=20,
                                      pady=10)
            btn_frame.label.pack(fill='both', expand=True)
            btn_frame.label.bind("<Button-1>", lambda e: on_click())
            btn_frame.bind("<Button-1>", lambda e: on_click())
            
            if value == "admin":
                on_click()
            
            return btn_frame
        
        create_role_button(role_buttons_frame, "👤 Youth", "youth")
        create_role_button(role_buttons_frame, "👑 Admin", "admin")
        
        # Login button
        login_btn = RoundedButton(form_frame, 
                                 text="Sign In",
                                 command=self.do_login,
                                 bg=ModernTheme.COLORS['primary'],
                                 fg=ModernTheme.COLORS['white'],
                                 width=360,
                                 height=45)
        login_btn.pack(pady=(0, 20))
        
        # Register link
        register_frame = tk.Frame(self.card.inner, bg=ModernTheme.COLORS['white'])
        register_frame.pack(fill='x')
        
        tk.Label(register_frame, text="New to SK Portal?", 
                font=ModernTheme.FONTS['body_small'],
                fg=ModernTheme.COLORS['gray'],
                bg=ModernTheme.COLORS['white']).pack(side='left')
        
        register_link = tk.Label(register_frame, 
                               text="Create an account",
                               font=ModernTheme.FONTS['body_small'],
                               fg=ModernTheme.COLORS['primary'],
                               bg=ModernTheme.COLORS['white'],
                               cursor='hand2')
        register_link.pack(side='left', padx=5)
        register_link.bind("<Button-1>", lambda e: self.register())
        
        # Bind Enter key
        self.app.root.bind('<Return>', lambda e: self.do_login())
    
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
            "SELECT * FROM users WHERE email = %s AND password = %s AND role = %s",
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
            messagebox.showerror("Error", "Invalid login credentials")
    
    def register(self):
        win = tk.Toplevel(self.app.root)
        win.title("Register New Account")
        win.geometry("500x600")
        win.configure(bg=ModernTheme.COLORS['white'])
        
        # Center window
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (500 // 2)
        y = (win.winfo_screenheight() // 2) - (600 // 2)
        win.geometry(f'500x600+{x}+{y}')
        
        # Content frame
        content = tk.Frame(win, bg=ModernTheme.COLORS['white'], padx=40, pady=30)
        content.pack(fill='both', expand=True)
        
        tk.Label(content, text="Create Account", 
                font=ModernTheme.FONTS['h2'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(pady=(0, 30))
        
        # Form fields
        fields_frame = tk.Frame(content, bg=ModernTheme.COLORS['white'])
        fields_frame.pack(fill='x')
        
        entries = {}
        
        field_configs = [
            ("Full Name", "name", True),
            ("Email Address", "email", True),
            ("Phone Number", "phone", False),
            ("Barangay", "barangay", False),
            ("Password", "password", True),
            ("Confirm Password", "confirm", True)
        ]
        
        for label, key, required in field_configs:
            field_frame = tk.Frame(fields_frame, bg=ModernTheme.COLORS['white'])
            field_frame.pack(fill='x', pady=(0, 15))
            
            tk.Label(field_frame, text=label + ("*" if required else ""), 
                    font=ModernTheme.FONTS['body_small'],
                    fg=ModernTheme.COLORS['dark'],
                    bg=ModernTheme.COLORS['white']).pack(anchor='w', pady=(0, 5))
            
            entry = ModernEntry(field_frame, label="")
            entry.pack(fill='x')
            
            if "password" in key:
                entry.entry.config(show="*")
            
            entries[key] = entry
        
        def submit():
            data = {k: v.get().strip() for k, v in entries.items()}
            
            # Validation
            for key, (label, _, required) in zip(data.keys(), field_configs):
                if required and not data[key]:
                    messagebox.showerror("Error", f"{label} is required")
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
        
        # Buttons
        buttons_frame = tk.Frame(content, bg=ModernTheme.COLORS['white'])
        buttons_frame.pack(fill='x', pady=20)
        
        submit_btn = RoundedButton(buttons_frame, 
                                  text="Create Account",
                                  command=submit,
                                  bg=ModernTheme.COLORS['primary'],
                                  fg=ModernTheme.COLORS['white'],
                                  width=200,
                                  height=40)
        submit_btn.pack(side='left', padx=(0, 10))
        
        cancel_btn = RoundedButton(buttons_frame, 
                                  text="Cancel",
                                  command=win.destroy,
                                  bg=ModernTheme.COLORS['gray_light'],
                                  fg=ModernTheme.COLORS['dark'],
                                  width=100,
                                  height=40)
        cancel_btn.pack(side='left')