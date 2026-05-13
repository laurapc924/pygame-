import pygame
from src.settings import WIDTH


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
        self.rect.x += self.speed * self.direction * dt

        # Loop infinito: se sair de um lado, aparece no outro
        if self.direction == 1 and self.rect.left > WIDTH:
            # Estava indo pra direita e saiu pela direita → reaparece à esquerda
            self.rect.right = 0
        elif self.direction == -1 and self.rect.right < 0:
            # Estava indo pra esquerda e saiu pela esquerda → reaparece à direita
            self.rect.left = WIDTH