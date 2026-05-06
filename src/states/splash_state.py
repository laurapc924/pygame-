"""Estado temporário para testes da infraestrutura.

Este estado será substituído pelo Menu no futuro.
"""

import pygame

from src.settings import GREEN_FOREST
from src.states.base_state import BaseState


class SplashState(BaseState):
    """Estado temporário que apenas pinta a tela de verde.

    Usado para testar a infraestrutura da máquina de estados.
    Será substituído pelo estado de Menu.
    """

    def handle_events(self):
        """Processa eventos, encerrando o jogo ao clicar em X."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()

    def update(self, dt):
        """Não há atualização de lógica neste estado temporário."""
        pass

    def draw(self, screen):
        """Pinta a tela com a cor de fundo verde."""
        screen.fill(GREEN_FOREST)
