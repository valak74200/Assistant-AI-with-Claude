# src/components/title_bar.py

import tkinter as tk
from .modern_button import ModernButton

class TitleBar(tk.Frame):
    def __init__(self, master, theme, on_settings=None):
        super().__init__(
            master,
            bg=theme['bg_color'],
            height=50
        )
        self.pack_propagate(False)
        
        # Logo/Icon (un cercle violet simple pour commencer)
        self.logo_canvas = tk.Canvas(
            self,
            width=30,
            height=30,
            bg=theme['bg_color'],
            highlightthickness=0
        )
        self.logo_canvas.create_oval(
            2, 2, 28, 28,
            fill=theme['button_bg'],
            outline=""
        )
        self.logo_canvas.pack(side=tk.LEFT, padx=10)
        
        # Titre
        self.title_label = tk.Label(
            self,
            text="Claude Assistant",
            font=('Segoe UI', 12, 'bold'),
            bg=theme['bg_color'],
            fg=theme['text_color']
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Bouton paramètres
        if on_settings:
            self.settings_btn = ModernButton(
                self,
                text="⚙️",
                font=('Segoe UI', 12),
                bg=theme['button_bg'],
                fg='white',
                command=on_settings
            )
            self.settings_btn.pack(side=tk.RIGHT, padx=10)