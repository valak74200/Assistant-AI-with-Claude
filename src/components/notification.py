# src/components/notification.py

import tkinter as tk

class Notification(tk.Toplevel):
    def __init__(self, message, theme, duration=3000):
        super().__init__()
        
        # Configuration de la fenêtre
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        
        # Style
        bg_color = theme['bg_color']
        fg_color = theme['text_color']
        
        # Frame principale
        main_frame = tk.Frame(
            self,
            bg=bg_color,
            padx=20,
            pady=10,
            relief=tk.RIDGE,
            borderwidth=1
        )
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message
        tk.Label(
            main_frame,
            text=message,
            bg=bg_color,
            fg=fg_color,
            font=('Segoe UI', 10)
        ).pack()
        
        # Positionnement
        self.position_window()
        
        # Auto-destruction
        self.after(duration, self.destroy)
    
    def position_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        width = 300
        height = 50
        
        x = screen_width - width - 20
        y = screen_height - height - 40
        
        self.geometry(f'{width}x{height}+{x}+{y}')