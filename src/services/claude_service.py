# src/services/claude_service.py

from anthropic import Anthropic
import json
import os
from datetime import datetime

class ClaudeService:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
        self.conversations_file = 'conversations.json'
        self.load_conversations()
        
    def send_message(self, message, conversation_id=None):
        try:
            # Trouver la conversation
            conversation = next(
                (c for c in self.conversations if c['id'] == conversation_id),
                {'messages': []}
            ) if conversation_id else {'messages': []}
            
            # Préparer le contexte avec l'historique
            messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in conversation['messages'][-5:]  # Limiter au 5 derniers messages
            ]
            messages.append({"role": "user", "content": message})
            
            # Envoyer à l'API
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                messages=messages
            )
            
            # Extraire la réponse
            assistant_message = response.content[0].text
            
            # Sauvegarder dans l'historique
            if conversation_id:
                self.add_message_to_conversation(
                    conversation_id,
                    message,
                    assistant_message
                )
            
            return assistant_message
            
        except Exception as e:
            print(f"Erreur API Claude: {str(e)}")
            raise

    def create_conversation(self, title=None):
        """Crée une nouvelle conversation"""
        conversation_id = len(self.conversations) + 1
        new_conversation = {
            'id': conversation_id,
            'title': title or f"Discussion {conversation_id}",
            'created_at': datetime.now().isoformat(),
            'messages': []
        }
        self.conversations.append(new_conversation)
        self.save_conversations()
        return conversation_id

    def add_message_to_conversation(self, conversation_id, user_message, assistant_message):
        """Ajoute des messages à une conversation"""
        conversation = next(
            (c for c in self.conversations if c['id'] == conversation_id),
            None
        )
        
        if conversation:
            # Ajouter le message utilisateur
            conversation['messages'].append({
                'role': 'user',
                'content': user_message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Ajouter la réponse de l'assistant
            conversation['messages'].append({
                'role': 'assistant',
                'content': assistant_message,
                'timestamp': datetime.now().isoformat()
            })
            
            self.save_conversations()

    def get_conversation(self, conversation_id):
        """Récupère une conversation par son ID"""
        return next(
            (c for c in self.conversations if c['id'] == conversation_id),
            None
        )

    def get_conversations(self):
        """Récupère toutes les conversations"""
        return self.conversations

    def delete_conversation(self, conversation_id):
        """Supprime une conversation"""
        self.conversations = [
            c for c in self.conversations if c['id'] != conversation_id
        ]
        self.save_conversations()

    def load_conversations(self):
        """Charge les conversations depuis le fichier"""
        try:
            if os.path.exists(self.conversations_file):
                with open(self.conversations_file, 'r', encoding='utf-8') as f:
                    self.conversations = json.load(f)
            else:
                self.conversations = []
        except Exception as e:
            print(f"Erreur lors du chargement des conversations: {e}")
            self.conversations = []

    def save_conversations(self):
        """Sauvegarde les conversations dans le fichier"""
        try:
            with open(self.conversations_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des conversations: {e}")