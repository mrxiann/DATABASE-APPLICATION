# feedback_manager.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from tkinter import filedialog

class FeedbackManagement:
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
        
        self.show_feedback()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='white', width=250)
        sidebar.pack(side='left', fill='y')
        
        tk.Label(sidebar, text="SK Portal", bg='white',
                font=('Helvetica', 18, 'bold'), fg='#ec4899').pack(pady=30)
        
        tk.Button(sidebar, text="← Back to Dashboard", 
                 command=lambda: self.app.show_admin_dashboard(self.app.user),
                 bg='white', fg='#ec4899', font=('Helvetica', 11),
                 border=0, cursor='hand2').pack(pady=(0, 30))
        
        menu_items = [
            ("💬 All Feedback", self.show_feedback),
            ("⏳ Pending", self.show_pending),
            ("✅ Resolved", self.show_resolved),
            ("", None),
            ("📊 Analytics", self.show_analytics),
            ("📤 Export", self.export_feedback)
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
    
    def show_feedback(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header = tk.Frame(self.content, bg='white', padx=30, pady=20)
        header.pack(fill='x')
        
        tk.Label(header, text="💬 Feedback Management", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(side='left')
        
        # Filter frame
        filter_frame = tk.Frame(header, bg='white')
        filter_frame.pack(side='right')
        
        # Search
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, width=25, 
                               font=('Helvetica', 11))
        search_entry.pack(side='left', padx=5)
        search_entry.bind('<KeyRelease>', lambda e: self.filter_feedback())
        search_entry.insert(0, "Search feedback...")
        
        # Status filter
        self.status_filter = ttk.Combobox(filter_frame, values=['All', 'pending', 'in progress', 'resolved'], 
                                         width=12, state='readonly')
        self.status_filter.set('All')
        self.status_filter.pack(side='left', padx=5)
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_feedback())
        
        # Type filter
        self.type_filter = ttk.Combobox(filter_frame, values=['All', 'general', 'technical', 'suggestion', 'complaint', 'appreciation'], 
                                       width=12, state='readonly')
        self.type_filter.set('All')
        self.type_filter.pack(side='left', padx=5)
        self.type_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_feedback())
        
        # Feedback cards container
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
        
        # Load all feedback
        self.load_all_feedback()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_all_feedback(self):
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.*, u.name as user_name, u.youth_id
            FROM feedback f
            JOIN users u ON f.user_id = u.id
            ORDER BY f.created_at DESC
        """)
        self.all_feedback = cursor.fetchall()
        cursor.close()
        
        self.filter_feedback()
    
    def filter_feedback(self):
        # Clear existing cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        search_text = self.search_var.get().lower()
        status_filter = self.status_filter.get().lower()
        type_filter = self.type_filter.get().lower()
        
        filtered = []
        for feedback in self.all_feedback:
            matches_search = (not search_text or 
                            search_text in feedback['subject'].lower() or 
                            search_text in feedback['message'].lower() or
                            search_text in feedback['user_name'].lower())
            
            matches_status = (status_filter == 'all' or 
                            feedback['status'].lower() == status_filter)
            
            matches_type = (type_filter == 'all' or 
                           feedback['feedback_type'].lower() == type_filter)
            
            if matches_search and matches_status and matches_type:
                filtered.append(feedback)
        
        if not filtered:
            tk.Label(self.scrollable_frame, text="No feedback found", 
                    bg='#f8fafc', font=('Helvetica', 14), fg='#6b7280').pack(pady=50)
        else:
            for feedback in filtered:
                self.create_feedback_card(feedback)
    
    def create_feedback_card(self, feedback):
        # Colors based on status
        status_colors = {
            'pending': ('#f59e0b', '#fef3c7'),
            'in progress': ('#3b82f6', '#dbeafe'),
            'resolved': ('#10b981', '#d1fae5')
        }
        color, bg_color = status_colors.get(feedback['status'], ('#6b7280', '#f3f4f6'))
        
        # Type colors
        type_colors = {
            'general': ('#6b7280', '#f3f4f6'),
            'technical': ('#3b82f6', '#dbeafe'),
            'suggestion': ('#10b981', '#d1fae5'),
            'complaint': ('#ef4444', '#fee2e2'),
            'appreciation': ('#f59e0b', '#fef3c7')
        }
        type_color, type_bg_color = type_colors.get(feedback['feedback_type'], ('#6b7280', '#f3f4f6'))
        
        # Create card
        card = tk.Frame(self.scrollable_frame, bg='white', relief='flat', borderwidth=0)
        card.pack(fill='x', pady=10)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=20)
        inner.pack(fill='x', padx=1, pady=1)
        
        # Top row
        top_row = tk.Frame(inner, bg='white')
        top_row.pack(fill='x', pady=(0, 10))
        
        tk.Label(top_row, text=feedback['subject'], bg='white',
                font=('Helvetica', 14, 'bold'), fg='#1e293b').pack(side='left')
        
        # Status and type badges
        badges_frame = tk.Frame(top_row, bg='white')
        badges_frame.pack(side='right')
        
        # Status badge
        status_frame = tk.Frame(badges_frame, bg=bg_color)
        status_frame.pack(side='left', padx=5)
        tk.Label(status_frame, text=feedback['status'].upper(), bg=bg_color, fg=color,
                font=('Helvetica', 9, 'bold'), padx=8, pady=2).pack()
        
        # Type badge
        type_frame = tk.Frame(badges_frame, bg=type_bg_color)
        type_frame.pack(side='left', padx=5)
        tk.Label(type_frame, text=feedback['feedback_type'].upper(), bg=type_bg_color, fg=type_color,
                font=('Helvetica', 9, 'bold'), padx=8, pady=2).pack()
        
        # User info
        user_frame = tk.Frame(inner, bg='white')
        user_frame.pack(anchor='w', pady=(0, 5))
        
        tk.Label(user_frame, text=f"👤 {feedback['user_name']}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left', padx=(0, 15))
        
        if feedback['youth_id']:
            tk.Label(user_frame, text=f"ID: {feedback['youth_id']}", bg='white',
                    font=('Helvetica', 10), fg='#9ca3af').pack(side='left')
        
        # Date and linked item info
        info_frame = tk.Frame(inner, bg='white')
        info_frame.pack(anchor='w', pady=(0, 15))
        
        date_str = feedback['created_at'].strftime('%b %d, %Y %H:%M')
        tk.Label(info_frame, text=f"📅 {date_str}", bg='white',
                font=('Helvetica', 10), fg='#64748b').pack(side='left', padx=(0, 15))
        
        if feedback['linked_item_id'] and feedback['linked_item_type']:
            linked_text = f"🔗 {feedback['linked_item_type']}: {feedback['linked_item_id']}"
            tk.Label(info_frame, text=linked_text, bg='white',
                    font=('Helvetica', 10), fg='#64748b').pack(side='left')
        
        # Message preview (truncated)
        message_preview = feedback['message'][:200] + "..." if len(feedback['message']) > 200 else feedback['message']
        tk.Label(inner, text=message_preview, bg='white',
                font=('Helvetica', 11), fg='#4b5563', wraplength=800,
                justify='left').pack(anchor='w', pady=(0, 15))
        
        # Admin reply preview if exists
        if feedback['admin_reply']:
            reply_preview = feedback['admin_reply'][:150] + "..." if len(feedback['admin_reply']) > 150 else feedback['admin_reply']
            reply_frame = tk.Frame(inner, bg='#f0f9ff', relief='solid', borderwidth=1)
            reply_frame.pack(fill='x', pady=(0, 15))
            
            tk.Label(reply_frame, text=f"📝 Admin Reply: {reply_preview}", bg='#f0f9ff',
                    font=('Helvetica', 10), fg='#3b82f6', wraplength=780,
                    justify='left', padx=10, pady=8).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(inner, bg='white')
        btn_frame.pack(fill='x')
        
        if feedback['status'] != 'resolved':
            tk.Button(btn_frame, text="View & Respond", 
                     command=lambda f=feedback: self.view_feedback(f),
                     bg='#ec4899', fg='white', font=('Helvetica', 10),
                     padx=15, pady=5, cursor='hand2').pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="Mark In Progress", 
                     command=lambda f=feedback: self.mark_in_progress(f),
                     bg='#3b82f6', fg='white', font=('Helvetica', 10),
                     padx=15, pady=5, cursor='hand2').pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="Mark Resolved", 
                     command=lambda f=feedback: self.mark_resolved(f),
                     bg='#10b981', fg='white', font=('Helvetica', 10),
                     padx=15, pady=5, cursor='hand2').pack(side='left', padx=2)
        else:
            tk.Button(btn_frame, text="View Details", 
                     command=lambda f=feedback: self.view_feedback(f),
                     bg='#6b7280', fg='white', font=('Helvetica', 10),
                     padx=15, pady=5, cursor='hand2').pack(side='left', padx=2)
            
            tk.Button(btn_frame, text="Re-open", 
                     command=lambda f=feedback: self.reopen_feedback(f),
                     bg='#f59e0b', fg='white', font=('Helvetica', 10),
                     padx=15, pady=5, cursor='hand2').pack(side='left', padx=2)
    
    def view_feedback(self, feedback):
        win = tk.Toplevel(self.root)
        win.title(f"Feedback: {feedback['subject']}")
        win.geometry("700x600")
        win.configure(bg='white')
        
        # Center window
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (700 // 2)
        y = (win.winfo_screenheight() // 2) - (600 // 2)
        win.geometry(f'700x600+{x}+{y}')
        
        # Header
        tk.Label(win, text="💬 Feedback Details", bg='white',
                font=('Helvetica', 20, 'bold')).pack(pady=20)
        
        # Content frame
        content = tk.Frame(win, bg='white', padx=40)
        content.pack(fill='both', expand=True)
        
        # Subject
        tk.Label(content, text="Subject:", bg='white',
                font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        tk.Label(content, text=feedback['subject'], bg='white',
                font=('Helvetica', 14), fg='#1e293b', wraplength=600,
                justify='left').pack(anchor='w', pady=(0, 15))
        
        # User info
        info_frame = tk.Frame(content, bg='white')
        info_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(info_frame, text=f"From: {feedback['user_name']}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left', padx=(0, 20))
        
        tk.Label(info_frame, text=f"Type: {feedback['feedback_type']}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left', padx=(0, 20))
        
        date_str = feedback['created_at'].strftime('%B %d, %Y at %I:%M %p')
        tk.Label(info_frame, text=f"Date: {date_str}", bg='white',
                font=('Helvetica', 11), fg='#64748b').pack(side='left')
        
        # Message
        tk.Label(content, text="Message:", bg='white',
                font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        
        message_frame = tk.Frame(content, bg='#f8fafc', relief='sunken', borderwidth=1)
        message_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        message_text = tk.Text(message_frame, wrap='word', font=('Helvetica', 11),
                              bg='#f8fafc', relief='flat', height=6)
        message_text.insert('1.0', feedback['message'])
        message_text.config(state='disabled')
        
        scrollbar = tk.Scrollbar(message_frame, orient='vertical', command=message_text.yview)
        message_text.configure(yscrollcommand=scrollbar.set)
        
        message_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Admin reply section (if any)
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
        
        # Update status section
        if feedback['status'] != 'resolved':
            tk.Label(content, text="Update Status:", bg='white',
                    font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(10, 5))
            
            status_frame = tk.Frame(content, bg='white')
            status_frame.pack(fill='x', pady=(0, 10))
            
            self.status_var = tk.StringVar(value=feedback['status'])
            
            tk.Radiobutton(status_frame, text="In Progress", variable=self.status_var,
                          value='in progress', bg='white', font=('Helvetica', 11)).pack(side='left', padx=10)
            tk.Radiobutton(status_frame, text="Resolved", variable=self.status_var,
                          value='resolved', bg='white', font=('Helvetica', 11)).pack(side='left', padx=10)
            
            # Reply text
            tk.Label(content, text="Admin Reply:", bg='white',
                    font=('Helvetica', 11)).pack(anchor='w', pady=(10, 5))
            
            self.reply_text = tk.Text(content, height=4, font=('Helvetica', 11))
            self.reply_text.pack(fill='x', pady=(0, 20))
            
            # Buttons
            btn_frame = tk.Frame(content, bg='white')
            btn_frame.pack(fill='x')
            
            tk.Button(btn_frame, text="Save & Send Reply", 
                     command=lambda: self.update_feedback(feedback, win),
                     bg='#10b981', fg='white', font=('Helvetica', 11),
                     padx=20, cursor='hand2').pack(side='left', padx=5)
            
            tk.Button(btn_frame, text="Cancel", command=win.destroy,
                     bg='#6b7280', fg='white', font=('Helvetica', 11),
                     padx=20, cursor='hand2').pack(side='left', padx=5)
        else:
            # For resolved feedback, show option to re-open
            tk.Label(content, text="This feedback has been resolved.", bg='white',
                    font=('Helvetica', 11), fg='#10b981').pack(pady=(10, 5))
            
            btn_frame = tk.Frame(content, bg='white')
            btn_frame.pack(fill='x', pady=20)
            
            tk.Button(btn_frame, text="Re-open", 
                     command=lambda: self.reopen_feedback(feedback, win),
                     bg='#f59e0b', fg='white', font=('Helvetica', 11),
                     padx=20, cursor='hand2').pack(side='left', padx=5)
            
            tk.Button(btn_frame, text="Close", command=win.destroy,
                     bg='#6b7280', fg='white', font=('Helvetica', 11),
                     padx=20, cursor='hand2').pack(side='left', padx=5)
    
    def update_feedback(self, feedback, window):
        status = self.status_var.get()
        reply = self.reply_text.get("1.0", tk.END).strip()
        
        try:
            cursor = self.app.db.cursor()
            cursor.execute("""
                UPDATE feedback 
                SET status = %s, admin_reply = %s, updated_at = NOW()
                WHERE id = %s
            """, (status, reply, feedback['id']))
            
            self.app.db.commit()
            cursor.close()
            
            messagebox.showinfo("Success", "Feedback updated successfully!")
            window.destroy()
            self.load_all_feedback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {e}")
    
    def mark_in_progress(self, feedback):
        if messagebox.askyesno("Confirm", f"Mark '{feedback['subject']}' as in progress?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE feedback SET status = 'in progress', updated_at = NOW() WHERE id = %s", 
                              (feedback['id'],))
                self.app.db.commit()
                cursor.close()
                messagebox.showinfo("Success", "Feedback marked as in progress")
                self.load_all_feedback()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {e}")
    
    def mark_resolved(self, feedback):
        if messagebox.askyesno("Confirm", f"Mark '{feedback['subject']}' as resolved?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE feedback SET status = 'resolved', updated_at = NOW() WHERE id = %s", 
                              (feedback['id'],))
                self.app.db.commit()
                cursor.close()
                messagebox.showinfo("Success", "Feedback marked as resolved")
                self.load_all_feedback()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {e}")
    
    def reopen_feedback(self, feedback, window=None):
        if messagebox.askyesno("Confirm", f"Re-open '{feedback['subject']}'?"):
            try:
                cursor = self.app.db.cursor()
                cursor.execute("UPDATE feedback SET status = 'pending', updated_at = NOW() WHERE id = %s", 
                              (feedback['id'],))
                self.app.db.commit()
                cursor.close()
                messagebox.showinfo("Success", "Feedback re-opened")
                
                if window:
                    window.destroy()
                self.load_all_feedback()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to re-open: {e}")
    
    def show_pending(self):
        # Set filters to show only pending feedback
        self.status_filter.set('pending')
        self.filter_feedback()
    
    def show_resolved(self):
        # Set filters to show only resolved feedback
        self.status_filter.set('resolved')
        self.filter_feedback()
    
    def show_analytics(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        tk.Label(self.content, text="📊 Feedback Analytics", bg='white',
                font=('Helvetica', 24, 'bold'), fg='#1e293b').pack(pady=20)
        
        # Get statistics
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_feedback,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'in progress' THEN 1 ELSE 0 END) as in_progress,
                SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) as resolved,
                AVG(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) * 100 as resolution_rate,
                (SELECT COUNT(DISTINCT user_id) FROM feedback) as unique_users
            FROM feedback
        """)
        
        stats = cursor.fetchone()
        
        # Get feedback by type
        cursor.execute("""
            SELECT feedback_type, COUNT(*) as count
            FROM feedback
            GROUP BY feedback_type
            ORDER BY count DESC
        """)
        
        type_stats = cursor.fetchall()
        
        # Get feedback by month
        cursor.execute("""
            SELECT DATE_FORMAT(created_at, '%Y-%m') as month, COUNT(*) as count
            FROM feedback
            GROUP BY DATE_FORMAT(created_at, '%Y-%m')
            ORDER BY month DESC
            LIMIT 6
        """)
        
        month_stats = cursor.fetchall()
        cursor.close()
        
        # Display main stats
        stats_frame = tk.Frame(self.content, bg='white')
        stats_frame.pack(pady=20)
        
        main_stats = [
            ("Total Feedback", stats['total_feedback'] or 0, "#ec4899"),
            ("Pending", stats['pending'] or 0, "#f59e0b"),
            ("In Progress", stats['in_progress'] or 0, "#3b82f6"),
            ("Resolved", stats['resolved'] or 0, "#10b981"),
            ("Resolution Rate", f"{stats['resolution_rate'] or 0:.1f}%", "#8b5cf6"),
            ("Unique Users", stats['unique_users'] or 0, "#6366f1")
        ]
        
        for i, (title, value, color) in enumerate(main_stats):
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
        
        # Display type distribution
        type_frame = tk.Frame(self.content, bg='white')
        type_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(type_frame, text="Feedback by Type", bg='white',
                font=('Helvetica', 16, 'bold')).pack(anchor='w', pady=(0, 10))
        
        for type_stat in type_stats:
            type_row = tk.Frame(type_frame, bg='white')
            type_row.pack(fill='x', pady=2)
            
            tk.Label(type_row, text=type_stat['feedback_type'].title(), bg='white',
                    font=('Helvetica', 11), width=15, anchor='w').pack(side='left')
            
            # Progress bar
            progress_frame = tk.Frame(type_row, bg='#e5e7eb', height=20)
            progress_frame.pack(side='left', fill='x', expand=True, padx=10)
            progress_frame.pack_propagate(False)
            
            if stats['total_feedback'] > 0:
                percentage = (type_stat['count'] / stats['total_feedback']) * 100
                progress_width = int(percentage * 2)  # Scale factor for visual width
                
                color = self.get_type_color(type_stat['feedback_type'])
                progress_bar = tk.Frame(progress_frame, bg=color, width=progress_width)
                progress_bar.pack(side='left', fill='y')
            
            tk.Label(type_row, text=f"{type_stat['count']} ({percentage:.1f}%)", bg='white',
                    font=('Helvetica', 11), width=10).pack(side='right')
        
        # Display monthly trend
        trend_frame = tk.Frame(self.content, bg='white')
        trend_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(trend_frame, text="Monthly Trend (Last 6 months)", bg='white',
                font=('Helvetica', 16, 'bold')).pack(anchor='w', pady=(0, 10))
        
        if month_stats:
            max_count = max([m['count'] for m in month_stats])
            
            for month_stat in month_stats:
                month_row = tk.Frame(trend_frame, bg='white')
                month_row.pack(fill='x', pady=2)
                
                tk.Label(month_row, text=month_stat['month'], bg='white',
                        font=('Helvetica', 11), width=10, anchor='w').pack(side='left')
                
                # Progress bar
                progress_frame = tk.Frame(month_row, bg='#e5e7eb', height=20)
                progress_frame.pack(side='left', fill='x', expand=True, padx=10)
                progress_frame.pack_propagate(False)
                
                if max_count > 0:
                    percentage = (month_stat['count'] / max_count) * 100
                    progress_width = int(percentage * 2)  # Scale factor for visual width
                    
                    progress_bar = tk.Frame(progress_frame, bg='#ec4899', width=progress_width)
                    progress_bar.pack(side='left', fill='y')
                
                tk.Label(month_row, text=f"{month_stat['count']} feedback", bg='white',
                        font=('Helvetica', 11), width=15).pack(side='right')
    
    def get_type_color(self, feedback_type):
        type_colors = {
            'general': '#6b7280',
            'technical': '#3b82f6',
            'suggestion': '#10b981',
            'complaint': '#ef4444',
            'appreciation': '#f59e0b'
        }
        return type_colors.get(feedback_type, '#6b7280')
    
    def export_feedback(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Feedback Data"
        )
        
        if not file_path:
            return
        
        cursor = self.app.db.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.id, f.subject, f.message, f.feedback_type, f.status,
                   f.admin_reply, f.created_at, f.updated_at,
                   u.name as user_name, u.youth_id, u.email
            FROM feedback f
            JOIN users u ON f.user_id = u.id
            ORDER BY f.created_at DESC
        """)
        
        feedback_list = cursor.fetchall()
        cursor.close()
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['ID', 'Subject', 'Message', 'Type', 'Status', 'Admin Reply',
                             'Created At', 'Updated At', 'User Name', 'Youth ID', 'Email']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for feedback in feedback_list:
                    writer.writerow({
                        'ID': feedback['id'],
                        'Subject': feedback['subject'],
                        'Message': feedback['message'],
                        'Type': feedback['feedback_type'],
                        'Status': feedback['status'],
                        'Admin Reply': feedback['admin_reply'] or '',
                        'Created At': feedback['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
                        'Updated At': feedback['updated_at'].strftime('%Y-%m-%d %H:%M:%S') if feedback['updated_at'] else '',
                        'User Name': feedback['user_name'],
                        'Youth ID': feedback['youth_id'] or '',
                        'Email': feedback['email']
                    })
            
            messagebox.showinfo("Success", f"Feedback data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")