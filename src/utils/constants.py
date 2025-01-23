# src/utils/constants.py

# Configuration de l'application
APP_NAME = "Claude Assistant"
APP_VERSION = "2.0.0"
DEFAULT_WINDOW_SIZE = "1200x800"

# Messages système
WELCOME_MESSAGE = "Bonjour ! Je suis Claude, votre assistant. Comment puis-je vous aider ?"
ERROR_API_KEY = "Erreur: La clé API n'est pas configurée dans le fichier .env"
ERROR_CONNECTION = "Erreur de connexion au service. Veuillez vérifier votre connexion internet."
ERROR_UNKNOWN = "Une erreur inattendue s'est produite. Veuillez réessayer."

# Configuration des fichiers
CONFIG_FILE = "user_preferences.json"
HISTORY_FILE = "conversations.json"
LOG_FILE = "app.log"

# Limites et paramètres
MAX_CONVERSATIONS = 50
MAX_MESSAGES_HISTORY = 50
MAX_MESSAGE_LENGTH = 4000
TYPING_INDICATOR_DELAY = 300  # ms
AUTO_SAVE_INTERVAL = 300  # seconds

# Statuts
STATUS_CONNECTED = "Connecté"
STATUS_DISCONNECTED = "Déconnecté"
STATUS_TYPING = "Claude est en train d'écrire..."