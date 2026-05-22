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
GREEN_FOREST = (34, 85, 34)
GRAY_ROAD = (100, 100, 100)

# Paleta de cores oficial das telas de UI (menu, instruções, fim de jogo...).
COR_VERDE_ESCURO = (25, 60, 35)
COR_VERDE_MEDIO = (45, 100, 55)
COR_VERDE_CLARO = (130, 200, 110)
COR_LARANJA = (230, 130, 50)
COR_DOURADO = (255, 215, 0)
COR_TEXTO = (240, 240, 235)
COR_TEXTO_SEC = (160, 160, 155)
COR_VERMELHO = (200, 60, 60)

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
SOUNDS_DIR = ASSETS_DIR / "sounds"
