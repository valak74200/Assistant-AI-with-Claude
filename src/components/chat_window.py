import tkinter as tk
from tkinter import ttk
import threading
from datetime import datetime
from .chat_bubble import ChatBubble
from .modern_button import ModernButton
from .title_bar import TitleBar
from .typing_indicator import TypingIndicator
from .status_bar import StatusBar
from .settings_window import SettingsWindow
from .notification import Notification

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

        # Main container
        self.main_frame = tk.Frame(self.window, bg=self.theme['bg_color'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Chat container
        self.chat_container = tk.Frame(self.main_frame, bg=self.theme['bg_color'])
        self.chat_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas pour le défilement
        self.canvas = tk.Canvas(
            self.chat_container,
            bg=self.theme['bg_color'],
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self.chat_container,
            orient="vertical",
            command=self.canvas.yview
        )
        
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=self.theme['bg_color']
        )
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_reqwidth()
        )
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.chat_container.grid_rowconfigure(0, weight=1)
        self.chat_container.grid_columnconfigure(0, weight=1)
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.canvas.bind('<Configure>', self.on_canvas_configure)

        # Input area
        self.input_frame = tk.Frame(self.main_frame, bg=self.theme['bg_color'])
        self.input_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Separator
        separator = ttk.Separator(self.input_frame)
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Input container
        input_container = tk.Frame(self.input_frame, bg=self.theme['bg_color'])
        input_container.pack(fill=tk.X)
        
        # Input field
        self.input_field = tk.Text(
            input_container,
            font=('Segoe UI', 11),
            bg=self.theme['input_bg'],
            fg=self.theme['text_color'],
            relief=tk.FLAT,
            height=3,
            pady=10,
            padx=10,
            wrap=tk.WORD,
            insertbackground=self.theme['text_color']
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Send button
        self.send_button = tk.Button(
            input_container,
            text="Envoyer",
            font=('Segoe UI', 11, 'bold'),
            bg=self.theme['button_bg'],
            fg='white',
            relief=tk.FLAT,
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, pady=10)
        
        # Bind Enter key
        self.input_field.bind("<Control-Return>", lambda e: self.send_message())

        # Welcome message
        self.add_message("Bonjour ! Je suis Claude, votre assistant. Comment puis-je vous aider ?", False)

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def add_message(self, message, is_user=True):
        bubble = ChatBubble(self.scrollable_frame, message, is_user, self.theme)
        bubble.pack(fill=tk.X, padx=10, pady=5)
        self.canvas.yview_moveto(1)

    def send_message(self):
        message = self.input_field.get("1.0", tk.END).strip()
        if not message:
            return
            
        self.add_message(message, True)
        self.input_field.delete("1.0", tk.END)
        
        # Disable input during processing
        self.input_field.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        
        threading.Thread(target=self._get_response, args=(message,), daemon=True).start()

    def _get_response(self, message):
        try:
            print("Message à envoyer:", message)  # Debug
            response = self.claude_service.send_message(message)
            print("Réponse reçue:", response)  # Debug
            self.window.after(0, self._display_response, response)
        except Exception as e:
            print(f"ERREUR DÉTAILLÉE: {str(e)}")  # Debug
            print(f"Type d'erreur: {type(e)}")    # Debug
            self.window.after(0, self._display_error)

    def _display_response(self, response):
        self.add_message(response, False)
        # Re-enable input
        self.input_field.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.input_field.focus()

    def _display_error(self):
        self.add_message("Désolé, une erreur est survenue. Veuillez réessayer.", False)
        # Re-enable input
        self.input_field.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.input_field.focus()

    def run(self):
        self.window.mainloop()