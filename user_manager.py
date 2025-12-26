# user_manager.py
import tkinter as tk
from tkinter import ttk, messagebox
import csv
from tkinter import filedialog

class UserManagement:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.main = tk.Frame(self.root, bg='#f8fafc')
        self.main.pack(fill='both', expand=True)
        
        self.create_sidebar()
        
        self.content = tk.Frame(self.main, bg='#f8fafc')
        self.content.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        self.show_users()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='#10b981', width=250)
        sidebar.pack(side='left', fill='y')
        
        tk.Label(sidebar, text="SK System", bg='#10b981', fg='white',
                font=('Helvetica', 18, 'bold')).pack(pady=30)
        
        tk.Button(sidebar, text="← Back to Dashboard", 
                 command=lambda: self.app.show_admin_dashboard(self.app.user),
                 bg='#34d399', fg='white', font=('Helvetica', 11),
                 border=0, cursor='hand2').pack(pady=(0, 30))
        
        menu_items = [
            ("👥 All Users", self.show_users),
            ("⏳ Pending Approval", self.show_pending),
            ("➕ Add New User", self.add_user),
            ("", None),
            ("📊 Reports", self.show_reports),
            ("📤 Export Users", self.export_users)
        ]
        
        for text, command in menu_items:
            if text == "":
                tk.Frame(sidebar, bg='#34d399', height=1).pack(fill='x', pady=10, padx=20)
            else:
                btn = tk.Button(sidebar, text=text, anchor='w',
                              bg='#10b981', fg='white', font=('Helvetica', 12),
                              border=0, cursor='hand2', command=command)
                btn.pack(fill='x', padx=20, pady=5)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#34d399'))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#10b981'))
    
    def show_users(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="👥 User Management", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        # Search and filter
        filter_frame = tk.Frame(header, bg='white')
        filter_frame.pack(side='right')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, width=25, 
                               font=('Helvetica', 11))
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.filter_users())
        
        self.role_filter = ttk.Combobox(filter_frame, values=['All', 'youth', 'admin'], 
                                       width=10, state='readonly')
        self.role_filter.set('All')
        self.role_filter.pack(side='left', padx=5)
        self.role_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_users())
        
        self.status_filter = ttk.Combobox(filter_frame, values=['All', 'active', 'pending', 'inactive'], 
                                         width=10, state='readonly')
        self.status_filter.set('All')
        self.status_filter.pack(side='left', padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_users())
        
        # Add user button
        tk.Button(self.content, text="➕ Add New User", command=self.add_user,
                 bg='#3b82f6', fg='white', font=('Helvetica', 11, 'bold'),
                 padx=20, pady=10, cursor='hand2').pack(anchor='w', padx=30, pady=(10, 20))
        
        # Create treeview for users
        tree_frame = tk.Frame(self.content, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Create scrollable treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Email', 'Role', 'Status', 'Barangay', 'Join Date'), 
                                show='headings', height=20)
        
        # Define headings
        self.tree.heading('ID', text='Youth ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Role', text='Role')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Barangay', text='Barangay')
        self.tree.heading('Join Date', text='Join Date')
        
        # Define columns
        self.tree.column('ID', width=100)
        self.tree.column('Name', width=150)
        self.tree.column('Email', width=150)
        self.tree.column('Role', width=80)
        self.tree.column('Status', width=80)
        self.tree.column('Barangay', width=100)
        self.tree.column('Join Date', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Add right-click menu
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Load users
        self.load_all_users()
    
    def load_all_users(self):
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, email, role, status, barangay, youth_id, created_at
            FROM users
            ORDER BY created_at DESC
        """)
        self.all_users = cursor.fetchall()
        cursor.close()
        
        self.filter_users()
    
    def filter_users(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        search_text = self.search_var.get().lower()
        role_filter = self.role_filter.get().lower()
        status_filter = self.status_filter.get().lower()
        
        filtered = []
        for user in self.all_users:
            matches_search = (not search_text or 
                            search_text in user['name'].lower() or 
                            search_text in user['email'].lower() or
                            search_text in (user['youth_id'] or '').lower())
            
            matches_role = (role_filter == 'all' or 
                           user['role'].lower() == role_filter)
            
            matches_status = (status_filter == 'all' or 
                            user['status'].lower() == status_filter)
            
            if matches_search and matches_role and matches_status:
                filtered.append(user)
        
        # Add filtered users to tree
        for user in filtered:
            join_date = user['created_at'].strftime('%Y-%m-%d')
            self.tree.insert('', 'end', values=(
                user['youth_id'] or 'N/A',
                user['name'],
                user['email'],
                user['role'].title(),
                user['status'].title(),
                user['barangay'] or 'N/A',
                join_date
            ), tags=(user['id'],))
    
    def show_context_menu(self, event):
        # Get selected item
        item = self.tree.identify_row(event.y)
        if not item:
            return
        
        # Select the item
        self.tree.selection_set(item)
        
        # Get user ID from tags
        user_id = self.tree.item(item, 'tags')[0]
        
        # Create context menu
        menu = tk.Menu(self.root, tearoff=0)
        
        # Get user status
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT status FROM users WHERE id = %s", (user_id,))
        user_status = cursor.fetchone()['status']
        cursor.close()
        
        if user_status == 'pending':
            menu.add_command(label="Approve", command=lambda: self.approve_user(user_id))
            menu.add_command(label="Reject", command=lambda: self.reject_user(user_id))
        elif user_status == 'active':
            menu.add_command(label="Deactivate", command=lambda: self.deactivate_user(user_id))
        elif user_status == 'inactive':
            menu.add_command(label="Activate", command=lambda: self.activate_user(user_id))
        
        menu.add_separator()
        menu.add_command(label="Edit User", command=lambda: self.edit_user(user_id))
        menu.add_command(label="View Details", command=lambda: self.view_user_details(user_id))
        menu.add_command(label="Reset Password", command=lambda: self.reset_password(user_id))
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def approve_user(self, user_id):
        if messagebox.askyesno("Confirm", "Approve this user?"):
            try:
                cursor = self.app.db.cursor()
                # Generate youth ID if not exists
                cursor.execute("SELECT youth_id FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                if not result[0]:
                    # Generate youth ID
                    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'youth' AND status = 'active'")
                    count = cursor.fetchone()[0]
                    youth_id = f"SK-YOUTH-{count + 1:03d}"
                    cursor.execute("UPDATE users SET status = 'active', youth_id = %s WHERE id = %s", 
                                  (youth_id, user_id))
                else:
                    cursor.execute("UPDATE users SET status = 'active' WHERE id = %s", (user_id,))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "User approved successfully!")
                self.load_all_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to approve user: {e}")
            finally:
                cursor.close()
    
    def reject_user(self, user_id):
        if messagebox.askyesno("Confirm", "Reject this user registration?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE users SET status = 'rejected' WHERE id = %s", (user_id,))
                self.app.db.commit()
                messagebox.showinfo("Success", "User registration rejected!")
                self.load_all_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reject user: {e}")
            finally:
                cursor.close()
    
    def deactivate_user(self, user_id):
        if messagebox.askyesno("Confirm", "Deactivate this user?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE users SET status = 'inactive' WHERE id = %s", (user_id,))
                self.app.db.commit()
                messagebox.showinfo("Success", "User deactivated!")
                self.load_all_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to deactivate user: {e}")
            finally:
                cursor.close()
    
    def activate_user(self, user_id):
        if messagebox.askyesno("Confirm", "Activate this user?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE users SET status = 'active' WHERE id = %s", (user_id,))
                self.app.db.commit()
                messagebox.showinfo("Success", "User activated!")
                self.load_all_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to activate user: {e}")
            finally:
                cursor.close()
    
    def edit_user(self, user_id):
        # Get user details
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        
        win = tk.Toplevel(self.root)
        win.title(f"Edit User: {user['name']}")
        win.geometry("500x600")
        win.configure(bg='white')
        
        tk.Label(win, text="Edit User", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        form = tk.Frame(win, bg='white', padx=40)
        form.pack(fill='both', expand=True)
        
        # Name
        tk.Label(form, text="Full Name:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(10, 5))
        name_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        name_entry.pack(fill='x', pady=(0, 10))
        name_entry.insert(0, user['name'])
        
        # Email
        tk.Label(form, text="Email:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        email_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        email_entry.pack(fill='x', pady=(0, 10))
        email_entry.insert(0, user['email'])
        
        # Youth ID
        tk.Label(form, text="Youth ID:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        youth_id_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        youth_id_entry.pack(fill='x', pady=(0, 10))
        youth_id_entry.insert(0, user['youth_id'] or '')
        
        # Role
        tk.Label(form, text="Role:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        role_var = tk.StringVar(value=user['role'])
        role_frame = tk.Frame(form, bg='white')
        role_frame.pack(fill='x', pady=(0, 10))
        
        tk.Radiobutton(role_frame, text="Youth", variable=role_var,
                      value='youth', bg='white').pack(side='left', padx=(0, 10))
        tk.Radiobutton(role_frame, text="Admin", variable=role_var,
                      value='admin', bg='white').pack(side='left')
        
        # Status
        tk.Label(form, text="Status:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        status_combo = ttk.Combobox(form, values=['active', 'inactive', 'pending', 'rejected'], 
                                   width=28, state='readonly')
        status_combo.pack(fill='x', pady=(0, 10))
        status_combo.set(user['status'])
        
        # Barangay
        tk.Label(form, text="Barangay:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        barangay_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        barangay_entry.pack(fill='x', pady=(0, 10))
        barangay_entry.insert(0, user['barangay'] or '')
        
        # Phone
        tk.Label(form, text="Phone:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        phone_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        phone_entry.pack(fill='x', pady=(0, 10))
        phone_entry.insert(0, user['phone'] or '')
        
        def save_changes():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            youth_id = youth_id_entry.get().strip() or None
            role = role_var.get()
            status = status_combo.get()
            barangay = barangay_entry.get().strip() or None
            phone = phone_entry.get().strip() or None
            
            if not all([name, email]):
                messagebox.showerror("Error", "Name and Email are required")
                return
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET name = %s, email = %s, youth_id = %s, role = %s, 
                        status = %s, barangay = %s, phone = %s
                    WHERE id = %s
                """, (name, email, youth_id, role, status, barangay, phone, user_id))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "User updated successfully!")
                win.destroy()
                self.load_all_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update user: {e}")
            finally:
                cursor.close()
        
        tk.Button(win, text="Save Changes", command=save_changes,
                 bg='#10b981', fg='white', font=('Helvetica', 11, 'bold'),
                 width=20, pady=10, cursor='hand2').pack(pady=20)
    
    def view_user_details(self, user_id):
        # Get user details with statistics
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT er.event_id) as events_attended,
                COALESCE(SUM(er.hours_credited), 0) as total_hours,
                (SELECT COUNT(*) FROM opportunity_applications WHERE user_id = %s) as applications,
                (SELECT COUNT(*) FROM feedback WHERE user_id = %s) as feedback_count
            FROM event_registrations er
            WHERE er.user_id = %s AND er.attendance_status = 'attended'
        """, (user_id, user_id, user_id))
        
        stats = cursor.fetchone()
        cursor.close()
        
        win = tk.Toplevel(self.root)
        win.title(f"User Details: {user['name']}")
        win.geometry("600x700")
        win.configure(bg='white')
        
        tk.Label(win, text="User Details", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        content = tk.Frame(win, bg='white', padx=40)
        content.pack(fill='both', expand=True)
        
        # Basic info
        tk.Label(content, text="Basic Information", bg='white',
                font=('Helvetica', 16, 'bold'), fg='#1e293b').pack(anchor='w', pady=(0, 10))
        
        basic_info = [
            ("Name:", user['name']),
            ("Email:", user['email']),
            ("Youth ID:", user['youth_id'] or 'Not assigned'),
            ("Role:", user['role'].title()),
            ("Status:", user['status'].title()),
            ("Barangay:", user['barangay'] or 'Not provided'),
            ("Phone:", user['phone'] or 'Not provided'),
            ("Join Date:", user['created_at'].strftime('%B %d, %Y'))
        ]
        
        for label, value in basic_info:
            row = tk.Frame(content, bg='white')
            row.pack(fill='x', pady=2)
            tk.Label(row, text=label, bg='white', font=('Helvetica', 11, 'bold'),
                    width=15, anchor='w').pack(side='left')
            tk.Label(row, text=value, bg='white', font=('Helvetica', 11)).pack(side='left')
        
        # Statistics
        tk.Label(content, text="Statistics", bg='white',
                font=('Helvetica', 16, 'bold'), fg='#1e293b').pack(anchor='w', pady=(20, 10))
        
        stats_info = [
            ("Events Attended:", stats['events_attended'] if stats else 0),
            ("Volunteer Hours:", stats['total_hours'] if stats else 0),
            ("Applications:", stats['applications'] if stats else 0),
            ("Feedback Submitted:", stats['feedback_count'] if stats else 0)
        ]
        
        for label, value in stats_info:
            row = tk.Frame(content, bg='white')
            row.pack(fill='x', pady=2)
            tk.Label(row, text=label, bg='white', font=('Helvetica', 11, 'bold'),
                    width=20, anchor='w').pack(side='left')
            tk.Label(row, text=str(value), bg='white', font=('Helvetica', 11)).pack(side='left')
    
    def reset_password(self, user_id):
        win = tk.Toplevel(self.root)
        win.title("Reset Password")
        win.geometry("400x300")
        win.configure(bg='white')
        
        tk.Label(win, text="Reset Password", bg='white',
                font=('Helvetica', 18, 'bold')).pack(pady=20)
        
        form = tk.Frame(win, bg='white', padx=40)
        form.pack(fill='both', expand=True)
        
        # Get user name
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        user_name = cursor.fetchone()['name']
        cursor.close()
        
        tk.Label(form, text=f"User: {user_name}", bg='white',
                font=('Helvetica', 12)).pack(pady=(0, 20))
        
        tk.Label(form, text="New Password:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        password_entry = tk.Entry(form, width=30, font=('Helvetica', 11), show="*")
        password_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(form, text="Confirm Password:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        confirm_entry = tk.Entry(form, width=30, font=('Helvetica', 11), show="*")
        confirm_entry.pack(fill='x', pady=(0, 20))
        
        def reset():
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            if not password:
                messagebox.showerror("Error", "Please enter a password")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            import hashlib
            hashed = hashlib.sha256(password.encode()).hexdigest()
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed, user_id))
                self.app.db.commit()
                messagebox.showinfo("Success", "Password reset successfully!")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reset password: {e}")
            finally:
                cursor.close()
        
        tk.Button(win, text="Reset Password", command=reset,
                 bg='#ef4444', fg='white', font=('Helvetica', 11, 'bold'),
                 width=20, pady=10, cursor='hand2').pack(pady=20)
    
    def add_user(self):
        win = tk.Toplevel(self.root)
        win.title("Add New User")
        win.geometry("500x600")
        win.configure(bg='white')
        
        tk.Label(win, text="Add New User", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        form = tk.Frame(win, bg='white', padx=40)
        form.pack(fill='both', expand=True)
        
        # Name
        tk.Label(form, text="Full Name*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(10, 5))
        name_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        name_entry.pack(fill='x', pady=(0, 10))
        
        # Email
        tk.Label(form, text="Email*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        email_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        email_entry.pack(fill='x', pady=(0, 10))
        
        # Password
        tk.Label(form, text="Password*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        password_entry = tk.Entry(form, width=30, font=('Helvetica', 11), show="*")
        password_entry.pack(fill='x', pady=(0, 10))
        
        # Role
        tk.Label(form, text="Role*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        role_var = tk.StringVar(value='youth')
        role_frame = tk.Frame(form, bg='white')
        role_frame.pack(fill='x', pady=(0, 10))
        
        tk.Radiobutton(role_frame, text="Youth", variable=role_var,
                      value='youth', bg='white').pack(side='left', padx=(0, 10))
        tk.Radiobutton(role_frame, text="Admin", variable=role_var,
                      value='admin', bg='white').pack(side='left')
        
        # Status
        tk.Label(form, text="Status*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        status_combo = ttk.Combobox(form, values=['active', 'pending'], 
                                   width=28, state='readonly')
        status_combo.pack(fill='x', pady=(0, 10))
        status_combo.set('active')
        
        # Barangay
        tk.Label(form, text="Barangay:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        barangay_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        barangay_entry.pack(fill='x', pady=(0, 10))
        
        # Phone
        tk.Label(form, text="Phone:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        phone_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        phone_entry.pack(fill='x', pady=(0, 20))
        
        def save_user():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()
            role = role_var.get()
            status = status_combo.get()
            barangay = barangay_entry.get().strip() or None
            phone = phone_entry.get().strip() or None
            
            if not all([name, email, password]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            import hashlib
            hashed = hashlib.sha256(password.encode()).hexdigest()
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    INSERT INTO users (name, email, password, role, status, barangay, phone)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (name, email, hashed, role, status, barangay, phone))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "User added successfully!")
                win.destroy()
                self.load_all_users()
            except Exception as e:
                if "Duplicate" in str(e):
                    messagebox.showerror("Error", "Email already exists")
                else:
                    messagebox.showerror("Error", f"Failed to add user: {e}")
            finally:
                cursor.close()
        
        tk.Button(win, text="Add User", command=save_user,
                 bg='#10b981', fg='white', font=('Helvetica', 11, 'bold'),
                 width=20, pady=10, cursor='hand2').pack(pady=20)
    
    def show_pending(self):
        # Set filters to show only pending users
        self.status_filter.set('pending')
        self.filter_users()
    
    def show_reports(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="📊 User Reports", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
        # Get statistics
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_users,
                SUM(CASE WHEN role = 'youth' THEN 1 ELSE 0 END) as total_youth,
                SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) as total_admins,
                SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active_users,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_users,
                SUM(CASE WHEN status = 'inactive' THEN 1 ELSE 0 END) as inactive_users
            FROM users
        """)
        
        stats = cursor.fetchone()
        cursor.close()
        
        # Display stats 
        stats_frame = tk.Frame(self.content, bg='white')
        stats_frame.pack(pady=20)
        
        stat_cards = [
            ("Total Users", stats['total_users'], "#3b82f6", "#e0e7ff"),  # Added light color
            ("Youth Members", stats['total_youth'], "#10b981", "#d1fae5"),
            ("Admins", stats['total_admins'], "#f59e0b", "#fef3c7"),
            ("Active", stats['active_users'], "#8b5cf6", "#ede9fe"),
            ("Pending", stats['pending_users'], "#ec4899", "#fce7f3"),
            ("Inactive", stats['inactive_users'], "#ef4444", "#fee2e2")
        ]
        
        for i, (title, value, color, light_color) in enumerate(stat_cards):
            row, col = divmod(i, 3)
            
            if col == 0:
                stats_frame.columnconfigure(0, weight=1)
            if col == 1:
                stats_frame.columnconfigure(1, weight=1)
            if col == 2:
                stats_frame.columnconfigure(2, weight=1)
            
            card = tk.Frame(stats_frame, bg='white', relief='ridge', borderwidth=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # FIXED: Use light_color directly instead of trying to modify hex
            inner = tk.Frame(card, bg=light_color, padx=20, pady=20)
            inner.pack(fill='both', expand=True)
            
            tk.Label(inner, text=str(value), bg=light_color, fg=color,
                    font=('Helvetica', 28, 'bold')).pack()
            tk.Label(inner, text=title, bg=light_color, fg='#64748b',
                    font=('Helvetica', 12)).pack()
    
    def export_users(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Users to CSV"
        )
        
        if not file_path:
            return
        
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT name, email, youth_id, role, status, barangay, phone, 
                   DATE(created_at) as join_date
            FROM users
            ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        cursor.close()
        
        if not users:
            messagebox.showwarning("No Data", "No users to export")
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Name', 'Email', 'Youth ID', 'Role', 'Status', 
                             'Barangay', 'Phone', 'Join Date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for user in users:
                    writer.writerow({
                        'Name': user['name'],
                        'Email': user['email'],
                        'Youth ID': user['youth_id'] or '',
                        'Role': user['role'],
                        'Status': user['status'],
                        'Barangay': user['barangay'] or '',
                        'Phone': user['phone'] or '',
                        'Join Date': user['join_date'] or ''
                    })
            
            messagebox.showinfo("Success", f"Users exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")