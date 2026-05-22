"""Tela inicial (menu) do Fox Crossing."""

import pygame

from src.settings import (
    COR_DOURADO,
    COR_TEXTO,
    COR_TEXTO_SEC,
    COR_VERDE_CLARO,
    COR_VERDE_ESCURO,
    COR_VERDE_MEDIO,
    HEIGHT,
    WIDTH,
)
from src.states.base_state import BaseState
from src.states.game_state import GameState
from src.states.instructions_state import InstructionsState
from src.utils.sprite_factory import (
    criar_raposa_estatica,
    desenhar_gradiente_vertical,
    desenhar_painel,
    desenhar_titulo_estilizado,
)


class MenuState(BaseState):
    """Tela inicial: título, raposa decorativa e opções de navegação."""

    def __init__(self, game):
        """Inicializa fontes hierárquicas, background com gradiente e decoração."""
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 110)
        self.font_subtitulo = pygame.font.SysFont(None, 36)
        self.font_opcao = pygame.font.SysFont(None, 32)
        self.font_rodape = pygame.font.SysFont(None, 22)

        self.raposa_decoracao = criar_raposa_estatica(120, 120)

        self.background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_vertical(self.background, COR_VERDE_ESCURO, COR_VERDE_MEDIO)

        self.timer_piscar = 0
        self.mostrar_enter = True

        self.game.sound_manager.play_music("assets/sounds/menu.wav")

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
        """Anima o texto 'Pressione ENTER' piscando a cada 0.6s."""
        self.timer_piscar += dt
        if self.timer_piscar >= 0.6:
            self.mostrar_enter = not self.mostrar_enter
            self.timer_piscar = 0

    def draw(self, screen):
        """Desenha o background, o título, a raposa decorativa e o painel de opções."""
        screen.blit(self.background, (0, 0))

        screen.blit(self.raposa_decoracao, (50, HEIGHT - 180))

        desenhar_titulo_estilizado(
            screen, "FOX CROSSING", self.font_titulo, WIDTH // 2, 80, COR_DOURADO
        )
        subtitulo = self.font_subtitulo.render(
            "A travessia da raposa", True, COR_VERDE_CLARO
        )
        screen.blit(subtitulo, subtitulo.get_rect(center=(WIDTH // 2, 170)))

        painel_x = WIDTH // 2 - 200
        painel_y = HEIGHT // 2 - 80
        desenhar_painel(screen, painel_x, painel_y, 400, 200)

        if self.mostrar_enter:
            enter = self.font_opcao.render(
                "Pressione ENTER para jogar", True, COR_TEXTO
            )
            screen.blit(enter, enter.get_rect(center=(WIDTH // 2, painel_y + 55)))

        instrucoes = self.font_opcao.render("I - Instruções", True, COR_TEXTO)
        screen.blit(instrucoes, instrucoes.get_rect(center=(WIDTH // 2, painel_y + 105)))

        pausa = self.font_rodape.render(
            "P pausa durante o jogo", True, COR_TEXTO_SEC
        )
        screen.blit(pausa, pausa.get_rect(center=(WIDTH // 2, painel_y + 150)))

        rodape = self.font_rodape.render(
            "Insper 2026 — Design de Software", True, COR_TEXTO_SEC
        )
        screen.blit(rodape, rodape.get_rect(center=(WIDTH // 2, HEIGHT - 25)))
