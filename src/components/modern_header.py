# src/components/modern_header.py

import tkinter as tk
from .modern_button import ModernButton

class ModernHeader(tk.Frame):
    def __init__(self, master, theme, on_toggle_sidebar, on_settings):
        super().__init__(
            master,
            bg=theme['bg_color'],
            height=64  # h-16 in tailwind
        )
        self.theme = theme
        
        # Don't shrink
        self.pack_propagate(False)
        
        # Add bottom border
        self.border = tk.Frame(
            self,
            height=1,
            bg=theme['border_color']
        )
        self.border.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Main content container with padding
        content = tk.Frame(
            self,
            bg=theme['bg_color'],
            padx=24,  # px-6 in tailwind
        )
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left side container
        left_container = tk.Frame(content, bg=theme['bg_color'])
        left_container.pack(side=tk.LEFT, fill=tk.Y)
        
        # Toggle sidebar button
        self.toggle_btn = tk.Frame(
            left_container,
            bg=theme['bg_color'],
            cursor='hand2',
            padx=8,  # p-2 in tailwind
            pady=8
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=(0, 16))  # gap-4 in tailwind
        
        # Menu icon
        self.menu_icon = tk.Label(
            self.toggle_btn,
            text="☰",
            font=('Segoe UI', 16),
            bg=theme['bg_color'],
            fg=theme['icon_color'],
            cursor='hand2'
        )
        self.menu_icon.pack()
        
        # Title
        self.title = tk.Label(
            left_container,
            text="Claude Assistant",
            font=('Segoe UI', 14, 'bold'),  # text-lg font-semibold
            bg=theme['bg_color'],
            fg=theme['text_color']
        )
        self.title.pack(side=tk.LEFT)
        
        # Right container
        right_container = tk.Frame(content, bg=theme['bg_color'])
        right_container.pack(side=tk.RIGHT, fill=tk.Y)
        
        # More options button
        self.more_btn = tk.Frame(
            right_container,
            bg=theme['bg_color'],
            cursor='hand2',
            padx=8,
            pady=8
        )
        self.more_btn.pack(side=tk.RIGHT)
        
        # More icon (three dots vertical)
        self.more_icon = tk.Label(
            self.more_btn,
            text="⋮",
            font=('Segoe UI', 16),
            bg=theme['bg_color'],
            fg=theme['icon_color'],
            cursor='hand2'
        )
        self.more_icon.pack()
        
        # Bind events
        for widget in [self.toggle_btn, self.menu_icon]:
            widget.bind('<Button-1>', lambda e: on_toggle_sidebar())
            widget.bind('<Enter>', lambda e: self._on_hover_enter(self.toggle_btn))
            widget.bind('<Leave>', lambda e: self._on_hover_leave(self.toggle_btn))
        
        for widget in [self.more_btn, self.more_icon]:
            widget.bind('<Button-1>', lambda e: on_settings())
            widget.bind('<Enter>', lambda e: self._on_hover_enter(self.more_btn))
            widget.bind('<Leave>', lambda e: self._on_hover_leave(self.more_btn))

    def _on_hover_enter(self, widget):
        """Handle hover enter event"""
        widget.configure(bg=self.theme['hover_color'])
        for child in widget.winfo_children():
            child.configure(bg=self.theme['hover_color'])

    def _on_hover_leave(self, widget):
        """Handle hover leave event"""
        widget.configure(bg=self.theme['bg_color'])
        for child in widget.winfo_children():
            child.configure(bg=self.theme['bg_color'])