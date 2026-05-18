"""Gerenciador do mapa: floresta nas laterais e 3 faixas de rua verticais."""

import pygame
import random

from src.entities.obstacle import Obstacle
from src.settings import GRAY_ROAD, GREEN_FOREST, HEIGHT, IMG_DIR, WHITE, WIDTH


SIDE_STRIP_WIDTH = 120
NUM_LANES = 3
ROAD_AREA_WIDTH = WIDTH - 2 * SIDE_STRIP_WIDTH
LANE_WIDTH = ROAD_AREA_WIDTH // NUM_LANES

DASH_LENGTH = 20
DASH_GAP = 15
DASH_THICKNESS = 3

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

    def _load_car_images(self):
        cars_dir = IMG_DIR / "cars"
        target_size = (50, 92)
        images = []
        for name in CAR_FILES:
            img = pygame.image.load(str(cars_dir / name)).convert_alpha()
            images.append(pygame.transform.smoothscale(img, target_size))
        return images

    def spawn_obstacles(self):
        self.obstacles = pygame.sprite.Group()
        lanes = self.get_lanes()

        for indice_faixa, lane in enumerate(lanes):
            # Alterna direção: faixa 0 desce, faixa 1 sobe, faixa 2 desce
            direcao = 1 if indice_faixa % 2 == 0 else -1

            for _ in range(2):
                velocidade = random.randint(150, 300)
                imagem = random.choice(self.car_images)
                largura_carro = imagem.get_width()
                x = lane - largura_carro // 2
                y = random.randint(0, HEIGHT)
                carro = Obstacle(x, y, velocidade, direcao, imagem)
                self.obstacles.add(carro)

    def draw(self, screen):
        """Desenha as faixas laterais, as faixas de rua, as linhas tracejadas e a zona de chegada."""
        screen.fill(GREEN_FOREST)
        pygame.draw.rect(screen, GREEN_FOREST, self.left_strip)
        pygame.draw.rect(screen, GREEN_FOREST, self.right_strip)
        for lane in self.lanes:
            pygame.draw.rect(screen, GRAY_ROAD, lane)
        for i in range(1, NUM_LANES):
            x = SIDE_STRIP_WIDTH + i * LANE_WIDTH
            self._draw_dashed_line(screen, x)
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

    def update_obstacles(self, dt):
        """Atualiza a posição de todos os carros."""
        self.obstacles.update(dt)

    def draw_obstacles(self, screen):
        """Desenha todos os carros na tela."""
        self.obstacles.draw(screen)

    def get_goal_zone(self):
        """Retorna o pygame.Rect que representa a zona de chegada (toca da raposa)."""
        return self.goal_zone
