"""Personagem principal do jogo: a raposa."""

import pygame


ORANGE = (255, 140, 0)


class Fox:
    """Raposa controlada pelo jogador."""

    def __init__(self, x, y):
        """Inicializa a raposa na posição (x, y)."""
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.y += 5
                if event.key == pygame.K_UP:
                    self.y -= 5
                if event.key == pygame.K_RIGHT:
                    self.x += 5
                if event.key == pygame.K_LEFT:
                    self.x -= 5

    def draw(self, screen):
        """Desenha a raposa (placeholder: retângulo laranja)."""
        pygame.draw.rect(screen, ORANGE, (self.x, self.y, self.width, self.height))
