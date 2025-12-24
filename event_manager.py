import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from tkinter import filedialog

class EventManagement:
    def __init__(self, app):
        self.app = app
        self.app.clear_window()
        
        self.main = tk.Frame(self.app.root, bg='#f8fafc')
        self.main.pack(fill='both', expand=True)
        
        self.create_sidebar()
        
        self.content = tk.Frame(self.main, bg='white')
        self.content.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        self.show_events()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='#1e40af', width=250)
        sidebar.pack(side='left', fill='y')
        
        tk.Label(sidebar, text="SK Portal", bg='#1e40af', fg='white',
                font=('Helvetica', 18, 'bold')).pack(pady=30)
        
        # Back button - WORKING
        tk.Button(sidebar, text="← Back to Dashboard", 
                 command=lambda: self.app.show_admin_dashboard(self.app.user),
                 bg='#3b82f6', fg='white', font=('Helvetica', 11),
                 border=0, cursor='hand2').pack(pady=(0, 30), padx=20)
        
        # Menu items - ALL WORKING
        menu_items = [
            ("📅 All Events", self.show_events),
            ("➕ Add New Event", self.add_event),
            ("📊 Event Reports", self.show_reports),
            ("", None),
            ("📋 Attendance", lambda: self.app.show_attendance_management())
        ]
        
        for text, command in menu_items:
            if text == "":
                tk.Frame(sidebar, bg='#3b82f6', height=1).pack(fill='x', pady=10, padx=20)
            else:
                btn = tk.Button(sidebar, text=text, anchor='w',
                              bg='#1e40af', fg='white', font=('Helvetica', 12),
                              border=0, cursor='hand2', command=command)
                btn.pack(fill='x', padx=20, pady=5)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#2563eb'))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#1e40af'))
    
    def show_events(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="📅 Event Management", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        # Search and filter
        filter_frame = tk.Frame(header, bg='white')
        filter_frame.pack(side='right')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, width=25, 
                               font=('Helvetica', 11))
        search_entry.pack(side='left', padx=5)
        search_entry.insert(0, "Search events...")
        search_entry.bind('<KeyRelease>', lambda e: self.filter_events())
        
        self.status_filter = ttk.Combobox(filter_frame, values=['All', 'Upcoming', 'Ongoing', 'Completed', 'Cancelled'], 
                                         width=12, state='readonly')
        self.status_filter.set('All')
        self.status_filter.pack(side='left', padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_events())
        
        # Add event button - WORKING
        tk.Button(self.content, text="➕ Add New Event", command=self.add_event,
                 bg='#10b981', fg='white', font=('Helvetica', 11, 'bold'),
                 padx=20, pady=10, cursor='hand2').pack(anchor='w', padx=30, pady=(10, 20))
        
        # Events container with scroll
        container = tk.Frame(self.content, bg='#f8fafc')
        container.pack(fill='both', expand=True, padx=30)
        
        # Create canvas for scrollable area
        self.canvas = tk.Canvas(container, bg='#f8fafc', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f8fafc')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Load events
        self.load_all_events()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
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
        
        search_text = self.search_var.get().lower()
        status_filter = self.status_filter.get().lower()
        
        filtered_events = []
        for event in self.all_events:
            matches_search = (not search_text or 
                            search_text in event['title'].lower() or 
                            search_text in event['location'].lower() or
                            search_text in event['event_type'].lower())
            
            matches_status = (status_filter == 'all' or 
                            event['status'].lower() == status_filter)
            
            if matches_search and matches_status:
                filtered_events.append(event)
        
        if not filtered_events:
            tk.Label(self.scrollable_frame, text="No events found", 
                    bg='#f8fafc', font=('Helvetica', 14), fg='#6b7280').pack(pady=50)
        else:
            for event in filtered_events:
                self.create_event_card(event)
    
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
        
        # Bottom row
        bottom = tk.Frame(inner, bg='white')
        bottom.pack(fill='x')
        
        # Participants info
        tk.Label(bottom, text=f"👥 {event['registered']}/{event['max_participants']} registered", 
                bg='white', font=('Helvetica', 11), fg='#374151').pack(side='left')
        
        # Creator info
        tk.Label(bottom, text=f"By: {event['creator']}", bg='white',
                font=('Helvetica', 10), fg='#9ca3af').pack(side='left', padx=20)
        
        # Action buttons - ALL WORKING
        btn_frame = tk.Frame(bottom, bg='white')
        btn_frame.pack(side='right')
        
        if event['status'] in ['upcoming', 'ongoing']:
            tk.Button(btn_frame, text="Edit", 
                     command=lambda e=event: self.edit_event(e),
                     bg='#f59e0b', fg='white', font=('Helvetica', 10),
                     padx=12, pady=5, cursor='hand2').pack(side='left', padx=2)
            
            if event['status'] == 'upcoming':
                tk.Button(btn_frame, text="Cancel", 
                         command=lambda e=event: self.cancel_event(e),
                         bg='#ef4444', fg='white', font=('Helvetica', 10),
                         padx=12, pady=5, cursor='hand2').pack(side='left', padx=2)
            
            if event['status'] == 'ongoing':
                tk.Button(btn_frame, text="Complete", 
                         command=lambda e=event: self.complete_event(e),
                         bg='#10b981', fg='white', font=('Helvetica', 10),
                         padx=12, pady=5, cursor='hand2').pack(side='left', padx=2)
        
        tk.Button(btn_frame, text="View Report", 
                 command=lambda e=event: self.view_report(e),
                 bg='#3b82f6', fg='white', font=('Helvetica', 10),
                 padx=12, pady=5, cursor='hand2').pack(side='left', padx=2)
    
    def add_event(self):
        win = tk.Toplevel(self.app.root)
        win.title("Add New Event")
        win.geometry("600x700")
        win.configure(bg='white')
        
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (600 // 2)
        y = (win.winfo_screenheight() // 2) - (700 // 2)
        win.geometry(f'600x700+{x}+{y}')
        
        tk.Label(win, text="➕ Create New Event", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=30)
        
        form = tk.Frame(win, bg='white', padx=40)
        form.pack(fill='both', expand=True)
        
        # Title
        tk.Label(form, text="Event Title*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        title_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        title_entry.pack(fill='x', pady=(0, 15))
        
        # Date
        tk.Label(form, text="Date* (YYYY-MM-DD)", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        date_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        date_entry.pack(fill='x', pady=(0, 15))
        date_entry.insert(0, "2024-12-25")
        
        # Time
        tk.Label(form, text="Time* (HH:MM)", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        time_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        time_entry.pack(fill='x', pady=(0, 15))
        time_entry.insert(0, "09:00")
        
        # Location
        tk.Label(form, text="Location*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        location_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        location_entry.pack(fill='x', pady=(0, 15))
        
        # Event type
        tk.Label(form, text="Event Type*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        type_combo = ttk.Combobox(form, values=['Volunteer', 'Seminar', 'Sports', 'Social', 'Training'], 
                                 width=38, state='readonly')
        type_combo.pack(fill='x', pady=(0, 15))
        type_combo.set('Volunteer')
        
        # Max participants
        tk.Label(form, text="Maximum Participants*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        max_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        max_entry.pack(fill='x', pady=(0, 15))
        max_entry.insert(0, "50")
        
        # Description
        tk.Label(form, text="Description", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        desc_text = tk.Text(form, width=40, height=5, font=('Helvetica', 11))
        desc_text.pack(fill='x', pady=(0, 20))
        
        def save_event():
            title = title_entry.get().strip()
            date = date_entry.get().strip()
            time = time_entry.get().strip()
            location = location_entry.get().strip()
            event_type = type_combo.get()
            max_parts = max_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            
            if not all([title, date, time, location, event_type, max_parts]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    INSERT INTO events (title, description, event_date, event_time, location, 
                                      event_type, max_participants, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (title, description, date, time, location, event_type, max_parts, self.app.user['id']))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "Event created successfully!")
                win.destroy()
                self.load_all_events()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create event: {e}")
            finally:
                cursor.close()
        
        tk.Button(win, text="Publish Event", command=save_event,
                 bg='#10b981', fg='white', font=('Helvetica', 12, 'bold'),
                 width=20, pady=10, cursor='hand2').pack(pady=30)
    
    def edit_event(self, event):
        win = tk.Toplevel(self.app.root)
        win.title(f"Edit Event: {event['title']}")
        win.geometry("600x700")
        win.configure(bg='white')
        
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (600 // 2)
        y = (win.winfo_screenheight() // 2) - (700 // 2)
        win.geometry(f'600x700+{x}+{y}')
        
        tk.Label(win, text="✏️ Edit Event", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=30)
        
        form = tk.Frame(win, bg='white', padx=40)
        form.pack(fill='both', expand=True)
        
        # Title
        tk.Label(form, text="Event Title*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        title_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        title_entry.pack(fill='x', pady=(0, 15))
        title_entry.insert(0, event['title'])
        
        # Date
        tk.Label(form, text="Date* (YYYY-MM-DD)", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        date_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        date_entry.pack(fill='x', pady=(0, 15))
        date_entry.insert(0, str(event['event_date']))
        
        # Time
        tk.Label(form, text="Time* (HH:MM)", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        time_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        time_entry.pack(fill='x', pady=(0, 15))
        time_entry.insert(0, str(event['event_time']))
        
        # Location
        tk.Label(form, text="Location*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        location_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        location_entry.pack(fill='x', pady=(0, 15))
        location_entry.insert(0, event['location'])
        
        # Event type
        tk.Label(form, text="Event Type*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        type_combo = ttk.Combobox(form, values=['Volunteer', 'Seminar', 'Sports', 'Social', 'Training'], 
                                 width=38, state='readonly')
        type_combo.pack(fill='x', pady=(0, 15))
        type_combo.set(event['event_type'])
        
        # Max participants
        tk.Label(form, text="Maximum Participants*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        max_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        max_entry.pack(fill='x', pady=(0, 15))
        max_entry.insert(0, str(event['max_participants']))
        
        # Status
        tk.Label(form, text="Status*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        status_combo = ttk.Combobox(form, values=['upcoming', 'ongoing', 'completed', 'cancelled'], 
                                   width=38, state='readonly')
        status_combo.pack(fill='x', pady=(0, 15))
        status_combo.set(event['status'])
        
        # Description
        tk.Label(form, text="Description", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        desc_text = tk.Text(form, width=40, height=5, font=('Helvetica', 11))
        desc_text.pack(fill='x', pady=(0, 20))
        desc_text.insert('1.0', event['description'] or "")
        
        def update_event():
            title = title_entry.get().strip()
            date = date_entry.get().strip()
            time = time_entry.get().strip()
            location = location_entry.get().strip()
            event_type = type_combo.get()
            max_parts = max_entry.get().strip()
            status = status_combo.get()
            description = desc_text.get("1.0", tk.END).strip()
            
            if not all([title, date, time, location, event_type, max_parts, status]):
                messagebox.showerror("Error", "Please fill all required fields")
                return
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    UPDATE events 
                    SET title = %s, description = %s, event_date = %s, event_time = %s,
                        location = %s, event_type = %s, max_participants = %s, status = %s
                    WHERE id = %s
                """, (title, description, date, time, location, event_type, max_parts, status, event['id']))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "Event updated successfully!")
                win.destroy()
                self.load_all_events()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update event: {e}")
            finally:
                cursor.close()
        
        tk.Button(win, text="Update Event", command=update_event,
                 bg='#3b82f6', fg='white', font=('Helvetica', 12, 'bold'),
                 width=20, pady=10, cursor='hand2').pack(pady=30)
    
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
        if messagebox.askyesno("Confirm", f"Mark '{event['title']}' as completed?"):
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
        win = tk.Toplevel(self.app.root)
        win.title(f"Report: {event['title']}")
        win.geometry("800x600")
        
        tk.Label(win, text=f"📊 {event['title']} - Attendance Report", 
                font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Get attendance data
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.name, u.youth_id, er.check_in_time, er.check_out_time, er.attendance_status
            FROM event_registrations er
            JOIN users u ON er.user_id = u.id
            WHERE er.event_id = %s
            ORDER BY er.check_in_time DESC
        """, (event['id'],))
        
        attendees = cursor.fetchall()
        cursor.close()
        
        # Stats
        stats_frame = tk.Frame(win)
        stats_frame.pack(pady=10)
        
        total = len(attendees)
        attended = len([a for a in attendees if a['check_in_time']])
        
        tk.Label(stats_frame, text=f"Total Registered: {total}", 
                font=('Helvetica', 12)).pack(side='left', padx=20)
        tk.Label(stats_frame, text=f"Attended: {attended}", 
                font=('Helvetica', 12)).pack(side='left', padx=20)
        
        # Table
        tree = ttk.Treeview(win, columns=('Name', 'Youth ID', 'Check In', 'Check Out', 'Status'), show='headings')
        
        for col in tree['columns']:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        for att in attendees:
            tree.insert('', 'end', values=(
                att['name'],
                att['youth_id'],
                att['check_in_time'].strftime('%H:%M') if att['check_in_time'] else 'N/A',
                att['check_out_time'].strftime('%H:%M') if att['check_out_time'] else 'N/A',
                att['attendance_status']
            ))
        
        tree.pack(fill='both', expand=True, padx=20, pady=10)
    
    def show_reports(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="📊 Event Reports", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
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
        
        # Display stats
        stats_frame = tk.Frame(self.content, bg='white')
        stats_frame.pack(pady=20)
        
        stat_cards = [
            ("Total Events", stats['total_events'], "#3b82f6"),
            ("Completed", stats['completed_events'], "#10b981"),
            ("Upcoming", stats['upcoming_events'], "#f59e0b"),
            ("Ongoing", stats['ongoing_events'], "#8b5cf6"),
            ("Total Participants", stats['total_participants'], "#ec4899")
        ]
        
        for i, (title, value, color) in enumerate(stat_cards):
            row, col = divmod(i, 3)
            
            if col == 0:
                stats_frame.columnconfigure(0, weight=1)
            if col == 1:
                stats_frame.columnconfigure(1, weight=1)
            if col == 2:
                stats_frame.columnconfigure(2, weight=1)
            
            card = tk.Frame(stats_frame, bg='white', relief='ridge', borderwidth=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            inner = tk.Frame(card, bg=color + '20', padx=20, pady=20)
            inner.pack(fill='both', expand=True)
            
            tk.Label(inner, text=str(value), bg=color + '20', fg=color,
                    font=('Helvetica', 28, 'bold')).pack()
            tk.Label(inner, text=title, bg=color + '20', fg='#64748b',
                    font=('Helvetica', 12)).pack()