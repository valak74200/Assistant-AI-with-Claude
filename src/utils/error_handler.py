# src/utils/error_handler.py

import logging
import traceback
from datetime import datetime
import os

class ErrorHandler:
    def __init__(self, log_file='app.log'):
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        """Configure le système de logging"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def handle_error(self, error, context=None):
        """Gère une erreur et retourne un message approprié"""
        # Log l'erreur
        error_details = {
            'type': type(error).__name__,
            'message': str(error),
            'context': context,
            'traceback': traceback.format_exc()
        }
        
        logging.error(
            f"Erreur: {error_details['type']}\n"
            f"Message: {error_details['message']}\n"
            f"Contexte: {error_details['context']}\n"
            f"Traceback: {error_details['traceback']}"
        )

        # Retourne un message d'erreur approprié pour l'utilisateur
        if isinstance(error, ConnectionError):
            return "Impossible de se connecter au service. Veuillez vérifier votre connexion internet."
        elif isinstance(error, TimeoutError):
            return "Le service met trop de temps à répondre. Veuillez réessayer."
        elif isinstance(error, ValueError):
            return "Une erreur est survenue avec les données fournies. Veuillez réessayer."
        else:
            return "Une erreur inattendue est survenue. Veuillez réessayer plus tard."

    def get_error_stats(self):
        """Retourne des statistiques sur les erreurs"""
        if not os.path.exists(self.log_file):
            return {}

        error_counts = {}
        with open(self.log_file, 'r') as f:
            for line in f:
                if 'ERROR' in line:
                    error_type = line.split('Erreur: ')[-1].split('\n')[0]
                    error_counts[error_type] = error_counts.get(error_type, 0) + 1

        return error_counts

    def clear_logs(self):
        """Nettoie les fichiers de logs"""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
            self.setup_logging()