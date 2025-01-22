# src/utils/animations.py

import tkinter as tk

class AnimationManager:
    @staticmethod
    def slide_in(widget, direction='right', duration=300):
        """Anime l'entrée d'un widget avec un effet de glissement"""
        if direction == 'right':
            start_x = widget.winfo_screenwidth()
            end_x = widget.winfo_x()
            
            def animate(current_x):
                if current_x > end_x:
                    widget.place(x=current_x)
                    new_x = current_x - (current_x - end_x) * 0.3
                    widget.after(16, lambda: animate(new_x))
                else:
                    widget.place(x=end_x)
            
            animate(start_x)