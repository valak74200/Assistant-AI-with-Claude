# src/components/conversation_list.py

import tkinter as tk
from tkinter import ttk

class ConversationList(tk.Frame):
    def __init__(self, master, theme, on_select=None):
        super().__init__(master, bg=theme['bg_color'])
        self.theme = theme
        self.on_select = on_select
        
        # Container principal
        self.list_container = tk.Frame(
            self,
            bg=self.theme['bg_color']
        )
        self.list_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas pour le défilement
        self.canvas = tk.Canvas(
            self.list_container,
            bg=self.theme['bg_color'],
            highlightthickness=0
        )
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.list_container,
            orient="vertical",
            command=self.canvas.yview
        )
        
        # Frame pour les conversations
        self.conversations_frame = tk.Frame(
            self.canvas,
            bg=self.theme['bg_color']
        )
        
        # Configuration du canvas
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.conversations_frame,
            anchor="nw",
            width=self.canvas.winfo_reqwidth()
        )
        
        # Configuration du scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.conversations_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Layout
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def on_canvas_configure(self, event):
        """Ajuste la largeur du frame des conversations"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def add_conversation(self, conversation):
        """Ajoute une conversation à la liste"""
        frame = tk.Frame(
            self.conversations_frame,
            bg=self.theme['bg_color'],
            padx=10,
            pady=5
        )
        frame.pack(fill=tk.X, pady=2)
        
        # Titre de la conversation
        title = tk.Label(
            frame,
            text=conversation['title'],
            font=('Segoe UI', 10),
            bg=self.theme['bg_color'],
            fg=self.theme['text_color'],
            anchor='w'
        )
        title.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Binding des événements
        for widget in [frame, title]:
            widget.bind('<Button-1>', lambda e, c=conversation: self._on_click(c))
            widget.bind('<Enter>', lambda e, f=frame: self._on_enter(f))
            widget.bind('<Leave>', lambda e, f=frame: self._on_leave(f))

    def clear(self):
        """Efface toutes les conversations"""
        for widget in self.conversations_frame.winfo_children():
            widget.destroy()

    def update_conversations(self, conversations):
        """Met à jour la liste des conversations"""
        self.clear()
        for conv in conversations:
            self.add_conversation(conv)

    def _on_click(self, conversation):
        """Gestion du clic sur une conversation"""
        if self.on_select:
            self.on_select(conversation['id'])

    def _on_enter(self, frame):
        """Effet de survol - entrée"""
        frame.configure(bg=self.theme['button_hover'])
        for child in frame.winfo_children():
            child.configure(bg=self.theme['button_hover'])

    def _on_leave(self, frame):
        """Effet de survol - sortie"""
        frame.configure(bg=self.theme['bg_color'])
        for child in frame.winfo_children():
            child.configure(bg=self.theme['bg_color'])