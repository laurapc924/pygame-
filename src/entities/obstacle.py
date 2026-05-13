import pygame
from src.settings import HEIGHT


class Obstacle(pygame.sprite.Sprite):
    #Representa um carro/obstáculo que se move horizontalmente em uma faixa

    def __init__(self, x, y, width, height, speed, color, direction):
        
        
        super().__init__()

        # Cria a imagem do carro (placeholder: retângulo colorido)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        # Cria o "retângulo de posição" (PyGame usa isso pra desenhar e colidir)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Guarda os atributos pra usar depois
        self.speed = speed
        self.direction = direction

    def update(self, dt):
      
        # Movimento: posição += velocidade * direção * tempo
        self.rect.y += self.speed * self.direction * dt

        # Loop infinito: se sair de um lado, aparece no outro
        if self.direction == 1 and self.rect.top > HEIGHT:
            # Estava indo pra baixo e saiu pela parte de baixo → reaparece na parte de cima
            self.rect.bottom = 0
        elif self.direction == -1 and self.rect.bottom < 0:
            # Estava indo pra cima e saiu pela parte de cima → reaparece na parte de baixo
            self.rect.top = HEIGHT
            