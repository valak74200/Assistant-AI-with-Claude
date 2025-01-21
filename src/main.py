# src/main.py

import os
import sys
from utils.config import Config
from services.claude_service import ClaudeService
from components.chat_window import ChatWindow

def main():
    try:
        # Chargement de la configuration
        config = Config.load_config()
        
        # Vérification de la clé API
        if not config['api_key']:
            print("Erreur: La clé API n'est pas configurée dans le fichier .env")
            sys.exit(1)
            
        # Initialisation des services
        claude_service = ClaudeService(config['api_key'])
        
        # Création et lancement de l'interface
        chat_window = ChatWindow(claude_service, config)
        chat_window.run()
        
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()