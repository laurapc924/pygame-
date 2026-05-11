import pygame
from src.settings import GREEN_FOREST, WHITE, HEIGHT
from src.states.base_state import BaseState
from src.states.game_state import GameState


class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.SysFont(None, 80)
        self.font_medium = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 30)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
			
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_state(GameState(self.game))
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(GREEN_FOREST)
    
        titulo = self.font_title.render("FOX CROSSING", True, WHITE)
        screen.blit(titulo, (screen.get_width() // 2 - titulo.get_width() // 2, HEIGHT // 3))
    
        medio = self.font_medium.render("Pressione ENTER para jogar", True, WHITE)
        screen.blit(medio, (screen.get_width() // 2 - medio.get_width() // 2, HEIGHT // 2))
    
        pequeno = self.font_small.render("Pressione ESC para sair", True, WHITE)
        screen.blit(pequeno, (screen.get_width() // 2 - pequeno.get_width() // 2, HEIGHT // 2 + 60))
