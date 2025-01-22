# src/components/status_bar.py

import tkinter as tk
from datetime import datetime

class StatusBar(tk.Frame):
    def __init__(self, master, theme):
        super().__init__(master, bg=theme['bg_color'])
        
        # État de la connexion
        self.connection_frame = tk.Frame(
            self,
            bg=theme['bg_color']
        )
        self.connection_frame.pack(side=tk.LEFT, padx=10)
        
        self.status_dot = tk.Label(
            self.connection_frame,
            text="●",
            font=('Segoe UI', 10),
            fg="#4CAF50",
            bg=theme['bg_color']
        )
        self.status_dot.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(
            self.connection_frame,
            text="Connecté",
            font=('Segoe UI', 9),
            fg=theme['text_color'],
            bg=theme['bg_color']
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Horloge
        self.time_label = tk.Label(
            self,
            font=('Segoe UI', 9),
            fg=theme['text_color'],
            bg=theme['bg_color']
        )
        self.time_label.pack(side=tk.RIGHT, padx=10)
        self.update_clock()
    
    def update_clock(self):
        time_str = datetime.now().strftime('%H:%M:%S')
        self.time_label.config(text=time_str)
        self.after(1000, self.update_clock)
    
    def set_status(self, connected=True):
        if connected:
            self.status_dot.config(fg="#4CAF50")
            self.status_label.config(text="Connecté")
        else:
            self.status_dot.config(fg="#f44336")
            self.status_label.config(text="Déconnecté")