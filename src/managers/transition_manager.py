"""Gerenciador de transições visuais entre estados do jogo."""

import pygame

from src.settings import HEIGHT, WIDTH


class TransitionManager:
    """Gerencia transições de fade-to-black e fade-from-black entre estados."""

    FADE_DURATION = 0.25

    def __init__(self):
        """Inicializa o gerenciador sem transição ativa."""
        self.is_transitioning = False
        self.phase = "none"
        self.timer = 0
        self.pending_state = None
        self.alpha = 0

    def start(self, new_state):
        """Inicia transição para o new_state."""
        if self.is_transitioning:
            return

        self.is_transitioning = True
        self.phase = "fade_out"
        self.timer = 0
        self.pending_state = new_state
        self.alpha = 0

    def update(self, dt, game):
        """Atualiza a transição e troca o estado no momento certo."""
        if not self.is_transitioning:
            return

        self.timer += dt
        progress = min(self.timer / self.FADE_DURATION, 1.0)

        if self.phase == "fade_out":
            self.alpha = int(255 * progress)
            if progress >= 1.0:
                game.current_state = self.pending_state
                self.phase = "fade_in"
                self.timer = 0
                self.alpha = 255
        elif self.phase == "fade_in":
            self.alpha = int(255 * (1 - progress))
            if progress >= 1.0:
                self.is_transitioning = False
                self.phase = "none"
                self.alpha = 0
                self.pending_state = None

    def draw(self, screen):
        """Desenha o overlay de fade por cima de tudo."""
        if not self.is_transitioning:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.alpha))
        screen.blit(overlay, (0, 0))
