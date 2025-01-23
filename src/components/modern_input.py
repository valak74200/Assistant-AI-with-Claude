# src/components/modern_input.py

import tkinter as tk
from .modern_button import ModernButton

class ModernInput(tk.Frame):
    def __init__(self, master, theme, send_callback, upload_callback):
        super().__init__(master, bg=theme['bg_color'])
        self.theme = theme
        
        # Main container
        self.container = tk.Frame(
            self,
            bg=theme['bg_color'],
            padx=24,  # p-6 in tailwind
            pady=24
        )
        self.container.pack(fill=tk.X)
        
        # Add top border
        separator = tk.Frame(
            self.container,
            height=1,
            bg=theme['border_color']
        )
        separator.pack(fill=tk.X)
        
        # Input container with rounded corners and border
        self.input_frame = tk.Frame(
            self.container,
            bg=theme['input_bg'],
            padx=8,  # p-2 in tailwind
            pady=8,
            highlightbackground=theme['border_color'],
            highlightthickness=1
        )
        self.input_frame.pack(fill=tk.X, pady=(16, 0))
        
        # Text input area
        self.input_field = tk.Text(
            self.input_frame,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=theme['input_bg'],
            fg=theme['text_color'],
            insertbackground=theme['text_color'],
            relief=tk.FLAT,
            height=3,
            padx=2,
            pady=2
        )
        self.input_field.pack(fill=tk.X, expand=True)
        
        # Insert placeholder
        self.input_field.insert('1.0', "Envoyez un message...")
        self.input_field.configure(fg=theme['placeholder_color'])
        
        # Toolbar
        toolbar = tk.Frame(
            self.input_frame,
            bg=theme['input_bg'],
            pady=8
        )
        toolbar.pack(fill=tk.X)
        
        # Attachment button
        self.attach_btn = tk.Label(
            toolbar,
            text="📎",
            font=('Segoe UI', 14),
            bg=theme['input_bg'],
            fg=theme['icon_color'],
            cursor='hand2',
            padx=8,
            pady=2
        )
        self.attach_btn.pack(side=tk.LEFT)
        
        # Send button
        self.send_btn = tk.Frame(
            toolbar,
            bg=theme['button_bg'],
            padx=16,  # px-4 in tailwind
            pady=8,   # py-2 in tailwind
            cursor='hand2'
        )
        self.send_btn.pack(side=tk.RIGHT)
        
        self.send_text = tk.Label(
            self.send_btn,
            text="Envoyer",
            font=('Segoe UI', 11),
            bg=theme['button_bg'],
            fg='white',
            cursor='hand2'
        )
        self.send_text.pack(side=tk.LEFT, padx=(0, 8))
        
        self.send_icon = tk.Label(
            self.send_btn,
            text="➤",
            font=('Segoe UI', 11),
            bg=theme['button_bg'],
            fg='white',
            cursor='hand2'
        )
        self.send_icon.pack(side=tk.LEFT)
        
        # Round corners for send button
        self._round_corners(self.send_btn)
        
        # Bind events
        self.input_field.bind('<FocusIn>', self._on_focus_in)
        self.input_field.bind('<FocusOut>', self._on_focus_out)
        self.input_field.bind('<Control-Return>', lambda e: self._handle_send(send_callback))
        
        self.attach_btn.bind('<Button-1>', lambda e: upload_callback())
        self.attach_btn.bind('<Enter>', lambda e: self.attach_btn.configure(fg=theme['text_color']))
        self.attach_btn.bind('<Leave>', lambda e: self.attach_btn.configure(fg=theme['icon_color']))
        
        for widget in [self.send_btn, self.send_text, self.send_icon]:
            widget.bind('<Button-1>', lambda e: self._handle_send(send_callback))
            widget.bind('<Enter>', lambda e: self._on_send_hover_enter())
            widget.bind('<Leave>', lambda e: self._on_send_hover_leave())

    def _round_corners(self, widget, radius=8):
        """Apply rounded corners to a widget"""
        widget.radius = radius
        widget._canvas = tk.Canvas(
            widget,
            width=radius*2,
            height=radius*2,
            bg=widget['bg'],
            highlightthickness=0
        )

    def _on_focus_in(self, event):
        """Handle focus in event"""
        if self.input_field.get('1.0', tk.END).strip() == "Envoyez un message...":
            self.input_field.delete('1.0', tk.END)
            self.input_field.configure(fg=self.theme['text_color'])

    def _on_focus_out(self, event):
        """Handle focus out event"""
        if not self.input_field.get('1.0', tk.END).strip():
            self.input_field.insert('1.0', "Envoyez un message...")
            self.input_field.configure(fg=self.theme['placeholder_color'])

    def _on_send_hover_enter(self):
        """Handle send button hover enter"""
        self.send_btn.configure(bg=self.theme['button_hover'])
        self.send_text.configure(bg=self.theme['button_hover'])
        self.send_icon.configure(bg=self.theme['button_hover'])

    def _on_send_hover_leave(self):
        """Handle send button hover leave"""
        self.send_btn.configure(bg=self.theme['button_bg'])
        self.send_text.configure(bg=self.theme['button_bg'])
        self.send_icon.configure(bg=self.theme['button_bg'])

    def _handle_send(self, callback):
        """Handle send button click"""
        text = self.input_field.get('1.0', tk.END).strip()
        if text and text != "Envoyez un message...":
            callback(text)
            self.clear()

    def clear(self):
        """Clear input field"""
        self.input_field.delete('1.0', tk.END)

    def set_state(self, state):
        """Set input state"""
        self.input_field.configure(state=state)
        if state == 'disabled':
            self.send_btn.configure(bg=self.theme['placeholder_color'])
            self.send_text.configure(bg=self.theme['placeholder_color'])
            self.send_icon.configure(bg=self.theme['placeholder_color'])
        else:
            self.send_btn.configure(bg=self.theme['button_bg'])
            self.send_text.configure(bg=self.theme['button_bg'])
            self.send_icon.configure(bg=self.theme['button_bg'])