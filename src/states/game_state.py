"""Estado principal de gameplay do Fox Crossing."""

import pygame

from src.entities.fox import Fox
from src.settings import GRAY_ROAD, HEIGHT, WIDTH
from src.states.base_state import BaseState


class GameState(BaseState):
    """Estado em que o jogador controla a raposa atravessando a tela."""

    def __init__(self, game):
        super().__init__(game)
        fox_x = WIDTH // 2 - 20
        fox_y = HEIGHT // 2 - 20
        self.fox = Fox(fox_x, fox_y)

    def handle_events(self):
        if pygame.event.get(pygame.QUIT) or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.game.running = False
            return
        self.fox.handle_events()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(GRAY_ROAD)
        self.fox.draw(screen)
