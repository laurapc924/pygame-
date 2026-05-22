"""Tela de Vitória: mostrada quando a raposa chega na toca."""

import math
import random

import pygame

from src.settings import (
    COR_DOURADO,
    COR_LARANJA,
    COR_TEXTO,
    COR_TEXTO_SEC,
    COR_VERDE_CLARO,
    COR_VERDE_MEDIO,
    COR_VERMELHO,
    HEIGHT,
    WIDTH,
)
from src.states.base_state import BaseState
from src.utils.sprite_factory import (
    criar_arvore,
    criar_raposa_estatica,
    desenhar_estrela,
    desenhar_gradiente_vertical,
    desenhar_painel,
    desenhar_titulo_estilizado,
)


# Altura da faixa de grama decorativa no rodapé.
GROUND_H = 84
# Cores festivas usadas no confete.
CORES_CONFETE = [COR_DOURADO, COR_LARANJA, COR_VERDE_CLARO, COR_TEXTO, COR_VERMELHO]


class VictoryState(BaseState):
    """Estado de Vitória exibido quando a raposa alcança a zona de chegada."""

    def __init__(self, game, score_manager=None):
        """Inicializa fontes, cenário, confete, decoração e verifica novo recorde."""
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 104, bold=True)
        self.font_subtitulo = pygame.font.SysFont(None, 36)
        self.font_texto = pygame.font.SysFont(None, 32)
        self.font_botao = pygame.font.SysFont(None, 28)

        self.background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_vertical(self.background, COR_VERDE_MEDIO, COR_VERDE_CLARO)

        self.raposa_feliz = criar_raposa_estatica(120, 120)
        self.arvore = criar_arvore(60, 90)
        self.tempo = 0.0

        # Confete colorido caindo do topo da tela.
        self.confete = [
            {
                "x": random.randint(0, WIDTH),
                "y": random.randint(-HEIGHT, 0),
                "speed": random.randint(90, 200),
                "cor": random.choice(CORES_CONFETE),
                "fase": random.uniform(0, 6.28),
                "w": random.randint(4, 8),
                "h": random.randint(7, 12),
            }
            for _ in range(45)
        ]

        self.score_manager = score_manager
        self.novo_recorde = False
        if self.score_manager is not None:
            self.novo_recorde = self.score_manager.check_and_update_highscore()
        self.game.sound_manager.play_sfx(self.game.sound_manager.sfx_victory)

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
        """Avança o tempo (estrelas/raposa) e faz o confete cair, reciclando no topo."""
        self.tempo += dt
        for c in self.confete:
            c["y"] += c["speed"] * dt
            if c["y"] > HEIGHT:
                c["y"] = random.randint(-40, -5)
                c["x"] = random.randint(0, WIDTH)

    def _desenhar_confete(self, screen):
        """Desenha o confete caindo, com leve balanço horizontal.

        Args:
            screen: Surface destino.
        """
        for c in self.confete:
            px = c["x"] + math.sin(self.tempo * 3 + c["fase"]) * 12
            pygame.draw.rect(screen, c["cor"], (int(px), int(c["y"]), c["w"], c["h"]))

    def draw(self, screen):
        """Desenha cenário, confete, estrelas, título, pontuação, recorde e botões."""
        screen.blit(self.background, (0, 0))
        self._desenhar_confete(screen)

        # 3 estrelas cintilando acima do título (raio varia com seno do tempo).
        for i in range(3):
            raio = 18 + 5 * math.sin(self.tempo * 3 + i * 1.5)
            desenhar_estrela(screen, WIDTH // 2 - 110 + i * 110, 48, raio, COR_DOURADO)

        # Faixa de grama com árvores no rodapé.
        chao_y = HEIGHT - GROUND_H
        pygame.draw.rect(screen, (60, 135, 65), (0, chao_y, WIDTH, GROUND_H))
        for tx in range(20, WIDTH, 150):
            screen.blit(self.arvore, (tx, chao_y - 58))

        # Raposa pulando de alegria sobre a grama.
        hop = int(abs(math.sin(self.tempo * 3)) * 16)
        screen.blit(self.raposa_feliz, (62, chao_y - 104 - hop))

        desenhar_titulo_estilizado(
            screen, "VITÓRIA!", self.font_titulo, WIDTH // 2, 108, COR_DOURADO
        )
        subtitulo = self.font_subtitulo.render(
            "A raposa chegou em casa!", True, COR_TEXTO
        )
        screen.blit(subtitulo, subtitulo.get_rect(center=(WIDTH // 2, 172)))

        painel_w = 440
        painel_x = WIDTH // 2 - painel_w // 2
        desenhar_painel(screen, painel_x, 210, painel_w, 118)
        if self.score_manager is not None:
            pontos = self.font_texto.render(
                f"Pontos finais: {self.score_manager.current_score}", True, COR_TEXTO
            )
            screen.blit(pontos, pontos.get_rect(center=(WIDTH // 2, 247)))
            recorde = self.font_texto.render(
                f"Recorde: {self.score_manager.highscore}", True, COR_TEXTO_SEC
            )
            screen.blit(recorde, recorde.get_rect(center=(WIDTH // 2, 293)))

        if self.novo_recorde and int(self.tempo * 2) % 2 == 0:
            desenhar_painel(
                screen,
                WIDTH // 2 - 150,
                340,
                300,
                46,
                cor=(80, 65, 0, 215),
                borda_cor=COR_DOURADO,
            )
            recorde_novo = self.font_texto.render("NOVO RECORDE!", True, COR_DOURADO)
            screen.blit(recorde_novo, recorde_novo.get_rect(center=(WIDTH // 2, 363)))

        self._desenhar_botoes(screen)

    def _desenhar_botoes(self, screen):
        """Desenha os botões '[ENTER] Voltar ao menu' e '[ESC] Sair' em painéis.

        Args:
            screen: Surface destino.
        """
        botao_y = 430
        botao_h = 52
        esq_w, dir_w = 280, 150
        esq_x = WIDTH // 2 - (esq_w + 16 + dir_w) // 2
        dir_x = esq_x + esq_w + 16

        desenhar_painel(screen, esq_x, botao_y, esq_w, botao_h)
        voltar = self.font_botao.render("[ENTER] Voltar ao menu", True, COR_TEXTO)
        screen.blit(
            voltar, voltar.get_rect(center=(esq_x + esq_w // 2, botao_y + botao_h // 2))
        )

        desenhar_painel(screen, dir_x, botao_y, dir_w, botao_h)
        sair = self.font_botao.render("[ESC] Sair", True, COR_TEXTO_SEC)
        screen.blit(
            sair, sair.get_rect(center=(dir_x + dir_w // 2, botao_y + botao_h // 2))
        )
