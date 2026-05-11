"""Ponto de entrada do jogo Fox Crossing."""

from src.game import Game
from src.states.game_state import GameState

if __name__ == "__main__":
    game = Game()
    game.change_state(GameState(game))
    game.run()
    game.quit()
