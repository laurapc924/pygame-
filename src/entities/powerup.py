"""Item coletável com efeito especial: cogumelo (+1 vida) ou trevo (invencibilidade)."""

import pygame

from src.utils.sprite_factory import criar_cogumelo, criar_trevo


class PowerUp(pygame.sprite.Sprite):
    """Sprite estático que a raposa coleta para ganhar um efeito especial."""

    TYPE_MUSHROOM = "mushroom"
    TYPE_CLOVER = "clover"

    SIZE = 30

    def __init__(self, x, y, powerup_type):
        """Cria o power-up na posição (x, y) com visual em pixel art baseado no tipo."""
        super().__init__()
        self.type = powerup_type

        if self.type == self.TYPE_MUSHROOM:
            self.image = criar_cogumelo(size=self.SIZE)
        elif self.type == self.TYPE_CLOVER:
            self.image = criar_trevo(size=self.SIZE)
        else:
            self.image = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt):
        """Power-ups são estáticos: nenhuma atualização necessária."""
        pass
