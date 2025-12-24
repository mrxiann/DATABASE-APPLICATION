import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import sys
import os

# Add current directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class SKYouthPortal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SK Youth Portal")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f8fafc')
        
        # Set window icon (optional)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Configure ttk styles for modern look
        self.configure_styles()
        
        self.center_window()
        
        self.db = self.connect_db()
        self.user = None
        
        self.show_login()
    
    def configure_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Configure Treeview
        style.configure('Treeview',
                       background='white',
                       foreground='#1e293b',
                       fieldbackground='white',
                       borderwidth=0)
        
        style.configure('Treeview.Heading',
                       background='#f1f5f9',
                       foreground='#475569',
                       relief='flat',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Treeview.Heading',
                 background=[('active', '#e2e8f0')])
        
        # Configure Scrollbar
        style.configure('Vertical.TScrollbar',
                       background='#e2e8f0',
                       darkcolor='#e2e8f0',
                       lightcolor='#e2e8f0',
                       troughcolor='#f8fafc',
                       bordercolor='#f8fafc',
                       arrowcolor='#64748b',
                       gripcount=0)
        
        style.map('Vertical.TScrollbar',
                 background=[('active', '#cbd5e1')])
        
        # Configure Combobox
        style.configure('TCombobox',
                       selectbackground='#6366f1',
                       selectforeground='white',
                       fieldbackground='white',
                       background='white',
                       bordercolor='#cbd5e1',
                       lightcolor='#cbd5e1',
                       darkcolor='#cbd5e1')
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def connect_db(self):
        """Connect to MySQL database"""
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='sk_youth_portal',
                autocommit=True
            )
            print("✅ Database connected successfully!")
            return conn
        except mysql.connector.Error as err:
            print(f"❌ Database connection error: {err}")
            messagebox.showerror("Database Error", 
                               f"Cannot connect to database.\n\nError: {err}\n\nPlease ensure:\n1. XAMPP is running\n2. MySQL is started\n3. Run database.py first")
            return None
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Show login window"""
        self.clear_window()
        from login import LoginWindow
        LoginWindow(self)
    
    def show_admin_dashboard(self, user_data):
        """Show admin dashboard"""
        self.user = user_data
        self.clear_window()
        from admin import AdminDashboard
        AdminDashboard(self)
    
    def show_youth_dashboard(self, user_data):
        """Show youth dashboard"""
        self.user = user_data
        self.clear_window()
        from youth import YouthDashboard
        YouthDashboard(self)
    
    def show_event_management(self):
        """Show event management"""
        self.clear_window()
        from event_manager import EventManagement
        EventManagement(self)
    
    def show_opportunity_management(self):
        """Show opportunity management"""
        self.clear_window()
        from opportunity_manager import OpportunityManagement
        OpportunityManagement(self)
    
    def show_attendance_management(self):
        """Show attendance management"""
        self.clear_window()
        from attendance_manager import AttendanceManagement
        AttendanceManagement(self)
    
    def show_feedback_management(self):
        """Show feedback management"""
        self.clear_window()
        from feedback_manager import FeedbackManagement
        FeedbackManagement(self)
    
    def show_user_management(self):
        """Show user management"""
        self.clear_window()
        from user_manager import UserManagement
        UserManagement(self)
    
    def logout(self):
        """Logout current user"""
        self.user = None
        self.show_login()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SKYouthPortal()
    app.run()