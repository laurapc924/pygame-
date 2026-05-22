"""Gerenciador do mapa: floresta nas laterais e 3 faixas de rua verticais."""

import pygame
import random

from src.entities.obstacle import Obstacle
from src.entities.powerup import PowerUp
from src.settings import HEIGHT, IMG_DIR, WHITE, WIDTH
from src.utils.sprite_factory import (
    criar_arvore,
    criar_asfalto_textura,
    criar_asfalto_textura_colorida,
    criar_cerca,
    criar_coqueiro,
    criar_grama_textura,
    criar_grama_textura_colorida,
    criar_pedra,
    criar_pinheiro,
    criar_poste,
    desenhar_gradiente_vertical,
)


SIDE_STRIP_WIDTH = 120
NUM_LANES = 3
ROAD_AREA_WIDTH = WIDTH - 2 * SIDE_STRIP_WIDTH
LANE_WIDTH = ROAD_AREA_WIDTH // NUM_LANES

DASH_LENGTH = 20
DASH_GAP = 15
DASH_THICKNESS = 3

DECOR_W = 50
DECOR_H = 80

# Sprites decorativos laterais disponíveis, indexados pelo tema da fase.
DECORACOES = {
    "arvore": criar_arvore,
    "poste": criar_poste,
    "coqueiro": criar_coqueiro,
    "pinheiro": criar_pinheiro,
    "pedra": criar_pedra,
    "cerca": criar_cerca,
}

CAR_FILES = [
    "car_red_1.png",
    "car_blue_1.png",
    "car_green_1.png",
    "car_yellow_1.png",
    "car_black_1.png",
    "car_red_3.png",
    "car_blue_2.png",
]


class MapManager:
    """Desenha o mapa e expõe a posição das faixas para outras entidades."""

    def __init__(self):
        """Inicializa as faixas laterais de floresta, as faixas de rua e a zona de chegada."""
        self.left_strip = pygame.Rect(0, 0, SIDE_STRIP_WIDTH, HEIGHT)
        right_strip_x = SIDE_STRIP_WIDTH + NUM_LANES * LANE_WIDTH
        self.right_strip = pygame.Rect(
            right_strip_x, 0, WIDTH - right_strip_x, HEIGHT
        )
        self.lanes = [
            pygame.Rect(
                SIDE_STRIP_WIDTH + i * LANE_WIDTH, 0, LANE_WIDTH, HEIGHT
            )
            for i in range(NUM_LANES)
        ]
        self.goal_zone = pygame.Rect(WIDTH - 80, 0, 60, HEIGHT)
        self.car_images = self._load_car_images()

        # Texturas de fundo geradas UMA vez (otimização: nunca no draw).
        self.textura_grama_esquerda = criar_grama_textura(SIDE_STRIP_WIDTH, HEIGHT)
        self.textura_grama_direita = criar_grama_textura(
            WIDTH - (SIDE_STRIP_WIDTH + NUM_LANES * LANE_WIDTH), HEIGHT
        )
        self.textura_asfalto = criar_asfalto_textura(LANE_WIDTH, HEIGHT)

        # Decorações laterais — definidas por fase via set_phase_config.
        self.decoracoes = []

        # Configuração visual da fase atual (definida via set_phase_config).
        self.current_phase_config = None
        self.gradient_background = None
        self.snow_particles = []
        # Brilho de farol pré-renderizado, usado na fase NOITE FINAL.
        self._headlight_glow = self._criar_headlight_glow()

    def set_phase_config(self, config):
        """Atualiza cores e visuais conforme a fase atual.

        Recria as texturas de grama e asfalto e o gradiente de fundo com as
        cores temáticas da fase recebida.

        Args:
            config: Dicionário de configuração da fase (vindo do LevelManager).
        """
        self.current_phase_config = config
        largura_direita = WIDTH - (SIDE_STRIP_WIDTH + NUM_LANES * LANE_WIDTH)
        self.textura_grama_esquerda = criar_grama_textura_colorida(
            SIDE_STRIP_WIDTH, HEIGHT, config["grass_color"]
        )
        self.textura_grama_direita = criar_grama_textura_colorida(
            largura_direita, HEIGHT, config["grass_color"]
        )
        self.textura_asfalto = criar_asfalto_textura_colorida(
            LANE_WIDTH, HEIGHT, config["asphalt_color"]
        )
        self.gradient_background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_vertical(
            self.gradient_background,
            config["bg_color_top"],
            config["bg_color_bottom"],
        )
        self.snow_particles = []
        self.decoracoes = self._posicionar_decoracoes(config["decoration"])

    def update(self, dt):
        """Atualiza os efeitos visuais da fase (partículas de neve na fase NEVE).

        Args:
            dt: Delta time em segundos.
        """
        if self.current_phase_config and self.current_phase_config["name"] == "NEVE":
            if not self.snow_particles:
                self.snow_particles = [
                    {
                        "x": random.randint(0, WIDTH),
                        "y": random.randint(0, HEIGHT),
                        "speed": random.randint(60, 160),
                    }
                    for _ in range(50)
                ]
            for particula in self.snow_particles:
                particula["y"] += particula["speed"] * dt
                if particula["y"] > HEIGHT:
                    particula["y"] = random.randint(-20, 0)
                    particula["x"] = random.randint(0, WIDTH)
        else:
            self.snow_particles = []

    def _criar_headlight_glow(self):
        """Cria a Surface do brilho de farol (círculo amarelado semi-transparente).

        Returns:
            pygame.Surface com o brilho pré-renderizado.
        """
        raio = 32
        glow = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 240, 180, 80), (raio, raio), raio)
        return glow

    def _draw_snow(self, screen):
        """Desenha as partículas de neve caindo (fase NEVE).

        Args:
            screen: Surface destino.
        """
        for particula in self.snow_particles:
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(particula["x"]), int(particula["y"])),
                2,
            )

    def _draw_headlights(self, screen):
        """Desenha o brilho dos faróis à frente de cada carro (fase NOITE FINAL).

        Args:
            screen: Surface destino.
        """
        raio = self._headlight_glow.get_width() // 2
        for carro in self.obstacles:
            if carro.direction == -1:
                cone_y = carro.rect.top - 20
            else:
                cone_y = carro.rect.bottom + 20
            screen.blit(
                self._headlight_glow, (carro.rect.centerx - raio, cone_y - raio)
            )

    def _posicionar_decoracoes(self, tipo):
        """Posiciona as decorações laterais da fase em slots fixos, sem sobreposição.

        Cada decoração ocupa uma coluna e uma fatia vertical exclusivas, então
        duas nunca se sobrepõem — só há jitter aleatório dentro do slot. O sprite
        usado depende do tema da fase (árvore, poste, coqueiro, etc.).

        Args:
            tipo: Identificador do sprite decorativo do tema da fase.

        Returns:
            Lista de tuplas (Surface, x, y) prontas para desenhar.
        """
        fabrica = DECORACOES.get(tipo, criar_arvore)
        sprite = fabrica(DECOR_W, DECOR_H)
        decoracoes = []

        # Faixa esquerda: 8 decorações em 2 colunas x 4 linhas.
        colunas_esq = [0, SIDE_STRIP_WIDTH // 2]
        linhas_esq = 4
        slot_h_esq = HEIGHT // linhas_esq
        jitter_x_esq = max(0, SIDE_STRIP_WIDTH // 2 - DECOR_W)
        for indice in range(8):
            x_base = colunas_esq[indice % 2]
            linha = indice // 2
            x = x_base + random.randint(0, jitter_x_esq)
            y = linha * slot_h_esq + random.randint(0, max(0, slot_h_esq - DECOR_H))
            decoracoes.append((sprite, x, y))

        # Faixa direita: 6 decorações empilhadas em 1 coluna x 6 linhas.
        # Faixa estreita; ficam no início da faixa, sem cobrir a goal_zone.
        direita_x = SIDE_STRIP_WIDTH + NUM_LANES * LANE_WIDTH
        linhas_dir = 6
        slot_h_dir = HEIGHT // linhas_dir
        for linha in range(linhas_dir):
            y = linha * slot_h_dir + random.randint(0, max(0, slot_h_dir - DECOR_H))
            decoracoes.append((sprite, direita_x, y))

        return decoracoes

    def _load_car_images(self):
        cars_dir = IMG_DIR / "cars"
        target_size = (50, 92)
        images = []
        for name in CAR_FILES:
            img = pygame.image.load(str(cars_dir / name)).convert_alpha()
            images.append(pygame.transform.smoothscale(img, target_size))
        return images

    def spawn_obstacles(self, speed_min=150, speed_max=300, cars_per_lane=2):
        """Cria os carros distribuídos uniformemente em cada faixa com velocidade aleatória."""
        self.obstacles = pygame.sprite.Group()
        lanes = self.get_lanes()
        espacamento = HEIGHT // cars_per_lane

        for indice_faixa, lane in enumerate(lanes):
            # Alterna direção: faixa 0 desce, faixa 1 sobe, faixa 2 desce
            direcao = 1 if indice_faixa % 2 == 0 else -1

            for i in range(cars_per_lane):
                velocidade = random.randint(speed_min, speed_max)
                imagem = random.choice(self.car_images)
                largura_carro = imagem.get_width()
                x = lane - largura_carro // 2
                y = i * espacamento
                carro = Obstacle(x, y, velocidade, direcao, imagem)
                carro.lane_id = indice_faixa
                self.obstacles.add(carro)

    def spawn_powerups(self):
        """Cria 2 power-ups aleatórios nas faixas (1 cogumelo, 1 trevo)."""
        self.powerups = pygame.sprite.Group()
        lane_centers = self.get_lanes()
        for powerup_type in (PowerUp.TYPE_MUSHROOM, PowerUp.TYPE_CLOVER):
            lane_x = random.choice(lane_centers)
            x = lane_x - PowerUp.SIZE // 2
            y = random.randint(50, HEIGHT - 80)
            self.powerups.add(PowerUp(x, y, powerup_type))

    def draw_powerups(self, screen):
        """Desenha todos os power-ups na tela."""
        self.powerups.draw(screen)

    def draw(self, screen):
        """Desenha gradiente de fundo, texturas, árvores, tracejado, neve e zona de chegada."""
        # Gradiente de fundo da fase (atrás de tudo).
        if self.gradient_background is not None:
            screen.blit(self.gradient_background, (0, 0))
        # Texturas de grama nas faixas verdes laterais.
        screen.blit(self.textura_grama_esquerda, (0, 0))
        screen.blit(
            self.textura_grama_direita,
            (SIDE_STRIP_WIDTH + NUM_LANES * LANE_WIDTH, 0),
        )
        # Textura de asfalto em cada faixa de rua (self.lanes guarda Rects).
        for lane in self.lanes:
            screen.blit(self.textura_asfalto, (lane.x, 0))
        # Decorações laterais, desenhadas sobre a grama e antes do tracejado.
        for sprite, x, y in self.decoracoes:
            screen.blit(sprite, (x, y))
        for i in range(1, NUM_LANES):
            x = SIDE_STRIP_WIDTH + i * LANE_WIDTH
            self._draw_dashed_line(screen, x)
        # Neve cai por cima do cenário, antes da zona de chegada.
        self._draw_snow(screen)
        pygame.draw.rect(screen, (255, 215, 0), self.goal_zone)

    def _draw_dashed_line(self, screen, x):
        y = 0
        while y < HEIGHT:
            y_end = min(y + DASH_LENGTH, HEIGHT)
            pygame.draw.line(screen, WHITE, (x, y), (x, y_end), DASH_THICKNESS)
            y += DASH_LENGTH + DASH_GAP

    def get_lanes(self):
        """Retorna a posição x do centro de cada faixa de rua."""
        return [lane.centerx for lane in self.lanes]

    def prevent_overlap(self):
        """Detecta carros próximos demais na mesma faixa e desacelera o que está atrás."""
        DISTANCIA_MINIMA = 150

        for indice_faixa in range(len(self.lanes)):
            carros_na_faixa = [c for c in self.obstacles if c.lane_id == indice_faixa]
            if len(carros_na_faixa) < 2:
                continue

            direcao = carros_na_faixa[0].direction
            # Ordena com o carro mais à frente primeiro
            if direcao == 1:  # descendo: maior y está na frente
                carros_na_faixa.sort(key=lambda c: c.rect.centery, reverse=True)
            else:             # subindo: menor y está na frente
                carros_na_faixa.sort(key=lambda c: c.rect.centery)

            for i in range(len(carros_na_faixa) - 1):
                carro_frente = carros_na_faixa[i]
                carro_atras = carros_na_faixa[i + 1]
                distancia = abs(carro_frente.rect.centery - carro_atras.rect.centery)

                if distancia < DISTANCIA_MINIMA + 20:
                    carro_atras.set_effective_speed(carro_frente.effective_speed)
                elif distancia > DISTANCIA_MINIMA * 2:
                    carro_atras.set_effective_speed(carro_atras.original_speed)

    def update_obstacles(self, dt):
        """Atualiza a posição de todos os carros e previne sobreposição na mesma faixa."""
        self.obstacles.update(dt)
        self.prevent_overlap()

    def draw_obstacles(self, screen):
        """Desenha os carros e, na fase RUA DE NOITE, os faróis iluminando à frente."""
        self.obstacles.draw(screen)
        if (
            self.current_phase_config
            and self.current_phase_config["name"] == "RUA DE NOITE"
        ):
            self._draw_headlights(screen)

    def get_goal_zone(self):
        """Retorna o pygame.Rect que representa a zona de chegada (toca da raposa)."""
        return self.goal_zone
