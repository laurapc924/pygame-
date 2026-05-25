"""Gerenciador centralizado de música e efeitos sonoros do Fox Crossing."""

import pygame


class SoundManager:
    """Gerencia músicas e efeitos sonoros do jogo.

    Carrega os SFX uma única vez no início (colisão, vitória) e oferece
    helpers para tocar música em loop ou efeitos pontuais. Falhas ao
    carregar áudios são tratadas de forma silenciosa para que o jogo
    continue rodando mesmo sem som disponível.
    """

    def __init__(self):
        """Inicializa o mixer do pygame e pré-carrega os efeitos sonoros."""
        pygame.mixer.init()
        try:
            self.sfx_collision = pygame.mixer.Sound("assets/sounds/collision.wav")
        except pygame.error:
            self.sfx_collision = None
        try:
            self.sfx_victory = pygame.mixer.Sound("assets/sounds/victory.wav")
        except pygame.error:
            self.sfx_victory = None

    def play_music(self, track, loop=-1):
        """Para a música atual e toca o arquivo informado em loop.

        Args:
            track: Caminho do arquivo de música (.wav ou .mp3).
            loop: Quantas vezes repetir; -1 (padrão) repete indefinidamente.
        """
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(track)
            pygame.mixer.music.play(loop)
        except pygame.error:
            pass

    def stop_music(self):
        """Interrompe imediatamente a música em execução."""
        pygame.mixer.music.stop()

    def play_sfx(self, sound):
        """Toca um efeito sonoro pré-carregado se ele existir.

        Args:
            sound: pygame.mixer.Sound ou None (se o arquivo não carregou).
        """
        if sound:
            sound.play()
