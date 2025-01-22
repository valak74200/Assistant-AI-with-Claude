# src/components/placeholder_text.py

import tkinter as tk

class PlaceholderText(tk.Text):
    def __init__(self, master, placeholder="", theme=None, **kwargs):
        super().__init__(
            master,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            height=3,
            relief=tk.FLAT,
            padx=10,
            pady=8,
            **kwargs
        )
        
        self.placeholder = placeholder
        self.placeholder_color = '#888888'
        self.default_fg = theme['text_color']
        self.theme = theme
        
        self.configure(bg=theme['input_bg'], fg=self.default_fg)
        
        self.show_placeholder()
        
        self.bind('<FocusIn>', self.clear_placeholder)
        self.bind('<FocusOut>', self.show_placeholder)
        
    def show_placeholder(self, *args):
        if not self.get('1.0', 'end-1c'):
            self.configure(fg=self.placeholder_color)
            self.insert('1.0', self.placeholder)
    
    def clear_placeholder(self, *args):
        if self.get('1.0', 'end-1c') == self.placeholder:
            self.configure(fg=self.default_fg)
            self.delete('1.0', tk.END)