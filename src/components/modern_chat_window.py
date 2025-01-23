# src/components/modern_chat_window.py

import tkinter as tk
from tkinter import ttk
import threading
from .modern_input import ModernInput
from .modern_header import ModernHeader
from .chat_bubble import ChatBubble
from .sidebar import Sidebar

class ModernChatWindow:
    def __init__(self, claude_service, config):
        self.claude_service = claude_service
        self.config = config
        self.theme = config['theme']
        self.conversations = [
            {"id": 1, "title": "Discussion générale", "selected": True},
            {"id": 2, "title": "Analyse de données", "selected": False},
            {"id": 3, "title": "Aide au code", "selected": False}
        ]
        self.create_window()

    def create_window(self):
        self.window = tk.Tk()
        self.window.title("Claude Assistant")
        self.window.geometry(self.config['window_size'])
        self.window.configure(bg=self.theme['bg_color'])

        # Main container
        self.main_container = tk.Frame(
            self.window,
            bg=self.theme['bg_color']
        )
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar (initiallement visible)
        self.sidebar_visible = True
        self.sidebar = Sidebar(
            self.main_container,
            self.theme,
            self.create_new_chat,
            self.select_conversation
        )
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Chat area (zone principale)
        self.chat_area = tk.Frame(
            self.main_container,
            bg=self.theme['bg_color']
        )
        self.chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Header
        self.header = ModernHeader(
            self.chat_area,
            self.theme,
            on_toggle_sidebar=self.toggle_sidebar,
            on_settings=self.show_settings
        )
        self.header.pack(fill=tk.X)

        # Messages container
        self.messages_frame = tk.Frame(
            self.chat_area,
            bg=self.theme['bg_color']
        )
        self.messages_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Canvas pour le défilement
        self.canvas = tk.Canvas(
            self.messages_frame,
            bg=self.theme['bg_color'],
            highlightthickness=0,
            borderwidth=0
        )
        self.scrollbar = ttk.Scrollbar(
            self.messages_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        # Container for messages
        self.messages_container = tk.Frame(
            self.canvas,
            bg=self.theme['bg_color']
        )

        # Configure canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.messages_container,
            anchor="nw",
            width=self.canvas.winfo_reqwidth()
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.messages_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Layout scrollable area
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(10, 0))
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(10, 0))

        # Input area
        self.input_area = ModernInput(
            self.chat_area,
            self.theme,
            self.send_message,
            self.handle_file_upload
        )
        self.input_area.pack(fill=tk.X, side=tk.BOTTOM)

        # Welcome message
        self.add_message(
            "Bonjour ! Je suis Claude, votre assistant. Comment puis-je vous aider ?",
            is_user=False
        )

        # Configure style for modern scrollbar
        style = ttk.Style()
        style.configure(
            "Custom.Vertical.TScrollbar",
            background=self.theme['bg_color'],
            troughcolor=self.theme['bg_color'],
            width=8,
            arrowsize=0
        )

        # Update initial conversation list
        self.sidebar.update_conversations(self.conversations)

    def create_new_chat(self):
        """Create a new conversation"""
        new_id = len(self.conversations) + 1
        new_conversation = {
            "id": new_id,
            "title": f"Nouvelle discussion {new_id}",
            "selected": True
        }
        
        # Update selections
        for conv in self.conversations:
            conv['selected'] = False
        
        self.conversations.append(new_conversation)
        self.sidebar.update_conversations(self.conversations)
        self.clear_messages()

    def select_conversation(self, conv_id):
        """Select a conversation"""
        for conv in self.conversations:
            conv['selected'] = (conv['id'] == conv_id)
        self.sidebar.update_conversations(self.conversations)
        # Here you would load the messages for the selected conversation

    def toggle_sidebar(self):
        """Toggle sidebar visibility"""
        if self.sidebar_visible:
            self.sidebar.pack_forget()
        else:
            self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_visible = not self.sidebar_visible

    def add_message(self, message, is_user=True):
        """Add a new message to the chat"""
        bubble = ChatBubble(
            self.messages_container,
            message,
            is_user,
            self.theme
        )
        bubble.pack(fill=tk.X, pady=2)
        self.canvas.yview_moveto(1.0)

    def clear_messages(self):
        """Clear all messages"""
        for widget in self.messages_container.winfo_children():
            widget.destroy()

    def send_message(self, message):
        """Send a message and get response"""
        if not message.strip():
            return

        self.add_message(message, True)
        self.input_area.clear()

        # Disable input during processing
        self.input_area.set_state('disabled')
        threading.Thread(target=self._get_response, args=(message,), daemon=True).start()

    def _get_response(self, message):
        """Get response from Claude"""
        try:
            response = self.claude_service.send_message(message)
            self.window.after(0, self._display_response, response)
        except Exception as e:
            self.window.after(0, self._display_error)

    def _display_response(self, response):
        """Display Claude's response"""
        self.add_message(response, False)
        self.input_area.set_state('normal')

    def _display_error(self):
        """Display error message"""
        self.add_message(
            "Désolé, une erreur est survenue. Veuillez réessayer.",
            False
        )
        self.input_area.set_state('normal')

    def handle_file_upload(self):
        """Handle file upload"""
        # Implement file upload functionality
        pass

    def show_settings(self):
        """Show settings window"""
        # Implement settings window
        pass

    def run(self):
        """Run the application"""
        self.window.mainloop()