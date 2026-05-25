"""Tela inicial (menu) do Fox Crossing."""

import pygame

from src.settings import (
    COR_DOURADO,
    COR_LARANJA,
    COR_TEXTO,
    COR_TEXTO_SEC,
    HEIGHT,
    WIDTH,
)
from src.states.base_state import BaseState
from src.states.game_state import GameState
from src.states.instructions_state import InstructionsState
from src.utils.fonts import get_font
from src.utils.sprite_factory import (
    criar_background_menu_cidade,
    desenhar_painel,
    desenhar_titulo_glow,
)


class MenuState(BaseState):
    """Tela inicial: cidade pixel-art ao fundo com título e opções de navegação."""

    def __init__(self, game):
        """Inicializa fontes, background da cidade e estado da animação de piscar."""
        super().__init__(game)
        self.font_titulo = get_font(96, bold=True)
        self.font_subtitulo = get_font(32)
        self.font_opcao = get_font(26, bold=True)
        self.font_key = get_font(20, bold=True)
        self.font_hint = pygame.font.SysFont("Arial", 18)
        self.font_rodape = get_font(18)

        # Background fixo: cena pixel-art de cidade de dia (céu, prédios, rua).
        self.background = criar_background_menu_cidade(WIDTH, HEIGHT)

        self.timer_piscar = 0
        self.mostrar_enter = True

        self.game.sound_manager.play_music("assets/sounds/menu.wav")

    def _draw_menu_button(self, screen, rect, key, text, active=False):
        """Desenha uma opção do menu com tecla destacada."""
        fill = (36, 74, 46, 225) if active else (18, 30, 27, 205)
        border = (255, 215, 90) if active else (180, 215, 170)
        pygame.draw.rect(screen, fill, rect, border_radius=14)
        pygame.draw.rect(screen, border, rect, 2, border_radius=14)
        if active:
            pygame.draw.rect(
                screen, (255, 215, 90), (rect.x, rect.y, 7, rect.h), border_radius=14
            )

        key_rect = pygame.Rect(rect.x + 14, rect.y + 10, 104, rect.h - 20)
        pygame.draw.rect(screen, (18, 26, 24, 210), key_rect, border_radius=10)
        pygame.draw.rect(screen, border, key_rect, 1, border_radius=10)

        key_surf = self.font_key.render(key, True, COR_DOURADO)
        screen.blit(key_surf, key_surf.get_rect(center=key_rect.center))
        text_color = (255, 240, 160) if active else COR_TEXTO
        text_surf = self.font_opcao.render(text, True, text_color)
        screen.blit(text_surf, text_surf.get_rect(midleft=(rect.x + 140, rect.centery)))

    def handle_events(self):
        """Processa teclado: ENTER joga, I abre instruções, ESC sai."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_state(GameState(self.game))
                if event.key == pygame.K_i:
                    self.game.change_state(InstructionsState(self.game))
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self, dt):
        """Anima o texto 'ENTER' piscando a cada 0.6s."""
        self.timer_piscar += dt
        if self.timer_piscar >= 0.6:
            self.mostrar_enter = not self.mostrar_enter
            self.timer_piscar = 0

    def draw(self, screen):
        """Desenha a cidade ao fundo e o painel com as opções por cima."""
        screen.blit(self.background, (0, 0))

        desenhar_titulo_glow(
            screen, "FOX CROSSING", self.font_titulo,
            WIDTH // 2, 86, COR_DOURADO, COR_LARANJA, passos=6,
        )
        subtitulo = self.font_subtitulo.render(
            "Volta ao mundo da raposa", True, (0, 0, 0)
        )
        screen.blit(subtitulo, subtitulo.get_rect(center=(WIDTH // 2, 152)))

        painel_x = WIDTH // 2 - 230
        painel_y = 198
        desenhar_painel(screen, painel_x, painel_y, 460, 206)

        jogar_rect = pygame.Rect(painel_x + 28, painel_y + 28, 404, 58)
        self._draw_menu_button(screen, jogar_rect, "ENTER", "Jogar", self.mostrar_enter)

        self._draw_menu_button(
            screen, pygame.Rect(painel_x + 28, painel_y + 98, 404, 50), "I", "Instruções"
        )

        pausa = self.font_hint.render("Durante o jogo: P para pausar", True, COR_TEXTO_SEC)
        screen.blit(pausa, pausa.get_rect(center=(WIDTH // 2, painel_y + 174)))

        rodape = self.font_rodape.render(
            "Insper 2026 — Design de Software", True, COR_TEXTO
        )
        screen.blit(rodape, rodape.get_rect(center=(WIDTH // 2, HEIGHT - 20)))
