# Claude Assistant

Une application de bureau moderne pour interagir avec Claude, l'assistant IA d'Anthropic, développée en Python avec Tkinter.

## 🌟 Fonctionnalités

- Interface graphique moderne et intuitive
- Thèmes clair et sombre
- Bulles de conversation personnalisables
- Indicateur de frappe
- Barre de statut avec état de connexion
- Gestion des paramètres utilisateur
- Notifications système
- Barre de titre personnalisée
- Animations fluides
- Support du format Markdown dans les messages

## 🛠 Prérequis

- Python 3.7+
- Tkinter (généralement inclus avec Python)
- API key Anthropic

## 📦 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/username/Assistant-AI-with-Claude.git
cd Assistant-AI-with-Claude
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Créez un fichier `.env` à la racine du projet :
```env
ANTHROPIC_API_KEY=your_api_key_here
```

## 🚀 Démarrage

Pour lancer l'application :

```bash
python main.py
```

## 🏗 Structure du Projet

```
src/
├── components/             # Composants de l'interface
│   ├── chat_bubble.py     # Bulles de conversation
│   ├── chat_window.py     # Fenêtre principale
│   ├── modern_button.py   # Boutons stylisés
│   ├── notification.py    # Système de notifications
│   ├── settings_window.py # Fenêtre des paramètres
│   ├── status_bar.py     # Barre de statut
│   ├── title_bar.py      # Barre de titre
│   └── typing_indicator.py # Indicateur de frappe
├── services/
│   └── claude_service.py  # Service d'API Claude
└── utils/
    ├── animations.py      # Gestionnaire d'animations
    └── config.py         # Configuration de l'application
```

## ⚙️ Configuration

L'application utilise un système de thèmes et de préférences utilisateur configurables via l'interface graphique. Les paramètres sont sauvegardés dans un fichier `user_preferences.json`.

### Thèmes disponibles

- **Clair** : Interface claire avec accents violets
- **Sombre** : Interface sombre avec accents violets

### Personnalisation

Vous pouvez personnaliser :
- La couleur des bulles de messages (utilisateur et assistant)
- Le thème général de l'application
- La taille de la fenêtre (via le fichier de configuration)

## 🔐 Sécurité

- L'API key est stockée dans un fichier `.env` séparé
- Les messages sont traités de manière sécurisée
- La connexion à l'API utilise HTTPS

## 🤝 Contribution

Les contributions sont bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- Anthropic pour l'API Claude
- La communauté Python/Tkinter pour les ressources et inspirations
