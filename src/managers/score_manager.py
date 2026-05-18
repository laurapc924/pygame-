"""Gerencia a pontuação atual da sessão e o recorde persistente em arquivo."""


class ScoreManager:
    """Mantém o score da partida e salva/carrega o recorde em data/highscore.txt."""

    HIGHSCORE_PATH = "data/highscore.txt"

    def __init__(self):
        """Inicializa o score zerado e carrega o recorde do arquivo."""
        self.current_score = 0
        self.highscore = self._load_highscore()

    def _load_highscore(self):
        """Carrega o recorde do arquivo, retorna 0 se arquivo não existir."""
        try:
            with open(self.HIGHSCORE_PATH, "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        """Salva o recorde atual no arquivo."""
        with open(self.HIGHSCORE_PATH, "w") as f:
            f.write(str(self.highscore))

    def add_points(self, points):
        """Adiciona pontos ao score atual."""
        self.current_score += points

    def check_and_update_highscore(self):
        """Verifica se o score atual virou novo recorde. Retorna True se sim."""
        if self.current_score > self.highscore:
            self.highscore = self.current_score
            self.save_highscore()
            return True
        return False

    def reset_current_score(self):
        """Zera o score atual (sem mexer no recorde)."""
        self.current_score = 0
