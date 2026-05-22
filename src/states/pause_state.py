"""Estado de pausa do Fox Crossing."""

import pygame

from src.settings import COR_DOURADO, COR_TEXTO, COR_TEXTO_SEC, COR_VERDE_CLARO, HEIGHT, WIDTH
from src.states.base_state import BaseState
from src.utils.sprite_factory import desenhar_painel, desenhar_titulo_estilizado


class PauseState(BaseState):
    """Pausa o jogo atual, mantém seu estado em memória e mostra opções ao jogador."""

    def __init__(self, game, game_state):
        """Inicializa a pausa guardando referência ao GameState interrompido."""
        super().__init__(game)
        self.game_state = game_state
        self.font_titulo = pygame.font.SysFont(None, 80)
        self.font_subtitulo = pygame.font.SysFont(None, 26)
        self.font_opcoes = pygame.font.SysFont(None, 32)

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
        """Desenha o jogo congelado ao fundo e aplica o painel de pausa."""
        self.game_state.draw(screen)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        painel_w, painel_h = 440, 300
        painel_x = WIDTH // 2 - painel_w // 2
        painel_y = HEIGHT // 2 - painel_h // 2
        desenhar_painel(screen, painel_x, painel_y, painel_w, painel_h)

        desenhar_titulo_estilizado(
            screen, "PAUSADO", self.font_titulo, WIDTH // 2, painel_y + 52, COR_DOURADO
        )
        subtitulo = self.font_subtitulo.render("Tempo congelado", True, COR_VERDE_CLARO)
        screen.blit(subtitulo, subtitulo.get_rect(center=(WIDTH // 2, painel_y + 95)))

        opcoes = [
            ("P - Continuar", COR_TEXTO),
            ("M - Menu Principal", COR_TEXTO),
            ("ESC - Sair", COR_TEXTO_SEC),
        ]
        for i, (texto, cor) in enumerate(opcoes):
            opcao_surf = self.font_opcoes.render(texto, True, cor)
            screen.blit(
                opcao_surf,
                opcao_surf.get_rect(center=(WIDTH // 2, painel_y + 150 + i * 45)),
            )
