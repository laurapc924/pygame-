"""Ponto de entrada do jogo Fox Crossing.

Este módulo inicializa a janela PyGame e executa o loop principal do jogo.
"""

import pygame

from src.settings import FPS, GREEN_FOREST, HEIGHT, TITLE, WIDTH


def handle_events() -> bool:
    """Processa os eventos do PyGame e retorna False quando o jogo deve encerrar."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def main() -> None:
    """Inicializa o PyGame, cria a janela do jogo e executa o loop principal."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    running = True
    while running:
        running = handle_events()
        screen.fill(GREEN_FOREST)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
