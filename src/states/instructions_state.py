"""Tela de instruções e tutorial do Fox Crossing."""

import pygame

from src.settings import HEIGHT, WIDTH
from src.states.base_state import BaseState


class InstructionsState(BaseState):
    """Exibe o tutorial do jogo com objetivo, controles, power-ups e habilidade especial."""

    def __init__(self, game):
        """Inicializa a tela de instruções e suas fontes."""
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 70)
        self.font_secao = pygame.font.SysFont(None, 40)
        self.font_texto = pygame.font.SysFont(None, 28)
        self.font_rodape = pygame.font.SysFont(None, 24)

    def handle_events(self):
        """Processa eventos da tela de instruções e permite voltar ao menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_m, pygame.K_ESCAPE):
                    from src.states.menu import MenuState

                    self.game.change_state(MenuState(self.game))

    def update(self, dt):
        """Mantém a tela estática, sem lógica de atualização."""
        pass

    def _draw_text(self, screen, text, font, color, y):
        """Renderiza texto centralizado horizontalmente na posição vertical indicada."""
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(WIDTH // 2, y))
        screen.blit(surface, rect)

    def draw(self, screen):
        """Desenha todas as seções de instruções na tela."""
        screen.fill((20, 60, 30))

        dourado = (255, 215, 0)
        branco = (255, 255, 255)
        cinza_claro = (200, 200, 200)
        cinza_rodape = (180, 180, 180)

        self._draw_text(screen, "COMO JOGAR", self.font_titulo, dourado, 45)

        self._draw_text(screen, "OBJETIVO", self.font_secao, branco, 112)
        self._draw_text(screen, "Ajude a raposa a atravessar a cidade", self.font_texto, cinza_claro, 147)
        self._draw_text(screen, "e chegar na zona dourada (a toca)", self.font_texto, cinza_claro, 174)

        self._draw_text(screen, "CONTROLES", self.font_secao, branco, 222)
        self._draw_text(screen, "Setas do teclado: mover a raposa", self.font_texto, cinza_claro, 257)
        self._draw_text(screen, "SHIFT: ativar habilidade Instinto", self.font_texto, cinza_claro, 284)
        self._draw_text(screen, "P: pausar o jogo", self.font_texto, cinza_claro, 311)

        self._draw_text(screen, "ITENS ESPECIAIS", self.font_secao, branco, 359)
        self._draw_text(screen, "Cogumelo vermelho: +1 vida", self.font_texto, cinza_claro, 394)
        self._draw_text(
            screen,
            "Trevo verde: invencibilidade por 3 segundos",
            self.font_texto,
            cinza_claro,
            421,
        )

        self._draw_text(screen, "HABILIDADE: INSTINTO", self.font_secao, branco, 452)
        self._draw_text(
            screen,
            "Aperte SHIFT para reduzir a velocidade dos carros",
            self.font_texto,
            cinza_claro,
            486,
        )
        self._draw_text(screen, "Dura 2s, recarrega em 10s", self.font_texto, cinza_claro, 513)

        self._draw_text(
            screen,
            "Pressione M ou ESC para voltar ao menu",
            self.font_rodape,
            cinza_rodape,
            HEIGHT - 18,
        )
