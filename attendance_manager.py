# attendance_manager.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from tkinter import filedialog

class AttendanceManagement:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.main = tk.Frame(self.root, bg='#f8fafc')
        self.main.pack(fill='both', expand=True)
        
        self.create_sidebar()
        
        self.content = tk.Frame(self.main, bg='#f8fafc')
        self.content.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        self.show_attendance()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='white', width=250)
        sidebar.pack(side='left', fill='y')
        
        tk.Label(sidebar, text="SK System", bg='white',
                font=('Helvetica', 18, 'bold'), fg='#6366f1').pack(pady=30)
        
        tk.Button(sidebar, text="← Back to Dashboard", 
                 command=lambda: self.app.show_admin_dashboard(self.app.user),
                 bg='white', fg='#6366f1', font=('Helvetica', 11),
                 border=0, cursor='hand2').pack(pady=(0, 30))
        
        menu_items = [
            ("📋 Live Scanner", self.show_attendance),
            ("📊 View Records", self.view_records),
            ("📅 By Event", self.by_event),
            ("👤 By Youth", self.by_youth),
            ("", None),
            ("📈 Reports", self.show_reports),
            ("📤 Export", self.export_data)
        ]
        
        for text, command in menu_items:
            if text == "":
                tk.Frame(sidebar, bg='#e5e7eb', height=1).pack(fill='x', pady=10, padx=20)
            else:
                btn = tk.Button(sidebar, text=text, anchor='w',
                              bg='white', fg='#374151', font=('Helvetica', 12),
                              border=0, cursor='hand2', command=command)
                btn.pack(fill='x', padx=20, pady=8)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#f3f4f6'))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg='white'))
    
    def show_attendance(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="📋 Live Attendance Scanner", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        # Event selection
        event_frame = tk.Frame(header, bg='white')
        event_frame.pack(side='right')
        
        tk.Label(event_frame, text="Select Event:", bg='white',
                font=('Helvetica', 11)).pack(side='left')
        
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT id, title FROM events WHERE status IN ('upcoming', 'ongoing') ORDER BY event_date ASC")
        events = cursor.fetchall()
        cursor.close()
        
        self.event_ids = [e['id'] for e in events]
        event_names = [e['title'] for e in events]
        
        self.event_combo = ttk.Combobox(event_frame, values=event_names, width=25, state='readonly')
        self.event_combo.pack(side='left', padx=10)
        if event_names:
            self.event_combo.set(event_names[0])
        
        # Main content - 2 columns
        main_content = tk.Frame(self.content, bg='#f8fafc', padx=30)
        main_content.pack(fill='both', expand=True)
        
        # Left column - Scanner
        left = tk.Frame(main_content, bg='white', width=400)
        left.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        tk.Label(left, text="QR Code Scanner", bg='white',
                font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Scanner placeholder
        scanner_frame = tk.Frame(left, bg='black', height=300)
        scanner_frame.pack(fill='x', pady=10, padx=20)
        tk.Label(scanner_frame, text="[Live Camera Feed]", bg='black', fg='white',
                font=('Helvetica', 14)).pack(expand=True)
        
        # Manual entry
        tk.Label(left, text="Manual Entry", bg='white',
                font=('Helvetica', 12, 'bold')).pack(anchor='w', padx=20, pady=(20, 10))
        
        entry_frame = tk.Frame(left, bg='white')
        entry_frame.pack(fill='x', padx=20)
        
        self.manual_entry = tk.Entry(entry_frame, font=('Helvetica', 12))
        self.manual_entry.pack(side='left', fill='x', expand=True)
        
        tk.Button(entry_frame, text="Scan", command=self.scan_manual,
                 bg='#6366f1', fg='white', font=('Helvetica', 11),
                 padx=20, cursor='hand2').pack(side='right')
        
        # Feedback
        self.feedback_label = tk.Label(left, text="", bg='white',
                                      font=('Helvetica', 11))
        self.feedback_label.pack(pady=20)
        
        # Right column - Attendance log
        right = tk.Frame(main_content, bg='white')
        right.pack(side='right', fill='both', expand=True)
        
        tk.Label(right, text="Attendance Log", bg='white',
                font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Stats
        stats_frame = tk.Frame(right, bg='white')
        stats_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.in_count = tk.Label(stats_frame, text="In: 0", bg='#d1fae5', fg='#065f46',
                                font=('Helvetica', 12, 'bold'), padx=15, pady=5)
        self.in_count.pack(side='left', padx=5)
        
        self.out_count = tk.Label(stats_frame, text="Out: 0", bg='#fee2e2', fg='#991b1b',
                                 font=('Helvetica', 12, 'bold'), padx=15, pady=5)
        self.out_count.pack(side='left', padx=5)
        
        tk.Button(stats_frame, text="Export CSV", command=self.export_csv,
                 bg='#6b7280', fg='white', font=('Helvetica', 10)).pack(side='right')
        
        # Attendance table
        table_frame = tk.Frame(right, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20)
        
        # Create treeview
        self.tree = ttk.Treeview(table_frame, columns=('Youth ID', 'Name', 'Time In', 'Time Out', 'Status'), show='headings')
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load initial data
        self.load_attendance_data()
    
    def scan_manual(self):
        code = self.manual_entry.get().strip()
        if not code:
            messagebox.showwarning("Warning", "Please enter a Youth ID")
            return
        
        # Get selected event
        event_index = self.event_combo.current()
        if event_index == -1:
            messagebox.showwarning("Warning", "Please select an event first")
            return
        
        event_id = self.event_ids[event_index]
        
        current_time = datetime.now().strftime("%H:%M")
        
        # Check if youth exists
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM users WHERE youth_id = %s OR id = %s", (code, code))
        youth = cursor.fetchone()
        
        if not youth:
            self.feedback_label.config(text="❌ Youth not found", fg='#ef4444')
            cursor.close()
            return
        
        # Check if youth is registered for the event
        cursor.execute("SELECT * FROM event_registrations WHERE event_id = %s AND user_id = %s", 
                      (event_id, youth['id']))
        registration = cursor.fetchone()
        
        if not registration:
            # Register youth for event
            try:
                cursor.execute("""
                    INSERT INTO event_registrations (event_id, user_id, attendance_status, check_in_time)
                    VALUES (%s, %s, 'checked_in', NOW())
                """, (event_id, youth['id']))
                status = "checked in"
                self.feedback_label.config(text=f"✅ {youth['name']} registered and checked in at {current_time}", fg='#10b981')
            except Exception as e:
                self.feedback_label.config(text=f"❌ Error: {str(e)}", fg='#ef4444')
                cursor.close()
                return
        else:
            # Check if already checked in
            if registration['check_out_time']:
                # Check in again
                cursor.execute("""
                    UPDATE event_registrations 
                    SET check_in_time = NOW(), check_out_time = NULL, attendance_status = 'checked_in'
                    WHERE event_id = %s AND user_id = %s
                """, (event_id, youth['id']))
                status = "checked in"
                self.feedback_label.config(text=f"✅ {youth['name']} checked in at {current_time}", fg='#10b981')
            else:
                # Check out
                cursor.execute("""
                    UPDATE event_registrations 
                    SET check_out_time = NOW(), attendance_status = 'attended'
                    WHERE event_id = %s AND user_id = %s
                """, (event_id, youth['id']))
                status = "checked out"
                self.feedback_label.config(text=f"✅ {youth['name']} checked out at {current_time}", fg='#3b82f6')
        
        self.app.db.commit()
        cursor.close()
        
        # Clear entry and update display
        self.manual_entry.delete(0, tk.END)
        self.load_attendance_data()
        
        # Clear feedback after 3 seconds
        self.root.after(3000, lambda: self.feedback_label.config(text=""))
    
    def load_attendance_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get event ID
        event_index = self.event_combo.current()
        if event_index == -1:
            return
        
        event_id = self.event_ids[event_index]
        
        # Get attendance for selected event
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.youth_id, u.name, er.check_in_time, er.check_out_time, er.attendance_status
            FROM event_registrations er
            JOIN users u ON er.user_id = u.id
            WHERE er.event_id = %s
            ORDER BY er.check_in_time DESC
        """, (event_id,))
        
        records = cursor.fetchall()
        cursor.close()
        
        in_count = 0
        out_count = 0
        
        for record in records:
            time_in = record['check_in_time'].strftime("%H:%M") if record['check_in_time'] else "N/A"
            time_out = record['check_out_time'].strftime("%H:%M") if record['check_out_time'] else "N/A"
            
            status = "In" if record['check_out_time'] is None else "Out"
            if status == "In":
                in_count += 1
            else:
                out_count += 1
            
            self.tree.insert('', 'end', values=(
                record['youth_id'] or "N/A",
                record['name'],
                time_in,
                time_out,
                status
            ))
        
        # Update counters
        self.in_count.config(text=f"In: {in_count}")
        self.out_count.config(text=f"Out: {out_count}")
    
    def export_csv(self):
        # Get event ID
        event_index = self.event_combo.current()
        if event_index == -1:
            messagebox.showwarning("Warning", "Please select an event first")
            return
        
        event_id = self.event_ids[event_index]
        
        # Get event title
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT title FROM events WHERE id = %s", (event_id,))
        event_title = cursor.fetchone()['title']
        cursor.close()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title=f"Export attendance for {event_title}"
        )
        
        if not file_path:
            return
        
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.youth_id, u.name, u.email, er.check_in_time, er.check_out_time, 
                   er.attendance_status, e.title as event_name
            FROM event_registrations er
            JOIN users u ON er.user_id = u.id
            JOIN events e ON er.event_id = e.id
            WHERE er.event_id = %s
            ORDER BY er.check_in_time DESC
        """, (event_id,))
        
        records = cursor.fetchall()
        cursor.close()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Youth ID', 'Name', 'Email', 'Check In', 'Check Out', 'Status', 'Event']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in records:
                writer.writerow({
                    'Youth ID': record['youth_id'] or '',
                    'Name': record['name'],
                    'Email': record['email'],
                    'Check In': record['check_in_time'].strftime("%Y-%m-%d %H:%M") if record['check_in_time'] else 'N/A',
                    'Check Out': record['check_out_time'].strftime("%Y-%m-%d %H:%M") if record['check_out_time'] else 'N/A',
                    'Status': record['attendance_status'],
                    'Event': record['event_name']
                })
        
        messagebox.showinfo("Success", f"Data exported to {file_path}")
    
    def view_records(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="📊 All Attendance Records", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
        # Create filters
        filter_frame = tk.Frame(self.content, bg='white')
        filter_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(filter_frame, text="From:", bg='white').pack(side='left', padx=5)
        from_date = tk.Entry(filter_frame, width=12)
        from_date.pack(side='left', padx=5)
        from_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(filter_frame, text="To:", bg='white').pack(side='left', padx=5)
        to_date = tk.Entry(filter_frame, width=12)
        to_date.pack(side='left', padx=5)
        to_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        def load_records():
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            cursor = self.app.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.youth_id, u.name, e.title as event_name, 
                       er.check_in_time, er.check_out_time, er.attendance_status
                FROM event_registrations er
                JOIN users u ON er.user_id = u.id
                JOIN events e ON er.event_id = e.id
                WHERE DATE(er.check_in_time) BETWEEN %s AND %s
                ORDER BY er.check_in_time DESC
            """, (from_date.get(), to_date.get()))
            
            records = cursor.fetchall()
            cursor.close()
            
            for record in records:
                tree.insert('', 'end', values=(
                    record['youth_id'] or 'N/A',
                    record['name'],
                    record['event_name'],
                    record['check_in_time'].strftime("%Y-%m-%d %H:%M") if record['check_in_time'] else 'N/A',
                    record['check_out_time'].strftime("%Y-%m-%d %H:%M") if record['check_out_time'] else 'N/A',
                    record['attendance_status']
                ))
        
        tk.Button(filter_frame, text="Load", command=load_records,
                 bg='#6366f1', fg='white').pack(side='left', padx=10)
        
        # Create treeview
        tree_frame = tk.Frame(self.content)
        tree_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Youth ID', 'Name', 'Event', 'Check In', 'Check Out', 'Status'), 
                           show='headings', height=20)
        
        tree.heading('Youth ID', text='Youth ID')
        tree.heading('Name', text='Name')
        tree.heading('Event', text='Event')
        tree.heading('Check In', text='Check In')
        tree.heading('Check Out', text='Check Out')
        tree.heading('Status', text='Status')
        
        for col in tree['columns']:
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load initial data
        load_records()
    
    def by_event(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="📅 Attendance by Event", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
        # Get all events
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT id, title, event_date FROM events ORDER BY event_date DESC")
        events = cursor.fetchall()
        cursor.close()
        
        if not events:
            tk.Label(self.content, text="No events found", bg='white',
                    font=('Helvetica', 14)).pack(pady=50)
            return
        
        # Create frame for event buttons
        events_frame = tk.Frame(self.content, bg='#f8fafc')
        events_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        canvas = tk.Canvas(events_frame, bg='#f8fafc', highlightthickness=0)
        scrollbar = tk.Scrollbar(events_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8fafc')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for event in events:
            self.create_event_attendance_card(scrollable_frame, event)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_event_attendance_card(self, parent, event):
        # Get attendance count for this event
        cursor = self.app.db.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN check_in_time IS NOT NULL THEN 1 ELSE 0 END) as checked_in,
                SUM(CASE WHEN check_out_time IS NOT NULL THEN 1 ELSE 0 END) as attended
            FROM event_registrations 
            WHERE event_id = %s
        """, (event['id'],))
        
        stats = cursor.fetchone()
        cursor.close()
        
        total = stats[0] if stats else 0
        checked_in = stats[1] if stats else 0
        attended = stats[2] if stats else 0
        
        card = tk.Frame(parent, bg='white', relief='ridge', borderwidth=1)
        card.pack(fill='x', pady=5, padx=5)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=15)
        inner.pack(fill='x')
        
        # Event title and date
        tk.Label(inner, text=event['title'], bg='white',
                font=('Helvetica', 14, 'bold'), fg='#1e293b').pack(anchor='w')
        
        tk.Label(inner, text=f"📅 {event['event_date']}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(anchor='w', pady=(5, 0))
        
        # Attendance stats
        stats_frame = tk.Frame(inner, bg='white')
        stats_frame.pack(anchor='w', pady=10)
        
        tk.Label(stats_frame, text=f"Total Registered: {total}", bg='white',
                font=('Helvetica', 11)).pack(side='left', padx=(0, 15))
        tk.Label(stats_frame, text=f"Checked In: {checked_in}", bg='white',
                font=('Helvetica', 11)).pack(side='left', padx=(0, 15))
        tk.Label(stats_frame, text=f"Attended: {attended}", bg='white',
                font=('Helvetica', 11)).pack(side='left')
        
        # View button
        def view_event_attendance():
            self.view_event_attendance_details(event)
        
        tk.Button(inner, text="View Details", command=view_event_attendance,
                 bg='#6366f1', fg='white', font=('Helvetica', 10),
                 padx=15, pady=5, cursor='hand2').pack(anchor='e')
    
    def view_event_attendance_details(self, event):
        win = tk.Toplevel(self.root)
        win.title(f"Attendance: {event['title']}")
        win.geometry("800x600")
        
        tk.Label(win, text=f"📊 {event['title']} - Attendance Details", 
                font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Get attendance details
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.youth_id, u.name, u.email, 
                   er.check_in_time, er.check_out_time, er.attendance_status
            FROM event_registrations er
            JOIN users u ON er.user_id = u.id
            WHERE er.event_id = %s
            ORDER BY er.check_in_time DESC
        """, (event['id'],))
        
        attendees = cursor.fetchall()
        cursor.close()
        
        # Create treeview
        tree_frame = tk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Youth ID', 'Name', 'Email', 'Check In', 'Check Out', 'Status'), 
                           show='headings', height=20)
        
        tree.heading('Youth ID', text='Youth ID')
        tree.heading('Name', text='Name')
        tree.heading('Email', text='Email')
        tree.heading('Check In', text='Check In')
        tree.heading('Check Out', text='Check Out')
        tree.heading('Status', text='Status')
        
        for col in tree['columns']:
            tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for att in attendees:
            tree.insert('', 'end', values=(
                att['youth_id'] or 'N/A',
                att['name'],
                att['email'],
                att['check_in_time'].strftime('%Y-%m-%d %H:%M') if att['check_in_time'] else 'N/A',
                att['check_out_time'].strftime('%Y-%m-%d %H:%M') if att['check_out_time'] else 'N/A',
                att['attendance_status']
            ))
    
    def by_youth(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="👤 Attendance by Youth", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(self.content, bg='white')
        search_frame.pack(fill='x', padx=30, pady=10)
        
        tk.Label(search_frame, text="Search Youth:", bg='white').pack(side='left', padx=5)
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        def search_youth():
            # Clear existing items
            for item in tree.get_children():
                tree.delete(item)
            
            search_text = search_var.get().lower()
            
            cursor = self.app.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, name, youth_id, email
                FROM users 
                WHERE role = 'youth' AND status = 'active'
                AND (LOWER(name) LIKE %s OR LOWER(email) LIKE %s OR LOWER(youth_id) LIKE %s)
                ORDER BY name
            """, (f'%{search_text}%', f'%{search_text}%', f'%{search_text}%'))
            
            youth_list = cursor.fetchall()
            cursor.close()
            
            for youth in youth_list:
                tree.insert('', 'end', values=(
                    youth['youth_id'] or 'N/A',
                    youth['name'],
                    youth['email'],
                    'View Attendance'
                ), tags=(youth['id'],))
        
        search_entry.bind('<KeyRelease>', lambda e: search_youth())
        
        # Create treeview
        tree_frame = tk.Frame(self.content)
        tree_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Youth ID', 'Name', 'Email', 'Action'), 
                           show='headings', height=20)
        
        tree.heading('Youth ID', text='Youth ID')
        tree.heading('Name', text='Name')
        tree.heading('Email', text='Email')
        tree.heading('Action', text='Action')
        
        tree.column('Youth ID', width=100)
        tree.column('Name', width=150)
        tree.column('Email', width=150)
        tree.column('Action', width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        def view_youth_attendance(event):
            item = tree.identify_row(event.y)
            if item:
                user_id = tree.item(item, 'tags')[0]
                self.view_youth_attendance_details(user_id)
        
        tree.bind('<Double-1>', view_youth_attendance)
        
        # Load all youth initially
        search_youth()
    
    def view_youth_attendance_details(self, user_id):
        # Get youth details
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("SELECT name, youth_id FROM users WHERE id = %s", (user_id,))
        youth = cursor.fetchone()
        cursor.close()
        
        win = tk.Toplevel(self.root)
        win.title(f"Attendance: {youth['name']}")
        win.geometry("800x600")
        
        tk.Label(win, text=f"📊 {youth['name']} - Attendance History", 
                font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Get attendance history
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.title, e.event_date, e.event_time,
                   er.check_in_time, er.check_out_time, er.attendance_status,
                   er.hours_credited
            FROM event_registrations er
            JOIN events e ON er.event_id = e.id
            WHERE er.user_id = %s
            ORDER BY e.event_date DESC
        """, (user_id,))
        
        attendance_history = cursor.fetchall()
        cursor.close()
        
        # Create treeview
        tree_frame = tk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Event', 'Date', 'Time', 'Check In', 'Check Out', 'Status', 'Hours'), 
                           show='headings', height=20)
        
        tree.heading('Event', text='Event')
        tree.heading('Date', text='Date')
        tree.heading('Time', text='Time')
        tree.heading('Check In', text='Check In')
        tree.heading('Check Out', text='Check Out')
        tree.heading('Status', text='Status')
        tree.heading('Hours', text='Hours')
        
        for col in tree['columns']:
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        total_hours = 0
        for record in attendance_history:
            hours = record['hours_credited'] or 0
            total_hours += hours
            
            tree.insert('', 'end', values=(
                record['title'],
                str(record['event_date']),
                str(record['event_time']),
                record['check_in_time'].strftime('%H:%M') if record['check_in_time'] else 'N/A',
                record['check_out_time'].strftime('%H:%M') if record['check_out_time'] else 'N/A',
                record['attendance_status'],
                f"{hours:.1f}"
            ))
        
        # Display total hours
        tk.Label(win, text=f"Total Volunteer Hours: {total_hours:.1f}", 
                font=('Helvetica', 12, 'bold')).pack(pady=10)
    
    def show_reports(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="📈 Attendance Reports", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
        # Get statistics
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT er.event_id) as total_events,
                COUNT(DISTINCT er.user_id) as unique_participants,
                SUM(CASE WHEN er.attendance_status = 'attended' THEN 1 ELSE 0 END) as total_attendances,
                COALESCE(SUM(er.hours_credited), 0) as total_hours,
                AVG(CASE WHEN er.attendance_status = 'attended' THEN 1 ELSE 0 END) as attendance_rate
            FROM event_registrations er
            JOIN events e ON er.event_id = e.id
            WHERE e.event_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        """)
        
        stats = cursor.fetchone()
        cursor.close()
        
        # Display stats
        stats_frame = tk.Frame(self.content, bg='white')
        stats_frame.pack(pady=20)
        
        stat_cards = [
            ("Events (30 days)", stats['total_events'] or 0, "#3b82f6", "#e0e7ff"),
            ("Unique Participants", stats['unique_participants'] or 0, "#10b981", "#d1fae5"),
            ("Total Attendances", stats['total_attendances'] or 0, "#f59e0b", "#fef3c7"),
            ("Total Hours", f"{stats['total_hours'] or 0:.1f}", "#8b5cf6", "#ede9fe"),
            ("Attendance Rate", f"{(stats['attendance_rate'] or 0) * 100:.1f}%", "#ec4899", "#fce7f3")
        ]
        
        for i, (title, value, color, light_color) in enumerate(stat_cards):
            row, col = divmod(i, 3)
            
            if col == 0:
                stats_frame.columnconfigure(0, weight=1)
            if col == 1:
                stats_frame.columnconfigure(1, weight=1)
            if col == 2:
                stats_frame.columnconfigure(2, weight=1)
            
            card = tk.Frame(stats_frame, bg='white', relief='ridge', borderwidth=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            # FIXED: Use light_color directly instead of trying to modify hex
            inner = tk.Frame(card, bg=light_color, padx=20, pady=20)
            inner.pack(fill='both', expand=True)
            
            tk.Label(inner, text=str(value), bg=light_color, fg=color,
                    font=('Helvetica', 28, 'bold')).pack()
            tk.Label(inner, text=title, bg=light_color, fg='#64748b',
                    font=('Helvetica', 12)).pack()
    
    def export_data(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export All Attendance Data"
        )
        
        if not file_path:
            return
        
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.youth_id, u.name, u.email, 
                   e.title as event_name, e.event_date,
                   er.check_in_time, er.check_out_time, 
                   er.attendance_status, er.hours_credited
            FROM event_registrations er
            JOIN users u ON er.user_id = u.id
            JOIN events e ON er.event_id = e.id
            ORDER BY e.event_date DESC, er.check_in_time DESC
        """)
        
        records = cursor.fetchall()
        cursor.close()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Youth ID', 'Name', 'Email', 'Event', 'Event Date', 
                         'Check In', 'Check Out', 'Status', 'Hours']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for record in records:
                writer.writerow({
                    'Youth ID': record['youth_id'] or '',
                    'Name': record['name'],
                    'Email': record['email'],
                    'Event': record['event_name'],
                    'Event Date': str(record['event_date']),
                    'Check In': record['check_in_time'].strftime("%Y-%m-%d %H:%M") if record['check_in_time'] else '',
                    'Check Out': record['check_out_time'].strftime("%Y-%m-%d %H:%M") if record['check_out_time'] else '',
                    'Status': record['attendance_status'],
                    'Hours': record['hours_credited'] or 0
                })
        
        messagebox.showinfo("Success", f"All attendance data exported to {file_path}")