"""Ponto de entrada do jogo Fox Crossing."""

from src.game import Game
from src.states.splash_state import SplashState

if __name__ == "__main__":
    game = Game()
    game.change_state(SplashState(game))
    game.run()
    game.quit()
