"""Gerencia as configurações de cada fase: dificuldade, tema e cores."""


class LevelManager:
    """Guarda as configs de cada fase (dificuldade, tema, cores) e a fase ativa."""

    TOTAL_LEVELS = 10

    def __init__(self):
        """Inicializa na fase 1 com as configs temáticas de todas as 10 fases."""
        self.current_level = 1
        self.configs = {
            1: {
                "name": "AMAZÔNIA",
                "subtitle": "Floresta",
                "decoration": "amazonia",
                "car_speed_min": 110,
                "car_speed_max": 200,
                "cars_per_lane": 2,
                "points": 100,
                "bg_color_top": (50, 110, 60),
                "bg_color_bottom": (30, 80, 30),
                "asphalt_color": (70, 70, 60),
                "grass_color": (30, 80, 30),
            },
            2: {
                "name": "INGLATERRA",
                "subtitle": "Cidade à noite",
                "decoration": "londres",
                "car_speed_min": 130,
                "car_speed_max": 220,
                "cars_per_lane": 2,
                "points": 150,
                "bg_color_top": (10, 14, 26),
                "bg_color_bottom": (20, 28, 50),
                "asphalt_color": (40, 42, 50),
                "grass_color": (18, 24, 36),
            },
            3: {
                "name": "HAVAÍ",
                "subtitle": "Praia",
                "decoration": "havai",
                "car_speed_min": 150,
                "car_speed_max": 240,
                "cars_per_lane": 2,
                "points": 200,
                "bg_color_top": (74, 184, 240),
                "bg_color_bottom": (235, 215, 160),
                "asphalt_color": (185, 165, 115),
                "grass_color": (235, 215, 160),
            },
            4: {
                "name": "SUÍÇA",
                "subtitle": "Neve",
                "decoration": "suica",
                "car_speed_min": 170,
                "car_speed_max": 260,
                "cars_per_lane": 3,
                "points": 250,
                "bg_color_top": (168, 216, 240),
                "bg_color_bottom": (220, 232, 244),
                "asphalt_color": (135, 145, 155),
                "grass_color": (220, 232, 244),
            },
            5: {
                "name": "FRANÇA",
                "subtitle": "Montanha",
                "decoration": "franca",
                "car_speed_min": 180,
                "car_speed_max": 280,
                "cars_per_lane": 3,
                "points": 350,
                "bg_color_top": (106, 180, 224),
                "bg_color_bottom": (170, 210, 220),
                "asphalt_color": (95, 95, 100),
                "grass_color": (200, 215, 220),
            },
            6: {
                "name": "ÁFRICA DO SUL",
                "subtitle": "Safari",
                "decoration": "africa",
                "car_speed_min": 200,
                "car_speed_max": 300,
                "cars_per_lane": 3,
                "points": 450,
                "bg_color_top": (232, 120, 32),
                "bg_color_bottom": (170, 80, 30),
                "asphalt_color": (90, 60, 30),
                "grass_color": (160, 100, 40),
            },
            7: {
                "name": "EGITO",
                "subtitle": "Deserto",
                "decoration": "egito",
                "car_speed_min": 210,
                "car_speed_max": 295,
                "cars_per_lane": 3,
                "points": 600,
                "bg_color_top": (212, 160, 40),
                "bg_color_bottom": (220, 170, 60),
                "asphalt_color": (170, 130, 50),
                "grass_color": (200, 150, 30),
            },
            8: {
                "name": "CANADÁ",
                "subtitle": "Bosque",
                "decoration": "canada",
                "car_speed_min": 225,
                "car_speed_max": 310,
                "cars_per_lane": 3,
                "points": 750,
                "bg_color_top": (184, 204, 216),
                "bg_color_bottom": (220, 232, 240),
                "asphalt_color": (110, 115, 125),
                "grass_color": (232, 240, 246),
            },
            9: {
                "name": "BÉLGICA",
                "subtitle": "Cidade com chuva",
                "decoration": "belgica",
                "car_speed_min": 240,
                "car_speed_max": 325,
                "cars_per_lane": 3,
                "points": 900,
                "bg_color_top": (74, 82, 96),
                "bg_color_bottom": (95, 105, 120),
                "asphalt_color": (58, 58, 68),
                "grass_color": (60, 70, 80),
            },
            10: {
                "name": "ITÁLIA",
                "subtitle": "Cidade",
                "decoration": "milao",
                "car_speed_min": 255,
                "car_speed_max": 345,
                "cars_per_lane": 3,
                "points": 1200,
                "bg_color_top": (90, 142, 192),
                "bg_color_bottom": (130, 175, 215),
                "asphalt_color": (75, 75, 85),
                "grass_color": (200, 184, 160),
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
