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
    COR_VERMELHO,
    HEIGHT,
    WIDTH,
)
from src.states.base_state import BaseState
from src.utils.sprite_factory import (
    criar_arvore,
    criar_raposa_estatica,
    desenhar_estrela,
    desenhar_gradiente_multicolor,
    desenhar_painel,
    desenhar_titulo_glow,
)


GROUND_H = 84
CORES_CONFETE = [COR_DOURADO, COR_LARANJA, COR_VERDE_CLARO, (240, 240, 240), COR_VERMELHO,
                 (100, 200, 255), (220, 100, 255)]


def _cantos_rotacionados(cx, cy, w, h, angulo):
    cos_a, sin_a = math.cos(angulo), math.sin(angulo)
    hw, hh = w * 0.5, h * 0.5
    return [
        (cx + (-hw) * cos_a - (-hh) * sin_a, cy + (-hw) * sin_a + (-hh) * cos_a),
        (cx + hw * cos_a - (-hh) * sin_a,    cy + hw * sin_a + (-hh) * cos_a),
        (cx + hw * cos_a - hh * sin_a,        cy + hw * sin_a + hh * cos_a),
        (cx + (-hw) * cos_a - hh * sin_a,     cy + (-hw) * sin_a + hh * cos_a),
    ]


class VictoryState(BaseState):
    """Estado de Vitória exibido quando a raposa alcança a zona de chegada."""

    def __init__(self, game, score_manager=None):
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 104, bold=True)
        self.font_subtitulo = pygame.font.SysFont(None, 36)
        self.font_texto = pygame.font.SysFont(None, 32)
        self.font_botao = pygame.font.SysFont(None, 28)

        # Gradiente nascer do sol: azul escuro → roxo → âmbar → dourado brilhante
        self.background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_multicolor(self.background, [
            (0.00, (18, 14, 48)),
            (0.25, (65, 28, 92)),
            (0.55, (190, 88, 30)),
            (0.80, (218, 162, 38)),
            (1.00, (238, 198, 80)),
        ])

        self.raposa_feliz = criar_raposa_estatica(120, 120)
        self.arvore = criar_arvore(60, 90)
        self.tempo = 0.0
        self.timer_piscar = 0
        self.mostrar_recorde = True

        # Confete misto: retângulos giratórios + círculos + mini estrelas
        self.confete = []
        for _ in range(36):
            self.confete.append({
                "forma": "rect",
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(-HEIGHT, 0),
                "speed": random.randint(90, 200),
                "cor": random.choice(CORES_CONFETE),
                "fase": random.uniform(0, 6.28),
                "w": random.randint(5, 9),
                "h": random.randint(8, 14),
                "angulo": random.uniform(0, 6.28),
                "giro": random.uniform(-3.5, 3.5),
            })
        for _ in range(14):
            self.confete.append({
                "forma": "circulo",
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(-HEIGHT, 0),
                "speed": random.randint(80, 180),
                "cor": random.choice(CORES_CONFETE),
                "fase": random.uniform(0, 6.28),
                "r": random.randint(3, 6),
            })
        for _ in range(5):
            self.confete.append({
                "forma": "estrela",
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(-HEIGHT, 0),
                "speed": random.randint(70, 150),
                "cor": random.choice([COR_DOURADO, COR_LARANJA, (255, 255, 200)]),
                "fase": random.uniform(0, 6.28),
                "r": random.randint(5, 9),
            })

        # Fogos de artifício (5 instâncias que se reiniciam)
        self.fogos = []
        for i in range(5):
            self.fogos.append(self._novo_fogo(delay=i * 0.9))

        self.fogos_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.raios_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self.score_manager = score_manager
        self.novo_recorde = False
        if self.score_manager is not None:
            self.novo_recorde = self.score_manager.check_and_update_highscore()
        self.game.sound_manager.play_sfx(self.game.sound_manager.sfx_victory)

    def _novo_fogo(self, delay=0.0):
        return {
            "x": random.randint(WIDTH // 5, 4 * WIDTH // 5),
            "y": random.randint(40, HEIGHT // 3),
            "cor": random.choice([
                (255, 215, 0), (255, 110, 110), (110, 200, 255),
                (200, 110, 255), (255, 175, 50), (100, 255, 150),
            ]),
            "particulas": [
                {
                    "ang": i * 2 * math.pi / 18,
                    "vel": random.uniform(52, 108),
                    "vida": 1.0,
                    "decaimento": random.uniform(0.55, 0.85),
                }
                for i in range(18)
            ],
            "ativo": delay == 0,
            "timer": delay,
        }

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

        for c in self.confete:
            c["y"] += c["speed"] * dt
            if "angulo" in c:
                c["angulo"] += c["giro"] * dt
            if c["y"] > HEIGHT:
                c["y"] = random.uniform(-40, -5)
                c["x"] = random.uniform(0, WIDTH)

        for fogo in self.fogos:
            if not fogo["ativo"]:
                fogo["timer"] -= dt
                if fogo["timer"] <= 0:
                    fogo["ativo"] = True
                continue
            vivos = False
            for p in fogo["particulas"]:
                if p["vida"] > 0:
                    p["vida"] -= dt * p["decaimento"]
                    vivos = True
            if not vivos:
                novo = self._novo_fogo(delay=random.uniform(1.2, 3.8))
                fogo.update(novo)

    def _desenhar_raios_luz(self, screen):
        self.raios_surf.fill((0, 0, 0, 0))
        ox, oy = WIDTH // 2, -20
        for i in range(12):
            angulo = (i / 12) * math.pi + self.tempo * 0.05
            metade = 0.088
            ang1 = angulo - metade
            ang2 = angulo + metade
            comprimento = HEIGHT * 2.2
            p1 = (ox + math.cos(ang1) * comprimento, oy + math.sin(ang1) * comprimento)
            p2 = (ox + math.cos(ang2) * comprimento, oy + math.sin(ang2) * comprimento)
            brilho = 18 + int(10 * math.sin(self.tempo * 1.2 + i * 0.8))
            pygame.draw.polygon(self.raios_surf, (255, 218, 80, brilho), [(ox, oy), p1, p2])
        screen.blit(self.raios_surf, (0, 0))

    def _desenhar_confete(self, screen):
        for c in self.confete:
            px = c["x"] + math.sin(self.tempo * 3 + c["fase"]) * 13
            py = c["y"]
            forma = c["forma"]
            if forma == "rect":
                cantos = _cantos_rotacionados(px, py, c["w"], c["h"], c["angulo"])
                pygame.draw.polygon(screen, c["cor"], [(int(x), int(y)) for x, y in cantos])
            elif forma == "circulo":
                pygame.draw.circle(screen, c["cor"], (int(px), int(py)), c["r"])
            elif forma == "estrela":
                desenhar_estrela(screen, int(px), int(py), c["r"], c["cor"])

    def _desenhar_fogos(self, screen):
        self.fogos_surf.fill((0, 0, 0, 0))
        for fogo in self.fogos:
            if not fogo["ativo"]:
                continue
            for p in fogo["particulas"]:
                if p["vida"] <= 0:
                    continue
                t = 1.0 - p["vida"]
                px = fogo["x"] + math.cos(p["ang"]) * p["vel"] * t
                py = fogo["y"] + math.sin(p["ang"]) * p["vel"] * t + 55 * t * t
                alpha = int(255 * min(1.0, p["vida"] * 1.8))
                r = max(1, int(4 * p["vida"]))
                pygame.draw.circle(
                    self.fogos_surf, (*fogo["cor"], alpha), (int(px), int(py)), r
                )
        screen.blit(self.fogos_surf, (0, 0))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self._desenhar_raios_luz(screen)
        self._desenhar_confete(screen)

        # 3 estrelas cintilando acima do título
        for i in range(3):
            raio = 18 + 5 * math.sin(self.tempo * 3 + i * 1.5)
            desenhar_estrela(screen, WIDTH // 2 - 110 + i * 110, 48, raio, COR_DOURADO)

        chao_y = HEIGHT - GROUND_H
        pygame.draw.rect(screen, (50, 115, 55), (0, chao_y, WIDTH, GROUND_H))
        for tx in range(20, WIDTH, 150):
            screen.blit(self.arvore, (tx, chao_y - 58))

        hop = int(abs(math.sin(self.tempo * 3)) * 16)
        screen.blit(self.raposa_feliz, (62, chao_y - 104 - hop))

        # Título com glow dourado
        desenhar_titulo_glow(
            screen, "VITÓRIA!", self.font_titulo,
            WIDTH // 2, 108, COR_DOURADO, COR_LARANJA, passos=7,
        )
        subtitulo = self.font_subtitulo.render("A raposa chegou em casa!", True, COR_TEXTO)
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

        if self.novo_recorde and self.mostrar_recorde:
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

        self._desenhar_fogos(screen)
        self._desenhar_botoes(screen)

    def _desenhar_botoes(self, screen):
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
