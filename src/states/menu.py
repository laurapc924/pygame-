"""Tela inicial (menu) do Fox Crossing."""

import math
import random

import pygame

from src.settings import (
    COR_DOURADO,
    COR_LARANJA,
    COR_TEXTO,
    COR_TEXTO_SEC,
    COR_VERDE_CLARO,
    HEIGHT,
    WIDTH,
)
from src.states.base_state import BaseState
from src.states.game_state import GameState
from src.states.instructions_state import InstructionsState
from src.utils.fonts import get_font
from src.utils.sprite_factory import (
    criar_arvore,
    criar_arvore_silhueta,
    criar_raposa_estatica,
    desenhar_estrela,
    desenhar_gradiente_multicolor,
    desenhar_painel,
    desenhar_titulo_glow,
)


GROUND_H = 96


class MenuState(BaseState):
    """Tela inicial: floresta ao entardecer, título e opções de navegação."""

    def __init__(self, game):
        super().__init__(game)
        self.font_titulo = get_font(96, bold=True)
        self.font_subtitulo = get_font(32)
        self.font_opcao = get_font(26, bold=True)
        self.font_key = get_font(20, bold=True)
        self.font_hint = pygame.font.SysFont("Arial", 18)
        self.font_rodape = get_font(18)

        self.raposa_decoracao = criar_raposa_estatica(118, 118)
        self.arvore_silhueta = criar_arvore_silhueta(40, 60, (18, 10, 32))
        self.arvore_meio = criar_arvore(58, 88)
        self.arvore_frente = criar_arvore(82, 122)

        # Gradiente entardecer: índigo → roxo → âmbar → dourado
        self.background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_multicolor(self.background, [
            (0.00, (22, 12, 50)),
            (0.30, (80, 28, 75)),
            (0.62, (178, 68, 28)),
            (1.00, (212, 138, 36)),
        ])

        # Estrelas cintilando no céu entardecer
        self.estrelas = [
            {
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, int(HEIGHT * 0.48)),
                "r": random.choice([1, 1, 1, 2]),
                "fase": random.uniform(0, 6.28),
            }
            for _ in range(40)
        ]

        # Vagalumes perto da floresta
        self.vagalumes = [
            {
                "x": random.uniform(120, WIDTH - 20),
                "y": random.uniform(HEIGHT * 0.44, HEIGHT - GROUND_H - 8),
                "vx": random.uniform(-15, 15),
                "vy": random.uniform(-8, 8),
                "fase": random.uniform(0, 6.28),
                "r": random.choice([2, 2, 3]),
            }
            for _ in range(20)
        ]

        self.tempo = 0.0
        self.timer_piscar = 0
        self.mostrar_enter = True

        self.game.sound_manager.play_music("assets/sounds/menu.wav")

    def _draw_menu_button(self, screen, rect, key, text, active=False):
        """Desenha uma opcao do menu com tecla destacada."""
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
        self.tempo += dt
        self.timer_piscar += dt
        if self.timer_piscar >= 0.6:
            self.mostrar_enter = not self.mostrar_enter
            self.timer_piscar = 0

        for v in self.vagalumes:
            v["x"] += v["vx"] * dt + math.sin(self.tempo * 0.8 + v["fase"]) * 0.9
            v["y"] += v["vy"] * dt + math.cos(self.tempo * 0.6 + v["fase"]) * 0.5
            if v["x"] < 80 or v["x"] > WIDTH - 10:
                v["vx"] *= -1
            if v["y"] < HEIGHT * 0.43 or v["y"] > HEIGHT - GROUND_H - 6:
                v["vy"] *= -1

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        # Estrelas cintilando individualmente
        for e in self.estrelas:
            brilho = 0.5 + 0.5 * math.sin(self.tempo * 1.6 + e["fase"])
            alpha = int(210 * brilho)
            sv = pygame.Surface((e["r"] * 2 + 2, e["r"] * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(sv, (255, 245, 200, alpha), (e["r"] + 1, e["r"] + 1), e["r"])
            screen.blit(sv, (int(e["x"]) - e["r"] - 1, int(e["y"]) - e["r"] - 1))

        # Silhueta de árvores ao fundo (menores, mais escuras)
        chao_y = HEIGHT - GROUND_H
        for tx in range(0, WIDTH, 76):
            screen.blit(self.arvore_silhueta, (tx, chao_y - 44))

        # Faixa de grama
        pygame.draw.rect(screen, (22, 52, 24), (0, chao_y, WIDTH, GROUND_H))

        # Árvores no plano médio
        for tx in range(22, WIDTH, 128):
            screen.blit(self.arvore_meio, (tx, chao_y - 66))

        # Árvores no primeiro plano
        for tx in range(200, WIDTH, 220):
            screen.blit(self.arvore_frente, (tx, chao_y - 90))

        # Vagalumes brilhando com halo suave
        for v in self.vagalumes:
            brilho_v = 0.35 + 0.65 * abs(math.sin(self.tempo * 3.5 + v["fase"]))
            alpha_v = int(220 * brilho_v)
            sv = pygame.Surface((v["r"] * 6, v["r"] * 6), pygame.SRCALPHA)
            cx_v, cy_v = v["r"] * 3, v["r"] * 3
            pygame.draw.circle(sv, (160, 255, 100, alpha_v // 5), (cx_v, cy_v), v["r"] * 3)
            pygame.draw.circle(sv, (200, 255, 140, alpha_v // 2), (cx_v, cy_v), v["r"] * 2)
            pygame.draw.circle(sv, (230, 255, 180, alpha_v), (cx_v, cy_v), v["r"])
            screen.blit(sv, (int(v["x"]) - v["r"] * 3, int(v["y"]) - v["r"] * 3))

        # Raposa quicando suavemente na grama
        bob = int(math.sin(self.tempo * 2.2) * 7)
        screen.blit(self.raposa_decoracao, (66, chao_y - 100 + bob))

        # Estrela decorativa pulsando no canto
        raio_estrela = 18 + 4 * math.sin(self.tempo * 2.2)
        desenhar_estrela(screen, WIDTH - 80, 54, raio_estrela, COR_DOURADO)

        # Título com glow laranja/dourado
        desenhar_titulo_glow(
            screen, "FOX CROSSING", self.font_titulo,
            WIDTH // 2, 86, COR_DOURADO, COR_LARANJA, passos=6,
        )
        subtitulo = self.font_subtitulo.render("A travessia da raposa", True, COR_VERDE_CLARO)
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

        rodape = self.font_rodape.render("Insper 2026 — Design de Software", True, COR_TEXTO)
        screen.blit(rodape, rodape.get_rect(center=(WIDTH // 2, HEIGHT - 20)))
