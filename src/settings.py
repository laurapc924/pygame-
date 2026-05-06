"""Configurações globais do jogo Fox Crossing.

Este módulo define constantes de tela, cores e caminhos de recursos usados
por todo o projeto.
"""

from pathlib import Path

WIDTH = 1024
HEIGHT = 576
FPS = 60
TITLE = "Fox Crossing"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_FOREST = (0, 100, 0)
GRAY_ROAD = (100, 100, 100)

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
SOUNDS_DIR = ASSETS_DIR / "sounds"
