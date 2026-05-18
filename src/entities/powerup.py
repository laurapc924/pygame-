"""Item coletável com efeito especial: cogumelo (+1 vida) ou trevo (invencibilidade)."""

import pygame


class PowerUp(pygame.sprite.Sprite):
    """Sprite estático que a raposa coleta para ganhar um efeito especial."""

    TYPE_MUSHROOM = "mushroom"
    TYPE_CLOVER = "clover"

    SIZE = 30

    def __init__(self, x, y, powerup_type):
        """Cria o power-up na posição (x, y) com visual baseado no tipo."""
        super().__init__()
        self.type = powerup_type
        self.image = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)

        if self.type == self.TYPE_MUSHROOM:
            self.image.fill((220, 50, 50))
            center = self.SIZE // 2
            pygame.draw.circle(self.image, (255, 255, 255), (center, center), 7)
        elif self.type == self.TYPE_CLOVER:
            self.image.fill((100, 200, 100))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt):
        """Power-ups são estáticos: nenhuma atualização necessária."""
        pass
