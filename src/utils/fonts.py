"""Helpers para escolher fontes com fallback visualmente agradavel."""

import pygame


FONT_CANDIDATES = (
    "Avenir Next",
    "Avenir",
    "Helvetica Neue",
    "Verdana",
    "Arial",
)


def get_font(size, bold=False):
    """Retorna uma fonte do sistema com fallback para a fonte padrao do pygame."""
    path = pygame.font.match_font(FONT_CANDIDATES, bold=bold)
    if path:
        return pygame.font.Font(path, size)
    return pygame.font.SysFont(None, size, bold=bold)
