import sys
import os

# Ajouter le chemin du projet au PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    main()