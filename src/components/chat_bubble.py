# src/components/chat_bubble.py

import tkinter as tk
from datetime import datetime

class ChatBubble(tk.Frame):
    def __init__(self, master, message, is_user=True, theme=None):
        super().__init__(master, bg=theme['bg_color'])
        self.theme = theme
        
        # Main container
        self.container = tk.Frame(
            self,
            bg=theme['bg_color']
        )
        self.container.pack(fill=tk.X, padx=10, pady=5)
        
        # Message alignment container
        self.message_frame = tk.Frame(
            self.container,
            bg=theme['bg_color']
        )
        self.message_frame.pack(
            side=tk.RIGHT if is_user else tk.LEFT,
            fill=tk.X,
            padx=5
        )
        
        # Name label
        name = tk.Label(
            self.message_frame,
            text="Vous" if is_user else "Claude",
            font=('Segoe UI', 10),
            bg=theme['bg_color'],
            fg=theme['text_color']
        )
        name.pack(anchor='w' if not is_user else 'e', pady=(0, 2))
        
        # Message bubble
        bubble_bg = theme['user_bubble_bg'] if is_user else theme['bot_bubble_bg']
        bubble_fg = theme['user_bubble_text'] if is_user else theme['bot_bubble_text']
        
        self.bubble = tk.Frame(
            self.message_frame,
            bg=bubble_bg,
            padx=12,
            pady=8,
        )
        self.bubble.pack(anchor='w' if not is_user else 'e')
        
        # Message text
        self.message_text = tk.Text(
            self.bubble,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=bubble_bg,
            fg=bubble_fg,
            relief=tk.FLAT,
            borderwidth=0,
            padx=0,
            pady=0,
            highlightthickness=0,
            width=40,
            height=self.calculate_text_height(message)
        )
        self.message_text.pack()
        
        # Insert and disable editing
        self.message_text.insert('1.0', message)
        self.message_text.configure(state='disabled')

    def calculate_text_height(self, text):
        """Calcule la hauteur nécessaire pour le texte"""
        num_lines = len(text.split('\n'))
        chars_per_line = 40
        estimated_lines = len(text) / chars_per_line
        total_lines = max(num_lines, estimated_lines)
        return min(max(int(total_lines) + 1, 1), 10)