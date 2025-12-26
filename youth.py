import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
import io
from datetime import datetime

class YouthDashboard:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        self.main = tk.Frame(self.root, bg='white')
        self.main.pack(fill='both', expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Content area
        self.content = tk.Frame(self.main, bg='#f8fafc')
        self.content.pack(side='right', fill='both', expand=True)
        
        # Show dashboard
        self.show_dashboard()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='#4f46e5', width=250)
        sidebar.pack(side='left', fill='y')
        
        # Logo
        tk.Label(sidebar, text="SK System", bg='#4f46e5', fg='white',
                font=('Helvetica', 18, 'bold')).pack(pady=30)
        
        # Menu items
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📅 View Events", self.show_events),
            ("💼 Opportunities", self.show_opportunities),
            ("📱 My QR Code", self.show_qr),
            ("👤 My Profile", self.show_profile),
            ("💬 Feedback", self.show_feedback)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(sidebar, text=text, anchor='w',
                          bg='#4f46e5', fg='white', font=('Helvetica', 12),
                          border=0, cursor='hand2', command=command)
            btn.pack(fill='x', padx=20, pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#6366f1'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#4f46e5'))
        
        # Logout button
        tk.Frame(sidebar, bg='#4f46e5', height=100).pack(side='bottom', fill='x')
        tk.Button(sidebar, text="🚪 Logout", command=self.app.logout,
                 bg='#ef4444', fg='white', font=('Helvetica', 11),
                 width=15).pack(side='bottom', pady=20)
    
    def show_dashboard(self):
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Welcome header
        user = self.app.user
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text=f"Welcome, {user['name']}!", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(anchor='w')
        tk.Label(header, text="Youth Dashboard", bg='white',
                font=('Helvetica', 14), fg='#64748b').pack(anchor='w')
        
        # Stats cards - get real data from database
        stats_frame = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=10)
        stats_frame.pack(fill='x')
        
        # Get real stats from database
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
        
        stats = [
            ("Events Attended", str(events_attended), "#3b82f6"),
            ("Volunteer Hours", str(total_hours), "#10b981"),
            ("Applications", str(applications), "#f59e0b"),
            ("Latest Award", latest_award, "#ef4444")
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg='white', relief='ridge', borderwidth=1)
            card.grid(row=0, column=i, padx=10, sticky='nsew')
            
            inner = tk.Frame(card, bg='white', padx=20, pady=20)
            inner.pack()
            
            tk.Label(inner, text=value, bg='white', fg=color,
                    font=('Helvetica', 32, 'bold')).pack()
            tk.Label(inner, text=title, bg='white', fg='#64748b',
                    font=('Helvetica', 12)).pack()
        
        # Main content
        main_content = tk.Frame(self.content, bg='#f8fafc', padx=30)
        main_content.pack(fill='both', expand=True)
        
        # Quick links (left)
        left = tk.Frame(main_content, bg='white', relief='ridge', borderwidth=1)
        left.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        tk.Label(left, text="Quick Links", bg='white',
                font=('Helvetica', 16, 'bold'), fg='#1e293b').pack(pady=20, padx=20, anchor='w')
        
        # Define lighter colors for button backgrounds
        link_colors = {
            "#3b82f6": "#dbeafe",  # blue
            "#10b981": "#d1fae5",  # green
            "#ef4444": "#fee2e2"   # red
        }
        
        links = [
            ("📅 Register for Events", "#3b82f6", self.show_events),
            ("👤 Update Profile", "#10b981", self.show_profile),
            ("💬 Submit Feedback", "#ef4444", self.show_feedback)
        ]
        
        for text, color, command in links:
            btn_bg = link_colors.get(color, "#f3f4f6")  # Use lighter color for background
            btn = tk.Button(left, text=text, anchor='w',
                          bg=btn_bg, fg=color, font=('Helvetica', 12),
                          border=0, cursor='hand2', width=20, height=2,
                          command=command)
            btn.pack(pady=5, padx=20, anchor='w')
        
        # Recent activity (right)
        right = tk.Frame(main_content, bg='white', relief='ridge', borderwidth=1)
        right.pack(side='right', fill='both', expand=True)
        
        tk.Label(right, text="Recent Activity", bg='white',
                font=('Helvetica', 16, 'bold'), fg='#1e293b').pack(pady=20, padx=20, anchor='w')
        
        # Get real recent activities
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 'event_registration' as type, CONCAT('Registered for ', e.title) as description, er.registration_date as timestamp
            FROM event_registrations er
            JOIN events e ON er.event_id = e.id
            WHERE er.user_id = %s
            UNION
            SELECT 'application' as type, CONCAT('Applied for ', o.title) as description, oa.application_date as timestamp
            FROM opportunity_applications oa
            JOIN opportunities o ON oa.opportunity_id = o.id
            WHERE oa.user_id = %s
            UNION
            SELECT 'feedback' as type, CONCAT('Submitted feedback: ', f.subject) as description, f.created_at as timestamp
            FROM feedback f
            WHERE f.user_id = %s
            ORDER BY timestamp DESC
            LIMIT 5
        """, (user['id'], user['id'], user['id']))
        
        activities = cursor.fetchall()
        cursor.close()
        
        if activities:
            for act in activities:
                tk.Label(right, text=f"• {act['description']}", bg='white',
                        font=('Helvetica', 11), fg='#475569', anchor='w').pack(padx=20, pady=8, anchor='w')
        else:
            tk.Label(right, text="• No recent activity", bg='white',
                    font=('Helvetica', 11), fg='#475569', anchor='w').pack(padx=20, pady=8, anchor='w')
    
    def show_qr(self):
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Create QR code
        user_id = self.app.user['id']
        qr_data = f"SK-YOUTH-{user_id:06d}"
        
        qr = qrcode.make(qr_data)
        
        # Convert to PhotoImage
        img = ImageTk.PhotoImage(qr)
        
        # Display
        center = tk.Frame(self.content, bg='#f8fafc')
        center.pack(expand=True)
        
        tk.Label(center, text="Your QR Code", bg='#f8fafc',
                font=('Helvetica', 24, 'bold')).pack(pady=20)
        
        qr_label = tk.Label(center, image=img, bg='#f8fafc')
        qr_label.image = img
        qr_label.pack(pady=10)
        
        tk.Label(center, text=qr_data, bg='#f8fafc',
                font=('Helvetica', 16, 'bold')).pack(pady=10)
        
        tk.Label(center, text="Show this code for attendance", bg='#f8fafc',
                font=('Helvetica', 12), fg='#64748b').pack()
        
        # Add download button
        def download_qr():
            try:
                # Save QR code to file
                qr.save(f"qr_code_{user_id}.png")
                messagebox.showinfo("Success", f"QR code saved as qr_code_{user_id}.png")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {e}")
        
        tk.Button(center, text="Download QR Code", command=download_qr,
                 bg='#4f46e5', fg='white', font=('Helvetica', 12),
                 cursor='hand2', padx=20, pady=10).pack(pady=20)
    
    def show_events(self):
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="Events", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        # Search frame
        search_frame = tk.Frame(header, bg='white')
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Search:", bg='white',
                font=('Helvetica', 11)).pack(side='left')
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=25,
                               font=('Helvetica', 11))
        search_entry.pack(side='left', padx=5)
        
        # Get events from database
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM events WHERE status IN ('upcoming', 'ongoing') ORDER BY event_date ASC")
        events = cursor.fetchall()
        cursor.close()
        
        # Display events in scrollable container
        container = tk.Frame(self.content, bg='#f8fafc', padx=30)
        container.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(container, bg='#f8fafc', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f8fafc')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        def load_events():
            # Clear existing cards
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            search_text = search_var.get().lower()
            
            if not events:
                tk.Label(self.scrollable_frame, text="No upcoming events", bg='#f8fafc',
                        font=('Helvetica', 14)).pack(pady=50)
                return
            
            filtered_events = []
            for event in events:
                if (not search_text or 
                    search_text in event['title'].lower() or 
                    search_text in event['location'].lower() or
                    search_text in event['event_type'].lower()):
                    filtered_events.append(event)
            
            if not filtered_events:
                tk.Label(self.scrollable_frame, text="No events match your search", bg='#f8fafc',
                        font=('Helvetica', 14)).pack(pady=50)
            else:
                for event in filtered_events:
                    self.create_event_card(event)
        
        search_entry.bind('<KeyRelease>', lambda e: load_events())
        
        load_events()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_event_card(self, event):
        # Colors based on status
        status_colors = {
            'upcoming': ('#3b82f6', '#dbeafe'),
            'ongoing': ('#10b981', '#d1fae5'),
            'completed': ('#6b7280', '#f3f4f6'),
            'cancelled': ('#ef4444', '#fee2e2')
        }
        color, bg_color = status_colors.get(event['status'], ('#6b7280', '#f3f4f6'))
        
        # Card frame
        card = tk.Frame(self.scrollable_frame, bg='white', relief='ridge', borderwidth=1)
        card.pack(fill='x', pady=8, padx=5)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=15)
        inner.pack(fill='x')
        
        # Top row
        top_row = tk.Frame(inner, bg='white')
        top_row.pack(fill='x', pady=(0, 10))
        
        tk.Label(top_row, text=event['title'], bg='white',
                font=('Helvetica', 16, 'bold'), fg='#1e293b').pack(side='left')
        
        # Status badge
        status_frame = tk.Frame(top_row, bg=bg_color)
        status_frame.pack(side='right', padx=5)
        tk.Label(status_frame, text=event['status'].upper(), bg=bg_color, fg=color,
                font=('Helvetica', 9, 'bold'), padx=10, pady=3).pack()
        
        # Event details
        details = tk.Frame(inner, bg='white')
        details.pack(fill='x', pady=(0, 15))
        
        # Date and time
        date_str = f"📅 {event['event_date']}  🕒 {event['event_time']}"
        tk.Label(details, text=date_str, bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left', padx=(0, 20))
        
        # Location
        tk.Label(details, text=f"📍 {event['location']}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left', padx=(0, 20))
        
        # Type
        tk.Label(details, text=f"🏷️ {event['event_type']}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left')
        
        # Description preview
        if event['description']:
            desc_preview = event['description'][:100] + "..." if len(event['description']) > 100 else event['description']
            tk.Label(inner, text=desc_preview, bg='white',
                    font=('Helvetica', 11), fg='#4b5563', wraplength=600,
                    justify='left').pack(anchor='w', pady=(0, 15))
        
        # Check if already registered
        cursor = self.app.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM event_registrations WHERE event_id = %s AND user_id = %s", 
                      (event['id'], self.app.user['id']))
        is_registered = cursor.fetchone()[0] > 0
        cursor.close()
        
        # Register button with improved colors
        btn_text = "✅ Already Registered" if is_registered else "Register Now"
        btn_state = 'disabled' if is_registered else 'normal'
        # Modern colors: Purple for active, muted gray for disabled with clear text
        btn_bg = '#9ca3af' if is_registered else '#7c3aed'  # Lighter gray for disabled, vibrant purple for active
        btn_fg = '#f9fafb' if is_registered else 'white'  # Light gray text on disabled, white on active
        
        def register_event():
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    INSERT INTO event_registrations (event_id, user_id, attendance_status) 
                    VALUES (%s, %s, 'registered')
                """, (event['id'], self.app.user['id']))
                self.app.db.commit()
                messagebox.showinfo("Success", f"Successfully registered for {event['title']}!")
                # Refresh the view
                self.show_events()
            except Exception as e:
                if "Duplicate" in str(e) or "duplicate" in str(e):
                    messagebox.showwarning("Already Registered", "You are already registered for this event.")
                else:
                    messagebox.showerror("Error", f"Registration failed: {e}")
            finally:
                if 'cursor' in locals():
                    cursor.close()
        
        tk.Button(inner, text=btn_text, bg=btn_bg, fg=btn_fg,
                 font=('Helvetica', 11, 'bold' if not is_registered else 'normal'),
                 cursor='hand2' if not is_registered else 'arrow',
                 state=btn_state, command=register_event,
                 activebackground='#6d28d9' if not is_registered else btn_bg,
                 activeforeground='white' if not is_registered else btn_fg).pack(anchor='e')
    
    def show_opportunities(self):
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="Opportunities", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        # Search frame
        search_frame = tk.Frame(header, bg='white')
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Search:", bg='white',
                font=('Helvetica', 11)).pack(side='left')
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=25,
                               font=('Helvetica', 11))
        search_entry.pack(side='left', padx=5)
        
        # Type filter
        type_filter = ttk.Combobox(search_frame, values=['All', 'Job', 'Volunteer', 'Internship', 'Training'],
                                  width=12, state='readonly')
        type_filter.set('All')
        type_filter.pack(side='left', padx=5)
        
        # Get opportunities from database
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM opportunities WHERE status = 'open' ORDER BY created_at DESC")
        opportunities = cursor.fetchall()
        cursor.close()
        
        # Display opportunities in scrollable container
        container = tk.Frame(self.content, bg='#f8fafc', padx=30)
        container.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(container, bg='#f8fafc', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f8fafc')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        def load_opportunities():
            # Clear existing cards
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            search_text = search_var.get().lower()
            selected_type = type_filter.get().lower()
            
            if not opportunities:
                tk.Label(self.scrollable_frame, text="No open opportunities", bg='#f8fafc',
                        font=('Helvetica', 14)).pack(pady=50)
                return
            
            filtered_opps = []
            for opp in opportunities:
                matches_search = (not search_text or 
                                search_text in opp['title'].lower() or 
                                search_text in opp['location'].lower())
                
                matches_type = (selected_type == 'all' or 
                               opp['type'].lower() == selected_type)
                
                if matches_search and matches_type:
                    filtered_opps.append(opp)
            
            if not filtered_opps:
                tk.Label(self.scrollable_frame, text="No opportunities match your search", bg='#f8fafc',
                        font=('Helvetica', 14)).pack(pady=50)
            else:
                for opp in filtered_opps:
                    self.create_opportunity_card(opp)
        
        search_entry.bind('<KeyRelease>', lambda e: load_opportunities())
        type_filter.bind('<<ComboboxSelected>>', lambda e: load_opportunities())
        
        load_opportunities()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_opportunity_card(self, opportunity):
        # Type colors
        type_colors = {
            'Job': ('#ef4444', '#fee2e2'),
            'Volunteer': ('#10b981', '#d1fae5'),
            'Internship': ('#f59e0b', '#fef3c7'),
            'Training': ('#3b82f6', '#dbeafe')
        }
        color, bg_color = type_colors.get(opportunity['type'], ('#6b7280', '#f3f4f6'))
        
        card = tk.Frame(self.scrollable_frame, bg='white', relief='ridge', borderwidth=1)
        card.pack(fill='x', pady=10)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=15)
        inner.pack(fill='x')
        
        # Type badge
        type_frame = tk.Frame(inner, bg=bg_color)
        type_frame.pack(anchor='w', pady=(0, 10))
        tk.Label(type_frame, text=opportunity['type'], bg=bg_color, fg=color,
                font=('Helvetica', 10, 'bold'), padx=10, pady=3).pack()
        
        # Title
        tk.Label(inner, text=opportunity['title'], bg='white',
                font=('Helvetica', 16, 'bold'), fg='#1e293b').pack(anchor='w')
        
        # Details
        details_frame = tk.Frame(inner, bg='white')
        details_frame.pack(anchor='w', pady=5)
        
        details = [
            f"📍 {opportunity['location']}",
            f"💰 {opportunity['compensation'] or 'Not specified'}",
            f"⏰ {opportunity['commitment'] or 'Flexible'}"
        ]
        
        for detail in details:
            tk.Label(details_frame, text=detail, bg='white',
                    font=('Helvetica', 11), fg='#64748b').pack(side='left', padx=(0, 15))
        
        # Deadline
        if opportunity['deadline']:
            deadline_date = opportunity['deadline']
            days_left = (deadline_date - datetime.now().date()).days
            deadline_color = '#ef4444' if days_left <= 3 else '#f59e0b' if days_left <= 7 else '#10b981'
            tk.Label(inner, text=f"📅 Deadline: {deadline_date} ({days_left} days left)", bg='white',
                    font=('Helvetica', 11, 'bold'), fg=deadline_color).pack(anchor='w', pady=(5, 0))
        
        # Description preview
        if opportunity['description']:
            desc_preview = opportunity['description'][:150] + "..." if len(opportunity['description']) > 150 else opportunity['description']
            tk.Label(inner, text=desc_preview, bg='white',
                    font=('Helvetica', 11), fg='#4b5563', wraplength=600,
                    justify='left').pack(anchor='w', pady=(10, 0))
        
        # Check if already applied
        cursor = self.app.db.cursor()
        cursor.execute("SELECT COUNT(*) FROM opportunity_applications WHERE opportunity_id = %s AND user_id = %s", 
                      (opportunity['id'], self.app.user['id']))
        already_applied = cursor.fetchone()[0] > 0
        cursor.close()
        
        # Apply button with improved colors
        btn_text = "✅ Already Applied" if already_applied else "Apply Now"
        btn_state = 'disabled' if already_applied else 'normal'
        # Modern gradient-inspired colors: Teal for active, soft gray for disabled
        btn_bg = '#9ca3af' if already_applied else '#0d9488'  # Teal for active, light gray for disabled
        btn_fg = '#f9fafb' if already_applied else 'white'   # Light gray text on disabled, white on active
        
        def apply_opportunity():
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    INSERT INTO opportunity_applications (opportunity_id, user_id, status) 
                    VALUES (%s, %s, 'pending')
                """, (opportunity['id'], self.app.user['id']))
                self.app.db.commit()
                messagebox.showinfo("Success", f"Application submitted for {opportunity['title']}!")
                # Refresh the view
                self.show_opportunities()
            except Exception as e:
                if "Duplicate" in str(e) or "duplicate" in str(e):
                    messagebox.showwarning("Already Applied", "You have already applied for this opportunity.")
                else:
                    messagebox.showerror("Error", f"Application failed: {e}")
            finally:
                if 'cursor' in locals():
                    cursor.close()
        
        tk.Button(inner, text=btn_text, bg=btn_bg, fg=btn_fg,
                 font=('Helvetica', 11, 'bold' if not already_applied else 'normal'),
                 cursor='hand2' if not already_applied else 'arrow',
                 state=btn_state, command=apply_opportunity,
                 activebackground='#0f766e' if not already_applied else btn_bg,
                 activeforeground='white' if not already_applied else btn_fg).pack(anchor='e', pady=(10, 0))
    
    def show_profile(self):
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="My Profile", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        # Edit button
        tk.Button(header, text="✏️ Edit Profile", command=self.edit_profile,
                 bg='#4f46e5', fg='white', font=('Helvetica', 11, 'bold'),
                 cursor='hand2', padx=15, pady=5,
                 activebackground='#4338ca',
                 activeforeground='white').pack(side='right')
        
        # Profile form
        form_frame = tk.Frame(self.content, bg='white', padx=30)
        form_frame.pack(fill='both', expand=True)
        
        user = self.app.user
        
        # Get full user details
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user['id'],))
        full_user = cursor.fetchone()
        cursor.close()
        
        # Create scrollable form
        canvas = tk.Canvas(form_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(form_frame, orient='vertical', command=canvas.yview)
        scrollable_form = tk.Frame(canvas, bg='white')
        
        scrollable_form.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        fields = [
            ("Name:", full_user['name']),
            ("Email:", full_user['email']),
            ("Youth ID:", full_user['youth_id'] or 'Not assigned'),
            ("Phone:", full_user['phone'] or 'Not provided'),
            ("Barangay:", full_user['barangay'] or 'Not provided'),
            ("Address:", full_user['address'] or 'Not provided'),
            ("Birthdate:", str(full_user['birthdate']) if full_user['birthdate'] else 'Not provided'),
            ("Gender:", full_user['gender'] or 'Not specified'),
            ("Status:", full_user['status'].title()),
            ("Member Since:", full_user['created_at'].strftime('%B %d, %Y'))
        ]
        
        for i, (label, value) in enumerate(fields):
            row_frame = tk.Frame(scrollable_form, bg='white')
            row_frame.pack(fill='x', pady=5)
            
            tk.Label(row_frame, text=label, bg='white', font=('Helvetica', 11, 'bold'),
                    width=15, anchor='w').pack(side='left', padx=(0, 10))
            tk.Label(row_frame, text=value, bg='white', font=('Helvetica', 11),
                    anchor='w').pack(side='left')
        
        # Statistics section
        stats_frame = tk.Frame(scrollable_form, bg='#f8fafc', relief='ridge', borderwidth=1)
        stats_frame.pack(fill='x', pady=20)
        
        tk.Label(stats_frame, text="📊 Your Statistics", bg='#f8fafc',
                font=('Helvetica', 14, 'bold'), fg='#1e293b').pack(pady=10)
        
        # Get user statistics
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT er.event_id) as events_attended,
                COALESCE(SUM(er.hours_credited), 0) as total_hours,
                (SELECT COUNT(*) FROM opportunity_applications WHERE user_id = %s) as applications,
                (SELECT COUNT(*) FROM feedback WHERE user_id = %s) as feedback_count
            FROM event_registrations er
            WHERE er.user_id = %s AND er.attendance_status = 'attended'
        """, (user['id'], user['id'], user['id']))
        
        stats = cursor.fetchone()
        cursor.close()
        
        stats_data = [
            ("Events Attended", stats['events_attended'] or 0, "#3b82f6"),
            ("Volunteer Hours", f"{stats['total_hours'] or 0:.1f}", "#10b981"),
            ("Applications", stats['applications'] or 0, "#f59e0b"),
            ("Feedback Submitted", stats['feedback_count'] or 0, "#ec4899")
        ]
        
        stats_grid = tk.Frame(stats_frame, bg='#f8fafc')
        stats_grid.pack(pady=10, padx=20)
        
        # Define lighter colors for stat card backgrounds
        stat_bg_colors = {
            "#3b82f6": "#dbeafe",  # blue
            "#10b981": "#d1fae5",  # green  
            "#f59e0b": "#fef3c7",  # yellow
            "#ec4899": "#fce7f3"   # pink
        }
        
        for i, (title, value, color) in enumerate(stats_data):
            row, col = divmod(i, 2)
            
            if col == 0:
                stats_grid.columnconfigure(0, weight=1)
            if col == 1:
                stats_grid.columnconfigure(1, weight=1)
            
            stat_card = tk.Frame(stats_grid, bg='white', relief='ridge', borderwidth=1)
            stat_card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            bg_color = stat_bg_colors.get(color, "#f3f4f6")
            inner = tk.Frame(stat_card, bg=bg_color, padx=15, pady=15)
            inner.pack(fill='both', expand=True)
            
            tk.Label(inner, text=str(value), bg=bg_color, fg=color,
                    font=('Helvetica', 20, 'bold')).pack()
            tk.Label(inner, text=title, bg=bg_color, fg='#64748b',
                    font=('Helvetica', 10)).pack()
        
        # Awards section
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM awards WHERE user_id = %s ORDER BY award_date DESC", (user['id'],))
        awards = cursor.fetchall()
        cursor.close()
        
        if awards:
            awards_frame = tk.Frame(scrollable_form, bg='#f8fafc', relief='ridge', borderwidth=1)
            awards_frame.pack(fill='x', pady=20)
            
            tk.Label(awards_frame, text="🏆 Your Awards", bg='#f8fafc',
                    font=('Helvetica', 14, 'bold'), fg='#1e293b').pack(pady=10)
            
            for award in awards:
                award_frame = tk.Frame(awards_frame, bg='white')
                award_frame.pack(fill='x', padx=20, pady=5)
                
                tk.Label(award_frame, text=f"• {award['award_name']}", bg='white',
                        font=('Helvetica', 11, 'bold'), anchor='w').pack(side='left')
                tk.Label(award_frame, text=f"({award['award_date']})", bg='white',
                        font=('Helvetica', 10), fg='#64748b').pack(side='right')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def edit_profile(self):
        win = tk.Toplevel(self.root)
        win.title("Edit Profile")
        win.geometry("500x600")
        win.configure(bg='white')
        
        # Center window
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (500 // 2)
        y = (win.winfo_screenheight() // 2) - (600 // 2)
        win.geometry(f'500x600+{x}+{y}')
        
        tk.Label(win, text="Edit Profile", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        # Create scrollable form
        main_frame = tk.Frame(win, bg='white')
        main_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        form = tk.Frame(canvas, bg='white')
        
        form.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=40)
        scrollbar.pack(side="right", fill="y")
        
        # Get current user data
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (self.app.user['id'],))
        user_data = cursor.fetchone()
        cursor.close()
        
        fields = []
        
        # Name
        tk.Label(form, text="Full Name*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(10, 5))
        name_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        name_entry.pack(fill='x', pady=(0, 10))
        name_entry.insert(0, user_data['name'])
        fields.append(('name', name_entry))
        
        # Phone
        tk.Label(form, text="Phone:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        phone_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        phone_entry.pack(fill='x', pady=(0, 10))
        phone_entry.insert(0, user_data['phone'] or '')
        fields.append(('phone', phone_entry))
        
        # Address
        tk.Label(form, text="Address:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        address_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        address_entry.pack(fill='x', pady=(0, 10))
        address_entry.insert(0, user_data['address'] or '')
        fields.append(('address', address_entry))
        
        # Barangay
        tk.Label(form, text="Barangay:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        barangay_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        barangay_entry.pack(fill='x', pady=(0, 10))
        barangay_entry.insert(0, user_data['barangay'] or '')
        fields.append(('barangay', barangay_entry))
        
        # Birthdate
        tk.Label(form, text="Birthdate (YYYY-MM-DD):", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        birthdate_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        birthdate_entry.pack(fill='x', pady=(0, 10))
        if user_data['birthdate']:
            birthdate_entry.insert(0, str(user_data['birthdate']))
        fields.append(('birthdate', birthdate_entry))
        
        # Gender
        tk.Label(form, text="Gender:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        gender_var = tk.StringVar(value=user_data['gender'] or '')
        gender_frame = tk.Frame(form, bg='white')
        gender_frame.pack(fill='x', pady=(0, 10))
        
        genders = ['Male', 'Female', 'Other', 'Prefer not to say']
        for gender in genders:
            rb = tk.Radiobutton(gender_frame, text=gender, variable=gender_var,
                               value=gender, bg='white')
            rb.pack(side='left', padx=(0, 10))
        
        def save_profile():
            data = {}
            for field_name, entry in fields:
                data[field_name] = entry.get().strip()
            data['gender'] = gender_var.get()
            
            # Validate birthdate format if provided
            if data['birthdate']:
                try:
                    datetime.strptime(data['birthdate'], '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Error", "Birthdate must be in YYYY-MM-DD format")
                    return
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET name = %s, phone = %s, address = %s, barangay = %s, 
                        birthdate = %s, gender = %s
                    WHERE id = %s
                """, (data['name'], data['phone'] or None, data['address'] or None, 
                      data['barangay'] or None, data['birthdate'] or None, 
                      data['gender'] or None, self.app.user['id']))
                
                self.app.db.commit()
                
                # Refresh user data
                cursor.execute("SELECT * FROM users WHERE id = %s", (self.app.user['id'],))
                self.app.user = cursor.fetchone()
                cursor.close()
                
                messagebox.showinfo("Success", "Profile updated successfully!")
                win.destroy()
                self.show_profile()  # Refresh profile view
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {e}")
        
        # Save button frame
        btn_frame = tk.Frame(win, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Save Changes", command=save_profile,
                 bg='#10b981', fg='white', font=('Helvetica', 11, 'bold'),
                 width=20, pady=10, cursor='hand2',
                 activebackground='#0d9c6f',
                 activeforeground='white').pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Cancel", command=win.destroy,
                 bg='#6b7280', fg='white', font=('Helvetica', 11),
                 width=10, pady=10, cursor='hand2',
                 activebackground='#4b5563',
                 activeforeground='white').pack(side='left', padx=5)
    
    def show_feedback(self):
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="Feedback", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        # Create feedback button
        tk.Button(header, text="➕ Submit New Feedback", 
                 command=self.submit_feedback,
                 bg='#4f46e5', fg='white', font=('Helvetica', 11, 'bold'),
                 cursor='hand2', padx=15, pady=5,
                 activebackground='#4338ca',
                 activeforeground='white').pack(side='right')
        
        # Feedback history in scrollable container
        container = tk.Frame(self.content, bg='#f8fafc', padx=30)
        container.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(container, bg='#f8fafc', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f8fafc')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get user's feedback history
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM feedback 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (self.app.user['id'],))
        
        feedback_list = cursor.fetchall()
        cursor.close()
        
        if not feedback_list:
            tk.Label(self.scrollable_frame, text="No feedback submitted yet", bg='#f8fafc',
                    font=('Helvetica', 14)).pack(pady=50)
        else:
            for feedback in feedback_list:
                self.create_feedback_card(feedback)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_feedback_card(self, feedback):
        status_colors = {
            'pending': ('#f59e0b', '#fef3c7'),
            'in progress': ('#3b82f6', '#dbeafe'),
            'resolved': ('#10b981', '#d1fae5')
        }
        color, bg_color = status_colors.get(feedback['status'], ('#6b7280', '#f3f4f6'))
        
        card = tk.Frame(self.scrollable_frame, bg='white', relief='ridge', borderwidth=1)
        card.pack(fill='x', pady=5)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=15)
        inner.pack(fill='x')
        
        # Top row
        top_row = tk.Frame(inner, bg='white')
        top_row.pack(fill='x', pady=(0, 10))
        
        tk.Label(top_row, text=feedback['subject'], bg='white',
                font=('Helvetica', 14, 'bold'), fg='#1e293b').pack(side='left')
        
        # Status badge
        status_frame = tk.Frame(top_row, bg=bg_color)
        status_frame.pack(side='right', padx=5)
        tk.Label(status_frame, text=feedback['status'].upper(), bg=bg_color, fg=color,
                font=('Helvetica', 9, 'bold'), padx=8, pady=2).pack()
        
        # Date and type
        info_frame = tk.Frame(inner, bg='white')
        info_frame.pack(anchor='w', pady=(0, 10))
        
        date_str = feedback['created_at'].strftime('%b %d, %Y')
        tk.Label(info_frame, text=f"📅 {date_str}", bg='white',
                font=('Helvetica', 10), fg='#64748b').pack(side='left', padx=(0, 15))
        
        tk.Label(info_frame, text=f"🏷️ {feedback['feedback_type']}", bg='white',
                font=('Helvetica', 10), fg='#64748b').pack(side='left')
        
        # Message preview
        message_preview = feedback['message'][:100] + "..." if len(feedback['message']) > 100 else feedback['message']
        tk.Label(inner, text=message_preview, bg='white',
                font=('Helvetica', 11), fg='#4b5563', wraplength=600,
                justify='left').pack(anchor='w', pady=(0, 10))
        
        # Admin reply if exists
        if feedback['admin_reply']:
            reply_preview = feedback['admin_reply'][:100] + "..." if len(feedback['admin_reply']) > 100 else feedback['admin_reply']
            reply_frame = tk.Frame(inner, bg='#f0f9ff', relief='solid', borderwidth=1)
            reply_frame.pack(fill='x', pady=(0, 5))
            
            tk.Label(reply_frame, text=f"📝 Admin Reply: {reply_preview}", bg='#f0f9ff',
                    font=('Helvetica', 10), fg='#3b82f6', wraplength=580,
                    justify='left', padx=10, pady=8).pack(anchor='w')
        
        # View button
        def view_feedback():
            self.view_feedback_details(feedback)
        
        tk.Button(inner, text="View Details", command=view_feedback,
                 bg='#4f46e5', fg='white', font=('Helvetica', 10, 'bold'),
                 padx=15, pady=5, cursor='hand2',
                 activebackground='#4338ca',
                 activeforeground='white').pack(anchor='e', pady=(5, 0))
    
    def view_feedback_details(self, feedback):
        win = tk.Toplevel(self.root)
        win.title(f"Feedback: {feedback['subject']}")
        win.geometry("600x500")
        win.configure(bg='white')
        
        # Center window
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (600 // 2)
        y = (win.winfo_screenheight() // 2) - (500 // 2)
        win.geometry(f'600x500+{x}+{y}')
        
        tk.Label(win, text="Feedback Details", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        # Content frame
        content = tk.Frame(win, bg='white', padx=40)
        content.pack(fill='both', expand=True)
        
        # Subject
        tk.Label(content, text="Subject:", bg='white',
                font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        tk.Label(content, text=feedback['subject'], bg='white',
                font=('Helvetica', 14), fg='#1e293b', wraplength=500,
                justify='left').pack(anchor='w', pady=(0, 15))
        
        # Status and type
        info_frame = tk.Frame(content, bg='white')
        info_frame.pack(fill='x', pady=(0, 15))
        
        status_colors = {
            'pending': ('#f59e0b', '#fef3c7'),
            'in progress': ('#3b82f6', '#dbeafe'),
            'resolved': ('#10b981', '#d1fae5')
        }
        color, bg_color = status_colors.get(feedback['status'], ('#6b7280', '#f3f4f6'))
        
        status_frame = tk.Frame(info_frame, bg=bg_color)
        status_frame.pack(side='left', padx=(0, 15))
        tk.Label(status_frame, text=f"Status: {feedback['status'].upper()}", bg=bg_color, fg=color,
                font=('Helvetica', 10, 'bold'), padx=10, pady=3).pack()
        
        tk.Label(info_frame, text=f"Type: {feedback['feedback_type']}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left', padx=(0, 15))
        
        date_str = feedback['created_at'].strftime('%B %d, %Y at %I:%M %p')
        tk.Label(info_frame, text=f"Date: {date_str}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left')
        
        # Message
        tk.Label(content, text="Your Message:", bg='white',
                font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        
        message_frame = tk.Frame(content, bg='#f8fafc', relief='sunken', borderwidth=1)
        message_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        message_text = tk.Text(message_frame, wrap='word', font=('Helvetica', 11),
                              bg='#f8fafc', relief='flat', height=8)
        message_text.insert('1.0', feedback['message'])
        message_text.config(state='disabled')
        
        scrollbar = tk.Scrollbar(message_frame, orient='vertical', command=message_text.yview)
        message_text.configure(yscrollcommand=scrollbar.set)
        
        message_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Admin reply if exists
        if feedback['admin_reply']:
            tk.Label(content, text="Admin Reply:", bg='white',
                    font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(10, 5))
            
            reply_frame = tk.Frame(content, bg='#e0f2fe', relief='sunken', borderwidth=1)
            reply_frame.pack(fill='x', pady=(0, 20))
            
            reply_text = tk.Text(reply_frame, wrap='word', font=('Helvetica', 11),
                                bg='#e0f2fe', relief='flat', height=4)
            reply_text.insert('1.0', feedback['admin_reply'])
            reply_text.config(state='disabled')
            reply_text.pack(fill='x', padx=5, pady=5)
        
        tk.Button(win, text="Close", command=win.destroy,
                 bg='#6b7280', fg='white', font=('Helvetica', 11, 'bold'),
                 width=20, pady=10, cursor='hand2',
                 activebackground='#4b5563',
                 activeforeground='white').pack(pady=20)
    
    def submit_feedback(self):
        win = tk.Toplevel(self.root)
        win.title("Submit Feedback")
        win.geometry("500x500")
        win.configure(bg='white')
        
        # Center window
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (500 // 2)
        y = (win.winfo_screenheight() // 2) - (500 // 2)
        win.geometry(f'500x500+{x}+{y}')
        
        tk.Label(win, text="Submit Feedback", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        form = tk.Frame(win, bg='white', padx=40)
        form.pack(fill='both', expand=True)
        
        # Subject
        tk.Label(form, text="Subject*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        subject_entry = tk.Entry(form, width=30, font=('Helvetica', 11))
        subject_entry.pack(fill='x', pady=(0, 15))
        
        # Type
        tk.Label(form, text="Type*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        type_combo = ttk.Combobox(form, values=['General', 'Technical', 'Suggestion', 'Complaint', 'Appreciation'], 
                                 width=28, state='readonly')
        type_combo.pack(fill='x', pady=(0, 15))
        type_combo.set('General')
        
        # Message
        tk.Label(form, text="Message*:", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        message_text = tk.Text(form, width=30, height=8, font=('Helvetica', 11))
        message_text.pack(fill='x', pady=(0, 20))
        
        def submit():
            subject = subject_entry.get().strip()
            ftype = type_combo.get().lower()
            message = message_text.get("1.0", tk.END).strip()
            
            if not all([subject, message]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    INSERT INTO feedback (user_id, subject, message, feedback_type, status)
                    VALUES (%s, %s, %s, %s, 'pending')
                """, (self.app.user['id'], subject, message, ftype))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "Feedback submitted successfully!")
                win.destroy()
                self.show_feedback()  # Refresh feedback view
            except Exception as e:
                messagebox.showerror("Error", f"Failed to submit feedback: {e}")
            finally:
                cursor.close()
        
        tk.Button(win, text="Submit Feedback", command=submit,
                 bg='#4f46e5', fg='white', font=('Helvetica', 11, 'bold'),
                 width=20, pady=10, cursor='hand2',
                 activebackground='#4338ca',
                 activeforeground='white').pack(pady=20)
        
        tk.Button(win, text="Cancel", command=win.destroy,
                 bg='#6b7280', fg='white', font=('Helvetica', 11),
                 width=10, pady=10, cursor='hand2',
                 activebackground='#4b5563',
                 activeforeground='white').pack(pady=(0, 20))