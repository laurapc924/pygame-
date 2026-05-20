import pygame
from src.settings import HEIGHT


# Margem (em pixels) que tiramos do rect do carro para formar a hitbox.
# Sprites do Kenney têm um pouco de transparência nas bordas + sombra.
HITBOX_MARGIN_X = 6
HITBOX_MARGIN_Y = 8


class Obstacle(pygame.sprite.Sprite):
    """Carro que se move verticalmente em uma faixa, usando sprite top-down."""

    speed_multiplier = 1.0

    def __init__(self, x, y, speed, direction, image):
        super().__init__()

        # Os sprites do Kenney apontam para cima por padrão.
        # Se o carro desce (direction=1), rotaciona 180°.
        if direction == 1:
            self.image = pygame.transform.rotate(image, 180)
        else:
            self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.hitbox = self.rect.inflate(-2 * HITBOX_MARGIN_X, -2 * HITBOX_MARGIN_Y)

        self.speed = speed
        self.original_speed = speed
        self.effective_speed = speed
        self.direction = direction
        self.lane_id = None

    def set_effective_speed(self, new_speed):
        """Ajusta velocidade efetiva (usado pra evitar atropelamento entre carros da mesma faixa)."""
        self.effective_speed = max(50, min(new_speed, self.original_speed))

    def update(self, dt):
        self.rect.y += self.effective_speed * self.direction * dt * Obstacle.speed_multiplier

        # Loop infinito: se sair de um lado, reaparece no outro e restaura velocidade original
        if self.direction == 1 and self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.effective_speed = self.original_speed
        elif self.direction == -1 and self.rect.bottom < 0:
            self.rect.top = HEIGHT
            self.effective_speed = self.original_speed

        self.hitbox.center = self.rect.center
