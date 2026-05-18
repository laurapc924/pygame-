import pygame

class SoundManager:
    "Gerencia músicas e efeitos sonoros do jogo."

    def __init__(self):
        """Inicializa o mixer e carrega os sons."""
        pygame.mixer.init()
        try:
            self.sfx_collision = pygame.mixer.Sound("assets/sounds/collision.wav")
        except:
            self.sfx_collision = None
        try:
            self.sfx_victory = pygame.mixer.Sound("assets/sounds/victory.wav")
        except:
            self.sfx_victory = None

    def play_music(self, track, loop=-1):
        "Toca uma música em loop."
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(track)
            pygame.mixer.music.play(loop)
        except:
            pass

    def stop_music(self):
        "Para a música."
        pygame.mixer.music.stop()

    def play_sfx(self, sound):
        "Toca um efeito sonoro."
        if sound:
            sound.play()