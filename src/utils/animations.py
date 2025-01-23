# src/utils/animations.py

import tkinter as tk
import time

class AnimationManager:
    @staticmethod
    def fade_in(widget, duration=500):
        """Effet de fondu à l'apparition"""
        widget.attributes('-alpha', 0.0)
        steps = 20
        step_time = duration / steps
        
        for i in range(steps + 1):
            alpha = i / steps
            widget.attributes('-alpha', alpha)
            widget.update()
            time.sleep(step_time / 1000)

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
            
    @staticmethod
    def loading_animation(widget, duration=1000):
        """Animation de chargement avec des points"""
        dots = [".", "..", "..."]
        original_text = widget["text"]
        
        def update_dots(count=0):
            if not hasattr(widget, "_loading"):
                widget["text"] = original_text
                return
                
            widget["text"] = original_text + dots[count % 3]
            widget.after(300, lambda: update_dots(count + 1))
        
        widget._loading = True
        update_dots()
        
    @staticmethod
    def stop_loading(widget):
        """Arrête l'animation de chargement"""
        if hasattr(widget, "_loading"):
            delattr(widget, "_loading")

    @staticmethod
    def pulse_attention(widget, times=3):
        """Effet de pulsation pour attirer l'attention"""
        original_bg = widget["bg"]
        attention_color = "#ff9800"  # Orange
        
        def pulse(count=0):
            if count >= times * 2:
                widget["bg"] = original_bg
                return
                
            widget["bg"] = attention_color if count % 2 == 0 else original_bg
            widget.after(500, lambda: pulse(count + 1))
        
        pulse()

    @staticmethod
    def smooth_resize(widget, target_height, duration=300):
        """Redimensionne un widget de manière fluide"""
        current_height = widget.winfo_height()
        steps = 20
        step_time = duration / steps
        height_step = (target_height - current_height) / steps
        
        def resize(step=0):
            if step >= steps:
                return
                
            new_height = current_height + (height_step * step)
            widget.configure(height=int(new_height))
            widget.after(int(step_time), lambda: resize(step + 1))
        
        resize()