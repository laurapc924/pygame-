"""Estado principal de gameplay do Fox Crossing."""

import pygame

from src.entities.fox import Fox
from src.managers.map_manager import MapManager
from src.settings import HEIGHT
from src.states.base_state import BaseState
from src.states.game_over_state import GameOverState
from src.states.victory_state import VictoryState


class GameState(BaseState):
    """Estado em que o jogador controla a raposa atravessando a tela."""

    def __init__(self, game):
        super().__init__(game)
        self.map_manager = MapManager()
        self.map_manager.spawn_obstacles()
        fox_x = 30
        fox_y = HEIGHT // 2 - 20
        self.fox = Fox(fox_x, fox_y)
        self.font_hud = pygame.font.SysFont(None, 36)
        self.game.sound_manager.play_music("assets/sounds/game.mp3")

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
        """Atualiza a raposa, obstáculos, verifica colisões e condição de vitória."""
        self.fox.update(dt)
        self.map_manager.update_obstacles(dt)
        hits = pygame.sprite.spritecollide(
            self.fox,
            self.map_manager.obstacles,
            False,
            collided=lambda fox, car: fox.hitbox.colliderect(car.hitbox),
        )
        if hits and self.fox.invincible_timer <= 0:
            self.fox.lives -= 1
            self.fox.reset_position()
            self.fox.invincible_timer = 1.5
            if self.fox.lives <= 0:
                self.game.change_state(GameOverState(self.game))
                return
        goal_zone = self.map_manager.get_goal_zone()
        if self.fox.rect.colliderect(goal_zone):
            self.game.change_state(VictoryState(self.game))
            return

    def draw(self, screen):
        """Desenha mapa, obstáculos, raposa e HUD de vidas."""
        self.map_manager.draw(screen)
        self.map_manager.draw_obstacles(screen)
        self.fox.draw(screen)
        hud_text = self.font_hud.render(f"Vidas: {self.fox.lives}", True, (255, 255, 255))
        screen.blit(hud_text, (10, 10))
