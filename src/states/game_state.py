"""Estado principal de gameplay do Fox Crossing."""

import pygame

from src.entities.fox import Fox
from src.entities.obstacle import Obstacle
from src.managers.level_manager import LevelManager
from src.managers.map_manager import MapManager
from src.managers.score_manager import ScoreManager
from src.settings import HEIGHT, WIDTH
from src.states.base_state import BaseState
from src.states.game_over_state import GameOverState
from src.states.pause_state import PauseState
from src.states.victory_state import VictoryState


class GameState(BaseState):
    """Estado em que o jogador controla a raposa atravessando as fases."""

    def __init__(self, game):
        super().__init__(game)
        Obstacle.speed_multiplier = 1.0
        self.level_manager = LevelManager()
        self.map_manager = MapManager()
        config = self.level_manager.get_config()
        self.map_manager.set_phase_config(config)
        self.map_manager.spawn_obstacles(
            speed_min=config["car_speed_min"],
            speed_max=config["car_speed_max"],
            cars_per_lane=config["cars_per_lane"],
        )
        self.map_manager.spawn_powerups()
        fox_x = 30
        fox_y = HEIGHT // 2 - 20
        self.fox = Fox(fox_x, fox_y)
        self.font_hud = pygame.font.SysFont(None, 22)
        self.font_transition = pygame.font.SysFont(None, 100)
        self.font_phase_name = pygame.font.SysFont(None, 60)
        self.font_phase_subtitle = pygame.font.SysFont(None, 28)
        self.score_manager = ScoreManager()
        self.is_transitioning = False
        self.transition_timer = 0
        self.transition_duration = 1.5
        self.transition_message = ""
        self.transition_phase_name = ""
        self.transition_phase_subtitle = ""
        self.invincible = False
        self.invincible_timer = 0.0
        self.invincible_duration = 3.0
        self.blink_timer = 0.0
        self.fox_visible = True
        self.instinct_active = False
        self.instinct_timer = 0.0
        self.instinct_duration = 2.0
        self.instinct_cooldown = 0.0
        self.instinct_cooldown_max = 10.0
        self.font_instinct = pygame.font.SysFont(None, 48)
        self.game.sound_manager.play_music("assets/sounds/game.wav")

    def handle_events(self):
        """Processa teclado: ESC encerra, SHIFT ativa Instinto, demais eventos vão para a raposa."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game.change_state(PauseState(self.game, self))
                    return
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                    return
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    if not self.instinct_active and self.instinct_cooldown <= 0:
                        self.instinct_active = True
                        self.instinct_timer = self.instinct_duration
                        Obstacle.speed_multiplier = 0.3
        if not self.is_transitioning:
            self.fox.handle_events(events)

    def _update_invincibility(self, dt):
        """Decrementa o timer de invencibilidade do power-up e controla o piscar da raposa."""
        if not self.invincible:
            return
        self.invincible_timer -= dt
        self.blink_timer += dt
        if self.blink_timer >= 0.1:
            self.fox_visible = not self.fox_visible
            self.blink_timer = 0.0
        if self.invincible_timer <= 0:
            self.invincible = False
            self.fox_visible = True

    def _update_instinct(self, dt):
        """Decrementa o timer do Instinto ativo e o cooldown após o uso."""
        if self.instinct_active:
            self.instinct_timer -= dt
            if self.instinct_timer <= 0:
                self.instinct_active = False
                Obstacle.speed_multiplier = 1.0
                self.instinct_cooldown = self.instinct_cooldown_max
        elif self.instinct_cooldown > 0:
            self.instinct_cooldown = max(0.0, self.instinct_cooldown - dt)

    def _collect_powerups(self):
        """Verifica colisão com power-ups e aplica seus efeitos."""
        coletados = pygame.sprite.spritecollide(self.fox, self.map_manager.powerups, True)
        for powerup in coletados:
            if powerup.type == "mushroom":
                self.fox.lives += 1
            elif powerup.type == "clover":
                self.invincible = True
                self.invincible_timer = self.invincible_duration
                self.blink_timer = 0.0

    def _advance_phase(self):
        """Avança para a próxima fase, reconfigura o mapa e inicia a transição visual."""
        self.level_manager.next_level()
        nova_config = self.level_manager.get_config()
        self.map_manager.set_phase_config(nova_config)
        self.map_manager.spawn_obstacles(
            speed_min=nova_config["car_speed_min"],
            speed_max=nova_config["car_speed_max"],
            cars_per_lane=nova_config["cars_per_lane"],
        )
        self.map_manager.spawn_powerups()
        self.fox.reset_position()
        self.transition_message = f"FASE {self.level_manager.current_level}"
        self.transition_phase_name = nova_config["name"]
        self.transition_phase_subtitle = nova_config["subtitle"]
        self.is_transitioning = True
        self.transition_timer = 0

    def update(self, dt):
        """Atualiza a raposa, obstáculos, power-ups, colisões, transição e condição de vitória."""
        if dt > 0.1:
            dt = 0.016

        if self.is_transitioning:
            self.transition_timer += dt
            if self.transition_timer >= self.transition_duration:
                self.is_transitioning = False
            return

        self._update_instinct(dt)
        self._update_invincibility(dt)
        self.fox.update(dt)
        self.map_manager.update_obstacles(dt)
        self.map_manager.update(dt)
        self._collect_powerups()

        if not self.invincible:
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
                    self.game.change_state(GameOverState(self.game, self.score_manager))
                    return

        goal_zone = self.map_manager.get_goal_zone()
        if self.fox.rect.colliderect(goal_zone):
            config = self.level_manager.get_config()
            self.score_manager.add_points(config["points"])

            if self.level_manager.is_final_level():
                self.game.change_state(VictoryState(self.game, self.score_manager))
                return

            self._advance_phase()

    def draw(self, screen):
        """Desenha mapa, power-ups, obstáculos, raposa (se visível), HUD e overlay de transição."""
        self.map_manager.draw(screen)
        self.map_manager.draw_obstacles(screen)
        self.map_manager.draw_powerups(screen)
        if self.fox_visible:
            self.fox.draw(screen)
        hud_vidas = self.font_hud.render(f"Vidas: {self.fox.lives}", True, (255, 255, 255))
        screen.blit(hud_vidas, (10, 10))
        hud_pontos = self.font_hud.render(f"Pontos: {self.score_manager.current_score}", True, (255, 255, 255))
        screen.blit(hud_pontos, (10, 34))
        hud_recorde = self.font_hud.render(f"Recorde: {self.score_manager.highscore}", True, (255, 255, 255))
        screen.blit(hud_recorde, (10, 58))
        hud_fase = self.font_hud.render(
            f"Fase: {self.level_manager.current_level}/{self.level_manager.TOTAL_LEVELS}",
            True, (255, 255, 255),
        )
        screen.blit(hud_fase, (10, 82))
        if self.invincible:
            hud_inv = self.font_hud.render(
                f"Inv: {self.invincible_timer:.1f}s", True, (100, 255, 100)
            )
            screen.blit(hud_inv, (10, 106))

        barra_x, barra_y = 10, 152
        barra_largura, barra_altura = 100, 14
        texto_label = self.font_hud.render("Instinto", True, (255, 255, 255))
        screen.blit(texto_label, (barra_x, barra_y - 22))
        pygame.draw.rect(screen, (60, 60, 60), (barra_x, barra_y, barra_largura, barra_altura))
        if self.instinct_active:
            fill_ratio = self.instinct_timer / self.instinct_duration
            cor = (50, 200, 220)
        elif self.instinct_cooldown > 0:
            fill_ratio = 1.0 - (self.instinct_cooldown / self.instinct_cooldown_max)
            cor = (220, 130, 30)
        else:
            fill_ratio = 1.0
            cor = (50, 200, 50)
        pygame.draw.rect(screen, cor, (barra_x, barra_y, int(barra_largura * fill_ratio), barra_altura))

        if self.instinct_active:
            texto_ativo = self.font_instinct.render("INSTINTO ATIVO", True, (50, 200, 220))
            rect_texto = texto_ativo.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(texto_ativo, rect_texto)

        if self.is_transitioning:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            linha1 = self.font_transition.render(
                self.transition_message, True, (255, 215, 0)
            )
            screen.blit(linha1, linha1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
            linha2 = self.font_phase_name.render(
                self.transition_phase_name, True, (255, 255, 255)
            )
            screen.blit(linha2, linha2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))
            linha3 = self.font_phase_subtitle.render(
                self.transition_phase_subtitle, True, (200, 200, 200)
            )
            screen.blit(linha3, linha3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 68)))
