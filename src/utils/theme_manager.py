# src/utils/theme_manager.py

import json
import os
from typing import Dict, Any

class ThemeManager:
    def __init__(self, config_file='themes.json'):
        self.config_file = config_file
        self.current_theme = 'light'
        self.custom_themes = {}
        self.load_themes()

    BUILT_IN_THEMES = {
        'light': {
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
            'success_color': '#4CAF50',
            'warning_color': '#ff9800',
            'info_color': '#2196F3',
            'shadow_color': 'rgba(0, 0, 0, 0.1)',
            'scrollbar_bg': '#f0f0f0',
            'scrollbar_thumb': '#c0c0c0',
            'link_color': '#2196F3',
            'selection_bg': '#e3f2fd',
            'selection_text': '#1a1a1a',
            'code_bg': '#f5f5f5',
            'code_text': '#24292e'
        },
        'dark': {
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
            'success_color': '#66bb6a',
            'warning_color': '#ffa726',
            'info_color': '#64b5f6',
            'shadow_color': 'rgba(0, 0, 0, 0.2)',
            'scrollbar_bg': '#2d2d2d',
            'scrollbar_thumb': '#404040',
            'link_color': '#64b5f6',
            'selection_bg': '#404040',
            'selection_text': '#ffffff',
            'code_bg': '#2d2d2d',
            'code_text': '#e6e6e6'
        }
    }

    def load_themes(self) -> None:
        """Charge les thèmes personnalisés depuis le fichier de configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.custom_themes = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des thèmes: {e}")
            self.custom_themes = {}

    def save_themes(self) -> None:
        """Sauvegarde les thèmes personnalisés dans le fichier de configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.custom_themes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des thèmes: {e}")

    def get_theme(self, theme_name: str = None) -> Dict[str, Any]:
        """Récupère un thème par son nom"""
        theme_name = theme_name or self.current_theme
        
        if theme_name in self.custom_themes:
            return self.custom_themes[theme_name]
        return self.BUILT_IN_THEMES.get(theme_name, self.BUILT_IN_THEMES['light'])

    def create_custom_theme(self, name: str, colors: Dict[str, str]) -> None:
        """Crée un nouveau thème personnalisé"""
        self.custom_themes[name] = colors
        self.save_themes()

    def delete_custom_theme(self, name: str) -> bool:
        """Supprime un thème personnalisé"""
        if name in self.custom_themes:
            del self.custom_themes[name]
            self.save_themes()
            return True
        return False

    def update_theme(self, name: str, colors: Dict[str, str]) -> bool:
        """Met à jour un thème existant"""
        if name in self.custom_themes:
            self.custom_themes[name].update(colors)
            self.save_themes()
            return True
        return False

    def get_all_themes(self) -> Dict[str, Dict[str, str]]:
        """Récupère tous les thèmes disponibles"""
        return {**self.BUILT_IN_THEMES, **self.custom_themes}

    def set_current_theme(self, theme_name: str) -> bool:
        """Définit le thème actuel"""
        if theme_name in self.BUILT_IN_THEMES or theme_name in self.custom_themes:
            self.current_theme = theme_name
            return True
        return False