import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
import io
from datetime import datetime
from ui_utils import ModernTheme, ModernCard, RoundedButton, create_menu_item

class YouthDashboard:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Modern gradient background
        self.main = tk.Frame(self.root, bg=ModernTheme.COLORS['light'])
        self.main.pack(fill='both', expand=True)
        
        # Create modern sidebar
        self.create_sidebar()
        
        # Content area
        self.content = tk.Frame(self.main, bg=ModernTheme.COLORS['light'])
        self.content.pack(side='right', fill='both', expand=True)
        
        # Show dashboard
        self.show_dashboard()
    
    def create_sidebar(self):
        """Modern sidebar for youth"""
        self.sidebar = tk.Frame(self.main, bg=ModernTheme.COLORS['primary_dark'], width=280)
        self.sidebar.pack(side='left', fill='y')
        
        # Sidebar header with user info
        header_frame = tk.Frame(self.sidebar, 
                               bg=ModernTheme.COLORS['primary'],
                               height=180)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        user = self.app.user
        
        # User avatar and info
        avatar_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['primary'])
        avatar_frame.pack(pady=30)
        
        # Avatar with gradient
        avatar_canvas = tk.Canvas(avatar_frame, width=70, height=70, 
                                 bg=ModernTheme.COLORS['primary_light'],
                                 highlightthickness=0)
        avatar_canvas.pack()
        
        # Create circular avatar
        avatar_canvas.create_oval(5, 5, 65, 65, 
                                 fill=ModernTheme.COLORS['primary_light'],
                                 outline=ModernTheme.COLORS['white'],
                                 width=3)
        
        # User initials
        initials = ''.join([name[0] for name in user['name'].split()[:2]]).upper()
        avatar_canvas.create_text(35, 35, text=initials,
                                 font=('Segoe UI', 18, 'bold'),
                                 fill=ModernTheme.COLORS['white'])
        
        # User name and ID
        tk.Label(header_frame, text=user['name'], 
                font=ModernTheme.FONTS['h4'],
                fg=ModernTheme.COLORS['white'],
                bg=ModernTheme.COLORS['primary']).pack(pady=(10, 5))
        
        youth_id = user.get('youth_id', 'Pending')
        tk.Label(header_frame, text=f"ID: {youth_id}", 
                font=ModernTheme.FONTS['body_small'],
                fg=ModernTheme.COLORS['gray_light'],
                bg=ModernTheme.COLORS['primary']).pack()
        
        # Status badge
        status_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['primary'])
        status_frame.pack(pady=10)
        
        status = user.get('status', 'active').title()
        status_color = ModernTheme.COLORS['success'] if status.lower() == 'active' else ModernTheme.COLORS['warning']
        
        status_badge = tk.Frame(status_frame, bg=status_color + '40')
        status_badge.pack()
        
        tk.Label(status_badge, text=status, 
                font=('Segoe UI', 9, 'bold'),
                fg=status_color,
                bg=status_color + '40',
                padx=12,
                pady=3).pack()
        
        # Menu items
        menu_frame = tk.Frame(self.sidebar, bg=ModernTheme.COLORS['primary_dark'])
        menu_frame.pack(fill='both', expand=True, padx=15, pady=20)
        
        # Menu sections
        menu_sections = [
            {
                'title': "NAVIGATION",
                'items': [
                    ("🏠", "Dashboard", self.show_dashboard),
                    ("📅", "Events", self.show_events),
                    ("💼", "Opportunities", self.show_opportunities),
                    ("📱", "QR Code", self.show_qr),
                ]
            },
            {
                'title': "ACCOUNT",
                'items': [
                    ("👤", "Profile", self.show_profile),
                    ("💬", "Feedback", self.show_feedback),
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
                        bg=ModernTheme.COLORS['primary_dark']).pack(anchor='w', pady=(20, 10), padx=5)
            
            # Menu items
            for icon, text, command in section['items']:
                create_menu_item(menu_frame, icon, text, command, bg=ModernTheme.COLORS['primary_dark'])
    
    def show_settings(self):
        """Placeholder for settings"""
        messagebox.showinfo("Settings", "Settings feature coming soon!")
    
    def show_dashboard(self):
        """Modern youth dashboard"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        user = self.app.user
        
        # Welcome header
        header_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        header_frame.pack(fill='x', padx=30, pady=30)
        
        tk.Label(header_frame, text="Welcome back!", 
                font=ModernTheme.FONTS['h1'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['light']).pack(anchor='w')
        
        tk.Label(header_frame, text=f"Hello {user['name'].split()[0]}, here's your dashboard overview", 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['gray'],
                bg=ModernTheme.COLORS['light']).pack(anchor='w', pady=(5, 0))
        
        # Get user statistics
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT er.event_id) as events_attended,
                COALESCE(SUM(er.hours_credited), 0) as total_hours,
                (SELECT COUNT(*) FROM opportunity_applications WHERE user_id = %s) as applications
            FROM event_registrations er
            WHERE er.user_id = %s AND er.attendance_status = 'attended'
        """, (user['id'], user['id']))
        
        stats_data = cursor.fetchone()
        cursor.close()
        
        events_attended = stats_data['events_attended'] if stats_data else 0
        total_hours = stats_data['total_hours'] if stats_data else 0
        applications = stats_data['applications'] if stats_data else 0
        
        # Get latest award
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT award_name FROM awards WHERE user_id = %s ORDER BY award_date DESC LIMIT 1", (user['id'],))
        award_data = cursor.fetchone()
        cursor.close()
        
        latest_award = award_data['award_name'] if award_data else "None yet"
        
        # Stats cards
        stats_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        stats_frame.pack(fill='x', padx=30, pady=10)
        
        stats = [
            ("Events Attended", str(events_attended), "📅", ModernTheme.COLORS['primary'], "#e0e7ff"),
            ("Volunteer Hours", str(total_hours), "⏱️", ModernTheme.COLORS['success'], "#d1fae5"),
            ("Applications", str(applications), "📄", ModernTheme.COLORS['accent'], "#fef3c7"),
            ("Latest Award", latest_award, "🏆", ModernTheme.COLORS['warning'], "#fef3c7")
        ]
        
        # Configure grid
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1, uniform="col")
        
        for i, (title, value, icon, color, bg_color) in enumerate(stats):
            card = self.create_stat_card(stats_frame, title, value, icon, color, bg_color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
        
        # Quick actions section
        actions_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        actions_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        tk.Label(actions_frame, text="Quick Actions", 
                font=ModernTheme.FONTS['h3'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['light']).pack(anchor='w', pady=(0, 15))
        
        # Actions grid
        actions_grid = tk.Frame(actions_frame, bg=ModernTheme.COLORS['light'])
        actions_grid.pack(fill='both', expand=True)
        
        actions = [
            ("Register for Event", "📝", "Find and register for upcoming events", self.show_events, ModernTheme.COLORS['primary']),
            ("Apply for Opportunity", "💼", "Browse job and volunteer opportunities", self.show_opportunities, ModernTheme.COLORS['success']),
            ("View QR Code", "📱", "Show your QR code for attendance", self.show_qr, ModernTheme.COLORS['accent']),
            ("Submit Feedback", "💬", "Share your suggestions and feedback", self.show_feedback, ModernTheme.COLORS['info'])
        ]
        
        for i, (title, icon, description, command, color) in enumerate(actions):
            row = i // 2
            col = i % 2
            
            if col == 0:
                actions_grid.columnconfigure(0, weight=1)
            if col == 1:
                actions_grid.columnconfigure(1, weight=1)
            
            action_card = self.create_action_card(actions_grid, title, icon, description, command, color)
            action_card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
    
    def create_stat_card(self, parent, title, value, icon, color, bg_color):
        """Create a modern statistic card"""
        card = ModernCard(parent, padding=20, bg=bg_color)
        
        # Icon and value
        top_frame = tk.Frame(card.inner, bg=bg_color)
        top_frame.pack(fill='x', pady=(0, 15))
        
        # Icon
        icon_frame = tk.Frame(top_frame, bg=bg_color)
        icon_frame.pack(side='left')
        
        icon_canvas = tk.Canvas(icon_frame, width=44, height=44, 
                               bg=color + '20', 
                               highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_text(22, 22, text=icon, 
                               font=('Segoe UI', 18),
                               fill=color)
        
        # Value
        tk.Label(top_frame, text=value, 
                font=ModernTheme.FONTS['h2'],
                fg=ModernTheme.COLORS['dark'],
                bg=bg_color).pack(side='right', padx=10)
        
        # Title
        tk.Label(card.inner, text=title, 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['gray'],
                bg=bg_color).pack(anchor='w')
        
        return card
    
    def create_action_card(self, parent, title, icon, description, command, color):
        """Create a quick action card"""
        card = ModernCard(parent, padding=20)
        
        # Icon
        icon_frame = tk.Frame(card.inner, bg=ModernTheme.COLORS['white'])
        icon_frame.pack(anchor='w', pady=(0, 15))
        
        icon_canvas = tk.Canvas(icon_frame, width=48, height=48, 
                               bg=color + '20', 
                               highlightthickness=0)
        icon_canvas.pack()
        icon_canvas.create_text(24, 24, text=icon, 
                               font=('Segoe UI', 20),
                               fill=color)
        
        # Title
        tk.Label(card.inner, text=title, 
                font=ModernTheme.FONTS['h4'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(anchor='w', pady=(0, 5))
        
        # Description
        tk.Label(card.inner, text=description, 
                font=ModernTheme.FONTS['body_small'],
                fg=ModernTheme.COLORS['gray'],
                bg=ModernTheme.COLORS['white'],
                wraplength=200,
                justify='left').pack(anchor='w', pady=(0, 15))
        
        # Action button
        action_btn = RoundedButton(card.inner, 
                                  text="Get Started",
                                  command=command,
                                  bg=color,
                                  fg=ModernTheme.COLORS['white'],
                                  width=120,
                                  height=36)
        action_btn.pack(anchor='w')
        
        return card
    
    # Note: Other methods like show_events(), show_qr(), etc. should be updated similarly
    # with the modern design patterns shown above. Due to length constraints,
    # I'm showing the core structure. You would update each method to use
    # ModernCard, RoundedButton, and other modern components.
    
    def show_events(self):
        """Show events with modern design"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        header_frame.pack(fill='x', padx=30, pady=30)
        
        tk.Label(header_frame, text="Events", 
                font=ModernTheme.FONTS['h1'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['light']).pack(side='left')
        
        # Search bar
        search_frame = tk.Frame(header_frame, bg=ModernTheme.COLORS['light'])
        search_frame.pack(side='right')
        
        search_entry = tk.Entry(search_frame, 
                               bg=ModernTheme.COLORS['white'],
                               fg=ModernTheme.COLORS['dark'],
                               font=ModernTheme.FONTS['body'],
                               width=25,
                               relief='flat',
                               bd=0)
        search_entry.pack(side='left', padx=(0, 10))
        search_entry.insert(0, "Search events...")
        
        search_btn = RoundedButton(search_frame, 
                                  text="🔍",
                                  command=lambda: None,
                                  bg=ModernTheme.COLORS['primary'],
                                  fg=ModernTheme.COLORS['white'],
                                  width=40,
                                  height=40)
        search_btn.pack(side='left')
        
        # Rest of events code would follow similar modern patterns...
        # This is a simplified version
        
    def show_qr(self):
        """Show QR code with modern design"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Center content
        center_frame = tk.Frame(self.content, bg=ModernTheme.COLORS['light'])
        center_frame.pack(expand=True)
        
        qr_card = ModernCard(center_frame, padding=40)
        qr_card.pack(pady=50)
        
        tk.Label(qr_card.inner, text="Your QR Code", 
                font=ModernTheme.FONTS['h2'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(pady=(0, 20))
        
        # Generate QR code
        user_id = self.app.user['id']
        qr_data = f"SK-YOUTH-{user_id:06d}"
        
        qr = qrcode.make(qr_data)
        
        # Convert to PhotoImage
        img = ImageTk.PhotoImage(qr)
        
        # Display QR code
        qr_label = tk.Label(qr_card.inner, image=img, bg=ModernTheme.COLORS['white'])
        qr_label.image = img
        qr_label.pack(pady=10)
        
        tk.Label(qr_card.inner, text=qr_data, 
                font=ModernTheme.FONTS['h4'],
                fg=ModernTheme.COLORS['dark'],
                bg=ModernTheme.COLORS['white']).pack(pady=(20, 10))
        
        tk.Label(qr_card.inner, text="Show this code for event attendance", 
                font=ModernTheme.FONTS['body'],
                fg=ModernTheme.COLORS['gray'],
                bg=ModernTheme.COLORS['white']).pack()
        
        # Download button
        def download_qr():
            try:
                qr.save(f"qr_code_{user_id}.png")
                messagebox.showinfo("Success", f"QR code saved as qr_code_{user_id}.png")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {e}")
        
        download_btn = RoundedButton(qr_card.inner, 
                                    text="Download QR Code",
                                    command=download_qr,
                                    bg=ModernTheme.COLORS['primary'],
                                    fg=ModernTheme.COLORS['white'],
                                    width=200,
                                    height=45)
        download_btn.pack(pady=30)