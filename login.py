import tkinter as tk
from tkinter import messagebox
import hashlib
from ui_utils import RoundedFrame, create_rounded_button, create_rounded_entry

class LoginWindow:
    def __init__(self, app):
        self.app = app
        
        # Main container
        container = tk.Frame(self.app.root, bg='#f8fafc')
        container.pack(fill='both', expand=True)
        
        # Center card
        card = RoundedFrame(container, radius=25)
        card.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        tk.Label(card.frame, text="SK Youth Portal", bg='white', 
                font=('Helvetica', 28, 'bold'), fg='#1e293b').pack(pady=(40, 30))
        
        # Email
        tk.Label(card.frame, text="Email", bg='white', 
                font=('Helvetica', 11), fg='#64748b').pack(anchor='w', padx=40)
        self.email_entry, self.email_frame = create_rounded_entry(card.frame)
        self.email_frame.pack(pady=(5, 15), padx=40)
        self.email_entry.insert(0, "admin@sk.ph")
        
        # Password
        tk.Label(card.frame, text="Password", bg='white', 
                font=('Helvetica', 11), fg='#64748b').pack(anchor='w', padx=40)
        self.password_entry, self.password_frame = create_rounded_entry(card.frame, show="*")
        self.password_frame.pack(pady=(5, 20), padx=40)
        self.password_entry.insert(0, "admin123")
        
        # Role selection
        role_frame = tk.Frame(card.frame, bg='white')
        role_frame.pack(pady=(0, 20), padx=40)
        
        self.role = tk.StringVar(value="admin")
        tk.Radiobutton(role_frame, text="Youth", variable=self.role, 
                      value="youth", bg='white', font=('Helvetica', 11), activebackground='white', selectcolor='#f8fafc').pack(side='left', padx=10)
        tk.Radiobutton(role_frame, text="Admin", variable=self.role, 
                      value="admin", bg='white', font=('Helvetica', 11), activebackground='white', selectcolor='#f8fafc').pack(side='left', padx=10)
        
        # Login button
        login_btn = create_rounded_button(card.frame, text="Login", command=self.do_login,
                                         fill='#4f46e5', fg='white', font=('Helvetica', 12, 'bold'))
        login_btn.pack(pady=(0, 20), padx=40)
        
        # Register link
        tk.Label(card.frame, text="Don't have an account?", bg='white',
                font=('Helvetica', 10), fg='#64748b').pack(padx=40)
        register_btn = create_rounded_button(card.frame, text="Register here", command=self.register,
                                            fill='white', fg='#4f46e5', font=('Helvetica', 10, 'underline'), radius=5)
        register_btn.pack(padx=40, pady=(0, 40))
        
        # Configure rounded after update
        card.frame.update()
        w = card.frame.winfo_width()
        h = card.frame.winfo_height()
        card.configure(width=w, height=h, fill='white', corner_bg='#f8fafc')
        
        self.app.root.bind('<Return>', lambda e: self.do_login())
    
    def do_login(self):
        email = self.email_entry.get()
        pwd = self.password_entry.get()
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
        win.configure(bg='#f8fafc')
        
        # Center card
        card = RoundedFrame(win, radius=25)
        card.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(card.frame, text="Register New Account", 
                font=('Helvetica', 18, 'bold'), bg='white', fg='#1e293b').pack(pady=(40, 20), padx=40)
        
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
        
        for label_text, key, required in field_configs:
            tk.Label(card.frame, text=label_text, bg='white', font=('Helvetica', 10), fg='#64748b').pack(pady=(10, 5), anchor='w', padx=40)
            if "password" in key:
                entry, entry_frame = create_rounded_entry(card.frame, show="*")
            else:
                entry, entry_frame = create_rounded_entry(card.frame)
            entry_frame.pack(pady=(0, 10), padx=40)
            entries[key] = entry
        
        # Submit button
        submit_btn = create_rounded_button(card.frame, text="Register", command=lambda: submit(),
                                          fill='#10b981', fg='white', font=('Helvetica', 11, 'bold'))
        submit_btn.pack(pady=(20, 40), padx=40)
        
        # Configure rounded after update
        card.frame.update()
        w = card.frame.winfo_width()
        h = card.frame.winfo_height()
        card.configure(width=w, height=h, fill='white', corner_bg='#f8fafc')
        
        def submit():
            data = {k: v.get().strip() for k, v in entries.items()}
            
            # Validation
            for cfg, val in zip(field_configs, data.values()):
                label, key, required = cfg
                if required and not val:
                    messagebox.showerror("Error", f"{label[:-1]} is required")
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