"""Gerencia as configurações de cada fase: dificuldade, tema e cores."""


class LevelManager:
    """Guarda as configs de cada fase (dificuldade, tema, cores) e a fase ativa."""

    TOTAL_LEVELS = 10

    def __init__(self):
        """Inicializa na fase 1 com as configs temáticas de todas as 10 fases."""
        self.current_level = 1
        self.configs = {
            # Fase 1: rua diurna básica; mantém 3 faixas, poucos carros e velocidade baixa.
            1: {
                "name": "RUA DE DIA",
                "subtitle": "O começo de tudo",
                "decoration": "arvore",
                "lane_count": 3,
                "car_speed_min": 130,
                "car_speed_max": 250,
                "cars_per_lane": 2,
                "points": 100,
                "bg_color_top": (120, 175, 230),
                "bg_color_bottom": (175, 210, 240),
                "asphalt_color": (82, 82, 88),
                "grass_color": (50, 120, 58),
            },
            # Fase 2: noite urbana; aumenta carros por faixa e escurece o cenário.
            2: {
                "name": "RUA DE NOITE",
                "subtitle": "Sob a luz dos postes",
                "decoration": "poste",
                "lane_count": 3,
                "car_speed_min": 170,
                "car_speed_max": 310,
                "cars_per_lane": 3,
                "points": 200,
                "bg_color_top": (12, 16, 38),
                "bg_color_bottom": (28, 34, 62),
                "asphalt_color": (46, 46, 54),
                "grass_color": (24, 44, 30),
            },
            # Fase 3: praia; mantém 3 faixas, mas sobe a velocidade e muda para tons de areia.
            3: {
                "name": "PRAIA",
                "subtitle": "Areia, sol e perigo",
                "decoration": "coqueiro",
                "lane_count": 3,
                "car_speed_min": 200,
                "car_speed_max": 360,
                "cars_per_lane": 3,
                "points": 350,
                "bg_color_top": (115, 200, 235),
                "bg_color_bottom": (240, 222, 165),
                "asphalt_color": (190, 170, 120),
                "grass_color": (240, 222, 165),
            },
            # Fase 4: neve; introduz 4 faixas e partículas de neve para reduzir a leitura visual.
            4: {
                "name": "NEVE",
                "subtitle": "Pista escorregadia",
                "decoration": "pinheiro",
                "lane_count": 4,
                "car_speed_min": 200,
                "car_speed_max": 350,
                "cars_per_lane": 3,
                "points": 500,
                "bg_color_top": (200, 220, 240),
                "bg_color_bottom": (232, 240, 250),
                "asphalt_color": (138, 144, 152),
                "grass_color": (226, 233, 242),
            },
            # Fase 5: montanha; mantém 4 faixas e aumenta a velocidade média.
            5: {
                "name": "MONTANHA",
                "subtitle": "Topo do mundo",
                "decoration": "pedra",
                "lane_count": 4,
                "car_speed_min": 220,
                "car_speed_max": 380,
                "cars_per_lane": 3,
                "points": 700,
                "bg_color_top": (118, 128, 148),
                "bg_color_bottom": (92, 102, 118),
                "asphalt_color": (96, 92, 86),
                "grass_color": (98, 112, 76),
            },
            # Fase 6: fazenda; segura a densidade em 3 carros para a estrada ficar atravessável.
            6: {
                "name": "FAZENDA",
                "subtitle": "Estrada de terra",
                "decoration": "cerca",
                "lane_count": 4,
                "car_speed_min": 220,
                "car_speed_max": 360,
                "cars_per_lane": 3,
                "points": 1000,
                "bg_color_top": (140, 190, 228),
                "bg_color_bottom": (192, 216, 236),
                "asphalt_color": (120, 95, 62),
                "grass_color": (108, 150, 58),
            },
            # Fase 7: deserto; chega a 5 faixas, mas mantém 3 carros para abrir janelas de passagem.
            7: {
                "name": "DESERTO",
                "subtitle": "Calor na pista",
                "decoration": "pedra",
                "lane_count": 5,
                "car_speed_min": 230,
                "car_speed_max": 390,
                "cars_per_lane": 3,
                "points": 1300,
                "bg_color_top": (230, 172, 96),
                "bg_color_bottom": (246, 212, 142),
                "asphalt_color": (156, 118, 74),
                "grass_color": (214, 176, 92),
            },
            # Fase 8: cidade chuvosa; mantém 3 carros e reduz velocidade para dar tempo entre eles.
            8: {
                "name": "CHUVA NA CIDADE",
                "subtitle": "Reflexos no asfalto",
                "decoration": "poste",
                "lane_count": 5,
                "car_speed_min": 230,
                "car_speed_max": 370,
                "cars_per_lane": 3,
                "points": 1650,
                "bg_color_top": (52, 78, 104),
                "bg_color_bottom": (96, 116, 128),
                "asphalt_color": (58, 70, 78),
                "grass_color": (42, 78, 64),
            },
            # Fase 9: bosque ao entardecer; sobe um pouco a velocidade, ainda com 3 carros por faixa.
            9: {
                "name": "BOSQUE AO ENTARDECER",
                "subtitle": "Sombras compridas",
                "decoration": "arvore",
                "lane_count": 5,
                "car_speed_min": 250,
                "car_speed_max": 410,
                "cars_per_lane": 3,
                "points": 2050,
                "bg_color_top": (210, 124, 84),
                "bg_color_bottom": (82, 86, 74),
                "asphalt_color": (78, 72, 68),
                "grass_color": (54, 94, 58),
            },
            # Fase 10: metrópole final; final difícil, mas com janelas reais entre os carros.
            10: {
                "name": "METROPOLE FINAL",
                "subtitle": "A ultima travessia",
                "decoration": "poste",
                "lane_count": 5,
                "car_speed_min": 260,
                "car_speed_max": 410,
                "cars_per_lane": 3,
                "points": 2600,
                "bg_color_top": (18, 24, 46),
                "bg_color_bottom": (92, 42, 72),
                "asphalt_color": (38, 38, 48),
                "grass_color": (32, 36, 48),
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
