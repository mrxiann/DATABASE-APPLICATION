import tkinter as tk
from tkinter import ttk, messagebox
import csv
from tkinter import filedialog

class OpportunityManagement:
    def __init__(self, app):
        self.app = app
        self.app.clear_window()
        
        self.main = tk.Frame(self.app.root, bg='#f8fafc')
        self.main.pack(fill='both', expand=True)
        
        self.create_sidebar()
        
        self.content = tk.Frame(self.main, bg='white')
        self.content.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        self.show_opportunities()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='#8b5cf6', width=250)
        sidebar.pack(side='left', fill='y')
        
        tk.Label(sidebar, text="SK Youth Management and Information System", bg='#8b5cf6', fg='white',
                font=('Helvetica', 18, 'bold')).pack(pady=30)
        
        tk.Button(sidebar, text="← Back to Dashboard", 
                 command=lambda: self.app.show_admin_dashboard(self.app.user),
                 bg='#a78bfa', fg='white', font=('Helvetica', 11),
                 border=0, cursor='hand2').pack(pady=(0, 30), padx=20)
        
        menu_items = [
            ("💼 All Opportunities", self.show_opportunities),
            ("➕ Post New", self.add_opportunity),
            ("📋 Applications", self.show_applications),
            ("", None),
            ("📊 Reports", self.show_reports)
        ]
        
        for text, command in menu_items:
            if text == "":
                tk.Frame(sidebar, bg='#a78bfa', height=1).pack(fill='x', pady=10, padx=20)
            else:
                btn = tk.Button(sidebar, text=text, anchor='w',
                              bg='#8b5cf6', fg='white', font=('Helvetica', 12),
                              border=0, cursor='hand2', command=command)
                btn.pack(fill='x', padx=20, pady=5)
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#a78bfa'))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#8b5cf6'))
    
    def show_opportunities(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="💼 Opportunities Management", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        filter_frame = tk.Frame(header, bg='white')
        filter_frame.pack(side='right')
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, width=25, 
                               font=('Helvetica', 11))
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.filter_opportunities())
        
        self.type_filter = ttk.Combobox(filter_frame, values=['All', 'Job', 'Volunteer', 'Internship', 'Training'], 
                                       width=12, state='readonly')
        self.type_filter.set('All')
        self.type_filter.pack(side='left', padx=5)
        self.type_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_opportunities())
        
        tk.Button(self.content, text="➕ Post New Opportunity", command=self.add_opportunity,
                 bg='#10b981', fg='white', font=('Helvetica', 11, 'bold'),
                 padx=20, pady=10, cursor='hand2').pack(anchor='w', padx=30, pady=(10, 20))
        
        container = tk.Frame(self.content, bg='#f8fafc')
        container.pack(fill='both', expand=True, padx=30)
        
        self.canvas = tk.Canvas(container, bg='#f8fafc', highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f8fafc')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.load_all_opportunities()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_all_opportunities(self):
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.*, u.name as creator,
                   (SELECT COUNT(*) FROM opportunity_applications WHERE opportunity_id = o.id) as applicants
            FROM opportunities o
            LEFT JOIN users u ON o.created_by = u.id
            ORDER BY o.created_at DESC
        """)
        self.all_opportunities = cursor.fetchall()
        cursor.close()
        
        self.filter_opportunities()
    
    def filter_opportunities(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        search_text = self.search_var.get().lower()
        type_filter = self.type_filter.get().lower()
        
        filtered = []
        for opp in self.all_opportunities:
            matches_search = (not search_text or 
                            search_text in opp['title'].lower() or 
                            search_text in opp['location'].lower())
            
            matches_type = (type_filter == 'all' or 
                           opp['type'].lower() == type_filter)
            
            if matches_search and matches_type:
                filtered.append(opp)
        
        if not filtered:
            tk.Label(self.scrollable_frame, text="No opportunities found", 
                    bg='#f8fafc', font=('Helvetica', 14), fg='#6b7280').pack(pady=50)
        else:
            for opp in filtered:
                self.create_opportunity_card(opp)
    
    def create_opportunity_card(self, opp):
        type_colors = {
            'Job': ('#ef4444', '#fee2e2'),
            'Volunteer': ('#10b981', '#d1fae5'),
            'Internship': ('#f59e0b', '#fef3c7'),
            'Training': ('#3b82f6', '#dbeafe')
        }
        color, bg_color = type_colors.get(opp['type'], ('#6b7280', '#f3f4f6'))
        
        card = tk.Frame(self.scrollable_frame, bg='white', relief='ridge', borderwidth=1)
        card.pack(fill='x', pady=8, padx=5)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=20)
        inner.pack(fill='x')
        
        # Type badge
        type_frame = tk.Frame(inner, bg=bg_color)
        type_frame.pack(anchor='w', pady=(0, 10))
        tk.Label(type_frame, text=opp['type'], bg=bg_color, fg=color,
                font=('Helvetica', 10, 'bold'), padx=10, pady=3).pack()
        
        # Title
        tk.Label(inner, text=opp['title'], bg='white',
                font=('Helvetica', 16, 'bold'), fg='#1e293b').pack(anchor='w', pady=(0, 10))
        
        # Details
        details = [
            f"📍 {opp['location']}",
            f"💰 {opp['compensation'] or 'Not specified'}",
            f"⏰ {opp['commitment'] or 'Flexible'}"
        ]
        
        for detail in details:
            tk.Label(inner, text=detail, bg='white',
                    font=('Helvetica', 11), fg='#64748b').pack(anchor='w', pady=2)
        
        # Deadline
        if opp['deadline']:
            tk.Label(inner, text=f"📅 Deadline: {opp['deadline']}", bg='white',
                    font=('Helvetica', 11, 'bold'), fg='#ef4444').pack(anchor='w', pady=(10, 0))
        
        # Applicants
        tk.Label(inner, text=f"👥 {opp['applicants']} applicants", bg='white',
                font=('Helvetica', 11), fg='#374151').pack(anchor='w', pady=(10, 0))
        
        # Status
        status_color = '#10b981' if opp['status'] == 'open' else '#6b7280'
        tk.Label(inner, text=f"Status: {opp['status']}", bg='white',
                font=('Helvetica', 11), fg=status_color).pack(anchor='w', pady=(5, 15))
        
        # Action buttons
        btn_frame = tk.Frame(inner, bg='white')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text="View Applicants", 
                 command=lambda o=opp: self.view_applicants(o),
                 bg='#3b82f6', fg='white', font=('Helvetica', 10),
                 padx=12, pady=5, cursor='hand2').pack(side='left', padx=2)
        
        if opp['status'] == 'open':
            tk.Button(btn_frame, text="Edit", 
                     command=lambda o=opp: self.edit_opportunity(o),
                     bg='#f59e0b', fg='white', font=('Helvetica', 10),
                     padx=12, pady=5, cursor='hand2').pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="Close", 
                     command=lambda o=opp: self.close_opportunity(o),
                     bg='#ef4444', fg='white', font=('Helvetica', 10),
                     padx=12, pady=5, cursor='hand2').pack(side='left', padx=2)
    
    def add_opportunity(self):
        win = tk.Toplevel(self.app.root)
        win.title("Post New Opportunity")
        win.geometry("600x650")
        win.configure(bg='white')
        
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (600 // 2)
        y = (win.winfo_screenheight() // 2) - (650 // 2)
        win.geometry(f'600x650+{x}+{y}')
        
        tk.Label(win, text="➕ Post New Opportunity", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=30)
        
        form = tk.Frame(win, bg='white', padx=40)
        form.pack(fill='both', expand=True)
        
        # Title
        tk.Label(form, text="Opportunity Title*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        title_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        title_entry.pack(fill='x', pady=(0, 15))
        
        # Type
        tk.Label(form, text="Type*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        type_combo = ttk.Combobox(form, values=['Job', 'Volunteer', 'Internship', 'Training'], 
                                 width=38, state='readonly')
        type_combo.pack(fill='x', pady=(0, 15))
        type_combo.set('Job')
        
        # Compensation
        tk.Label(form, text="Compensation", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        comp_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        comp_entry.pack(fill='x', pady=(0, 15))
        comp_entry.insert(0, "Not specified")
        
        # Location
        tk.Label(form, text="Location", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        loc_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        loc_entry.pack(fill='x', pady=(0, 15))
        
        # Commitment
        tk.Label(form, text="Time Commitment", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        commit_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        commit_entry.pack(fill='x', pady=(0, 15))
        commit_entry.insert(0, "Flexible")
        
        # Deadline
        tk.Label(form, text="Application Deadline (YYYY-MM-DD)", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        deadline_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        deadline_entry.pack(fill='x', pady=(0, 15))
        
        # Description
        tk.Label(form, text="Description*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        desc_text = tk.Text(form, width=40, height=5, font=('Helvetica', 11))
        desc_text.pack(fill='x', pady=(0, 20))
        
        def save_opportunity():
            title = title_entry.get().strip()
            opp_type = type_combo.get()
            compensation = comp_entry.get()
            location = loc_entry.get()
            commitment = commit_entry.get()
            deadline = deadline_entry.get() or None
            description = desc_text.get("1.0", tk.END).strip()
            
            if not all([title, opp_type, description]):
                messagebox.showerror("Error", "Please fill required fields")
                return
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    INSERT INTO opportunities (title, type, description, compensation, 
                                             location, commitment, deadline, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (title, opp_type, description, compensation, location, commitment, deadline, self.app.user['id']))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "Opportunity posted successfully!")
                win.destroy()
                self.load_all_opportunities()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to post opportunity: {e}")
            finally:
                cursor.close()
        
        tk.Button(win, text="Publish Opportunity", command=save_opportunity,
                 bg='#10b981', fg='white', font=('Helvetica', 12, 'bold'),
                 width=20, pady=10, cursor='hand2').pack(pady=30)
    
    def edit_opportunity(self, opp):
        win = tk.Toplevel(self.app.root)
        win.title(f"Edit: {opp['title']}")
        win.geometry("600x650")
        win.configure(bg='white')
        
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (600 // 2)
        y = (win.winfo_screenheight() // 2) - (650 // 2)
        win.geometry(f'600x650+{x}+{y}')
        
        tk.Label(win, text="✏️ Edit Opportunity", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=30)
        
        form = tk.Frame(win, bg='white', padx=40)
        form.pack(fill='both', expand=True)
        
        # Title
        tk.Label(form, text="Opportunity Title*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        title_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        title_entry.pack(fill='x', pady=(0, 15))
        title_entry.insert(0, opp['title'])
        
        # Type
        tk.Label(form, text="Type*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        type_combo = ttk.Combobox(form, values=['Job', 'Volunteer', 'Internship', 'Training'], 
                                 width=38, state='readonly')
        type_combo.pack(fill='x', pady=(0, 15))
        type_combo.set(opp['type'])
        
        # Compensation
        tk.Label(form, text="Compensation", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        comp_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        comp_entry.pack(fill='x', pady=(0, 15))
        comp_entry.insert(0, opp['compensation'] or "")
        
        # Location
        tk.Label(form, text="Location", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        loc_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        loc_entry.pack(fill='x', pady=(0, 15))
        loc_entry.insert(0, opp['location'] or "")
        
        # Commitment
        tk.Label(form, text="Time Commitment", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        commit_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        commit_entry.pack(fill='x', pady=(0, 15))
        commit_entry.insert(0, opp['commitment'] or "")
        
        # Deadline
        tk.Label(form, text="Application Deadline (YYYY-MM-DD)", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        deadline_entry = tk.Entry(form, width=40, font=('Helvetica', 12))
        deadline_entry.pack(fill='x', pady=(0, 15))
        if opp['deadline']:
            deadline_entry.insert(0, str(opp['deadline']))
        
        # Status
        tk.Label(form, text="Status*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        status_combo = ttk.Combobox(form, values=['open', 'closed', 'filled'], 
                                   width=38, state='readonly')
        status_combo.pack(fill='x', pady=(0, 15))
        status_combo.set(opp['status'])
        
        # Description
        tk.Label(form, text="Description*", bg='white',
                font=('Helvetica', 11)).pack(anchor='w', pady=(0, 5))
        desc_text = tk.Text(form, width=40, height=5, font=('Helvetica', 11))
        desc_text.pack(fill='x', pady=(0, 20))
        desc_text.insert('1.0', opp['description'] or "")
        
        def update_opportunity():
            title = title_entry.get().strip()
            opp_type = type_combo.get()
            compensation = comp_entry.get()
            location = loc_entry.get()
            commitment = commit_entry.get()
            deadline = deadline_entry.get() or None
            status = status_combo.get()
            description = desc_text.get("1.0", tk.END).strip()
            
            if not all([title, opp_type, description, status]):
                messagebox.showerror("Error", "Please fill required fields")
                return
            
            try:
                cursor = self.app.db.cursor()
                cursor.execute("""
                    UPDATE opportunities 
                    SET title = %s, type = %s, description = %s, compensation = %s, 
                        location = %s, commitment = %s, deadline = %s, status = %s
                    WHERE id = %s
                """, (title, opp_type, description, compensation, location, commitment, deadline, status, opp['id']))
                
                self.app.db.commit()
                messagebox.showinfo("Success", "Opportunity updated successfully!")
                win.destroy()
                self.load_all_opportunities()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update opportunity: {e}")
            finally:
                cursor.close()
        
        tk.Button(win, text="Update Opportunity", command=update_opportunity,
                 bg='#3b82f6', fg='white', font=('Helvetica', 12, 'bold'),
                 width=20, pady=10, cursor='hand2').pack(pady=30)
    
    def close_opportunity(self, opp):
        if messagebox.askyesno("Confirm", f"Close opportunity '{opp['title']}'?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE opportunities SET status = 'closed' WHERE id = %s", (opp['id'],))
                self.app.db.commit()
                messagebox.showinfo("Success", "Opportunity closed")
                self.load_all_opportunities()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to close opportunity: {e}")
            finally:
                cursor.close()
    
    def view_applicants(self, opp):
        win = tk.Toplevel(self.app.root)
        win.title(f"Applicants for: {opp['title']}")
        win.geometry("800x500")
        win.configure(bg='white')
        
        tk.Label(win, text=f"👥 Applicants for {opp['title']}", bg='white',
                font=('Helvetica', 18, 'bold')).pack(pady=20)
        
        # Get applicants
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT oa.*, u.name, u.email, u.phone, u.youth_id
            FROM opportunity_applications oa
            JOIN users u ON oa.user_id = u.id
            WHERE oa.opportunity_id = %s
            ORDER BY oa.application_date DESC
        """, (opp['id'],))
        
        applicants = cursor.fetchall()
        cursor.close()
        
        if not applicants:
            tk.Label(win, text="No applicants yet", bg='white',
                    font=('Helvetica', 14)).pack(pady=50)
            return
        
        # Create treeview
        tree_frame = tk.Frame(win)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Name', 'Youth ID', 'Email', 'Phone', 'Status', 'Date'), show='headings')
        
        tree.heading('Name', text='Name')
        tree.heading('Youth ID', text='Youth ID')
        tree.heading('Email', text='Email')
        tree.heading('Phone', text='Phone')
        tree.heading('Status', text='Status')
        tree.heading('Date', text='Application Date')
        
        for col in tree['columns']:
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for app in applicants:
            date_str = app['application_date'].strftime('%Y-%m-%d')
            tree.insert('', 'end', values=(
                app['name'],
                app['youth_id'],
                app['email'],
                app['phone'] or 'N/A',
                app['status'].title(),
                date_str
            ))
    
    def show_applications(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="📋 Opportunity Applications", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
        # Get all applications
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT oa.*, u.name as youth_name, u.youth_id, o.title as opportunity_title
            FROM opportunity_applications oa
            JOIN users u ON oa.user_id = u.id
            JOIN opportunities o ON oa.opportunity_id = o.id
            ORDER BY oa.application_date DESC
        """)
        
        applications = cursor.fetchall()
        cursor.close()
        
        if not applications:
            tk.Label(self.content, text="No applications found", bg='white',
                    font=('Helvetica', 14)).pack(pady=50)
            return
        
        # Create table
        tree_frame = tk.Frame(self.content)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Opportunity', 'Youth', 'Youth ID', 'Status', 'Date'), show='headings')
        
        tree.heading('Opportunity', text='Opportunity')
        tree.heading('Youth', text='Youth')
        tree.heading('Youth ID', text='Youth ID')
        tree.heading('Status', text='Status')
        tree.heading('Date', text='Application Date')
        
        for col in tree['columns']:
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        for app in applications:
            date_str = app['application_date'].strftime('%Y-%m-%d')
            tree.insert('', 'end', values=(
                app['opportunity_title'],
                app['youth_name'],
                app['youth_id'],
                app['status'].title(),
                date_str
            ))
    
    def show_reports(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="📊 Opportunity Reports", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
        # Get statistics
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_opportunities,
                SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open_opportunities,
                SUM(CASE WHEN status = 'closed' THEN 1 ELSE 0 END) as closed_opportunities,
                SUM(CASE WHEN status = 'filled' THEN 1 ELSE 0 END) as filled_opportunities,
                (SELECT COUNT(*) FROM opportunity_applications) as total_applications
            FROM opportunities
        """)
        
        stats = cursor.fetchone()
        cursor.close()
        
        # Display stats
        stats_frame = tk.Frame(self.content, bg='white')
        stats_frame.pack(pady=20)
        
        stat_cards = [
            ("Total Opportunities", stats['total_opportunities'], "#8b5cf6"),
            ("Open", stats['open_opportunities'], "#10b981"),
            ("Closed", stats['closed_opportunities'], "#ef4444"),
            ("Filled", stats['filled_opportunities'], "#f59e0b"),
            ("Total Applications", stats['total_applications'], "#ec4899")
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