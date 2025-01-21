# src/components/chat_bubble.py

import tkinter as tk
from datetime import datetime

class ChatBubble(tk.Frame):
    def __init__(self, master, message, is_user=False, theme=None):
        super().__init__(master, bg=theme['bg_color'] if theme else '#ffffff')
        
        self.message = message
        self.is_user = is_user
        self.theme = theme
        
        bubble_bg = (
            self.theme['user_bubble_bg'] if is_user else self.theme['bot_bubble_bg']
        ) if self.theme else ('#6e2cf2' if is_user else '#f0f0f0')
        
        bubble_fg = (
            self.theme['user_bubble_text'] if is_user else self.theme['bot_bubble_text']
        ) if self.theme else ('white' if is_user else 'black')
        
        self.bubble = tk.Text(
            self,
            wrap=tk.WORD,
            padx=15,
            pady=10,
            relief=tk.FLAT,
            border=0,
            font=('Segoe UI', 11),
            width=50,
            height=self.calculate_height(message),
            bg=bubble_bg,
            fg=bubble_fg,
        )
        
        self.bubble.insert(tk.END, message)
        self.bubble.config(state=tk.DISABLED)
        self.bubble.grid(row=0, column=1 if is_user else 0, padx=10, pady=5)
        
        # Timestamp
        time_label = tk.Label(
            self,
            text=datetime.now().strftime('%H:%M'),
            font=('Segoe UI', 8),
            fg=theme['text_color'] if theme else '#666666',
            bg=theme['bg_color'] if theme else '#ffffff'
        )
        time_label.grid(row=1, column=1 if is_user else 0, sticky='e' if is_user else 'w', padx=10)

    def calculate_height(self, text):
        char_per_line = 50
        lines = len(text) / char_per_line
        return min(max(int(lines) + 1, 1), 10)