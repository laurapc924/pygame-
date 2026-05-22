"""Tela de Game Over: mostrada quando o jogador perde todas as vidas."""

import math
import random

import pygame

from src.settings import (
    COR_DOURADO,
    COR_TEXTO,
    COR_TEXTO_SEC,
    COR_VERMELHO,
    HEIGHT,
    WIDTH,
)
from src.states.base_state import BaseState
from src.utils.sprite_factory import (
    criar_lua,
    criar_raposa_estatica,
    desenhar_gradiente_multicolor,
    desenhar_painel,
    desenhar_titulo_glow,
)


GROUND_H = 66


class GameOverState(BaseState):
    """Estado de Game Over exibido quando a raposa perde todas as vidas."""

    def __init__(self, game, score_manager=None):
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 120, bold=True)
        self.font_subtitulo = pygame.font.SysFont(None, 34)
        self.font_texto = pygame.font.SysFont(None, 32)
        self.font_botao = pygame.font.SysFont(None, 28)

        # Gradiente noturno dramático: azul-preto → roxo escuro → marrom escarlate
        self.background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_multicolor(self.background, [
            (0.00, (6,  4, 18)),
            (0.35, (22,  8, 32)),
            (0.65, (40,  8, 20)),
            (1.00, (16,  4,  8)),
        ])

        self.raposa_triste = criar_raposa_estatica(118, 118, olhos_fechados=True)
        self.lua = criar_lua(50)

        # Estrelas abundantes no céu
        self.estrelas = [
            {
                "x": random.randint(0, WIDTH),
                "y": random.randint(8, 340),
                "r": random.choice([1, 1, 1, 2, 2]),
                "fase": random.uniform(0, 6.28),
                "brilho_base": random.uniform(0.45, 0.75),
            }
            for _ in range(55)
        ]

        # Gotas de chuva
        self.chuva = [
            {
                "x": random.uniform(-80, WIDTH + 80),
                "y": random.uniform(-HEIGHT, 0),
                "velocidade": random.randint(320, 520),
            }
            for _ in range(70)
        ]

        # Estrela cadente ocasional
        self.estrela_cadente = {
            "ativa": False,
            "timer": random.uniform(2.0, 5.0),
            "x": 0.0, "y": 0.0,
            "dx": 0.0, "dy": 0.0,
            "vida": 1.0,
        }

        # Surface reutilizável para efeitos com alpha
        self.efeitos_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self.tempo = 0.0
        self.timer_piscar = 0
        self.mostrar_recorde = True

        self.score_manager = score_manager
        self.novo_recorde = False
        if self.score_manager is not None:
            self.novo_recorde = self.score_manager.check_and_update_highscore()
        self.game.sound_manager.play_sfx(self.game.sound_manager.sfx_collision)

    def handle_events(self):
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
        self.tempo += dt
        self.timer_piscar += dt
        if self.timer_piscar >= 0.5:
            self.mostrar_recorde = not self.mostrar_recorde
            self.timer_piscar = 0

        for gota in self.chuva:
            gota["y"] += gota["velocidade"] * dt
            gota["x"] -= gota["velocidade"] * 0.22 * dt
            if gota["y"] > HEIGHT:
                gota["y"] = random.uniform(-60, 0)
                gota["x"] = random.uniform(0, WIDTH + 80)

        ec = self.estrela_cadente
        if not ec["ativa"]:
            ec["timer"] -= dt
            if ec["timer"] <= 0:
                ec["ativa"] = True
                ec["x"] = float(random.randint(WIDTH // 3, WIDTH))
                ec["y"] = float(random.randint(0, HEIGHT // 6))
                ang = random.uniform(math.pi * 0.55, math.pi * 0.72)
                speed = random.randint(380, 580)
                ec["dx"] = math.cos(ang) * speed
                ec["dy"] = math.sin(ang) * speed
                ec["vida"] = 1.0
        else:
            ec["x"] += ec["dx"] * dt
            ec["y"] += ec["dy"] * dt
            ec["vida"] -= dt * 1.4
            if ec["vida"] <= 0 or ec["x"] < 0 or ec["y"] > HEIGHT:
                ec["ativa"] = False
                ec["timer"] = random.uniform(3.5, 7.0)

    def _desenhar_ceu(self, screen):
        for estrela in self.estrelas:
            amp = 1.0 - estrela["brilho_base"]
            brilho = estrela["brilho_base"] + amp * math.sin(self.tempo * 2 + estrela["fase"])
            tom = max(0, int(225 * brilho))
            pygame.draw.circle(
                screen, (tom, tom, max(0, tom - 20)), (estrela["x"], estrela["y"]), estrela["r"]
            )
        screen.blit(self.lua, (WIDTH - 165, 18))

    def _desenhar_efeitos(self, screen):
        self.efeitos_surf.fill((0, 0, 0, 0))

        # Chuva diagonal
        for gota in self.chuva:
            comp = 13
            x0, y0 = int(gota["x"]), int(gota["y"])
            x1 = int(gota["x"] - comp * 0.22)
            y1 = int(gota["y"] - comp)
            pygame.draw.line(self.efeitos_surf, (120, 155, 220, 150), (x0, y0), (x1, y1), 1)

        # Estrela cadente com rastro
        ec = self.estrela_cadente
        if ec["ativa"] and ec["vida"] > 0:
            norm = math.hypot(ec["dx"], ec["dy"])
            if norm > 0:
                ux, uy = ec["dx"] / norm, ec["dy"] / norm
                comprimento = int(ec["vida"] * 72)
                x1, y1 = int(ec["x"]), int(ec["y"])
                x0 = int(ec["x"] - ux * comprimento)
                y0 = int(ec["y"] - uy * comprimento)
                alpha = int(255 * ec["vida"])
                pygame.draw.line(
                    self.efeitos_surf, (255, 240, 180, alpha), (x0, y0), (x1, y1), 2
                )
                pygame.draw.circle(
                    self.efeitos_surf, (255, 255, 220, alpha), (x1, y1), 2
                )

        screen.blit(self.efeitos_surf, (0, 0))

    def _desenhar_nevoa(self, screen):
        chao_y = HEIGHT - GROUND_H
        nevoa = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i, (alfa, largura, y_offset) in enumerate([
            (28, WIDTH, 0),
            (18, WIDTH, -14),
            (12, int(WIDTH * 0.75), -26),
        ]):
            pygame.draw.ellipse(
                nevoa,
                (90, 110, 140, alfa),
                (-(largura // 6), chao_y + y_offset - 16, largura + largura // 3, 40),
            )
        screen.blit(nevoa, (0, 0))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self._desenhar_ceu(screen)
        self._desenhar_efeitos(screen)

        chao_y = HEIGHT - GROUND_H
        pygame.draw.rect(screen, (12, 4, 4), (0, chao_y, WIDTH, GROUND_H))
        self._desenhar_nevoa(screen)

        bob = int(math.sin(self.tempo * 1.6) * 4)
        screen.blit(self.raposa_triste, (46, chao_y - 104 + bob))

        # Título pulsando em vermelho com glow
        pulse = 0.5 + 0.5 * math.sin(self.tempo * 2.4)
        r_glow = int(160 + 40 * pulse)
        desenhar_titulo_glow(
            screen, "GAME OVER", self.font_titulo,
            WIDTH // 2, 92, COR_VERMELHO, (r_glow, 0, 0), passos=7,
        )
        subtitulo = self.font_subtitulo.render(
            "A raposa não conseguiu...", True, COR_TEXTO_SEC
        )
        screen.blit(subtitulo, subtitulo.get_rect(center=(WIDTH // 2, 162)))

        painel_w = 440
        painel_x = WIDTH // 2 - painel_w // 2
        desenhar_painel(screen, painel_x, 200, painel_w, 120)
        if self.score_manager is not None:
            pontos = self.font_texto.render(
                f"Pontos finais: {self.score_manager.current_score}", True, COR_TEXTO
            )
            screen.blit(pontos, pontos.get_rect(center=(WIDTH // 2, 237)))
            recorde = self.font_texto.render(
                f"Recorde: {self.score_manager.highscore}", True, COR_TEXTO_SEC
            )
            screen.blit(recorde, recorde.get_rect(center=(WIDTH // 2, 283)))

        if self.novo_recorde and self.mostrar_recorde:
            desenhar_painel(
                screen,
                WIDTH // 2 - 150,
                334,
                300,
                46,
                cor=(80, 65, 0, 215),
                borda_cor=COR_DOURADO,
            )
            recorde_novo = self.font_texto.render("NOVO RECORDE!", True, COR_DOURADO)
            screen.blit(recorde_novo, recorde_novo.get_rect(center=(WIDTH // 2, 357)))

        self._desenhar_botoes(screen)

    def _desenhar_botoes(self, screen):
        botao_y = 440
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
