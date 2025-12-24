import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ui_utils import ModernTheme, ModernCard, RoundedButton, create_menu_item

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
                               bg=ModernTheme.COLORS['primary'],
                               height=160)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Logo and title
        logo_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['primary'])
        logo_frame.pack(pady=30, padx=20)
        
        # Logo
        logo_canvas = tk.Canvas(logo_frame, width=60, height=60, 
                               bg=ModernTheme.COLORS['primary'], 
                               highlightthickness=0)
        logo_canvas.pack(side='left')
        logo_canvas.create_rectangle(10, 10, 50, 50, 
                                    fill=ModernTheme.COLORS['primary_light'],
                                    outline="")
        logo_canvas.create_text(30, 30, text="SK", 
                               font=('Segoe UI', 18, 'bold'),
                               fill=ModernTheme.COLORS['white'])
        
        # Title
        title_frame = tk.Frame(logo_frame, bg=ModernTheme.COLORS['primary'])
        title_frame.pack(side='left', padx=15)
        
        tk.Label(title_frame, text="Admin", 
                font=ModernTheme.FONTS['h4'],
                fg=ModernTheme.COLORS['white'],
                bg=ModernTheme.COLORS['primary']).pack(anchor='w')
        
        tk.Label(title_frame, text="Portal", 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['gray_light'],
                bg=ModernTheme.COLORS['primary']).pack(anchor='w')
        
        # Menu items
        menu_frame = tk.Frame(self.sidebar, bg=ModernTheme.COLORS['sidebar'])
        menu_frame.pack(fill='both', expand=True, padx=15, pady=20)
        
        # Main menu items
        menu_items = [
            ("📊", "Dashboard", self.show_dashboard),
            ("👥", "User Management", self.show_user_management),
            ("📅", "Event Management", self.show_event_management),
            ("💼", "Opportunities", self.show_opportunity_management),
            ("📋", "Attendance", self.show_attendance_management),
            ("💬", "Feedback", self.show_feedback_management),
            ("", "", None),  # Separator
            ("🚪", "Logout", self.app.logout)
        ]
        
        for icon, text, command in menu_items:
            if text == "":
                tk.Frame(menu_frame, bg=ModernTheme.COLORS['gray'], height=1).pack(fill='x', pady=15)
            elif command:
                create_menu_item(menu_frame, icon, text, command)
        
        # User info at bottom
        user_frame = tk.Frame(self.sidebar, 
                             bg=ModernTheme.COLORS['sidebar'])
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
    
    def show_dashboard(self):
        """Modern dashboard with cards"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header with date
        header_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        header_frame.pack(fill='x', padx=30, pady=30)
        
        tk.Label(header_frame, text="Dashboard Overview", 
                font=ModernTheme.FONTS['h2'],
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
        stats_frame.pack(fill='x', padx=30, pady=10)
        
        stats_data = [
            ("Total Youth", stats['total_youth'], "👥", ModernTheme.COLORS['primary']),
            ("Pending Users", stats['pending_users'], "⏳", ModernTheme.COLORS['warning']),
            ("Active Events", stats['active_events'], "📅", ModernTheme.COLORS['success']),
            ("Open Opportunities", stats['open_opportunities'], "💼", ModernTheme.COLORS['accent'])
        ]
        
        for i, (title, value, icon, color) in enumerate(stats_data):
            row = i // 2
            col = i % 2
            
            if col == 0:
                stats_frame.columnconfigure(0, weight=1)
            if col == 1:
                stats_frame.columnconfigure(1, weight=1)
            
            card = self.create_stat_card(stats_frame, title, value, icon, color)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
    
    def create_stat_card(self, parent, title, value, icon, color):
        """Create a modern statistic card"""
        card = ModernCard(parent)
        
        # Icon and value
        top_frame = tk.Frame(card.inner, bg=ModernTheme.COLORS['white'])
        top_frame.pack(fill='x', pady=(0, 15))
        
        # Icon
        icon_frame = tk.Frame(top_frame, bg=ModernTheme.COLORS['white'])
        icon_frame.pack(side='left')
        
        icon_canvas = tk.Canvas(icon_frame, width=44, height=44, 
                               bg=color + '20', 
                               highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_text(22, 22, text=icon, 
                               font=('Segoe UI', 18),
                               fill=color)
        
        # Value
        tk.Label(top_frame, text=str(value), 
                font=ModernTheme.FONTS['h2'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(side='right', padx=10)
        
        # Title
        tk.Label(card.inner, text=title, 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['gray'],
                bg=ModernTheme.COLORS['white']).pack(anchor='w')
        
        return card
    
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
            
        except Exception as e:
            print(f"Error getting stats: {e}")
            # Default values
            stats = {
                'total_youth': 0,
                'pending_users': 0,
                'active_events': 0,
                'open_opportunities': 0
            }
        finally:
            cursor.close()
        
        return stats
    
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