"""Gerenciador do mapa: floresta nas laterais e 3 faixas de rua verticais."""

import pygame
import random

from src.entities.obstacle import Obstacle 
from src.settings import HEIGHT


from src.settings import GRAY_ROAD, GREEN_FOREST, HEIGHT, WHITE, WIDTH


SIDE_STRIP_WIDTH = 120
NUM_LANES = 3
ROAD_AREA_WIDTH = WIDTH - 2 * SIDE_STRIP_WIDTH
LANE_WIDTH = ROAD_AREA_WIDTH // NUM_LANES

DASH_LENGTH = 20
DASH_GAP = 15
DASH_THICKNESS = 3


class MapManager:
    """Desenha o mapa e expõe a posição das faixas para outras entidades."""

    def __init__(self):
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
    def spawn_obstacles(self):
    

        # "Saco" que guarda todos os carros
        self.obstacles = pygame.sprite.Group()

        # Lista de centros X das faixas (já existe no seu código)
        lanes = self.get_lanes()

        # Tamanho dos carros: como faixas são verticais e carros descem/sobem,
        # eles ficam "deitados ao contrário": mais altos que largos
        largura_carro = 40
        altura_carro = 60

        # Cores variadas pra cada carro
        cores = [
            (220, 60, 60),    # vermelho
            (60, 100, 220),   # azul
            (230, 200, 50),   # amarelo
            (180, 60, 200),   # roxo
            (60, 180, 100),   # verde
            (240, 130, 30),   # laranja
        ]

        # Pra cada faixa, criar 2 carros
        for indice_faixa, lane in enumerate(lanes):
            # Alterna direção: faixa 0 desce, faixa 1 sobe, faixa 2 desce
            if indice_faixa % 2 == 0:
                direcao = 1   # desce
            else:
                direcao = -1  # sobe

            for i in range(2):
                # Velocidade aleatória
                velocidade = random.randint(150, 300)

                # X: centralizar o carro na faixa (faixa é vertical, centro_x é o meio dela)
                x = lane - largura_carro // 2

                # Y: posição vertical aleatória ao longo da tela
                y = random.randint(0, HEIGHT)

                # Cor aleatória
                cor = random.choice(cores)

                # Criar o carro e jogar no saco
                carro = Obstacle(x, y, largura_carro, altura_carro, velocidade, cor, direcao)
                self.obstacles.add(carro)

    def draw(self, screen):
        screen.fill(GREEN_FOREST)
        pygame.draw.rect(screen, GREEN_FOREST, self.left_strip)
        pygame.draw.rect(screen, GREEN_FOREST, self.right_strip)
        for lane in self.lanes:
            pygame.draw.rect(screen, GRAY_ROAD, lane)
        for i in range(1, NUM_LANES):
            x = SIDE_STRIP_WIDTH + i * LANE_WIDTH
            self._draw_dashed_line(screen, x)

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
