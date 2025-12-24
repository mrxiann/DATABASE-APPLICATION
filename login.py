import tkinter as tk
from tkinter import messagebox
import hashlib

class LoginWindow:
    def __init__(self, app):
        self.app = app
        
        # Main container
        container = tk.Frame(self.app.root, bg='#f8fafc')
        container.pack(fill='both', expand=True)
        
        # Center card
        card = tk.Frame(container, bg='white', padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        tk.Label(card, text="SK Youth Portal", bg='white', 
                font=('Helvetica', 28, 'bold'), fg='#1e293b').pack(pady=(0, 30))
        
        # Email
        tk.Label(card, text="Email", bg='white', 
                font=('Helvetica', 11), fg='#64748b').pack(anchor='w')
        self.email = tk.Entry(card, width=30, font=('Helvetica', 12))
        self.email.pack(pady=(5, 15))
        self.email.insert(0, "admin@sk.ph")
        
        # Password
        tk.Label(card, text="Password", bg='white', 
                font=('Helvetica', 11), fg='#64748b').pack(anchor='w')
        self.password = tk.Entry(card, width=30, font=('Helvetica', 12), show="*")
        self.password.pack(pady=(5, 20))
        self.password.insert(0, "admin123")
        
        # Role selection
        role_frame = tk.Frame(card, bg='white')
        role_frame.pack(pady=(0, 20))
        
        self.role = tk.StringVar(value="admin")
        tk.Radiobutton(role_frame, text="Youth", variable=self.role, 
                      value="youth", bg='white', font=('Helvetica', 11)).pack(side='left', padx=10)
        tk.Radiobutton(role_frame, text="Admin", variable=self.role, 
                      value="admin", bg='white', font=('Helvetica', 11)).pack(side='left', padx=10)
        
        # Login button
        login_btn = tk.Button(card, text="Login", command=self.do_login,
                            bg='#4f46e5', fg='white', font=('Helvetica', 12, 'bold'),
                            width=20, height=2, cursor='hand2')
        login_btn.pack(pady=(0, 20))
        
        # Register link
        tk.Label(card, text="Don't have an account?", bg='white',
                font=('Helvetica', 10), fg='#64748b').pack()
        tk.Button(card, text="Register here", command=self.register,
                 bg='white', fg='#4f46e5', font=('Helvetica', 10, 'underline'),
                 border=0, cursor='hand2').pack()
        
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
        win.title("Register")
        win.geometry("400x500")
        win.configure(bg='white')
        
        tk.Label(win, text="Register New Account", 
                font=('Helvetica', 18, 'bold'), bg='white').pack(pady=20)
        
        # Form fields
        fields = []
        entries = {}
        
        field_configs = [
            ("Full Name:", "name", True),
            ("Email:", "email", True),
            ("Phone:", "phone", False),
            ("Barangay:", "barangay", False),
            ("Password:", "password", True),
            ("Confirm Password:", "confirm", True)
        ]
        
        for label, key, required in field_configs:
            tk.Label(win, text=label, bg='white', font=('Helvetica', 10)).pack(pady=(10, 5))
            entry = tk.Entry(win, width=30, font=('Helvetica', 11))
            if "password" in key:
                entry.config(show="*")
            entry.pack(pady=(0, 10))
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
        
        tk.Button(win, text="Register", command=submit,
                 bg='#10b981', fg='white', font=('Helvetica', 11),
                 width=20).pack(pady=20)