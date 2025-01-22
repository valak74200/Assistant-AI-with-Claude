# src/components/chat_bubble.py

import tkinter as tk
from datetime import datetime

class ChatBubble(tk.Frame):
    def __init__(self, master, message, is_user=False, theme=None):
        super().__init__(master, bg=theme['bg_color'])
        
        # Frame principale pour la bulle
        bubble_frame = tk.Frame(self, bg=theme['bg_color'])
        bubble_frame.pack(fill=tk.X, pady=5)
        
        # Container du message
        message_container = tk.Frame(bubble_frame, bg=theme['bg_color'])
        message_container.pack(
            side=tk.RIGHT if is_user else tk.LEFT, 
            fill=tk.X, 
            padx=10
        )
        
        # Info (nom + heure)
        info_frame = tk.Frame(message_container, bg=theme['bg_color'])
        info_frame.pack(fill=tk.X, pady=(0, 2))
        
        name = tk.Label(
            info_frame,
            text="Vous" if is_user else "Claude",
            font=('Segoe UI', 9, 'bold'),
            fg=theme['text_color'],
            bg=theme['bg_color']
        )
        name.pack(side=tk.LEFT)
        
        time = tk.Label(
            info_frame,
            text=datetime.now().strftime('%H:%M'),
            font=('Segoe UI', 8),
            fg='#888888',
            bg=theme['bg_color']
        )
        time.pack(side=tk.LEFT, padx=(5, 0))
        
        # Message
        bubble_bg = theme['user_bubble_bg'] if is_user else theme['bot_bubble_bg']
        bubble_fg = theme['user_bubble_text'] if is_user else theme['bot_bubble_text']
        
        self.message_text = tk.Text(
            message_container,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            bg=bubble_bg,
            fg=bubble_fg,
            relief=tk.FLAT,
            borderwidth=0,
            padx=12,
            pady=8,
            height=self.calculate_height(message),
            width=50
        )
        self.message_text.pack(fill=tk.X)
        
        # Insérer le message et désactiver l'édition
        self.message_text.insert('1.0', message)
        self.message_text.configure(state='disabled')
        
    def calculate_height(self, text):
        char_per_line = 50
        lines = len(text) / char_per_line
        return min(max(int(lines) + 1, 2), 10)