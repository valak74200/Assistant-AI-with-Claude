# src/components/modern_button.py

import tkinter as tk

class ModernButton(tk.Button):
    def __init__(self, master=None, theme=None, **kwargs):
        self.theme = theme
        super().__init__(master, **kwargs)
        self.configure(
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self['background'] = self.theme['button_hover'] if self.theme else '#5a23c8'

    def on_leave(self, e):
        self['background'] = self.theme['button_bg'] if self.theme else '#6e2cf2'