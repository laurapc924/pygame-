"""Tela de Game Over: mostrada quando o jogador perde todas as vidas."""

import pygame

from src.settings import HEIGHT, WIDTH
from src.states.base_state import BaseState


class GameOverState(BaseState):
    """Estado de Game Over exibido quando a raposa perde todas as vidas."""

    def __init__(self, game, score_manager=None):
        """Inicializa as fontes e verifica se houve novo recorde."""
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 100)
        self.font_instrucoes = pygame.font.SysFont(None, 36)
        self.score_manager = score_manager
        self.novo_recorde = False
        if self.score_manager is not None:
            self.novo_recorde = self.score_manager.check_and_update_highscore()
        self.game.sound_manager.play_sfx(self.game.sound_manager.sfx_collision)

    def handle_events(self):
        """Processa eventos: ENTER volta ao menu, ESC encerra o jogo."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from src.states.menu import MenuState
                    self.game.change_state(MenuState(self.game))
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self, dt):
        """Tela estática: nada a atualizar."""
        pass

    def draw(self, screen):
        """Desenha fundo preto, título, pontuação, recorde/novo recorde e instruções."""
        screen.fill((0, 0, 0))

        titulo = self.font_titulo.render("GAME OVER", True, (220, 50, 50))
        titulo_rect = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(titulo, titulo_rect)

        if self.score_manager is not None:
            pontos_surf = self.font_instrucoes.render(
                f"Pontos finais: {self.score_manager.current_score}", True, (255, 255, 255)
            )
            pontos_rect = pontos_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            screen.blit(pontos_surf, pontos_rect)

            if self.novo_recorde:
                recorde_surf = self.font_instrucoes.render(
                    "NOVO RECORDE!", True, (255, 215, 0)
                )
            else:
                recorde_surf = self.font_instrucoes.render(
                    f"Recorde: {self.score_manager.highscore}", True, (200, 200, 200)
                )
            recorde_rect = recorde_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
            screen.blit(recorde_surf, recorde_rect)

        instrucao = self.font_instrucoes.render(
            "Pressione ENTER para voltar ao menu", True, (255, 255, 255)
        )
        instrucao_rect = instrucao.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(instrucao, instrucao_rect)

        sair = self.font_instrucoes.render("ESC para sair", True, (180, 180, 180))
        sair_rect = sair.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 110))
        screen.blit(sair, sair_rect)
