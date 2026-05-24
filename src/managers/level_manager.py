"""Gerencia as configurações de cada fase: dificuldade, tema e cores."""


class LevelManager:
    """Guarda as configs de cada fase (dificuldade, tema, cores) e a fase ativa."""

    TOTAL_LEVELS = 6

    def __init__(self):
        """Inicializa na fase 1 com as configs temáticas de todas as 6 fases."""
        self.current_level = 1
        self.configs = {
            1: {
                "name": "RUA DE DIA",
                "subtitle": "O começo de tudo",
                "decoration": "arvore",
                "car_speed_min": 130,
                "car_speed_max": 250,
                "cars_per_lane": 2,
                "points": 100,
                "bg_color_top": (120, 175, 230),
                "bg_color_bottom": (175, 210, 240),
                "asphalt_color": (82, 82, 88),
                "grass_color": (50, 120, 58),
            },
            2: {
                "name": "RUA DE NOITE",
                "subtitle": "Sob a luz dos postes",
                "decoration": "poste",
                "car_speed_min": 170,
                "car_speed_max": 310,
                "cars_per_lane": 3,
                "points": 200,
                "bg_color_top": (12, 16, 38),
                "bg_color_bottom": (28, 34, 62),
                "asphalt_color": (46, 46, 54),
                "grass_color": (24, 44, 30),
            },
            3: {
                "name": "PRAIA",
                "subtitle": "Areia, sol e perigo",
                "decoration": "coqueiro",
                "car_speed_min": 200,
                "car_speed_max": 360,
                "cars_per_lane": 3,
                "points": 350,
                "bg_color_top": (115, 200, 235),
                "bg_color_bottom": (240, 222, 165),
                "asphalt_color": (190, 170, 120),
                "grass_color": (240, 222, 165),
            },
            4: {
                "name": "NEVE",
                "subtitle": "Pista escorregadia",
                "decoration": "pinheiro",
                "car_speed_min": 200,
                "car_speed_max": 350,
                "cars_per_lane": 3,
                "points": 500,
                "bg_color_top": (200, 220, 240),
                "bg_color_bottom": (232, 240, 250),
                "asphalt_color": (138, 144, 152),
                "grass_color": (226, 233, 242),
            },
            5: {
                "name": "MONTANHA",
                "subtitle": "Topo do mundo",
                "decoration": "pedra",
                "car_speed_min": 220,
                "car_speed_max": 370,
                "cars_per_lane": 3,
                "points": 700,
                "bg_color_top": (118, 128, 148),
                "bg_color_bottom": (92, 102, 118),
                "asphalt_color": (96, 92, 86),
                "grass_color": (98, 112, 76),
            },
            6: {
                "name": "FAZENDA",
                "subtitle": "A reta final",
                "decoration": "cerca",
                "car_speed_min": 230,
                "car_speed_max": 390,
                "cars_per_lane": 4,
                "points": 1000,
                "bg_color_top": (140, 190, 228),
                "bg_color_bottom": (192, 216, 236),
                "asphalt_color": (120, 95, 62),
                "grass_color": (108, 150, 58),
            },
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
