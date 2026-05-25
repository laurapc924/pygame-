"""Gerenciador do mapa: laterais temáticas e faixas de rua verticais."""

import pygame
import random

from src.entities.obstacle import Obstacle
from src.entities.powerup import PowerUp
from src.settings import HEIGHT, IMG_DIR, WHITE, WIDTH
from src.utils.lateral_bars import criar_lateral
from src.utils.sprite_factory import (
    criar_ameia,
    criar_arvore,
    criar_arvore_floresta,
    criar_asfalto_textura,
    criar_asfalto_textura_colorida,
    criar_cacto,
    criar_cerca,
    criar_coqueiro,
    criar_grama_textura,
    criar_grama_textura_colorida,
    criar_junco,
    criar_pedra,
    criar_pinheiro,
    criar_poste,
    desenhar_gradiente_vertical,
)


SIDE_STRIP_WIDTH = 120
DEFAULT_NUM_LANES = 4
ROAD_AREA_WIDTH = WIDTH - 2 * SIDE_STRIP_WIDTH

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
    "cacto": criar_cacto,
    "ameia": criar_ameia,
    "junco": criar_junco,
    "arvore_floresta": criar_arvore_floresta,
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
        self.num_lanes = DEFAULT_NUM_LANES
        self.lane_width = ROAD_AREA_WIDTH // self.num_lanes
        self.left_strip = pygame.Rect(0, 0, SIDE_STRIP_WIDTH, HEIGHT)
        self._rebuild_lanes(self.num_lanes)
        self.goal_zone = pygame.Rect(WIDTH - 80, 0, 60, HEIGHT)
        self.car_images = self._load_car_images()

        # Textura padrão do asfalto (cor sobrescrita por set_phase_config).
        self.textura_asfalto = criar_asfalto_textura(self.lane_width, HEIGHT)

        # Barras laterais inteiras (cenário por país) — setadas por set_phase_config.
        self.lateral_esquerda = None
        self.lateral_direita = None

        # Configuração visual da fase atual (definida via set_phase_config).
        self.current_phase_config = None
        self.gradient_background = None
        self.snow_particles = []
        self.rain_particles = []
        # Brilho de farol pré-renderizado, usado na fase LONDRES (noite).
        self._headlight_glow = self._criar_headlight_glow()

    def _rebuild_lanes(self, lane_count):
        """Recalcula faixas e lateral direita quando a fase muda a quantidade de faixas."""
        self.num_lanes = lane_count
        self.lane_width = ROAD_AREA_WIDTH // self.num_lanes
        right_strip_x = SIDE_STRIP_WIDTH + self.num_lanes * self.lane_width
        self.right_strip = pygame.Rect(
            right_strip_x, 0, WIDTH - right_strip_x, HEIGHT
        )
        self.lanes = [
            pygame.Rect(
                SIDE_STRIP_WIDTH + i * self.lane_width, 0, self.lane_width, HEIGHT
            )
            for i in range(self.num_lanes)
        ]

    def set_phase_config(self, config):
        """Atualiza cores e visuais conforme a fase atual.

        Recria as texturas de grama e asfalto e o gradiente de fundo com as
        cores temáticas da fase recebida.

        Args:
            config: Dicionário de configuração da fase (vindo do LevelManager).
        """
        self.current_phase_config = config
        self._rebuild_lanes(config.get("lane_count", DEFAULT_NUM_LANES))
        # Asfalto sujo só nas fases com clima ruim (chuva/neve).
        asfalto_sujo = config["decoration"] in ("belgica", "suica", "canada")
        self.textura_asfalto = criar_asfalto_textura_colorida(
            self.lane_width, HEIGHT, config["asphalt_color"], sujo=asfalto_sujo
        )
        self.gradient_background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_vertical(
            self.gradient_background,
            config["bg_color_top"],
            config["bg_color_bottom"],
        )
        self.snow_particles = []
        self.rain_particles = []
        # Barras laterais temáticas inteiras (substituem grama + decoração).
        self.lateral_esquerda = criar_lateral(
            config["decoration"], "esq", SIDE_STRIP_WIDTH, HEIGHT
        )
        self.lateral_direita = criar_lateral(
            config["decoration"], "dir", self.right_strip.width, HEIGHT
        )

    def update(self, dt):
        """Atualiza efeitos visuais: neve em Suíça/Canadá, chuva na Bélgica.

        Args:
            dt: Delta time em segundos.
        """
        tema = self.current_phase_config["decoration"] if self.current_phase_config else None
        if tema in ("suica", "canada"):
            if not self.snow_particles:
                self.snow_particles = [
                    {
                        "x": random.randint(0, WIDTH),
                        "y": random.randint(0, HEIGHT),
                        "speed": random.randint(60, 160),
                    }
                    for _ in range(50)
                ]
            for p in self.snow_particles:
                p["y"] += p["speed"] * dt
                if p["y"] > HEIGHT:
                    p["y"] = random.randint(-20, 0)
                    p["x"] = random.randint(0, WIDTH)
        else:
            self.snow_particles = []

        if tema == "belgica":
            if not self.rain_particles:
                self.rain_particles = [
                    {
                        "x": random.randint(0, WIDTH),
                        "y": random.randint(0, HEIGHT),
                        "speed": random.randint(420, 600),
                    }
                    for _ in range(80)
                ]
            for p in self.rain_particles:
                p["y"] += p["speed"] * dt
                p["x"] -= 60 * dt
                if p["y"] > HEIGHT or p["x"] < -10:
                    p["y"] = random.randint(-40, -5)
                    p["x"] = random.randint(0, WIDTH + 40)
        else:
            self.rain_particles = []

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
        """Desenha as partículas de neve caindo (fases Suíça/Canadá).

        Args:
            screen: Surface destino.
        """
        for p in self.snow_particles:
            pygame.draw.circle(
                screen, (255, 255, 255), (int(p["x"]), int(p["y"])), 2
            )

    def _draw_rain(self, screen):
        """Desenha gotas de chuva diagonais (fase Bélgica).

        Args:
            screen: Surface destino.
        """
        for p in self.rain_particles:
            x, y = int(p["x"]), int(p["y"])
            pygame.draw.line(screen, (170, 196, 220), (x, y), (x - 3, y + 12), 1)

    def _draw_headlights(self, screen):
        """Desenha o brilho dos faróis à frente de cada carro (fase RUA DE NOITE).

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
            # Desloca cada faixa no eixo Y para evitar paredes de carros alinhados.
            offset_faixa = (indice_faixa * espacamento // len(lanes)) % espacamento

            for i in range(cars_per_lane):
                velocidade = random.randint(speed_min, speed_max)
                imagem = random.choice(self.car_images)
                largura_carro = imagem.get_width()
                x = lane - largura_carro // 2
                y = (i * espacamento + offset_faixa + espacamento // 4) % HEIGHT
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
        """Desenha gradiente, barras laterais temáticas, asfalto, tracejado e efeitos."""
        if self.gradient_background is not None:
            screen.blit(self.gradient_background, (0, 0))
        # Barras laterais inteiras (cenário por país).
        if self.lateral_esquerda is not None:
            screen.blit(self.lateral_esquerda, (0, 0))
        if self.lateral_direita is not None:
            screen.blit(self.lateral_direita, (self.right_strip.x, 0))
        # Textura de asfalto em cada faixa de rua.
        for lane in self.lanes:
            screen.blit(self.textura_asfalto, (lane.x, 0))
        for i in range(1, self.num_lanes):
            x = SIDE_STRIP_WIDTH + i * self.lane_width
            self._draw_dashed_line(screen, x)
        # Efeitos climáticos por cima do cenário, antes da zona dourada.
        self._draw_snow(screen)
        self._draw_rain(screen)
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
        """Desenha os carros e, na fase LONDRES (noite), os faróis iluminando à frente."""
        self.obstacles.draw(screen)
        if (
            self.current_phase_config
            and self.current_phase_config["decoration"] == "londres"
        ):
            self._draw_headlights(screen)

    def get_goal_zone(self):
        """Retorna o pygame.Rect que representa a zona de chegada (toca da raposa)."""
        return self.goal_zone
