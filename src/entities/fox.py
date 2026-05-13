"""Personagem principal do jogo: a raposa."""

import pygame

from src.settings import HEIGHT, WIDTH


ORANGE = (255, 140, 0)
SPEED = 300  # pixels por segundo


class Fox:
    """Raposa controlada pelo jogador."""

    def __init__(self, x, y):
        """Inicializa a raposa na posição (x, y)."""
        self.x = float(x)
        self.y = float(y)
        self.width = 40
        self.height = 40

    def handle_events(self, events):
        """Recebe a lista de eventos do frame atual (sem consumir do pygame).

        Args:
            events: Lista retornada por pygame.event.get() no GameState.
        """
        pass

    def update(self, dt):
        """Move a raposa com base nas teclas pressionadas e limita à tela.

        Args:
            dt: Delta time em segundos.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.x += SPEED * dt
        if keys[pygame.K_LEFT]:
            self.x -= SPEED * dt
        if keys[pygame.K_DOWN]:
            self.y += SPEED * dt
        if keys[pygame.K_UP]:
            self.y -= SPEED * dt

        self.x = max(0.0, min(self.x, WIDTH - self.width))
        self.y = max(0.0, min(self.y, HEIGHT - self.height))

    def draw(self, screen):
        """Desenha a raposa (placeholder: retângulo laranja)."""
        pygame.draw.rect(screen, ORANGE, (int(self.x), int(self.y), self.width, self.height))
