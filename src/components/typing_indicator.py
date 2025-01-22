# src/components/typing_indicator.py

import tkinter as tk

class TypingIndicator(tk.Frame):
    def __init__(self, master, theme):
        super().__init__(master, bg=theme['bg_color'])
        
        self.dots = []
        for _ in range(3):
            dot = tk.Label(
                self,
                text="●",
                font=('Segoe UI', 10),
                bg=theme['bot_bubble_bg'],
                fg=theme['text_color']
            )
            dot.pack(side=tk.LEFT, padx=2)
            self.dots.append(dot)
        
        self.current_dot = 0
        self.animation_running = False
        
    def start(self):
        self.pack(pady=(0, 10), padx=10, anchor='w')
        self.animation_running = True
        self.animate()
        
    def stop(self):
        self.animation_running = False
        self.pack_forget()
        
    def animate(self):
        if not self.animation_running:
            return
            
        for i, dot in enumerate(self.dots):
            if i == self.current_dot:
                dot.configure(fg=self.master.master['theme']['button_bg'])
            else:
                dot.configure(fg=self.master.master['theme']['text_color'])
        
        self.current_dot = (self.current_dot + 1) % 3
        self.after(300, self.animate)