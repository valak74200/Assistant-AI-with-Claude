# src/components/title_bar.py

import tkinter as tk
from .modern_button import ModernButton

class TitleBar(tk.Frame):
    def __init__(self, master, theme, title="Claude Assistant"):
        super().__init__(
            master,
            bg=theme['bg_color'],
            height=40
        )
        
        self.title_label = tk.Label(
            self,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            bg=theme['bg_color'],
            fg=theme['text_color']
        )
        self.title_label.pack(side=tk.LEFT, padx=20)
        
        # Version label
        self.version_label = tk.Label(
            self,
            text="v1.0",
            font=('Segoe UI', 8),
            bg=theme['bg_color'],
            fg=theme['text_color']
        )
        self.version_label.pack(side=tk.LEFT)