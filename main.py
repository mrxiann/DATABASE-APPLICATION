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
        
        self.center_window()
        
        self.db = self.connect_db()
        self.user = None
        
        self.show_login()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='sk_youth_portal'
            )
            print("Database connected successfully!")
            return conn
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            messagebox.showerror("Database Error", 
                               f"Cannot connect to database.\nError: {err}\n\nPlease ensure:\n1. XAMPP is running\n2. MySQL is started\n3. Run database.py first")
            return None
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login(self):
        self.clear_window()
        from login import LoginWindow
        LoginWindow(self)
    
    def show_admin_dashboard(self, user_data):
        self.user = user_data
        self.clear_window()
        from admin import AdminDashboard
        AdminDashboard(self)
    
    def show_youth_dashboard(self, user_data):
        self.user = user_data
        self.clear_window()
        from youth import YouthDashboard
        YouthDashboard(self)
    
    def show_event_management(self):
        self.clear_window()
        from event_manager import EventManagement
        EventManagement(self)
    
    def show_opportunity_management(self):
        self.clear_window()
        from opportunity_manager import OpportunityManagement
        OpportunityManagement(self)
    
    def show_attendance_management(self):
        self.clear_window()
        from attendance_manager import AttendanceManagement
        AttendanceManagement(self)
    
    def show_feedback_management(self):
        self.clear_window()
        from feedback_manager import FeedbackManagement
        FeedbackManagement(self)
    
    def show_user_management(self):
        self.clear_window()
        from user_manager import UserManagement
        UserManagement(self)
    
    def logout(self):
        self.user = None
        self.show_login()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SKYouthPortal()
    app.run()