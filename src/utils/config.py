# src/utils/config.py

import os
from dotenv import load_dotenv
import json

class ThemeConfig:
    LIGHT = {
        'name': 'light',
        'bg_color': '#ffffff',
        'text_color': '#000000',
        'input_bg': '#ffffff',
        'user_bubble_bg': '#7c3aed',  # purple-600
        'user_bubble_text': '#ffffff',
        'bot_bubble_bg': '#f3f4f6',   # gray-100
        'bot_bubble_text': '#000000',  # Noir pour plus de contraste
        'button_bg': '#7c3aed',       # purple-600
        'button_hover': '#6d28d9',    # purple-700
        'separator_color': '#e5e7eb',  # gray-200
        'hover_color': '#f3f4f6',     # gray-100
        'selected_bg': '#f3f4f6',     # gray-100
        'icon_color': '#4b5563',      # gray-600 pour meilleur contraste
        'placeholder_color': '#6b7280',# gray-500
        'border_color': '#e5e7eb',    # gray-200
        'shadow_color': '#e5e7eb',    # gray-200
        'scrollbar_bg': '#f3f4f6',    # gray-100
        'scrollbar_thumb': '#9ca3af'  # gray-400
    }
    
    DARK = {
        'name': 'dark',
        'bg_color': '#111827',        # gray-900
        'text_color': '#ffffff',
        'input_bg': '#1f2937',        # gray-800
        'user_bubble_bg': '#7c3aed',  # purple-600
        'user_bubble_text': '#ffffff',
        'bot_bubble_bg': '#374151',   # gray-700
        'bot_bubble_text': '#ffffff',
        'button_bg': '#7c3aed',       # purple-600
        'button_hover': '#6d28d9',    # purple-700
        'separator_color': '#374151',  # gray-700
        'hover_color': '#1f2937',     # gray-800
        'selected_bg': '#1f2937',     # gray-800
        'icon_color': '#d1d5db',      # gray-300
        'placeholder_color': '#9ca3af',# gray-400
        'border_color': '#374151',    # gray-700
        'shadow_color': '#000000',
        'scrollbar_bg': '#1f2937',    # gray-800
        'scrollbar_thumb': '#4b5563'  # gray-600
    }

class Config:
    @staticmethod
    def load_config():
        load_dotenv()
        
        # Charger ou créer les préférences utilisateur
        user_prefs = Config.load_user_preferences()
        
        return {
            'api_key': os.getenv('ANTHROPIC_API_KEY'),
            'window_size': '1200x800',
            'theme': ThemeConfig.LIGHT if user_prefs.get('theme') == 'light' else ThemeConfig.DARK,
            'enable_notifications': user_prefs.get('enable_notifications', True),
            'enable_sounds': user_prefs.get('enable_sounds', True),
            'save_conversations': user_prefs.get('save_conversations', True),
            'max_conversations': user_prefs.get('max_conversations', 50),
            'typing_indicator': user_prefs.get('typing_indicator', True),
            'auto_scroll': user_prefs.get('auto_scroll', True),
            'show_timestamps': user_prefs.get('show_timestamps', True),
            'sidebar_visible': user_prefs.get('sidebar_visible', True),
            'language': user_prefs.get('language', 'fr')
        }
    
    @staticmethod
    def save_user_preferences(preferences):
        try:
            with open('user_preferences.json', 'w', encoding='utf-8') as f:
                json.dump(preferences, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des préférences: {e}")
            return False
    
    @staticmethod
    def load_user_preferences():
        try:
            with open('user_preferences.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'theme': 'light',
                'enable_notifications': True,
                'enable_sounds': True,
                'save_conversations': True,
                'max_conversations': 50,
                'typing_indicator': True,
                'auto_scroll': True,
                'show_timestamps': True,
                'sidebar_visible': True,
                'language': 'fr'
            }