"""Gerenciador do mapa: floresta nas laterais e 3 faixas de rua verticais."""

import pygame

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
