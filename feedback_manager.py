import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
from tkinter import filedialog
from ui_utils import ModernButton, ModernCard, ModernEntry, create_modern_combobox, create_stat_card

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
        self.content.pack(side='right', fill='both', expand=True)
        
        self.show_feedback()
    
    def create_sidebar(self):
        sidebar = tk.Frame(self.main, bg='white', width=280)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Logo/Header
        header = tk.Frame(sidebar, bg='#ec4899', height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="Feedback Management", bg='#ec4899', fg='white',
                font=('Segoe UI', 18, 'bold')).pack(expand=True, pady=(30, 5))
        
        # Back button
        back_btn = tk.Label(header, text="← Back to Dashboard", bg='#ec4899',
                           fg='#fce7f3', font=('Segoe UI', 10), cursor='hand2')
        back_btn.pack(pady=(0, 20))
        back_btn.bind("<Button-1>", lambda e: self.app.show_admin_dashboard(self.app.user))
        back_btn.bind("<Enter>", lambda e: back_btn.config(fg='white'))
        back_btn.bind("<Leave>", lambda e: back_btn.config(fg='#fce7f3'))
        
        # Navigation Menu
        nav_frame = tk.Frame(sidebar, bg='white')
        nav_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        menu_items = [
            ("💬", "All Feedback", self.show_feedback, True),
            ("⏳", "Pending", self.show_pending, False),
            ("✅", "Resolved", self.show_resolved, False),
            ("", "", None, False),  # Separator
            ("📊", "Analytics", self.show_analytics, False),
            ("📤", "Export", self.export_feedback, False)
        ]
        
        for icon, text, command, active in menu_items:
            if text == "":
                tk.Frame(nav_frame, bg='#f1f5f9', height=1).pack(fill='x', pady=15)
            else:
                btn_frame = tk.Frame(nav_frame, bg='white')
                btn_frame.pack(fill='x', pady=2)
                
                btn = tk.Label(btn_frame, text=f"{icon} {text}", bg='white' if not active else '#fdf2f8',
                             fg='#374151' if not active else '#ec4899', font=('Segoe UI', 11),
                             cursor='hand2', anchor='w')
                btn.pack(fill='x', padx=10, pady=10)
                
                if command:
                    btn.bind("<Button-1>", lambda e, c=command: c())
                    btn.bind("<Enter>", lambda e, b=btn, active=active: 
                            b.config(bg='#f8fafc') if not active else None)
                    btn.bind("<Leave>", lambda e, b=btn, active=active: 
                            b.config(bg='white' if not active else '#fdf2f8'))
    
    def show_feedback(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Header
        header_frame = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=30)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="💬 Feedback Management", bg='#f8fafc',
                font=('Segoe UI', 28, 'bold'), fg='#1e293b').pack(side='left')
        
        # Search and filter
        filter_frame = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=(0, 20))
        filter_frame.pack(fill='x')
        
        # Search
        search_container = tk.Frame(filter_frame, bg='#f8fafc')
        search_container.pack(side='left')
        
        tk.Label(search_container, text="Search:", bg='#f8fafc',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ModernEntry(search_container, width=25, font=('Segoe UI', 11),
                                  placeholder="Search feedback...")
        search_entry.pack(side='left')
        search_entry.entry.bind('<KeyRelease>', lambda e: self.filter_feedback())
        self.search_entry = search_entry
        
        # Filters
        filters_container = tk.Frame(filter_frame, bg='#f8fafc')
        filters_container.pack(side='right')
        
        # Status filter
        tk.Label(filters_container, text="Status:", bg='#f8fafc',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left', padx=(0, 5))
        
        self.status_filter = create_modern_combobox(filters_container, 
                                                   ['All', 'pending', 'in progress', 'resolved'], 
                                                   width=12)
        self.status_filter.pack(side='left', padx=(0, 10))
        self.status_filter.set('All')
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_feedback())
        
        # Type filter
        tk.Label(filters_container, text="Type:", bg='#f8fafc',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left', padx=(0, 5))
        
        self.type_filter = create_modern_combobox(filters_container, 
                                                 ['All', 'general', 'technical', 'suggestion', 'complaint', 'appreciation'], 
                                                 width=12)
        self.type_filter.set('All')
        self.type_filter.pack(side='left')
        self.type_filter.bind('<<ComboboxSelected>>', lambda e: self.filter_feedback())
        
        # Feedback cards container
        feedback_container = ModernCard(self.content, padx=0, pady=0)
        feedback_container.pack(fill='both', expand=True, padx=30, pady=(0, 30))
        
        # Create scrollable canvas
        canvas_frame = tk.Frame(feedback_container, bg='white')
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
        
        # Load all feedback
        self.load_all_feedback()
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_modern_feedback_card(self, feedback):
        """Create a modern feedback card"""
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
        
        # Main card
        card = tk.Frame(self.scrollable_frame, bg='white', relief='flat',
                       highlightbackground='#e5e7eb', highlightthickness=1)
        card.pack(fill='x', pady=8, padx=2)
        
        inner = tk.Frame(card, bg='white', padx=20, pady=20)
        inner.pack(fill='x')
        
        # Top row: Subject and badges
        top_row = tk.Frame(inner, bg='white')
        top_row.pack(fill='x', pady=(0, 15))
        
        # Subject
        subject_label = tk.Label(top_row, text=feedback['subject'], bg='white',
                               font=('Segoe UI', 14, 'bold'), fg='#1e293b',
                               wraplength=400, justify='left')
        subject_label.pack(side='left')
        
        # Badges
        badges_frame = tk.Frame(top_row, bg='white')
        badges_frame.pack(side='right')
        
        # Status badge
        status_badge = tk.Frame(badges_frame, bg=bg_color)
        status_badge.pack(side='left', padx=(5, 0))
        tk.Label(status_badge, text=feedback['status'].upper(), bg=bg_color, fg=color,
                font=('Segoe UI', 8, 'bold'), padx=8, pady=2).pack()
        
        # Type badge
        type_badge = tk.Frame(badges_frame, bg=type_bg_color)
        type_badge.pack(side='left', padx=(5, 0))
        tk.Label(type_badge, text=feedback['feedback_type'].upper(), bg=type_bg_color, fg=type_color,
                font=('Segoe UI', 8, 'bold'), padx=8, pady=2).pack()
        
        # User info
        user_frame = tk.Frame(inner, bg='white')
        user_frame.pack(anchor='w', pady=(0, 10))
        
        tk.Label(user_frame, text=f"👤 {feedback['user_name']}", bg='white',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left', padx=(0, 15))
        
        if feedback['youth_id']:
            tk.Label(user_frame, text=f"ID: {feedback['youth_id']}", bg='white',
                    font=('Segoe UI', 10), fg='#9ca3af').pack(side='left')
        
        # Date and linked item
        info_frame = tk.Frame(inner, bg='white')
        info_frame.pack(anchor='w', pady=(0, 15))
        
        date_str = feedback['created_at'].strftime('%b %d, %Y %H:%M')
        tk.Label(info_frame, text=f"📅 {date_str}", bg='white',
                font=('Segoe UI', 10), fg='#64748b').pack(side='left', padx=(0, 15))
        
        if feedback['linked_item_id'] and feedback['linked_item_type']:
            linked_text = f"🔗 {feedback['linked_item_type']}: {feedback['linked_item_id']}"
            tk.Label(info_frame, text=linked_text, bg='white',
                    font=('Segoe UI', 10), fg='#64748b').pack(side='left')
        
        # Message preview
        message_preview = feedback['message'][:200] + "..." if len(feedback['message']) > 200 else feedback['message']
        message_frame = tk.Frame(inner, bg='#f8fafc', relief='flat',
                                highlightbackground='#e5e7eb', highlightthickness=1)
        message_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(message_frame, text=message_preview, bg='#f8fafc',
                font=('Segoe UI', 11), fg='#4b5563', wraplength=600,
                justify='left', padx=10, pady=10).pack(anchor='w')
        
        # Admin reply preview if exists
        if feedback['admin_reply']:
            reply_preview = feedback['admin_reply'][:150] + "..." if len(feedback['admin_reply']) > 150 else feedback['admin_reply']
            reply_frame = tk.Frame(inner, bg='#e0f2fe', relief='flat',
                                  highlightbackground='#bae6fd', highlightthickness=1)
            reply_frame.pack(fill='x', pady=(0, 15))
            
            tk.Label(reply_frame, text=f"📝 Admin Reply: {reply_preview}", bg='#e0f2fe',
                    font=('Segoe UI', 10), fg='#0c4a6e', wraplength=580,
                    justify='left', padx=10, pady=8).pack(anchor='w')
        
        # Action buttons
        btn_frame = tk.Frame(inner, bg='white')
        btn_frame.pack(fill='x')
        
        if feedback['status'] != 'resolved':
            view_btn = ModernButton(btn_frame, text="View & Respond", 
                                   command=lambda f=feedback: self.view_feedback(f),
                                   width=120, height=32, bg='#ec4899', fg='white',
                                   font=('Segoe UI', 10), radius=6)
            view_btn.pack(side='left', padx=(0, 5))
            
            progress_btn = ModernButton(btn_frame, text="Mark In Progress", 
                                       command=lambda f=feedback: self.mark_in_progress(f),
                                       width=130, height=32, bg='#3b82f6', fg='white',
                                       font=('Segoe UI', 10), radius=6)
            progress_btn.pack(side='left', padx=(0, 5))
            
            resolve_btn = ModernButton(btn_frame, text="Mark Resolved", 
                                      command=lambda f=feedback: self.mark_resolved(f),
                                      width=120, height=32, bg='#10b981', fg='white',
                                      font=('Segoe UI', 10), radius=6)
            resolve_btn.pack(side='left', padx=(0, 5))
        else:
            view_btn = ModernButton(btn_frame, text="View Details", 
                                   command=lambda f=feedback: self.view_feedback(f),
                                   width=100, height=32, bg='#6b7280', fg='white',
                                   font=('Segoe UI', 10), radius=6)
            view_btn.pack(side='left', padx=(0, 5))
            
            reopen_btn = ModernButton(btn_frame, text="Re-open", 
                                     command=lambda f=feedback: self.reopen_feedback(f),
                                     width=80, height=32, bg='#f59e0b', fg='white',
                                     font=('Segoe UI', 10), radius=6)
            reopen_btn.pack(side='left', padx=(0, 5))
    
    # REST OF THE METHODS (load_all_feedback, filter_feedback, view_feedback, etc.)
    # KEEP THE SAME BACKEND LOGIC, UPDATE UI COMPONENTS TO USE MODERN STYLING
    
    def view_feedback(self, feedback):
        # Modern modal window
        win = tk.Toplevel(self.root)
        win.title(f"Feedback: {feedback['subject']}")
        win.geometry("600x700")
        win.configure(bg='white')
        win.resizable(False, False)
        
        # Center window
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')
        
        # Header
        header = tk.Frame(win, bg='#ec4899', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="💬 Feedback Details", 
                font=('Segoe UI', 18, 'bold'), bg='#ec4899', fg='white').pack(expand=True)
        
        close_btn = tk.Label(header, text="✕", font=('Segoe UI', 16), 
                           bg='#ec4899', fg='white', cursor='hand2')
        close_btn.place(relx=0.95, rely=0.5, anchor='center')
        close_btn.bind("<Button-1>", lambda e: win.destroy())
        
        # Content frame
        content = tk.Frame(win, bg='white')
        content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Subject
        tk.Label(content, text="Subject:", bg='white',
                font=('Segoe UI', 12, 'bold'), fg='#475569').pack(anchor='w', pady=(0, 5))
        tk.Label(content, text=feedback['subject'], bg='white',
                font=('Segoe UI', 14), fg='#1e293b', wraplength=500,
                justify='left').pack(anchor='w', pady=(0, 15))
        
        # User info with modern styling
        info_card = tk.Frame(content, bg='#f8fafc', relief='flat',
                            highlightbackground='#e5e7eb', highlightthickness=1)
        info_card.pack(fill='x', pady=(0, 20))
        
        info_inner = tk.Frame(info_card, bg='#f8fafc', padx=15, pady=15)
        info_inner.pack(fill='x')
        
        tk.Label(info_inner, text=f"From: {feedback['user_name']}", bg='#f8fafc',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left', padx=(0, 20))
        
        tk.Label(info_inner, text=f"Type: {feedback['feedback_type']}", bg='#f8fafc',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left', padx=(0, 20))
        
        date_str = feedback['created_at'].strftime('%B %d, %Y at %I:%M %p')
        tk.Label(info_inner, text=f"Date: {date_str}", bg='#f8fafc',
                font=('Segoe UI', 11), fg='#64748b').pack(side='left')
        
        # Message
        tk.Label(content, text="Message:", bg='white',
                font=('Segoe UI', 12, 'bold'), fg='#475569').pack(anchor='w', pady=(0, 5))
        
        message_frame = tk.Frame(content, bg='#f8fafc', relief='flat',
                                highlightbackground='#e5e7eb', highlightthickness=1)
        message_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        message_text = tk.Text(message_frame, wrap='word', font=('Segoe UI', 11),
                              bg='#f8fafc', relief='flat', height=8)
        message_text.insert('1.0', feedback['message'])
        message_text.config(state='disabled')
        
        scrollbar = tk.Scrollbar(message_frame, orient='vertical', command=message_text.yview)
        message_text.configure(yscrollcommand=scrollbar.set)
        
        message_text.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
        # Update status section (if not resolved)
        if feedback['status'] != 'resolved':
            tk.Label(content, text="Update Status:", bg='white',
                    font=('Segoe UI', 12, 'bold'), fg='#475569').pack(anchor='w', pady=(10, 5))
            
            status_frame = tk.Frame(content, bg='white')
            status_frame.pack(fill='x', pady=(0, 10))
            
            self.status_var = tk.StringVar(value=feedback['status'])
            
            # Modern radio buttons
            for text, value in [("In Progress", 'in progress'), ("Resolved", 'resolved')]:
                rb_frame = tk.Frame(status_frame, bg='white')
                rb_frame.pack(side='left', padx=(0, 15))
                
                canvas = tk.Canvas(rb_frame, width=20, height=20, bg='white', highlightthickness=0)
                canvas.pack(side='left')
                
                # Create radio button
                indicator = canvas.create_oval(2, 2, 18, 18, outline='#cbd5e1', width=2, fill='white')
                inner = canvas.create_oval(6, 6, 14, 14, outline='', fill='#ec4899' if value == self.status_var.get() else 'white')
                
                def make_cmd(v, c=canvas, i=inner, ind=indicator):
                    return lambda: [self.status_var.set(v), 
                                   c.itemconfig(i, fill='#ec4899' if self.status_var.get() == v else 'white'),
                                   c.itemconfig(ind, outline='#ec4899' if self.status_var.get() == v else '#cbd5e1')]
                
                canvas.bind("<Button-1>", lambda e, v=value: make_cmd(v)())
                canvas.bind("<Enter>", lambda e, c=canvas, ind=indicator: 
                           c.itemconfig(ind, outline='#94a3b8' if self.status_var.get() != value else '#ec4899'))
                canvas.bind("<Leave>", lambda e, c=canvas, ind=indicator: 
                           c.itemconfig(ind, outline='#ec4899' if self.status_var.get() == value else '#cbd5e1'))
                
                tk.Label(rb_frame, text=text, bg='white', font=('Segoe UI', 11), 
                        fg='#475569').pack(side='left', padx=(8, 0))
            
            # Reply text
            tk.Label(content, text="Admin Reply:", bg='white',
                    font=('Segoe UI', 11), fg='#475569').pack(anchor='w', pady=(10, 5))
            
            self.reply_text = tk.Text(content, height=4, font=('Segoe UI', 11),
                                     relief='flat', bg='white', highlightthickness=1,
                                     highlightbackground='#cbd5e1', highlightcolor='#4f46e5')
            self.reply_text.pack(fill='x', pady=(0, 20))
            
            # Buttons
            btn_frame = tk.Frame(content, bg='white')
            btn_frame.pack(fill='x')
            
            save_btn = ModernButton(btn_frame, text="Save & Send Reply", 
                                   command=lambda: self.update_feedback(feedback, win),
                                   width=150, height=38, bg='#10b981', fg='white',
                                   font=('Segoe UI', 11, 'bold'), radius=8)
            save_btn.pack(side='left', padx=(0, 10))
            
            cancel_btn = ModernButton(btn_frame, text="Cancel", command=win.destroy,
                                     width=100, height=38, bg='#6b7280', fg='white',
                                     font=('Segoe UI', 11), radius=8)
            cancel_btn.pack(side='left')
        
        # KEEP THE REST OF THE METHOD WITH ORIGINAL BACKEND LOGIC
        # Only update the UI components
    
    def show_analytics(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Modern header
        header_frame = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=30)
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="📊 Feedback Analytics", bg='#f8fafc',
                font=('Segoe UI', 28, 'bold'), fg='#1e293b').pack(side='left')
        
        # Get statistics (same backend logic)
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
        cursor.close()
        
        # Modern stats cards
        stats_container = tk.Frame(self.content, bg='#f8fafc', padx=30, pady=20)
        stats_container.pack(fill='x')
        
        main_stats = [
            ("Total Feedback", stats['total_feedback'] or 0, "#ec4899", "💬"),
            ("Pending", stats['pending'] or 0, "#f59e0b", "⏳"),
            ("In Progress", stats['in_progress'] or 0, "#3b82f6", "🔄"),
            ("Resolved", stats['resolved'] or 0, "#10b981", "✅"),
            ("Resolution Rate", f"{stats['resolution_rate'] or 0:.1f}%", "#8b5cf6", "📈"),
            ("Unique Users", stats['unique_users'] or 0, "#6366f1", "👥")
        ]
        
        # Create cards in a 3x2 grid
        cards_frame = tk.Frame(stats_container, bg='#f8fafc')
        cards_frame.pack()
        
        for i, (title, value, color, icon) in enumerate(main_stats):
            row, col = divmod(i, 3)
            
            if col == 0:
                cards_frame.columnconfigure(0, weight=1)
            if col == 1:
                cards_frame.columnconfigure(1, weight=1)
            if col == 2:
                cards_frame.columnconfigure(2, weight=1)
            
            card = create_stat_card(cards_frame, title, value, color, icon)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')