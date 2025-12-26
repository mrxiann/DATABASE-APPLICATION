import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from tkinter import filedialog
from ui_utils import ModernButton, ModernCard, ModernEntry, create_modern_combobox
from ui_utils import create_stat_card

class EventManagement:
    def __init__(self, app):
        self.app = app
        self.app.clear_window()
        
        self.main = tk.Frame(self.app.root, bg='#f8fafc')
        self.main.pack(fill='both', expand=True)
        
        self.create_sidebar()
        
        self.content = tk.Frame(self.main, bg='#f8fafc')
        self.content.pack(side='right', fill='both', expand=True)
        
        self.show_events()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='white', width=280)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Logo/Header
        header = tk.Frame(sidebar, bg='#10b981', height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="Event Management", bg='#10b981', fg='white',
                font=('Segoe UI', 18, 'bold')).pack(expand=True, pady=(30, 5))
        
        # Back button
        back_btn = tk.Label(header, text="← Back to Dashboard", bg='#10b981',
                           fg='#d1fae5', font=('Segoe UI', 10), cursor='hand2')
        back_btn.pack(pady=(0, 20))
        back_btn.bind("<Button-1>", lambda e: self.app.show_admin_dashboard(self.app.user))
        back_btn.bind("<Enter>", lambda e: back_btn.config(fg='white'))
        back_btn.bind("<Leave>", lambda e: back_btn.config(fg='#d1fae5'))
        
        # Navigation Menu
        nav_frame = tk.Frame(sidebar, bg='white')
        nav_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        menu_items = [
            ("📅", "All Events", self.show_events, True),
            ("➕", "Add New Event", self.add_event, False),
            ("📊", "Event Reports", self.show_reports, False),
            ("", "", None, False),  # Separator
            ("📋", "Attendance", lambda: self.app.show_attendance_management(), False)
        ]
        
        for icon, text, command, active in menu_items:
            if text == "":
                tk.Frame(nav_frame, bg='#f1f5f9', height=1).pack(fill='x', pady=15)
            else:
                btn_frame = tk.Frame(nav_frame, bg='white')
                btn_frame.pack(fill='x', pady=2)
                
                btn = tk.Label(btn_frame, text=f"{icon} {text}", bg='white' if not active else '#f0fdf4',
                             fg='#374151' if not active else '#10b981', font=('Segoe UI', 11),
                             cursor='hand2', anchor='w')
                btn.pack(fill='x', padx=10, pady=10)
                
                if command:
                    btn.bind("<Button-1>", lambda e, c=command: c())
                    btn.bind("<Enter>", lambda e, b=btn, active=active: 
                            b.config(bg='#f8fafc') if not active else None)
                    btn.bind("<Leave>", lambda e, b=btn, active=active: 
                            b.config(bg='white' if not active else '#f0fdf4'))
    
    def show_events(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=30)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="📅 Event Management", bg='#f8fafc',
                font=('Segoe UI', 28, 'bold'), fg='#1e293b').pack(side='left')
        
        # Add event button
        add_btn = ModernButton(header_frame, text="➕ Add New Event", 
                              command=self.add_event, width=150, height=38,
                              bg='#10b981', fg='white',
                              font=('Segoe UI', 11, 'bold'), radius=8)
        add_btn.pack(side='right')
        
        # Search and filter
        filter_frame = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=10)
        filter_frame.pack(fill='x')
        
        # Search
        search_container = tk.Frame(filter_frame, bg='#f8fafc')
        search_container.pack(side='left')
        
        tk.Label(search_container, text="Search:", bg='#f8fafc',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ModernEntry(search_container, width=25, font=('Segoe UI', 11),
                                  placeholder="Search events...")
        search_entry.pack(side='left')
        search_entry.entry.bind('<KeyRelease>', lambda e: self.filter_events())
        self.search_entry = search_entry
        
        # Status filter
        filter_container = tk.Frame(filter_frame, bg='#f8fafc')
        filter_container.pack(side='right')
        
        tk.Label(filter_container, text="Filter:", bg='#f8fafc',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left', padx=(0, 10))
        
        self.status_filter = create_modern_combobox(filter_container, 
                                                   ['All', 'Upcoming', 'Ongoing', 'Completed', 'Cancelled'], 
                                                   width=15)
        self.status_filter.pack(side='left')
        self.status_filter.set('All')
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_events())
        
        # Events container
        events_container = ModernCard(self.content, padx=0, pady=0)
        events_container.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Create scrollable canvas
        canvas_frame = tk.Frame(events_container, bg='white')
        canvas_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.load_all_events()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Add mousewheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def load_all_events(self):
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.*, u.name as creator, 
                   (SELECT COUNT(*) FROM event_registrations WHERE event_id = e.id) as registered
            FROM events e
            LEFT JOIN users u ON e.created_by = u.id
            ORDER BY e.event_date DESC
        """)
        self.all_events = cursor.fetchall()
        cursor.close()
        
        self.filter_events()
    
    def filter_events(self):
        # Clear existing cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        search_text = self.search_entry.get().lower()
        status_filter = self.status_filter.get().lower()
        
        filtered_events = []
        for event in self.all_events:
            matches_search = (not search_text or 
                            search_text in event['title'].lower() or 
                            search_text in event['location'].lower() or
                            (event['event_type'] and search_text in event['event_type'].lower()))
            
            matches_status = (status_filter == 'all' or 
                            event['status'].lower() == status_filter)
            
            if matches_search and matches_status:
                filtered_events.append(event)
        
        if not filtered_events:
            no_events_frame = tk.Frame(self.scrollable_frame, bg='white', height=200)
            no_events_frame.pack(fill='both', expand=True)
            
            tk.Label(no_events_frame, text="No events found", bg='white',
                    font=('Segoe UI', 14), fg='#94a3b8').pack(expand=True)
            
            if search_text:
                tk.Label(no_events_frame, text="Try adjusting your search terms", bg='white',
                        font=('Segoe UI', 11), fg='#cbd5e1').pack(pady=10)
        else:
            for event in filtered_events:
                self.create_modern_event_card(event)
        
        # Update canvas scroll region
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def create_modern_event_card(self, event):
        """Create a modern event card"""
        # Status colors
        status_colors = {
            'upcoming': ('#3b82f6', '#dbeafe'),
            'ongoing': ('#10b981', '#d1fae5'),
            'completed': ('#6b7280', '#f3f4f6'),
            'cancelled': ('#ef4444', '#fee2e2')
        }
        color, bg_color = status_colors.get(event['status'], ('#6b7280', '#f3f4f6'))
        
        # Main card
        card = tk.Frame(self.scrollable_frame, bg='white', relief='flat',
                       highlightbackground='#e5e7eb', highlightthickness=1)
        card.pack(fill='x', pady=8, padx=2)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=20)
        inner.pack(fill='x')
        
        # Top row: Title and status
        top_row = tk.Frame(inner, bg='white')
        top_row.pack(fill='x', pady=(0, 15))
        
        # Title
        tk.Label(top_row, text=event['title'], bg='white',
                font=('Segoe UI', 16, 'bold'), fg='#1e293b').pack(side='left')
        
        # Status badge
        status_badge = tk.Frame(top_row, bg=bg_color)
        status_badge.pack(side='right', padx=(10, 0))
        tk.Label(status_badge, text=event['status'].upper(), bg=bg_color, fg=color,
                font=('Segoe UI', 9, 'bold'), padx=12, pady=4).pack()
        
        # Details row
        details_frame = tk.Frame(inner, bg='white')
        details_frame.pack(fill='x', pady=(0, 15))
        
        # Date and time
        date_frame = tk.Frame(details_frame, bg='white')
        date_frame.pack(side='left', padx=(0, 30))
        
        tk.Label(date_frame, text="📅 Date & Time", bg='white',
                font=('Segoe UI', 10), fg='#64748b').pack(anchor='w')
        tk.Label(date_frame, text=f"{event['event_date']} • {event['event_time']}", 
                bg='white', font=('Segoe UI', 11), fg='#374151').pack(anchor='w', pady=2)
        
        # Location
        location_frame = tk.Frame(details_frame, bg='white')
        location_frame.pack(side='left', padx=(0, 30))
        
        tk.Label(location_frame, text="📍 Location", bg='white',
                font=('Segoe UI', 10), fg='#64748b').pack(anchor='w')
        tk.Label(location_frame, text=event['location'] or 'Not specified', 
                bg='white', font=('Segoe UI', 11), fg='#374151').pack(anchor='w', pady=2)
        
        # Type
        type_frame = tk.Frame(details_frame, bg='white')
        type_frame.pack(side='left')
        
        tk.Label(type_frame, text="🏷️ Type", bg='white',
                font=('Segoe UI', 10), fg='#64748b').pack(anchor='w')
        tk.Label(type_frame, text=event['event_type'] or 'Not specified', 
                bg='white', font=('Segoe UI', 11), fg='#374151').pack(anchor='w', pady=2)
        
        # Bottom row: Stats and actions
        bottom_row = tk.Frame(inner, bg='white')
        bottom_row.pack(fill='x')
        
        # Participants info
        participants_frame = tk.Frame(bottom_row, bg='white')
        participants_frame.pack(side='left')
        
        max_participants = event['max_participants'] or 'Unlimited'
        registered = event['registered'] or 0
        tk.Label(participants_frame, 
                text=f"👥 {registered}/{max_participants} registered", 
                bg='white', font=('Segoe UI', 11), fg='#374151').pack(side='left')
        
        creator = event['creator'] or 'Unknown'
        tk.Label(participants_frame, text=f" • Created by: {creator}", 
                bg='white', font=('Segoe UI', 10), fg='#94a3b8').pack(side='left', padx=(10, 0))
        
        # Action buttons
        btn_frame = tk.Frame(bottom_row, bg='white')
        btn_frame.pack(side='right')
        
        if event['status'] in ['upcoming', 'ongoing']:
            edit_btn = ModernButton(btn_frame, text="Edit", 
                                   command=lambda e=event: self.edit_event(e),
                                   width=80, height=32, bg='#f59e0b', fg='white',
                                   font=('Segoe UI', 10), radius=6)
            edit_btn.pack(side='left', padx=(0, 5))
            
            if event['status'] == 'upcoming':
                cancel_btn = ModernButton(btn_frame, text="Cancel", 
                                         command=lambda e=event: self.cancel_event(e),
                                         width=80, height=32, bg='#ef4444', fg='white',
                                         font=('Segoe UI', 10), radius=6)
                cancel_btn.pack(side='left', padx=(0, 5))
            
            if event['status'] == 'ongoing':
                complete_btn = ModernButton(btn_frame, text="Complete", 
                                           command=lambda e=event: self.complete_event(e),
                                           width=90, height=32, bg='#10b981', fg='white',
                                           font=('Segoe UI', 10), radius=6)
                complete_btn.pack(side='left', padx=(0, 5))
        
        view_btn = ModernButton(btn_frame, text="View Report", 
                               command=lambda e=event: self.view_report(e),
                               width=100, height=32, bg='#3b82f6', fg='white',
                               font=('Segoe UI', 10), radius=6)
        view_btn.pack(side='left', padx=(0, 5))
    
    def add_event(self):
        # Create modal window with modern styling
        win = tk.Toplevel(self.app.root)
        win.title("Add New Event")
        win.geometry("500x700")
        win.configure(bg='white')
        win.resizable(False, False)
        
        # Center window
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make window modal
        win.transient(self.app.root)
        win.grab_set()
        
        # Header
        header = tk.Frame(win, bg='#10b981', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="➕ Create New Event", 
                font=('Segoe UI', 18, 'bold'), bg='#10b981', fg='white').pack(expand=True)
        
        close_btn = tk.Label(header, text="✕", font=('Segoe UI', 16), 
                           bg='#10b981', fg='white', cursor='hand2')
        close_btn.place(relx=0.95, rely=0.5, anchor='center')
        close_btn.bind("<Button-1>", lambda e: win.destroy())
        
        # Form container - MODERN FORM STYLING
        form_container = tk.Frame(win, bg='white')
        form_container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Create form with modern entries
        entries = {}
        field_configs = [
            ("Event Title", "title", True),
            ("Date (YYYY-MM-DD)", "date", True),
            ("Time (HH:MM)", "time", True),
            ("Location", "location", True),
            ("Event Type", "type", True),
            ("Max Participants", "max_participants", True),
            ("Description", "description", False)
        ]
        
        for i, (label, key, required) in enumerate(field_configs):
            # Label
            star = " *" if required else ""
            tk.Label(form_container, text=f"{label}{star}", bg='white', 
                    font=('Segoe UI', 11), fg='#475569').grid(row=i*2, column=0, 
                    sticky='w', pady=(15 if i == 0 else 10, 5))
            
            # Input field
            if key == 'type':
                entry = create_modern_combobox(form_container, 
                                              ['Volunteer', 'Seminar', 'Sports', 'Social', 'Training'], 
                                              width=25)
                entry.set('Volunteer')
            elif key == 'description':
                entry = tk.Text(form_container, width=35, height=4, font=('Segoe UI', 11),
                               relief='flat', bg='white', highlightthickness=1,
                               highlightbackground='#cbd5e1', highlightcolor='#4f46e5')
            else:
                placeholder = "2024-12-25" if key == 'date' else "09:00" if key == 'time' else "50" if key == 'max_participants' else ""
                entry = ModernEntry(form_container, width=25, font=('Segoe UI', 11),
                                   placeholder=placeholder)
                if key == 'date':
                    entry.insert(0, "2024-12-25")
                elif key == 'time':
                    entry.insert(0, "09:00")
                elif key == 'max_participants':
                    entry.insert(0, "50")
            
            entry.grid(row=i*2+1, column=0, sticky='ew', pady=(0, 0))
            entries[key] = entry
        
        def save_event():
            # Collect data with modern entry handling
            data = {}
            for key, entry in entries.items():
                if key == 'description':
                    data[key] = entry.get("1.0", tk.END).strip()
                else:
                    data[key] = entry.get() if hasattr(entry, 'get') else entry.get()
            
            # Validation
            required_fields = ['title', 'date', 'time', 'location', 'type', 'max_participants']
            for field in required_fields:
                if not data[field]:
                    messagebox.showerror("Error", f"Please fill all required fields")
                    return
            
            # Save to database
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    INSERT INTO events (title, description, event_date, event_time, location, 
                                      event_type, max_participants, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (data['title'], data['description'], data['date'], data['time'], 
                     data['location'], data['type'], data['max_participants'], self.app.user['id']))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "Event created successfully!")
                win.destroy()
                self.load_all_events()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create event: {e}")
            finally:
                cursor.close()
        
        # Submit button with modern styling
        submit_btn = ModernButton(form_container, text="Publish Event", 
                                 command=save_event, width=200, height=42, 
                                 bg='#10b981', fg='white',
                                 font=('Segoe UI', 12, 'bold'), radius=10)
        submit_btn.grid(row=len(field_configs)*2, column=0, pady=30)
    
    def edit_event(self, event):
        # Create modal window
        win = tk.Toplevel(self.app.root)
        win.title(f"Edit Event: {event['title']}")
        win.geometry("500x700")
        win.configure(bg='white')
        win.resizable(False, False)
        
        # Center window
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make window modal
        win.transient(self.app.root)
        win.grab_set()
        
        # Header
        header = tk.Frame(win, bg='#f59e0b', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="✏️ Edit Event", 
                font=('Segoe UI', 18, 'bold'), bg='#f59e0b', fg='white').pack(expand=True)
        
        close_btn = tk.Label(header, text="✕", font=('Segoe UI', 16), 
                           bg='#f59e0b', fg='white', cursor='hand2')
        close_btn.place(relx=0.95, rely=0.5, anchor='center')
        close_btn.bind("<Button-1>", lambda e: win.destroy())
        
        # Form container
        form_container = tk.Frame(win, bg='white')
        form_container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Create form with pre-filled values
        entries = {}
        field_configs = [
            ("Event Title", "title", True),
            ("Date (YYYY-MM-DD)", "date", True),
            ("Time (HH:MM)", "time", True),
            ("Location", "location", True),
            ("Event Type", "type", True),
            ("Max Participants", "max_participants", True),
            ("Description", "description", False)
        ]
        
        # Map field names to database columns
        field_map = {
            'title': 'title',
            'date': 'event_date',
            'time': 'event_time',
            'location': 'location',
            'type': 'event_type',
            'max_participants': 'max_participants',
            'description': 'description'
        }
        
        for i, (label, key, required) in enumerate(field_configs):
            # Label
            star = " *" if required else ""
            tk.Label(form_container, text=f"{label}{star}", bg='white', 
                    font=('Segoe UI', 11), fg='#475569').grid(row=i*2, column=0, 
                    sticky='w', pady=(15 if i == 0 else 10, 5))
            
            # Input field
            db_column = field_map[key]
            value = event[db_column] if event[db_column] else ""
            
            if key == 'type':
                entry = create_modern_combobox(form_container, 
                                              ['Volunteer', 'Seminar', 'Sports', 'Social', 'Training'], 
                                              width=25)
                entry.set(value if value else 'Volunteer')
            elif key == 'description':
                entry = tk.Text(form_container, width=35, height=4, font=('Segoe UI', 11),
                               relief='flat', bg='white', highlightthickness=1,
                               highlightbackground='#cbd5e1', highlightcolor='#4f46e5')
                if value:
                    entry.insert('1.0', value)
            else:
                entry = ModernEntry(form_container, width=25, font=('Segoe UI', 11))
                if value:
                    entry.insert(0, str(value))
            
            entry.grid(row=i*2+1, column=0, sticky='ew', pady=(0, 0))
            entries[key] = entry
        
        def update_event():
            # Collect data
            data = {}
            for key, entry in entries.items():
                if key == 'description':
                    data[key] = entry.get("1.0", tk.END).strip()
                else:
                    data[key] = entry.get() if hasattr(entry, 'get') else entry.get()
            
            # Validation
            required_fields = ['title', 'date', 'time', 'location', 'type', 'max_participants']
            for field in required_fields:
                if not data[field]:
                    messagebox.showerror("Error", f"Please fill all required fields")
                    return
            
            # Update database
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    UPDATE events 
                    SET title = %s, description = %s, event_date = %s, event_time = %s, 
                        location = %s, event_type = %s, max_participants = %s
                    WHERE id = %s
                """, (data['title'], data['description'], data['date'], data['time'], 
                     data['location'], data['type'], data['max_participants'], event['id']))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "Event updated successfully!")
                win.destroy()
                self.load_all_events()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update event: {e}")
            finally:
                cursor.close()
        
        # Submit button
        submit_btn = ModernButton(form_container, text="Update Event", 
                                 command=update_event, width=200, height=42, 
                                 bg='#f59e0b', fg='white',
                                 font=('Segoe UI', 12, 'bold'), radius=10)
        submit_btn.grid(row=len(field_configs)*2, column=0, pady=30)
    
    def cancel_event(self, event):
        if messagebox.askyesno("Confirm", f"Cancel event '{event['title']}'?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE events SET status = 'cancelled' WHERE id = %s", (event['id'],))
                self.app.db.commit()
                messagebox.showinfo("Success", "Event cancelled")
                self.load_all_events()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel event: {e}")
            finally:
                cursor.close()
    
    def complete_event(self, event):
        if messagebox.askyesno("Confirm", f"Mark event '{event['title']}' as completed?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE events SET status = 'completed' WHERE id = %s", (event['id'],))
                self.app.db.commit()
                messagebox.showinfo("Success", "Event marked as completed")
                self.load_all_events()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update event: {e}")
            finally:
                cursor.close()
    
    def view_report(self, event):
        # Get detailed report
        cursor = self.app.db.cursor(dictionary=True)
        
        # Get registrations
        cursor.execute("""
            SELECT er.*, u.name, u.youth_id, u.email
            FROM event_registrations er
            JOIN users u ON er.user_id = u.id
            WHERE er.event_id = %s
            ORDER BY er.registration_date DESC
        """, (event['id'],))
        
        registrations = cursor.fetchall()
        
        # Get attendance stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_registered,
                SUM(CASE WHEN attendance_status = 'attended' THEN 1 ELSE 0 END) as attended,
                SUM(CASE WHEN attendance_status = 'no_show' THEN 1 ELSE 0 END) as no_show,
                COALESCE(SUM(hours_credited), 0) as total_hours
            FROM event_registrations 
            WHERE event_id = %s
        """, (event['id'],))
        
        stats = cursor.fetchone()
        cursor.close()
        
        # Create report window
        win = tk.Toplevel(self.app.root)
        win.title(f"Report: {event['title']}")
        win.geometry("800x600")
        win.configure(bg='white')
        
        # Header
        header = tk.Frame(win, bg='#3b82f6', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="📊 Event Report", 
                font=('Segoe UI', 18, 'bold'), bg='#3b82f6', fg='white').pack(expand=True)
        
        # Content
        content = tk.Frame(win, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Event info
        tk.Label(content, text=event['title'], bg='white',
                font=('Segoe UI', 16, 'bold'), fg='#1e293b').pack(anchor='w', pady=(0, 10))
        
        info_frame = tk.Frame(content, bg='#f8fafc', relief='flat',
                            highlightbackground='#e5e7eb', highlightthickness=1)
        info_frame.pack(fill='x', pady=(0, 20))
        
        info_inner = tk.Frame(info_frame, bg='#f8fafc', padx=15, pady=15)
        info_inner.pack(fill='x')
        
        tk.Label(info_inner, text=f"Date: {event['event_date']} • Time: {event['event_time']}", 
                bg='#f8fafc', font=('Segoe UI', 11), fg='#64748b').pack(anchor='w', pady=2)
        tk.Label(info_inner, text=f"Location: {event['location']}", 
                bg='#f8fafc', font=('Segoe UI', 11), fg='#64748b').pack(anchor='w', pady=2)
        tk.Label(info_inner, text=f"Type: {event['event_type']}", 
                bg='#f8fafc', font=('Segoe UI', 11), fg='#64748b').pack(anchor='w', pady=2)
        
        # Stats cards
        stats_frame = tk.Frame(content, bg='white')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stat_cards = [
            ("Total Registered", stats['total_registered'] or 0, "#3b82f6"),
            ("Attended", stats['attended'] or 0, "#10b981"),
            ("No Show", stats['no_show'] or 0, "#ef4444"),
            ("Total Hours", f"{stats['total_hours'] or 0:.1f}", "#f59e0b")
        ]
        
        for i, (title, value, color) in enumerate(stat_cards):
            card = tk.Frame(stats_frame, bg='white', relief='flat',
                           highlightbackground='#e5e7eb', highlightthickness=1)
            card.pack(side='left', padx=(0, 10) if i < 3 else (0, 0), fill='both', expand=True)
            
            inner = tk.Frame(card, bg='white', padx=15, pady=15)
            inner.pack(fill='both', expand=True)
            
            tk.Label(inner, text=str(value), bg='white', font=('Segoe UI', 20, 'bold'), 
                    fg=color).pack()
            tk.Label(inner, text=title, bg='white', font=('Segoe UI', 10), 
                    fg='#64748b').pack()
        
        # Registrations table
        tk.Label(content, text="Registrations", bg='white',
                font=('Segoe UI', 14, 'bold'), fg='#1e293b').pack(anchor='w', pady=(0, 10))
        
        if registrations:
            # Create a simple list for registrations
            for reg in registrations[:10]:  # Show first 10
                reg_frame = tk.Frame(content, bg='#f8fafc', relief='flat',
                                   highlightbackground='#e5e7eb', highlightthickness=1)
                reg_frame.pack(fill='x', pady=2)
                
                inner = tk.Frame(reg_frame, bg='#f8fafc', padx=10, pady=8)
                inner.pack(fill='x')
                
                tk.Label(inner, text=reg['name'], bg='#f8fafc',
                        font=('Segoe UI', 11), fg='#374151').pack(side='left')
                
                status_color = '#10b981' if reg['attendance_status'] == 'attended' else '#ef4444' if reg['attendance_status'] == 'no_show' else '#6b7280'
                tk.Label(inner, text=reg['attendance_status'].title(), bg='#f8fafc',
                        font=('Segoe UI', 10), fg=status_color).pack(side='right', padx=(0, 10))
                
                if reg['hours_credited']:
                    tk.Label(inner, text=f"{reg['hours_credited']} hours", bg='#f8fafc',
                            font=('Segoe UI', 10), fg='#f59e0b').pack(side='right', padx=(0, 10))
            
            if len(registrations) > 10:
                tk.Label(content, text=f"... and {len(registrations) - 10} more", 
                        bg='white', font=('Segoe UI', 11), fg='#94a3b8').pack(pady=10)
        else:
            tk.Label(content, text="No registrations yet", bg='white',
                    font=('Segoe UI', 11), fg='#94a3b8').pack(pady=10)
    
    def show_reports(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=30)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="📊 Event Reports", bg='#f8fafc',
                font=('Segoe UI', 28, 'bold'), fg='#1e293b').pack(side='left')
        
        # Get statistics
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_events,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_events,
                SUM(CASE WHEN status = 'upcoming' THEN 1 ELSE 0 END) as upcoming_events,
                SUM(CASE WHEN status = 'ongoing' THEN 1 ELSE 0 END) as ongoing_events,
                SUM(registered_participants) as total_participants
            FROM events
        """)
        
        stats = cursor.fetchone()
        cursor.close()
        
        # Modern stats cards
        stats_container = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=20)
        stats_container.pack(fill='x')
        
        stat_cards = [
            ("Total Events", stats['total_events'], "#3b82f6", "📊"),
            ("Completed", stats['completed_events'], "#10b981", "✅"),
            ("Upcoming", stats['upcoming_events'], "#f59e0b", "📅"),
            ("Ongoing", stats['ongoing_events'], "#8b5cf6", "🔄"),
            ("Total Participants", stats['total_participants'], "#ec4899", "👥")
        ]
        
        # Create cards in a grid
        cards_frame = tk.Frame(stats_container, bg='#f8fafc')
        cards_frame.pack()
        
        for i, (title, value, color, icon) in enumerate(stat_cards):
            row, col = divmod(i, 3)
            
            if col == 0:
                cards_frame.columnconfigure(0, weight=1)
            if col == 1:
                cards_frame.columnconfigure(1, weight=1)
            if col == 2:
                cards_frame.columnconfigure(2, weight=1)
            
            card = create_stat_card(cards_frame, title, value, color, icon)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')