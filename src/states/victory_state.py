"""Tela de Vitória: mostrada quando a raposa chega na toca."""

import pygame

from src.settings import HEIGHT, WIDTH
from src.states.base_state import BaseState


class VictoryState(BaseState):
    """Estado de Vitória exibido quando a raposa alcança a zona de chegada."""

    def __init__(self, game):
        """Inicializa as fontes usadas na tela de Vitória."""
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 100)
        self.font_instrucoes = pygame.font.SysFont(None, 36)

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
        """Desenha o fundo verde, título 'VITORIA!' e instruções centralizadas."""
        screen.fill((20, 80, 40))

        titulo = self.font_titulo.render("VITORIA!", True, (255, 215, 0))
        titulo_rect = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(titulo, titulo_rect)

        subtitulo = self.font_instrucoes.render(
            "A raposa chegou na toca!", True, (255, 255, 255)
        )
        subtitulo_rect = subtitulo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
        screen.blit(subtitulo, subtitulo_rect)

        instrucao = self.font_instrucoes.render(
            "Pressione ENTER para voltar ao menu", True, (255, 255, 255)
        )
        instrucao_rect = instrucao.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(instrucao, instrucao_rect)

        sair = self.font_instrucoes.render("ESC para sair", True, (180, 180, 180))
        sair_rect = sair.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(sair, sair_rect)
