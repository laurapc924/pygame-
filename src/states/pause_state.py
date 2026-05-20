"""Estado de pausa do Fox Crossing."""

import pygame

from src.settings import HEIGHT, WIDTH
from src.states.base_state import BaseState


class PauseState(BaseState):
    """Pausa o jogo atual, mantém seu estado em memória e mostra opções ao jogador."""

    def __init__(self, game, game_state):
        """Inicializa a pausa guardando referência ao GameState interrompido."""
        super().__init__(game)
        self.game_state = game_state
        self.font_titulo = pygame.font.SysFont(None, 100)
        self.font_opcoes = pygame.font.SysFont(None, 36)

    def handle_events(self):
        """Processa comandos da tela de pausa sem atualizar o GameState pausado."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.game.change_state(self.game_state)
                elif event.key == pygame.K_m:
                    from src.states.menu import MenuState

                    self.game.change_state(MenuState(self.game))
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self, dt):
        """Mantém a pausa congelada, sem timers ou movimentos."""
        pass

    def draw(self, screen):
        """Desenha o jogo congelado ao fundo e aplica o overlay com opções de pausa."""
        self.game_state.draw(screen)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        titulo = self.font_titulo.render("PAUSADO", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(titulo, titulo_rect)

        continuar = self.font_opcoes.render("P - Continuar", True, (255, 255, 255))
        continuar_rect = continuar.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(continuar, continuar_rect)

        menu = self.font_opcoes.render("M - Menu Principal", True, (255, 255, 255))
        menu_rect = menu.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(menu, menu_rect)

        sair = self.font_opcoes.render("ESC - Sair", True, (180, 180, 180))
        sair_rect = sair.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(sair, sair_rect)
