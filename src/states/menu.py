"""Tela inicial (menu) do Fox Crossing."""

import math

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
    criar_arvore,
    criar_raposa_estatica,
    desenhar_gradiente_vertical,
    desenhar_painel,
    desenhar_titulo_estilizado,
)


# Altura da faixa de grama decorativa no rodapé da tela.
GROUND_H = 96


class MenuState(BaseState):
    """Tela inicial: cenário de floresta, título e opções de navegação."""

    def __init__(self, game):
        """Inicializa fontes, cenário de floresta e a raposa decorativa."""
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 110, bold=True)
        self.font_subtitulo = pygame.font.SysFont(None, 36)
        self.font_opcao = pygame.font.SysFont(None, 32)
        self.font_rodape = pygame.font.SysFont(None, 22)

        self.raposa_decoracao = criar_raposa_estatica(118, 118)
        self.arvore = criar_arvore(64, 96)

        self.background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_vertical(self.background, COR_VERDE_ESCURO, COR_VERDE_MEDIO)

        self.tempo = 0.0
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
        """Anima a raposa quicando e o texto 'Pressione ENTER' piscando."""
        self.tempo += dt
        self.timer_piscar += dt
        if self.timer_piscar >= 0.6:
            self.mostrar_enter = not self.mostrar_enter
            self.timer_piscar = 0

    def draw(self, screen):
        """Desenha o fundo, o chão com árvores, o título e o painel de opções."""
        screen.blit(self.background, (0, 0))

        # Faixa de grama com árvores no rodapé.
        chao_y = HEIGHT - GROUND_H
        pygame.draw.rect(screen, (38, 92, 46), (0, chao_y, WIDTH, GROUND_H))
        for tx in range(16, WIDTH, 146):
            screen.blit(self.arvore, (tx, chao_y - 66))

        # Raposa quicando suavemente, em pé na grama.
        bob = int(math.sin(self.tempo * 2.2) * 7)
        screen.blit(self.raposa_decoracao, (66, chao_y - 100 + bob))

        desenhar_titulo_estilizado(
            screen, "FOX CROSSING", self.font_titulo, WIDTH // 2, 86, COR_DOURADO
        )
        subtitulo = self.font_subtitulo.render(
            "A travessia da raposa", True, COR_VERDE_CLARO
        )
        screen.blit(subtitulo, subtitulo.get_rect(center=(WIDTH // 2, 152)))

        painel_x = WIDTH // 2 - 210
        painel_y = 198
        desenhar_painel(screen, painel_x, painel_y, 420, 196)

        if self.mostrar_enter:
            enter = self.font_opcao.render(
                "Pressione ENTER para jogar", True, COR_DOURADO
            )
            screen.blit(enter, enter.get_rect(center=(WIDTH // 2, painel_y + 56)))

        instrucoes = self.font_opcao.render("I - Instruções", True, COR_TEXTO)
        screen.blit(instrucoes, instrucoes.get_rect(center=(WIDTH // 2, painel_y + 108)))

        pausa = self.font_rodape.render("P pausa durante o jogo", True, COR_TEXTO_SEC)
        screen.blit(pausa, pausa.get_rect(center=(WIDTH // 2, painel_y + 154)))

        rodape = self.font_rodape.render(
            "Insper 2026 — Design de Software", True, COR_TEXTO
        )
        screen.blit(rodape, rodape.get_rect(center=(WIDTH // 2, HEIGHT - 20)))
