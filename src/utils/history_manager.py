# src/utils/history_manager.py

import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, filename='chat_history.json'):
        self.filename = filename
        self.history = self.load_history()

    def load_history(self):
        """Charge l'historique depuis le fichier"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Erreur lors du chargement de l'historique: {e}")
            return {}

    def save_history(self):
        """Sauvegarde l'historique dans le fichier"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'historique: {e}")

    def add_conversation(self, conversation_id, title=None):
        """Ajoute une nouvelle conversation à l'historique"""
        self.history[str(conversation_id)] = {
            'title': title or f"Discussion {conversation_id}",
            'created_at': datetime.now().isoformat(),
            'messages': []
        }
        self.save_history()

    def add_message(self, conversation_id, message, is_user=True):
        """Ajoute un message à une conversation"""
        conversation_id = str(conversation_id)
        if conversation_id not in self.history:
            self.add_conversation(conversation_id)

        self.history[conversation_id]['messages'].append({
            'content': message,
            'is_user': is_user,
            'timestamp': datetime.now().isoformat()
        })
        self.save_history()

    def get_conversation(self, conversation_id):
        """Récupère une conversation spécifique"""
        return self.history.get(str(conversation_id))

    def get_all_conversations(self):
        """Récupère toutes les conversations"""
        return self.history

    def delete_conversation(self, conversation_id):
        """Supprime une conversation"""
        conversation_id = str(conversation_id)
        if conversation_id in self.history:
            del self.history[conversation_id]
            self.save_history()

    def clear_history(self):
        """Efface tout l'historique"""
        self.history = {}
        self.save_history()

    def export_conversation(self, conversation_id, format='txt'):
        """Exporte une conversation dans différents formats"""
        conversation = self.get_conversation(str(conversation_id))
        if not conversation:
            return None

        if format == 'txt':
            output = f"Conversation: {conversation['title']}\n"
            output += f"Date: {conversation['created_at']}\n\n"
            
            for msg in conversation['messages']:
                sender = "Vous" if msg['is_user'] else "Claude"
                timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')
                output += f"[{timestamp}] {sender}: {msg['content']}\n\n"
            
            return output
            
        elif format == 'json':
            return json.dumps(conversation, ensure_ascii=False, indent=2)
            
        return None