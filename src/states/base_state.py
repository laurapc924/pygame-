"""Classe base para todos os estados do jogo.

Define a interface que todo estado deve implementar.
"""


class BaseState:
    """Classe base para os estados do jogo.

    Todos os estados (Menu, Playing, GameOver, etc.) devem herdar desta classe.
    Define os métodos que o Game espera chamar.
    """

    def __init__(self, game):
        """Inicializa o estado com uma referência ao jogo.

        Args:
            game: Instância da classe Game.
        """
        self.game = game

    def handle_events(self):
        """Processa eventos do PyGame (entrada do usuário, etc).

        Deve ser implementado pelas subclasses.
        """
        pass

    def update(self, dt):
        """Atualiza a lógica do estado.

        Args:
            dt: Delta time (tempo decorrido desde o último frame em segundos).

        Deve ser implementado pelas subclasses.
        """
        pass

    def draw(self, screen):
        """Desenha o estado na tela.

        Args:
            screen: Superfície do PyGame onde desenhar.

        Deve ser implementado pelas subclasses.
        """
        pass
