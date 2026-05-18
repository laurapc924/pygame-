"""Gerencia as configurações de cada fase: velocidade dos carros e quantidade por faixa."""


class LevelManager:
    """Guarda as configs de dificuldade de cada fase e controla qual fase está ativa."""

    TOTAL_LEVELS = 3

    def __init__(self):
        """Inicializa na fase 1 com as configs de todas as fases."""
        self.current_level = 1
        self.configs = {
            1: {"car_speed_min": 150, "car_speed_max": 300, "cars_per_lane": 2, "points": 100},
            2: {"car_speed_min": 200, "car_speed_max": 400, "cars_per_lane": 3, "points": 200},
            3: {"car_speed_min": 250, "car_speed_max": 500, "cars_per_lane": 4, "points": 300},
        }

    def get_config(self):
        """Retorna o dicionário de configuração da fase atual."""
        return self.configs[self.current_level]

    def next_level(self):
        """Avança para próxima fase. Retorna True se ainda há fase, False se acabou o jogo."""
        if self.current_level < self.TOTAL_LEVELS:
            self.current_level += 1
            return True
        return False

    def is_final_level(self):
        """Retorna True se está na última fase."""
        return self.current_level == self.TOTAL_LEVELS

    def reset(self):
        """Volta para fase 1."""
        self.current_level = 1
