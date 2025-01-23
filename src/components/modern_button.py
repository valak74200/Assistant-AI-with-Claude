# src/components/modern_button.py

import tkinter as tk

class ModernButton(tk.Frame):
    def __init__(self, master, text, command=None, theme=None, icon=None, **kwargs):
        super().__init__(master, bg=theme['bg_color'])
        self.theme = theme
        self.command = command
        self.is_disabled = False
        
        # Button frame with rounded corners
        self.button = tk.Frame(
            self,
            bg=theme['button_bg'],
            cursor='hand2',
            padx=16,  # px-4 in tailwind
            pady=8    # py-2 in tailwind
        )
        self.button.pack(fill=tk.BOTH, expand=True)
        
        # Container for icon and text
        content = tk.Frame(
            self.button,
            bg=theme['button_bg']
        )
        content.pack()
        
        # Add icon if provided
        if icon:
            self.icon_label = tk.Label(
                content,
                text=icon,
                font=('Segoe UI', 14),
                bg=theme['button_bg'],
                fg='white',
                cursor='hand2'
            )
            self.icon_label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Button text
        self.text_label = tk.Label(
            content,
            text=text,
            font=('Segoe UI', 11),
            bg=theme['button_bg'],
            fg='white',
            cursor='hand2'
        )
        self.text_label.pack(side=tk.LEFT)
        
        # Round the corners
        self._round_corners()
        
        # Bind events
        for widget in [self.button, self.text_label]:
            widget.bind('<Button-1>', self._on_click)
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
        
        if icon:
            self.icon_label.bind('<Button-1>', self._on_click)
            self.icon_label.bind('<Enter>', self._on_enter)
            self.icon_label.bind('<Leave>', self._on_leave)

    def _round_corners(self, radius=8):
        """Create rounded corners effect"""
        # Note: This is a simple simulation of rounded corners
        # For better rounded corners, you might want to use a custom canvas
        self.button.configure(highlightthickness=0, borderwidth=0)

    def _on_click(self, event):
        """Handle click event"""
        if not self.is_disabled and self.command:
            self.command()

    def _on_enter(self, event):
        """Handle mouse enter event"""
        if not self.is_disabled:
            self.button.configure(bg=self.theme['button_hover'])
            self.text_label.configure(bg=self.theme['button_hover'])
            if hasattr(self, 'icon_label'):
                self.icon_label.configure(bg=self.theme['button_hover'])

    def _on_leave(self, event):
        """Handle mouse leave event"""
        if not self.is_disabled:
            self.button.configure(bg=self.theme['button_bg'])
            self.text_label.configure(bg=self.theme['button_bg'])
            if hasattr(self, 'icon_label'):
                self.icon_label.configure(bg=self.theme['button_bg'])

    def configure(self, **kwargs):
        """Configure button properties"""
        if 'state' in kwargs:
            self.is_disabled = kwargs['state'] == 'disabled'
            
            if self.is_disabled:
                color = self.theme['placeholder_color']
                cursor = 'arrow'
            else:
                color = self.theme['button_bg']
                cursor = 'hand2'
            
            self.button.configure(bg=color, cursor=cursor)
            self.text_label.configure(bg=color, cursor=cursor)
            if hasattr(self, 'icon_label'):
                self.icon_label.configure(bg=color, cursor=cursor)
        
        if 'text' in kwargs:
            self.text_label.configure(text=kwargs['text'])
            
        super().configure(**{k: v for k, v in kwargs.items() if k not in ['state', 'text']})