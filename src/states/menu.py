import pygame
from src.settings import GREEN_FOREST, WHITE, HEIGHT
from src.states.base_state import BaseState
from src.states.game_state import GameState
from src.states.instructions_state import InstructionsState


class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.SysFont(None, 80)
        self.font_medium = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 30)
        self.font_pause_info = pygame.font.SysFont(None, 24)
        self.game.sound_manager.play_music("assets/sounds/menu.wav")
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
			
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_state(GameState(self.game))
                if event.key == pygame.K_i:
                    self.game.change_state(InstructionsState(self.game))
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

        pausa = self.font_pause_info.render("P pausa durante o jogo", True, (180, 180, 180))
        screen.blit(pausa, (screen.get_width() // 2 - pausa.get_width() // 2, HEIGHT // 2 + 38))

        instrucoes = self.font_small.render("I - Instruções", True, (180, 180, 180))
        screen.blit(instrucoes, (screen.get_width() // 2 - instrucoes.get_width() // 2, HEIGHT // 2 + 72))
    
        pequeno = self.font_small.render("Pressione ESC para sair", True, WHITE)
        screen.blit(pequeno, (screen.get_width() // 2 - pequeno.get_width() // 2, HEIGHT // 2 + 110))
