import tkinter as tk
from tkinter import ttk, messagebox
from ui_utils import ModernButton, ModernCard, create_stat_card, ModernSidebarButton

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
        self.content = tk.Frame(self.main, bg='#f8fafc')
        self.content.pack(side='right', fill='both', expand=True)
        
        # Show dashboard
        self.show_dashboard()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='white', width=280)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Logo/Header
        header = tk.Frame(sidebar, bg='#4f46e5', height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="SK System", bg='#4f46e5', fg='white',
                font=('Segoe UI', 20, 'bold')).pack(expand=True, pady=(20, 5))
        
        user = self.app.user
        tk.Label(header, text=user['name'], bg='#4f46e5', 
                fg='#e0e7ff', font=('Segoe UI', 11)).pack(pady=(0, 5))
        tk.Label(header, text=user['email'], bg='#4f46e5',
                fg='#a5b4fc', font=('Segoe UI', 9)).pack(pady=(0, 20))
        
        # Navigation Menu
        nav_frame = tk.Frame(sidebar, bg='white')
        nav_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Menu items with modern buttons
        menu_items = [
            ("📊", "Dashboard", self.show_dashboard, True),
            ("👥", "User Management", self.show_user_management, False),
            ("📅", "Event Management", self.show_event_management, False),
            ("💼", "Opportunities", self.show_opportunity_management, False),
            ("📋", "Attendance", self.show_attendance_management, False),
            ("💬", "Feedback", self.show_feedback_management, False),
        ]
        
        for icon, text, command, active in menu_items:
            btn = ModernSidebarButton(nav_frame, text, command, icon, active)
            btn.pack(fill='x', pady=2)
        
        # Logout section
        logout_frame = tk.Frame(sidebar, bg='#f8fafc', height=60)
        logout_frame.pack(side='bottom', fill='x')
        logout_frame.pack_propagate(False)
        
        logout_btn = tk.Label(logout_frame, text="🚪 Logout", bg='#f8fafc',
                             fg='#64748b', font=('Segoe UI', 11), cursor='hand2')
        logout_btn.pack(expand=True)
        logout_btn.bind("<Button-1>", lambda e: self.app.logout())
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(fg='#ef4444'))
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(fg='#64748b'))
    
    def show_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=30)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="Admin Dashboard", bg='#f8fafc',
                font=('Segoe UI', 28, 'bold'), fg='#1e293b').pack(side='left')
        
        # Stats cards
        stats = self.get_stats()
        
        stats_container = tk.Frame(self.content, bg='#f8fafc', padx=30)
        stats_container.pack(fill='x', pady=(0, 30))
        
        # Create stats cards in a 2x2 grid
        stats_frame = tk.Frame(stats_container, bg='#f8fafc')
        stats_frame.pack()
        
        stats_data = [
            ("Total Youth", stats['total_youth'], "#3b82f6", "👥"),
            ("Pending Users", stats['pending_users'], "#ef4444", "⏳"),
            ("Active Events", stats['active_events'], "#10b981", "📅"),
            ("Open Opportunities", stats['open_opportunities'], "#f59e0b", "💼")
        ]
        
        for i, (title, value, color, icon) in enumerate(stats_data):
            row, col = divmod(i, 2)
            
            if col == 0:
                stats_frame.columnconfigure(0, weight=1)
            if col == 1:
                stats_frame.columnconfigure(1, weight=1)
            
            card = create_stat_card(stats_frame, title, value, color, icon)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Recent activities
        activities_frame = ModernCard(self.content, padx=0, pady=0)
        activities_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Activities header
        activities_header = tk.Frame(activities_frame, bg='white')
        activities_header.pack(fill='x', padx=20, pady=(20, 10))
        
        tk.Label(activities_header, text="Recent Activities", bg='white',
                font=('Segoe UI', 18, 'bold'), fg='#1e293b').pack(side='left')
        
        # Refresh button
        refresh_btn = tk.Label(activities_header, text="⟳ Refresh", bg='white',
                              fg='#4f46e5', font=('Segoe UI', 11), cursor='hand2')
        refresh_btn.pack(side='right')
        refresh_btn.bind("<Button-1>", lambda e: self.refresh_activities(activities_content))
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(fg='#3730a3'))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(fg='#4f46e5'))
        
        # Activities content
        activities_content = tk.Frame(activities_frame, bg='white')
        activities_content.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Get and display activities
        activities = self.get_recent_activities()
        
        if not activities:
            tk.Label(activities_content, text="No recent activities", bg='white',
                    font=('Segoe UI', 12), fg='#94a3b8').pack(pady=50)
        else:
            for activity in activities:
                self.create_modern_activity_item(activities_content, activity)
    
    def create_modern_activity_item(self, parent, activity):
        """Create a modern activity item"""
        frame = tk.Frame(parent, bg='#f8fafc')
        frame.pack(fill='x', pady=4)
        
        inner = tk.Frame(frame, bg='white', padx=15, pady=12)
        inner.pack(fill='both', expand=True)
        
        # Icon based on type
        icon = "📅" if activity['type'] == 'event' else "👤"
        icon_color = "#3b82f6" if activity['type'] == 'event' else "#10b981"
        
        # Main content
        content_frame = tk.Frame(inner, bg='white')
        content_frame.pack(fill='x')
        
        # Icon
        tk.Label(content_frame, text=icon, bg='white', font=('Segoe UI', 12), 
                fg=icon_color).pack(side='left', padx=(0, 10))
        
        # Text
        text_frame = tk.Frame(content_frame, bg='white')
        text_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(text_frame, text=activity['description'], bg='white',
                font=('Segoe UI', 11), fg='#374151', anchor='w').pack(fill='x')
        
        date_str = activity['created_at'].strftime('%b %d, %Y at %I:%M %p')
        tk.Label(text_frame, text=date_str, bg='white',
                font=('Segoe UI', 9), fg='#94a3b8', anchor='w').pack(fill='x', pady=(2, 0))
    
    def refresh_activities(self, parent):
        """Refresh activities list"""
        for widget in parent.winfo_children():
            widget.destroy()
        
        activities = self.get_recent_activities()
        
        if not activities:
            tk.Label(parent, text="No recent activities", bg='white',
                    font=('Segoe UI', 12), fg='#94a3b8').pack(pady=50)
        else:
            for activity in activities:
                self.create_modern_activity_item(parent, activity)
    
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
        """)
        activities = cursor.fetchall()
        cursor.close()
        return activities
    
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