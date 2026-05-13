"""Estado principal de gameplay do Fox Crossing."""

import pygame

from src.entities.fox import Fox
from src.managers.map_manager import MapManager
from src.settings import HEIGHT
from src.states.base_state import BaseState


class GameState(BaseState):
    """Estado em que o jogador controla a raposa atravessando a tela."""

    def __init__(self, game):
        super().__init__(game)
        self.map_manager = MapManager()
        fox_x = 30
        fox_y = HEIGHT // 2 - 20
        self.fox = Fox(fox_x, fox_y)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.running = False
                return
        self.fox.handle_events(events)

    def update(self, dt):
        self.fox.update(dt)

    def draw(self, screen):
        self.map_manager.draw(screen)
        self.fox.draw(screen)
