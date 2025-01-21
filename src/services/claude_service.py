# src/services/claude_service.py

from anthropic import Anthropic
import os

class ClaudeService:
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
        self.messages = []

    def send_message(self, message):
        self.messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                messages=self.messages
            )
            
            assistant_message = response.content[0].text
            self.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            print(f"Erreur API Claude: {e}")
            raise