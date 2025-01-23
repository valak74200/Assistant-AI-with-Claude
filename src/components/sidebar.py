# src/components/sidebar.py

import tkinter as tk
from tkinter import ttk
from .modern_button import ModernButton

class Sidebar(tk.Frame):
    def __init__(self, master, theme, on_new_chat, on_select_chat):
        super().__init__(
            master,
            bg=theme['bg_color'],
            width=280  # Increased width
        )
        self.theme = theme
        self.on_new_chat = on_new_chat
        self.on_select_chat = on_select_chat
        
        # Don't shrink
        self.pack_propagate(False)
        
        # Main content container
        content = tk.Frame(
            self,
            bg=theme['bg_color']
        )
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # New chat button
        new_chat_btn = ModernButton(
            content,
            text="+ Nouvelle discussion",
            command=on_new_chat,
            theme=theme,
            font=('Segoe UI', 11, 'bold'),
            height=40
        )
        new_chat_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Search container
        search_container = tk.Frame(
            content,
            bg=theme['input_bg'],
            padx=10,
            pady=8
        )
        search_container.pack(fill=tk.X, pady=(0, 15))
        
        # Search icon
        search_label = tk.Label(
            search_container,
            text="🔍",
            font=('Segoe UI', 11),
            bg=theme['input_bg'],
            fg='#888888'
        )
        search_label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Search input
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self._filter_conversations)
        
        self.search_entry = tk.Entry(
            search_container,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            bg=theme['input_bg'],
            fg=theme['text_color'],
            insertbackground=theme['text_color'],
            relief=tk.FLAT,
            width=20
        )
        self.search_entry.pack(fill=tk.X, expand=True)
        
        # Conversations container
        self.conversations_frame = tk.Frame(
            content,
            bg=theme['bg_color']
        )
        self.conversations_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        self.canvas = tk.Canvas(
            self.conversations_frame,
            bg=theme['bg_color'],
            highlightthickness=0
        )
        
        # Scrollbar with modern styling
        self.scrollbar = ttk.Scrollbar(
            self.conversations_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Container for conversation items
        self.items_frame = tk.Frame(
            self.canvas,
            bg=theme['bg_color']
        )
        
        # Configure canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.items_frame,
            anchor="nw"
        )
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.items_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Pack scrollable area
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottom container for settings
        bottom_container = tk.Frame(
            self,
            bg=theme['bg_color'],
            padx=15,
            pady=15
        )
        bottom_container.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Add separator
        separator = tk.Frame(
            bottom_container,
            height=1,
            bg=theme['separator_color']
        )
        separator.pack(fill=tk.X, pady=(0, 15))
        
        # Settings buttons
        for text, icon in [
            ("Mode sombre", "🌙"),
            ("Paramètres", "⚙️"),
            ("Aide", "❔")
        ]:
            btn = tk.Frame(
                bottom_container,
                bg=theme['bg_color'],
                cursor="hand2"
            )
            btn.pack(fill=tk.X, pady=2)
            
            icon_label = tk.Label(
                btn,
                text=icon,
                font=('Segoe UI', 14),
                bg=theme['bg_color'],
                fg=theme['text_color']
            )
            icon_label.pack(side=tk.LEFT, padx=(5, 10))
            
            text_label = tk.Label(
                btn,
                text=text,
                font=('Segoe UI', 11),
                bg=theme['bg_color'],
                fg=theme['text_color']
            )
            text_label.pack(side=tk.LEFT)
            
            # Bind hover events
            for widget in [btn, icon_label, text_label]:
                widget.bind('<Enter>', lambda e, w=btn: self._on_hover_enter(w))
                widget.bind('<Leave>', lambda e, w=btn: self._on_hover_leave(w))

    def _on_hover_enter(self, widget):
        """Handle hover enter event"""
        widget.configure(bg=self.theme['button_hover'])
        for child in widget.winfo_children():
            child.configure(bg=self.theme['button_hover'])

    def _on_hover_leave(self, widget):
        """Handle hover leave event"""
        widget.configure(bg=self.theme['bg_color'])
        for child in widget.winfo_children():
            child.configure(bg=self.theme['bg_color'])

    def add_conversation(self, conversation, is_selected=False):
        """Add a conversation item to the sidebar"""
        item = ConversationItem(
            self.items_frame,
            conversation,
            self.theme,
            lambda: self.on_select_chat(conversation['id']),
            is_selected
        )
        item.pack(fill=tk.X, pady=1)

    def update_conversations(self, conversations):
        """Update the list of conversations"""
        # Clear existing items
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # Add new items
        for conv in conversations:
            self.add_conversation(conv)

    def _filter_conversations(self, *args):
        """Filter conversations based on search input"""
        search_text = self.search_var.get().lower()
        
        for child in self.items_frame.winfo_children():
            if isinstance(child, ConversationItem):
                if search_text in child.conversation['title'].lower():
                    child.pack(fill=tk.X, pady=1)
                else:
                    child.pack_forget()


class ConversationItem(tk.Frame):
    def __init__(self, master, conversation, theme, on_click, is_selected=False):
        super().__init__(
            master,
            bg=theme['bg_color' if not is_selected else 'button_hover'],
            cursor="hand2"
        )
        self.theme = theme
        self.conversation = conversation
        self.on_click = on_click
        self.is_selected = is_selected
        
        # Main container
        self.container = tk.Frame(
            self,
            bg=self.theme['bg_color' if not is_selected else 'button_hover'],
            padx=12,
            pady=8
        )
        self.container.pack(fill=tk.X)
        
        # Left side icon container
        icon_container = tk.Frame(
            self.container,
            bg=self.theme['bg_color' if not is_selected else 'button_hover']
        )
        icon_container.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create circular icon
        self.icon_canvas = tk.Canvas(
            icon_container,
            width=30,
            height=30,
            bg=self.theme['bg_color' if not is_selected else 'button_hover'],
            highlightthickness=0
        )
        self.icon_canvas.pack()
        
        # Draw icon circle
        self.icon_canvas.create_oval(
            2, 2, 28, 28,
            fill=self.theme['button_bg'],
            outline=""
        )
        
        # Add text on icon (first letter of conversation title)
        first_letter = conversation['title'][0].upper()
        self.icon_canvas.create_text(
            15, 15,
            text=first_letter,
            fill='white',
            font=('Segoe UI', 12, 'bold')
        )
        
        # Right side container
        content = tk.Frame(
            self.container,
            bg=self.theme['bg_color' if not is_selected else 'button_hover']
        )
        content.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Title and timestamp container
        header = tk.Frame(
            content,
            bg=self.theme['bg_color' if not is_selected else 'button_hover']
        )
        header.pack(fill=tk.X)
        
        # Title
        self.title = tk.Label(
            header,
            text=conversation['title'],
            font=('Segoe UI', 11, 'bold' if is_selected else 'normal'),
            bg=self.theme['bg_color' if not is_selected else 'button_hover'],
            fg=self.theme['text_color'],
            anchor='w'
        )
        self.title.pack(side=tk.LEFT)
        
        # Timestamp
        if 'timestamp' in conversation:
            self.timestamp = tk.Label(
                header,
                text=conversation['timestamp'],
                font=('Segoe UI', 9),
                bg=self.theme['bg_color' if not is_selected else 'button_hover'],
                fg='#888888',
                anchor='e'
            )
            self.timestamp.pack(side=tk.RIGHT)
        
        # Preview text
        if 'preview' in conversation:
            self.preview = tk.Label(
                content,
                text=conversation['preview'],
                font=('Segoe UI', 9),
                bg=self.theme['bg_color' if not is_selected else 'button_hover'],
                fg='#666666',
                anchor='w',
                wraplength=200
            )
            self.preview.pack(fill=tk.X, pady=(4, 0))
        
        # Options button
        self.options_btn = tk.Label(
            self.container,
            text="⋯",
            font=('Segoe UI', 14),
            bg=self.theme['bg_color' if not is_selected else 'button_hover'],
            fg=self.theme['text_color'],
            cursor="hand2"
        )
        self.options_btn.pack(side=tk.RIGHT)
        
        # Bind events
        self.bind_widgets([self, self.container, self.title, self.icon_canvas])
        self.options_btn.bind('<Button-1>', self._show_options)

    def bind_widgets(self, widgets):
        """Bind events to multiple widgets"""
        for widget in widgets:
            widget.bind('<Button-1>', lambda e: self.on_click())
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)

    def _on_enter(self, event=None):
        """Handle mouse enter event"""
        if not self.is_selected:
            self._update_bg(self.theme['button_hover'])

    def _on_leave(self, event=None):
        """Handle mouse leave event"""
        if not self.is_selected:
            self._update_bg(self.theme['bg_color'])

    def _update_bg(self, color):
        """Update background color of all components"""
        self.configure(bg=color)
        self.container.configure(bg=color)
        self.title.configure(bg=color)
        self.icon_canvas.configure(bg=color)
        self.options_btn.configure(bg=color)
        
        for widget in self.container.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=color)
            if hasattr(self, 'preview'):
                self.preview.configure(bg=color)
            if hasattr(self, 'timestamp'):
                self.timestamp.configure(bg=color)

    def _show_options(self, event):
        """Show conversation options menu"""
        menu = tk.Menu(self, tearoff=0)
        menu.configure(
            bg=self.theme['bg_color'],
            fg=self.theme['text_color'],
            activebackground=self.theme['button_hover'],
            activeforeground=self.theme['text_color'],
            font=('Segoe UI', 10)
        )
        
        menu.add_command(label="Renommer")
        menu.add_command(label="Supprimer")
        menu.add_command(label="Exporter")
        
        # Show menu at mouse position
        menu.post(event.x_root, event.y_root)