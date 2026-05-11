"""Ponto de entrada do jogo Fox Crossing."""

from src.game import Game
from src.states.menu import MenuState

if __name__ == "__main__":
    game = Game()
    game.change_state(MenuState(game))
    game.run()
    game.quit()
