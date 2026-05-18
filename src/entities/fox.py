"""Personagem principal do jogo: a raposa."""

import pygame

from src.settings import HEIGHT, IMG_DIR, WIDTH


SPEED = 300  # pixels por segundo

# Layout da sprite sheet fox.png (3 colunas x 4 linhas, frames 48x64).
# Linhas: 0=N, 1=E, 2=S, 3=W. 3 frames por direção (ciclo de caminhada).
FOX_FRAME_W = 48
FOX_FRAME_H = 64
FOX_FRAMES_PER_DIR = 3
FOX_DIR_ROWS = {"up": 0, "right": 1, "down": 2, "left": 3}
FOX_SCALE = 2  # multiplicador de tamanho da raposa em tela
ANIMATION_SPEED = 0.15  # segundos por frame
# Hitbox apertada em torno do corpo (ignora cauda/transparência).
FOX_HITBOX_W = 56
FOX_HITBOX_H = 72


class Fox:
    """Raposa controlada pelo jogador."""

    def __init__(self, x, y):
        """Inicializa a raposa na posição (x, y)."""
        self.width = FOX_FRAME_W * FOX_SCALE
        self.height = FOX_FRAME_H * FOX_SCALE
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        self.hitbox = pygame.Rect(0, 0, FOX_HITBOX_W, FOX_HITBOX_H)
        self.hitbox.center = self.rect.center
        self.start_x = self.rect.x
        self.start_y = self.rect.y
        self.lives = 3
        self.invincible_timer = 0.0
        self.facing = "right"
        self.frame_index = 0
        self.animation_timer = 0.0
        self._frames = self._load_frames()
        self.image = self._frames[self.facing][self.frame_index]

    def _load_frames(self):
        sheet = pygame.image.load(str(IMG_DIR / "fox.png")).convert_alpha()
        frames = {}
        for direction, row in FOX_DIR_ROWS.items():
            direction_frames = []
            for col in range(FOX_FRAMES_PER_DIR):
                rect = pygame.Rect(
                    col * FOX_FRAME_W, row * FOX_FRAME_H, FOX_FRAME_W, FOX_FRAME_H
                )
                frame = sheet.subsurface(rect).copy()
                scaled = pygame.transform.scale(
                    frame, (FOX_FRAME_W * FOX_SCALE, FOX_FRAME_H * FOX_SCALE)
                )
                direction_frames.append(scaled)
            frames[direction] = direction_frames
        return frames

    def handle_events(self, events):
        """Recebe a lista de eventos do frame atual (sem consumir do pygame).

        Args:
            events: Lista retornada por pygame.event.get() no GameState.
        """
        pass

    def update(self, dt):
        """Move a raposa com base nas teclas pressionadas e limita à tela.

        Args:
            dt: Delta time em segundos.
        """
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_RIGHT]:
            self.x += SPEED * dt
            self.facing = "right"
            moving = True
        if keys[pygame.K_LEFT]:
            self.x -= SPEED * dt
            self.facing = "left"
            moving = True
        if keys[pygame.K_DOWN]:
            self.y += SPEED * dt
            self.facing = "down"
            moving = True
        if keys[pygame.K_UP]:
            self.y -= SPEED * dt
            self.facing = "up"
            moving = True

        self.x = max(0.0, min(self.x, WIDTH - self.width))
        self.y = max(0.0, min(self.y, HEIGHT - self.height))
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.hitbox.center = self.rect.center

        if moving:
            self.animation_timer += dt
            if self.animation_timer >= ANIMATION_SPEED:
                self.animation_timer -= ANIMATION_SPEED
                self.frame_index = (self.frame_index + 1) % FOX_FRAMES_PER_DIR
        else:
            self.frame_index = 0
            self.animation_timer = 0.0

        self.image = self._frames[self.facing][self.frame_index]
        if self.invincible_timer > 0:
            self.invincible_timer -= dt

    def reset_position(self):
        """Volta a raposa para a posição inicial após colisão."""
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.x = float(self.start_x)
        self.y = float(self.start_y)
        self.hitbox.center = self.rect.center

    def draw(self, screen):
        """Desenha a raposa, piscando quando invencível."""
        if self.invincible_timer > 0 and int(self.invincible_timer * 10) % 2 == 0:
            return
        screen.blit(self.image, self.rect)
