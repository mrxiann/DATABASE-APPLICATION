import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ui_utils import ModernTheme, ModernCard, Badge, create_menu_item

class AdminDashboard:
    def __init__(self, app):
        self.app = app
        
        self.app.clear_window()
        
        # Modern main container
        self.main = tk.Frame(self.app.root, bg=ModernTheme.COLORS['light'])
        self.main.pack(fill='both', expand=True)
        
        # Create modern sidebar
        self.create_sidebar()
        
        # Content area
        self.content = tk.Frame(self.main, bg=ModernTheme.COLORS['light'])
        self.content.pack(side='right', fill='both', expand=True)
        
        # Show dashboard
        self.show_dashboard()
    
    def create_sidebar(self):
        """Modern sidebar with gradient"""
        self.sidebar = tk.Frame(self.main, bg=ModernTheme.COLORS['sidebar'], width=280)
        self.sidebar.pack(side='left', fill='y')
        
        # Sidebar header
        header_frame = tk.Frame(self.sidebar, 
                               bg=ModernTheme.COLORS['primary_dark'],
                               height=160)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Logo and title
        logo_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['primary_dark'])
        logo_frame.pack(pady=30, padx=20)
        
        # Logo
        logo_canvas = tk.Canvas(logo_frame, width=60, height=60, 
                               bg=ModernTheme.COLORS['primary_dark'], 
                               highlightthickness=0)
        logo_canvas.pack(side='left')
        logo_canvas.create_rectangle(10, 10, 50, 50, 
                                    fill=ModernTheme.COLORS['primary_light'],
                                    outline="")
        logo_canvas.create_text(30, 30, text="SK", 
                               font=('Segoe UI', 18, 'bold'),
                               fill=ModernTheme.COLORS['white'])
        
        # Title
        title_frame = tk.Frame(logo_frame, bg=ModernTheme.COLORS['primary_dark'])
        title_frame.pack(side='left', padx=15)
        
        tk.Label(title_frame, text="Admin", 
                font=ModernTheme.FONTS['h4'],
                fg=ModernTheme.COLORS['white'],
                bg=ModernTheme.COLORS['primary_dark']).pack(anchor='w')
        
        tk.Label(title_frame, text="Portal", 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['gray_light'],
                bg=ModernTheme.COLORS['primary_dark']).pack(anchor='w')
        
        # Menu items
        menu_frame = tk.Frame(self.sidebar, bg=ModernTheme.COLORS['sidebar'])
        menu_frame.pack(fill='both', expand=True, padx=15, pady=20)
        
        # Menu sections
        menu_sections = [
            {
                'title': "MAIN",
                'items': [
                    ("📊", "Dashboard", self.show_dashboard),
                    ("👥", "User Management", self.show_user_management),
                    ("📅", "Event Management", self.show_event_management),
                    ("💼", "Opportunities", self.show_opportunity_management),
                    ("📋", "Attendance", self.show_attendance_management),
                    ("💬", "Feedback", self.show_feedback_management),
                ]
            },
            {
                'title': "ACCOUNT",
                'items': [
                    ("⚙️", "Settings", self.show_settings),
                    ("🚪", "Logout", self.app.logout),
                ]
            }
        ]
        
        for section in menu_sections:
            # Section title
            if 'title' in section:
                tk.Label(menu_frame, 
                        text=section['title'],
                        font=('Segoe UI', 10, 'bold'),
                        fg=ModernTheme.COLORS['gray'],
                        bg=ModernTheme.COLORS['sidebar']).pack(anchor='w', pady=(20, 10), padx=5)
            
            # Menu items
            for icon, text, command in section['items']:
                create_menu_item(menu_frame, icon, text, command)
        
        # User info at bottom
        user_frame = tk.Frame(self.sidebar, 
                             bg=ModernTheme.COLORS['sidebar'],
                             highlightbackground=ModernTheme.COLORS['gray'],
                             highlightthickness=1)
        user_frame.pack(side='bottom', fill='x', padx=15, pady=20)
        
        user = self.app.user
        
        # Avatar and info
        avatar_frame = tk.Frame(user_frame, bg=ModernTheme.COLORS['sidebar'])
        avatar_frame.pack(pady=15, padx=15)
        
        # Avatar
        avatar_canvas = tk.Canvas(avatar_frame, width=40, height=40, 
                                 bg=ModernTheme.COLORS['primary'], 
                                 highlightthickness=0)
        avatar_canvas.pack(side='left')
        initials = ''.join([name[0] for name in user['name'].split()[:2]]).upper()
        avatar_canvas.create_text(20, 20, text=initials,
                                 font=('Segoe UI', 12, 'bold'),
                                 fill=ModernTheme.COLORS['white'])
        
        # User details
        details_frame = tk.Frame(user_frame, bg=ModernTheme.COLORS['sidebar'])
        details_frame.pack(side='left', padx=15, fill='both', expand=True)
        
        tk.Label(details_frame, text=user['name'], 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['white'],
                bg=ModernTheme.COLORS['sidebar']).pack(anchor='w')
        
        tk.Label(details_frame, text="Administrator", 
                font=ModernTheme.FONTS['body_small'],
                fg=ModernTheme.COLORS['gray_light'],
                bg=ModernTheme.COLORS['sidebar']).pack(anchor='w', pady=(2, 0))
    
    def show_settings(self):
        """Placeholder for settings"""
        messagebox.showinfo("Settings", "Settings feature coming soon!")
    
    def show_dashboard(self):
        """Modern dashboard with cards"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header with date
        header_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        header_frame.pack(fill='x', padx=30, pady=30)
        
        tk.Label(header_frame, text="Dashboard Overview", 
                font=ModernTheme.FONTS['h1'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['light']).pack(side='left')
        
        date_label = tk.Label(header_frame, 
                             text=datetime.now().strftime('%B %d, %Y'),
                             font=ModernTheme.FONTS['body'],
                             fg=ModernTheme.COLORS['gray'],
                             bg=ModernTheme.COLORS['light'])
        date_label.pack(side='right', pady=10)
        
        # Stats cards grid
        stats = self.get_stats()
        
        stats_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        stats_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        stats_data = [
            ("Total Youth", stats['total_youth'], "👥", ModernTheme.COLORS['primary'], "#e0e7ff"),
            ("Pending Users", stats['pending_users'], "⏳", ModernTheme.COLORS['warning'], "#fef3c7"),
            ("Active Events", stats['active_events'], "📅", ModernTheme.COLORS['success'], "#d1fae5"),
            ("Open Opportunities", stats['open_opportunities'], "💼", ModernTheme.COLORS['accent'], "#fef3c7"),
            ("Total Feedback", stats.get('total_feedback', 0), "💬", ModernTheme.COLORS['info'], "#dbeafe"),
            ("Attendance Rate", f"{stats.get('attendance_rate', 0)}%", "📈", ModernTheme.COLORS['secondary'], "#dcfce7")
        ]
        
        # Configure grid
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1, uniform="col")
        
        for i, (title, value, icon, color, bg_color) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            card = self.create_stat_card(stats_frame, title, value, icon, color, bg_color)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        # Recent activities section
        activities_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        activities_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        tk.Label(activities_frame, text="Recent Activities", 
                font=ModernTheme.FONTS['h3'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['light']).pack(anchor='w', pady=(0, 15))
        
        # Activities card
        activities_card = ModernCard(activities_frame)
        activities_card.pack(fill='both', expand=True)
        
        activities = self.get_recent_activities()
        
        if not activities:
            tk.Label(activities_card.inner, text="No recent activities", 
                    font=ModernTheme.FONTS['body'],
                    fg=ModernTheme.COLORS['gray'],
                    bg=ModernTheme.COLORS['white']).pack(pady=20)
        else:
            # Create scrollable activities list
            canvas = tk.Canvas(activities_card.inner, 
                              bg=ModernTheme.COLORS['white'],
                              highlightthickness=0)
            scrollbar = tk.Scrollbar(activities_card.inner, 
                                    orient='vertical', 
                                    command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=ModernTheme.COLORS['white'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for i, activity in enumerate(activities):
                self.create_activity_item(scrollable_frame, activity)
                if i < len(activities) - 1:
                    tk.Frame(scrollable_frame, 
                            bg=ModernTheme.COLORS['gray_light'], 
                            height=1).pack(fill='x', padx=10, pady=5)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
    
    def create_stat_card(self, parent, title, value, icon, color, bg_color):
        """Create a modern statistic card"""
        card = ModernCard(parent, padding=20, bg=bg_color)
        
        # Top section with icon and value
        top_frame = tk.Frame(card.inner, bg=bg_color)
        top_frame.pack(fill='x', pady=(0, 15))
        
        # Icon
        icon_frame = tk.Frame(top_frame, bg=bg_color)
        icon_frame.pack(side='left')
        
        icon_canvas = tk.Canvas(icon_frame, width=48, height=48, 
                               bg=color + '20', 
                               highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_text(24, 24, text=icon, 
                               font=('Segoe UI', 20),
                               fill=color)
        
        # Value
        tk.Label(top_frame, text=str(value), 
                font=ModernTheme.FONTS['h2'],
                fg=ModernTheme.COLORS['dark'],
                bg=bg_color).pack(side='right', padx=10)
        
        # Title
        tk.Label(card.inner, text=title, 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['gray'],
                bg=bg_color).pack(anchor='w')
        
        return card
    
    def create_activity_item(self, parent, activity):
        """Create a modern activity item"""
        item_frame = tk.Frame(parent, bg=ModernTheme.COLORS['white'], height=60)
        item_frame.pack(fill='x', pady=5)
        item_frame.pack_propagate(False)
        
        # Icon based on type
        icon = "📅" if activity['type'] == 'event' else "👤"
        icon_color = ModernTheme.COLORS['primary'] if activity['type'] == 'event' else ModernTheme.COLORS['success']
        
        # Icon circle
        icon_frame = tk.Frame(item_frame, bg=ModernTheme.COLORS['white'])
        icon_frame.pack(side='left', padx=(10, 15))
        
        icon_canvas = tk.Canvas(icon_frame, width=36, height=36, 
                               bg=icon_color + '20', 
                               highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_text(18, 18, text=icon, 
                               font=('Segoe UI', 14),
                               fill=icon_color)
        
        # Activity details
        details_frame = tk.Frame(item_frame, bg=ModernTheme.COLORS['white'])
        details_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(details_frame, text=activity['description'], 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(anchor='w')
        
        date_str = activity['created_at'].strftime('%b %d, %Y at %I:%M %p')
        tk.Label(details_frame, text=date_str, 
                font=ModernTheme.FONTS['body_small'],
                fg=ModernTheme.COLORS['gray'],
                bg=ModernTheme.COLORS['white']).pack(anchor='w', pady=(2, 0))
    
    def get_stats(self):
        """Get dashboard statistics"""
        cursor = self.app.db.cursor(dictionary=True)
        stats = {}
        
        try:
            # Total youth
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE role='youth' AND status='active'")
            stats['total_youth'] = cursor.fetchone()['count']
            
            # Pending users
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE status='pending'")
            stats['pending_users'] = cursor.fetchone()['count']
            
            # Active events
            cursor.execute("SELECT COUNT(*) as count FROM events WHERE status IN ('upcoming', 'ongoing')")
            stats['active_events'] = cursor.fetchone()['count']
            
            # Open opportunities
            cursor.execute("SELECT COUNT(*) as count FROM opportunities WHERE status='open'")
            stats['open_opportunities'] = cursor.fetchone()['count']
            
            # Total feedback
            cursor.execute("SELECT COUNT(*) as count FROM feedback")
            stats['total_feedback'] = cursor.fetchone()['count']
            
            # Attendance rate (placeholder)
            stats['attendance_rate'] = 85
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            # Default values
            stats = {
                'total_youth': 0,
                'pending_users': 0,
                'active_events': 0,
                'open_opportunities': 0,
                'total_feedback': 0,
                'attendance_rate': 0
            }
        finally:
            cursor.close()
        
        return stats
    
    def get_recent_activities(self):
        """Get recent activities"""
        cursor = self.app.db.cursor(dictionary=True)
        activities = []
        
        try:
            # Recent events
            cursor.execute("""
                SELECT 'event' as type, CONCAT('New event: ', title) as description, created_at 
                FROM events 
                ORDER BY created_at DESC 
                LIMIT 3
            """)
            events = cursor.fetchall()
            
            # Recent user registrations
            cursor.execute("""
                SELECT 'user' as type, CONCAT(name, ' registered') as description, created_at 
                FROM users 
                WHERE role = 'youth'
                ORDER BY created_at DESC 
                LIMIT 2
            """)
            users = cursor.fetchall()
            
            activities = events + users
            activities.sort(key=lambda x: x['created_at'], reverse=True)
            activities = activities[:5]
            
        except Exception as e:
            print(f"Error getting activities: {e}")
        finally:
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