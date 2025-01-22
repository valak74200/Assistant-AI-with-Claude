# src/components/settings_window.py

import tkinter as tk
from tkinter import ttk, colorchooser
from .modern_button import ModernButton

class SettingsWindow:
   def __init__(self, parent, config, apply_callback):
       self.window = tk.Toplevel(parent)
       self.window.title("Paramètres")
       self.window.geometry("400x600")
       self.window.resizable(False, False)
       self.config = config
       self.theme = config['theme']
       self.apply_callback = apply_callback
       
       # Configure window style
       self.window.configure(bg=self.theme['bg_color'])
       self.window.transient(parent)  # Make the window transient (always on top of parent)
       
       self.create_widgets()
       self.center_window()

   def create_widgets(self):
       # Main container
       main_frame = tk.Frame(self.window, bg=self.theme['bg_color'])
       main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

       # Appearance Section
       self.create_appearance_section(main_frame)
       
       # Message Colors Section
       self.create_colors_section(main_frame)
       
       # Bottom buttons
       self.create_bottom_buttons(main_frame)

   def create_appearance_section(self, parent):
       # Appearance Frame
       appearance_frame = tk.LabelFrame(
           parent,
           text="Apparence",
           bg=self.theme['bg_color'],
           fg=self.theme['text_color'],
           font=('Segoe UI', 10, 'bold'),
           padx=10,
           pady=10
       )
       appearance_frame.pack(fill=tk.X, pady=(0, 20))

       # Theme selector
       self.theme_var = tk.StringVar(value=self.theme['name'])
       
       theme_label = tk.Label(
           appearance_frame,
           text="Thème :",
           bg=self.theme['bg_color'],
           fg=self.theme['text_color'],
           font=('Segoe UI', 10)
       )
       theme_label.pack(anchor=tk.W)

       # Theme radio buttons
       themes_frame = tk.Frame(appearance_frame, bg=self.theme['bg_color'])
       themes_frame.pack(fill=tk.X, pady=5)

       ttk.Radiobutton(
           themes_frame,
           text="Clair",
           value="light",
           variable=self.theme_var
       ).pack(side=tk.LEFT, padx=(0, 10))

       ttk.Radiobutton(
           themes_frame,
           text="Sombre",
           value="dark",
           variable=self.theme_var
       ).pack(side=tk.LEFT)

   def create_colors_section(self, parent):
       # Colors Frame
       colors_frame = tk.LabelFrame(
           parent,
           text="Couleurs des messages",
           bg=self.theme['bg_color'],
           fg=self.theme['text_color'],
           font=('Segoe UI', 10, 'bold'),
           padx=10,
           pady=10
       )
       colors_frame.pack(fill=tk.X, pady=(0, 20))

       # User message color
       user_color_frame = tk.Frame(colors_frame, bg=self.theme['bg_color'])
       user_color_frame.pack(fill=tk.X, pady=5)

       tk.Label(
           user_color_frame,
           text="Vos messages :",
           bg=self.theme['bg_color'],
           fg=self.theme['text_color'],
           font=('Segoe UI', 10)
       ).pack(side=tk.LEFT)

       self.user_color_btn = ModernButton(
           user_color_frame,
           text="Choisir",
           command=self.choose_user_color,
           bg=self.theme['button_bg'],
           fg='white',
           font=('Segoe UI', 9)
       )
       self.user_color_btn.pack(side=tk.RIGHT)

       # Bot message color
       bot_color_frame = tk.Frame(colors_frame, bg=self.theme['bg_color'])
       bot_color_frame.pack(fill=tk.X, pady=5)

       tk.Label(
           bot_color_frame,
           text="Messages de Claude :",
           bg=self.theme['bg_color'],
           fg=self.theme['text_color'],
           font=('Segoe UI', 10)
       ).pack(side=tk.LEFT)

       self.bot_color_btn = ModernButton(
           bot_color_frame,
           text="Choisir",
           command=self.choose_bot_color,
           bg=self.theme['button_bg'],
           fg='white',
           font=('Segoe UI', 9)
       )
       self.bot_color_btn.pack(side=tk.RIGHT)

   def create_bottom_buttons(self, parent):
       button_frame = tk.Frame(parent, bg=self.theme['bg_color'])
       button_frame.pack(fill=tk.X, pady=(20, 0))

       # Cancel button
       ModernButton(
           button_frame,
           text="Annuler",
           command=self.window.destroy,
           bg=self.theme['button_bg'],
           fg='white',
           font=('Segoe UI', 10)
       ).pack(side=tk.LEFT)

       # Apply button
       ModernButton(
           button_frame,
           text="Appliquer",
           command=self.apply_settings,
           bg=self.theme['button_bg'],
           fg='white',
           font=('Segoe UI', 10, 'bold')
       ).pack(side=tk.RIGHT)

   def choose_user_color(self):
       color = colorchooser.askcolor(
           color=self.config['user_bubble_color'],
           title="Choisir la couleur de vos messages"
       )[1]
       if color:
           self.config['user_bubble_color'] = color

   def choose_bot_color(self):
       color = colorchooser.askcolor(
           color=self.config['bot_bubble_color'],
           title="Choisir la couleur des messages de Claude"
       )[1]
       if color:
           self.config['bot_bubble_color'] = color

   def apply_settings(self):
       # Create the new config
       new_config = {
           'theme': self.theme_var.get(),
           'user_bubble_color': self.config['user_bubble_color'],
           'bot_bubble_color': self.config['bot_bubble_color']
       }
       
       # Call the callback with the new settings
       if self.apply_callback:
           self.apply_callback(new_config)
           
       self.window.destroy()

   def center_window(self):
       # Center the window on the screen
       self.window.update_idletasks()
       width = self.window.winfo_width()
       height = self.window.winfo_height()
       x = (self.window.winfo_screenwidth() // 2) - (width // 2)
       y = (self.window.winfo_screenheight() // 2) - (height // 2)
       self.window.geometry(f'{width}x{height}+{x}+{y}')