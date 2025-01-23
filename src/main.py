import os
import sys
from src.utils.config import Config
from src.services.claude_service import ClaudeService
from src.components.modern_chat_window import ModernChatWindow

def main():
    try:
        config = Config.load_config()
        
        if not config['api_key']:
            print("Erreur: La clé API n'est pas configurée dans le fichier .env")
            sys.exit(1)
            
        claude_service = ClaudeService(config['api_key'])
        chat_window = ModernChatWindow(claude_service, config)
        chat_window.run()
        
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()