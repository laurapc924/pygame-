"""Classe principal do jogo Fox Crossing.

Gerencia a janela, o loop de jogo e a máquina de estados.
"""

import pygame

from src.settings import FPS, HEIGHT, TITLE, WIDTH
from src.states.menu import MenuState



class Game:
    """Classe principal que controla o loop do jogo e a máquina de estados."""

    def __init__(self):
        """Inicializa o jogo, a janela e o clock."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        from src.managers.sound_manager import SoundManager
        self.sound_manager = SoundManager()

        self.current_state = MenuState(self)
        

    def change_state(self, new_state):
        """Muda para um novo estado do jogo.

        Args:
            new_state: Instância do novo estado que deve ser ativado.
        """
        self.current_state = new_state

    def run(self):
        """Executa o loop principal do jogo.

        Calcula delta time, processa eventos, atualiza e desenha o estado atual.
        """
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time em segundos

            if self.current_state:
                self.current_state.handle_events()
                self.current_state.update(dt)
                self.current_state.draw(self.screen)

            pygame.display.flip()

    def quit(self):
        """Encerra o jogo e fecha o PyGame."""
        self.running = False
        pygame.quit()
