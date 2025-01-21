# src/components/settings_window.py

import tkinter as tk
from tkinter import ttk, colorchooser
from utils.config import ThemeConfig, Config

class SettingsWindow:
    def __init__(self, parent, current_config, callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Paramètres")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        
        self.config = current_config
        self.callback = callback
        
        self.create_widgets()
        
    def create_widgets(self):
        # Thème
        theme_frame = ttk.LabelFrame(self.window, text="Thème", padding=10)
        theme_frame.pack(fill='x', padx=20, pady=10)
        
        self.theme_var = tk.StringVar(value=self.config['theme']['name'])
        ttk.Radiobutton(theme_frame, text="Thème clair", value="light", 
                       variable=self.theme_var).pack(anchor='w')
        ttk.Radiobutton(theme_frame, text="Thème sombre", value="dark", 
                       variable=self.theme_var).pack(anchor='w')
        
        # Couleurs
        colors_frame = ttk.LabelFrame(self.window, text="Couleurs", padding=10)
        colors_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(colors_frame, text="Changer la couleur des messages utilisateur",
                  command=self.change_user_color).pack(fill='x', pady=5)
        
        ttk.Button(colors_frame, text="Changer la couleur des messages du bot",
                  command=self.change_bot_color).pack(fill='x', pady=5)
        
        # Bouton Appliquer
        ttk.Button(self.window, text="Appliquer",
                  command=self.apply_settings).pack(pady=20)
        
    def change_user_color(self):
        color = colorchooser.askcolor(color=self.config['user_bubble_color'])[1]
        if color:
            self.config['user_bubble_color'] = color
            
    def change_bot_color(self):
        color = colorchooser.askcolor(color=self.config['bot_bubble_color'])[1]
        if color:
            self.config['bot_bubble_color'] = color
            
    def apply_settings(self):
        new_theme = ThemeConfig.LIGHT if self.theme_var.get() == 'light' else ThemeConfig.DARK
        
        preferences = {
            'theme': self.theme_var.get(),
            'user_bubble_color': self.config['user_bubble_color'],
            'bot_bubble_color': self.config['bot_bubble_color']
        }
        
        Config.save_user_preferences(preferences)
        
        if self.callback:
            self.callback(new_theme, preferences)
            
        self.window.destroy()