import tkinter as tk
from tkinter import ttk, messagebox

class AdminDashboard:
    def __init__(self, app):
        self.app = app
        
        self.app.clear_window()
        
        # Main container
        self.main = tk.Frame(self.app.root, bg='#f8fafc')
        self.main.pack(fill='both', expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Content area
        self.content = tk.Frame(self.main, bg='white')
        self.content.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        # Show dashboard
        self.show_dashboard()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='#1e40af', width=250)
        sidebar.pack(side='left', fill='y')
        
        # Logo
        tk.Label(sidebar, text="SK Admin Portal", bg='#1e40af', fg='white',
                font=('Helvetica', 18, 'bold')).pack(pady=30)
        
        # Menu items - ALL WORKING
        menu_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("👥 User Management", self.show_user_management),
            ("📅 Event Management", self.show_event_management),
            ("💼 Opportunities", self.show_opportunity_management),
            ("📋 Attendance", self.show_attendance_management),
            ("💬 Feedback", self.show_feedback_management),
            ("", None),
            ("🚪 Logout", self.app.logout)
        ]
        
        for text, command in menu_items:
            if text == "":
                tk.Frame(sidebar, bg='#1e40af', height=20).pack()
            else:
                btn = tk.Button(sidebar, text=text, anchor='w',
                              bg='#1e40af', fg='white', font=('Helvetica', 12),
                              border=0, cursor='hand2', command=command)
                btn.pack(fill='x', padx=20, pady=5)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#2563eb'))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#1e40af'))
        
        # User info
        user_frame = tk.Frame(sidebar, bg='#1e3a8a', pady=10)
        user_frame.pack(side='bottom', fill='x')
        
        user = self.app.user
        tk.Label(user_frame, text=user['name'], bg='#1e3a8a', 
                fg='white', font=('Helvetica', 11, 'bold')).pack()
        tk.Label(user_frame, text=user['email'], bg='#1e3a8a',
                fg='#93c5fd', font=('Helvetica', 9)).pack()
    
    def show_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="Admin Dashboard", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(anchor='w')
        
        # Get statistics
        stats = self.get_stats()
        
        # Stats cards - 2x2 grid
        stats_frame = tk.Frame(self.content, bg='white', padx=30)
        stats_frame.pack(fill='x', pady=(0, 30))
        
        stats_data = [
            ("Total Youth", stats['total_youth'], "#3b82f6"),
            ("Pending Users", stats['pending_users'], "#ef4444"),
            ("Active Events", stats['active_events'], "#10b981"),
            ("Open Opportunities", stats['open_opportunities'], "#f59e0b")
        ]
        
        for i, (title, value, color) in enumerate(stats_data):
            row, col = divmod(i, 2)
            
            if col == 0:
                stats_frame.columnconfigure(0, weight=1)
            if col == 1:
                stats_frame.columnconfigure(1, weight=1)
            
            # Card frame
            card = tk.Frame(stats_frame, bg='white', relief='ridge', borderwidth=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # Card content
            inner = tk.Frame(card, bg='white', padx=20, pady=20)
            inner.pack(fill='both', expand=True)
            
            tk.Label(inner, text=str(value), bg='white', fg=color,
                    font=('Helvetica', 32, 'bold')).pack()
            tk.Label(inner, text=title, bg='white', fg='#64748b',
                    font=('Helvetica', 12)).pack()
        
        # Recent activities
        tk.Label(self.content, text="Recent Activities", bg='white',
                font=('Helvetica', 18, 'bold'), fg='#1e293b').pack(anchor='w', padx=30, pady=(0, 10))
        
        # Get recent activities
        activities = self.get_recent_activities()
        
        activities_frame = tk.Frame(self.content, bg='white', padx=30)
        activities_frame.pack(fill='both', expand=True)
        
        for activity in activities:
            self.create_activity_item(activities_frame, activity)
    
    def get_stats(self):
        cursor = self.app.db.cursor(dictionary=True)
        stats = {}
        
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE role='youth'")
        stats['total_youth'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE status='pending'")
        stats['pending_users'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM events WHERE status IN ('upcoming', 'ongoing')")
        stats['active_events'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM opportunities WHERE status='open'")
        stats['open_opportunities'] = cursor.fetchone()['count']
        
        cursor.close()
        return stats
    
    def get_recent_activities(self):
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 'event' as type, title as description, created_at 
            FROM events 
            ORDER BY created_at DESC 
            LIMIT 5
            UNION
            SELECT 'user' as type, CONCAT(name, ' registered') as description, created_at 
            FROM users 
            ORDER BY created_at DESC 
            LIMIT 5
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        activities = cursor.fetchall()
        cursor.close()
        return activities
    
    def create_activity_item(self, parent, activity):
        frame = tk.Frame(parent, bg='#f3f4f6', relief='ridge', borderwidth=1)
        frame.pack(fill='x', pady=2)
        
        inner = tk.Frame(frame, bg='white', padx=15, pady=10)
        inner.pack(fill='both', expand=True)
        
        # Icon based on type
        icon = "📅" if activity['type'] == 'event' else "👤"
        
        tk.Label(inner, text=f"{icon} {activity['description']}", bg='white',
                font=('Helvetica', 11), fg='#374151').pack(anchor='w')
        
        date_str = activity['created_at'].strftime('%b %d, %Y %I:%M %p')
        tk.Label(inner, text=date_str, bg='white',
                font=('Helvetica', 9), fg='#6b7280').pack(anchor='w', pady=(2, 0))
    
    def show_user_management(self):
        self.app.show_user_management()
    
    def show_event_management(self):
        self.app.show_event_management()
    
    def show_opportunity_management(self):
        self.app.show_opportunity_management()
    
    def show_attendance_management(self):
        self.app.show_attendance_management()
    
    def show_feedback_management(self):
        self.app.show_feedback_management()