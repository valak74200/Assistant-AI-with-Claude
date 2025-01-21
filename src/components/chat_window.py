# src/components/chat_window.py

import tkinter as tk
from tkinter import ttk
import threading
from .chat_bubble import ChatBubble
from .modern_button import ModernButton

class ChatWindow:
    def __init__(self, claude_service, config):
        self.claude_service = claude_service
        self.config = config
        self.theme = config['theme']
        self.create_window()
        
    def create_window(self):
        self.window = tk.Tk()
        self.window.title("Claude Assistant")
        self.window.geometry(self.config['window_size'])
        self.window.configure(bg=self.theme['bg_color'])

        # Main container with padding
        self.main_frame = tk.Frame(self.window, bg=self.theme['bg_color'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Chat container
        self.chat_container = tk.Frame(self.main_frame, bg=self.theme['bg_color'])
        self.chat_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        self.setup_chat_canvas()
        self.setup_input_area()
        
        # Welcome message
        self.add_message("Bonjour ! Je suis Claude, votre assistant. Comment puis-je vous aider ?", False)

        # Configure window closing
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_chat_canvas(self):
        self.canvas = tk.Canvas(self.chat_container, bg=self.theme['bg_color'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.chat_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.theme['bg_color'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.chat_container.grid_rowconfigure(0, weight=1)
        self.chat_container.grid_columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.canvas.bind('<Configure>', self.on_canvas_configure)

    def setup_input_area(self):
        input_frame = tk.Frame(self.main_frame, bg=self.theme['bg_color'])
        input_frame.pack(fill=tk.X, pady=(20, 0))
        
        separator = ttk.Separator(input_frame)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        input_container = tk.Frame(input_frame, bg=self.theme['bg_color'])
        input_container.pack(fill=tk.X)
        
        self.input_field = tk.Text(
            input_container,
            font=('Segoe UI', 11),
            bg=self.theme['input_bg'],
            fg=self.theme['text_color'],
            relief=tk.FLAT,
            height=3,
            pady=10,
            padx=10,
            wrap=tk.WORD
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Bouton paramètres
        self.settings_button = ModernButton(
            input_container,
            text="⚙️",
            font=('Segoe UI', 11),
            bg=self.theme['button_bg'],
            fg='white',
            command=self.open_settings
        )
        self.settings_button.pack(side=tk.RIGHT, pady=10, padx=(0, 10))
        
        # Bouton envoyer
        self.send_button = ModernButton(
            input_container,
            text="Envoyer",
            font=('Segoe UI', 11, 'bold'),
            bg=self.theme['button_bg'],
            fg='white',
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, pady=10)
        
        self.input_field.bind("<Control-Return>", lambda e: self.send_message())

    def open_settings(self):
        from .settings_window import SettingsWindow
        SettingsWindow(self.window, self.config, self.apply_theme)

    def apply_theme(self, new_theme, preferences):
        self.theme = new_theme
        self.config['theme'] = new_theme
        self.config.update(preferences)
        
        # Appliquer les nouvelles couleurs
        self.window.configure(bg=self.theme['bg_color'])
        self.main_frame.configure(bg=self.theme['bg_color'])
        self.chat_container.configure(bg=self.theme['bg_color'])
        self.canvas.configure(bg=self.theme['bg_color'])
        self.scrollable_frame.configure(bg=self.theme['bg_color'])
        
        # Mettre à jour l'input et les boutons
        self.input_field.configure(
            bg=self.theme['input_bg'],
            fg=self.theme['text_color']
        )
        self.send_button.configure(
            bg=self.theme['button_bg'],
            fg='white'
        )
        self.settings_button.configure(
            bg=self.theme['button_bg'],
            fg='white'
        )
        
        # Forcer le rafraîchissement de l'interface
        self.window.update()

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def add_message(self, message, is_user=True):
        bubble = ChatBubble(self.scrollable_frame, message, is_user, self.theme)
        bubble.pack(fill=tk.X, padx=10, pady=5)
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def send_message(self):
        message = self.input_field.get("1.0", tk.END).strip()
        if not message:
            return
            
        self.input_field.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        
        self.add_message(message, True)
        self.input_field.delete("1.0", tk.END)
        
        threading.Thread(target=self._get_claude_response, args=(message,), daemon=True).start()

    def _get_claude_response(self, message):
        try:
            response = self.claude_service.send_message(message)
            self.window.after(0, self._add_claude_response, response)
        except Exception as e:
            self.window.after(0, self.show_error)

    def _add_claude_response(self, message):
        self.add_message(message, False)
        self.input_field.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

    def show_error(self):
        self.add_message("Désolé, une erreur est survenue. Veuillez réessayer.", False)
        self.input_field.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)

    def on_closing(self):
        self.window.destroy()
        
    def run(self):
        self.window.mainloop()