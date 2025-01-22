import os
from dotenv import load_dotenv
import json

class ThemeConfig:
    LIGHT = {
        'name': 'light',
        'bg_color': '#ffffff',
        'text_color': '#1a1a1a',
        'input_bg': '#f8f8f8',
        'user_bubble_bg': '#6e2cf2',
        'user_bubble_text': '#ffffff',
        'bot_bubble_bg': '#f0f0f0',
        'bot_bubble_text': '#1a1a1a',
        'button_bg': '#6e2cf2',
        'button_hover': '#5a23c8',
        'separator_color': '#e0e0e0',
        'error_color': '#ff4444',
        'title_bg': '#ffffff',
    }
    
    DARK = {
        'name': 'dark',
        'bg_color': '#1a1a1a',
        'text_color': '#ffffff',
        'input_bg': '#2d2d2d',
        'user_bubble_bg': '#6e2cf2',
        'user_bubble_text': '#ffffff',
        'bot_bubble_bg': '#2d2d2d',
        'bot_bubble_text': '#ffffff',
        'button_bg': '#6e2cf2',
        'button_hover': '#5a23c8',
        'separator_color': '#333333',
        'error_color': '#ff6666',
        'title_bg': '#1a1a1a',
    }

class Config:
    @staticmethod
    def load_config():
        load_dotenv()
        
        # Charger ou créer les préférences utilisateur
        user_prefs = Config.load_user_preferences()
        
        return {
            'api_key': os.getenv('ANTHROPIC_API_KEY'),
            'window_size': '900x700',
            'theme': ThemeConfig.LIGHT if user_prefs.get('theme') == 'light' else ThemeConfig.DARK,
            'user_bubble_color': user_prefs.get('user_bubble_color', '#6e2cf2'),
            'bot_bubble_color': user_prefs.get('bot_bubble_color', '#f0f0f0'),
        }
    
    @staticmethod
    def save_user_preferences(preferences):
        with open('user_preferences.json', 'w') as f:
            json.dump(preferences, f)
    
    @staticmethod
    def load_user_preferences():
        try:
            with open('user_preferences.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'theme': 'light',
                'user_bubble_color': '#6e2cf2',
                'bot_bubble_color': '#f0f0f0'
            }