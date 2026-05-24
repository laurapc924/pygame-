"""Estado de pausa do Fox Crossing."""

import pygame

from src.settings import COR_DOURADO, COR_TEXTO, COR_TEXTO_SEC, COR_VERDE_CLARO, HEIGHT, WIDTH
from src.states.base_state import BaseState
from src.utils.fonts import get_font
from src.utils.sprite_factory import desenhar_painel, desenhar_titulo_estilizado


class PauseState(BaseState):
    """Pausa o jogo atual, mantém seu estado em memória e mostra opções ao jogador."""

    def __init__(self, game, game_state):
        """Inicializa a pausa guardando referência ao GameState interrompido."""
        super().__init__(game)
        self.game_state = game_state
        self.font_titulo = get_font(72, bold=True)
        self.font_subtitulo = get_font(23)
        self.font_opcoes = get_font(24, bold=True)
        self.font_tecla = get_font(19, bold=True)

    def _draw_pause_option(self, screen, rect, key, text, muted=False):
        """Desenha uma opcao de pausa com tecla destacada."""
        cor_texto = COR_TEXTO_SEC if muted else COR_TEXTO
        borda = (255, 255, 255, 45) if muted else (255, 215, 0, 150)
        pygame.draw.rect(screen, (255, 255, 255, 22), rect, border_radius=13)
        pygame.draw.rect(screen, borda, rect, 1, border_radius=13)

        key_rect = pygame.Rect(rect.x + 12, rect.y + 9, 58, rect.h - 18)
        pygame.draw.rect(screen, (16, 24, 22, 220), key_rect, border_radius=9)
        pygame.draw.rect(screen, COR_DOURADO if not muted else COR_TEXTO_SEC, key_rect, 1, border_radius=9)
        key_surf = self.font_tecla.render(key, True, COR_DOURADO if not muted else COR_TEXTO_SEC)
        screen.blit(key_surf, key_surf.get_rect(center=key_rect.center))

        text_surf = self.font_opcoes.render(text, True, cor_texto)
        screen.blit(text_surf, text_surf.get_rect(midleft=(rect.x + 88, rect.centery)))

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
            ("P", "Continuar", False),
            ("M", "Menu principal", False),
            ("ESC", "Sair", True),
        ]
        for i, (tecla, texto, muted) in enumerate(opcoes):
            option_rect = pygame.Rect(painel_x + 56, painel_y + 128 + i * 52, 328, 42)
            self._draw_pause_option(screen, option_rect, tecla, texto, muted)
