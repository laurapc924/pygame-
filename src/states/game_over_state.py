"""Tela de Game Over: mostrada quando o jogador perde todas as vidas."""

import pygame

from src.settings import (
    COR_DOURADO,
    COR_TEXTO,
    COR_TEXTO_SEC,
    COR_VERMELHO,
    HEIGHT,
    WIDTH,
)
from src.states.base_state import BaseState
from src.utils.sprite_factory import (
    criar_raposa_estatica,
    desenhar_gradiente_vertical,
    desenhar_painel,
    desenhar_titulo_estilizado,
)


class GameOverState(BaseState):
    """Estado de Game Over exibido quando a raposa perde todas as vidas."""

    def __init__(self, game, score_manager=None):
        """Inicializa fontes, background, decoração e verifica novo recorde."""
        super().__init__(game)
        self.font_titulo = pygame.font.SysFont(None, 120)
        self.font_subtitulo = pygame.font.SysFont(None, 34)
        self.font_texto = pygame.font.SysFont(None, 32)
        self.font_botao = pygame.font.SysFont(None, 28)

        self.background = pygame.Surface((WIDTH, HEIGHT))
        desenhar_gradiente_vertical(self.background, (20, 0, 0), (50, 10, 10))

        self.raposa_triste = criar_raposa_estatica(120, 120, olhos_fechados=True)

        self.timer_piscar = 0
        self.mostrar_recorde = True

        self.score_manager = score_manager
        self.novo_recorde = False
        if self.score_manager is not None:
            self.novo_recorde = self.score_manager.check_and_update_highscore()
        self.game.sound_manager.play_sfx(self.game.sound_manager.sfx_collision)

    def handle_events(self):
        """Processa eventos: ENTER volta ao menu, ESC encerra o jogo."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from src.states.menu import MenuState

                    self.game.change_state(MenuState(self.game))
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self, dt):
        """Anima o painel de novo recorde piscando a cada 0.5s."""
        self.timer_piscar += dt
        if self.timer_piscar >= 0.5:
            self.mostrar_recorde = not self.mostrar_recorde
            self.timer_piscar = 0

    def draw(self, screen):
        """Desenha background, título, pontuação, recorde e botões de navegação."""
        screen.blit(self.background, (0, 0))

        desenhar_titulo_estilizado(
            screen, "GAME OVER", self.font_titulo, WIDTH // 2, 92, COR_VERMELHO
        )
        subtitulo = self.font_subtitulo.render(
            "A raposa não conseguiu...", True, COR_TEXTO_SEC
        )
        screen.blit(subtitulo, subtitulo.get_rect(center=(WIDTH // 2, 168)))

        screen.blit(self.raposa_triste, (45, HEIGHT - 150))

        painel_w = 440
        painel_x = WIDTH // 2 - painel_w // 2
        desenhar_painel(screen, painel_x, 205, painel_w, 120)
        if self.score_manager is not None:
            pontos = self.font_texto.render(
                f"Pontos finais: {self.score_manager.current_score}", True, COR_TEXTO
            )
            screen.blit(pontos, pontos.get_rect(center=(WIDTH // 2, 242)))
            recorde = self.font_texto.render(
                f"Recorde: {self.score_manager.highscore}", True, COR_TEXTO_SEC
            )
            screen.blit(recorde, recorde.get_rect(center=(WIDTH // 2, 288)))

        if self.novo_recorde and self.mostrar_recorde:
            desenhar_painel(
                screen,
                WIDTH // 2 - 150,
                338,
                300,
                46,
                cor=(80, 65, 0, 215),
                borda_cor=COR_DOURADO,
            )
            recorde_novo = self.font_texto.render("NOVO RECORDE!", True, COR_DOURADO)
            screen.blit(recorde_novo, recorde_novo.get_rect(center=(WIDTH // 2, 361)))

        self._desenhar_botoes(screen)

    def _desenhar_botoes(self, screen):
        """Desenha os botões '[ENTER] Voltar ao menu' e '[ESC] Sair' em painéis.

        Args:
            screen: Surface destino.
        """
        botao_y = 445
        botao_h = 52
        esq_w, dir_w = 280, 150
        esq_x = WIDTH // 2 - (esq_w + 16 + dir_w) // 2
        dir_x = esq_x + esq_w + 16

        desenhar_painel(screen, esq_x, botao_y, esq_w, botao_h)
        voltar = self.font_botao.render("[ENTER] Voltar ao menu", True, COR_TEXTO)
        screen.blit(
            voltar, voltar.get_rect(center=(esq_x + esq_w // 2, botao_y + botao_h // 2))
        )

        desenhar_painel(screen, dir_x, botao_y, dir_w, botao_h)
        sair = self.font_botao.render("[ESC] Sair", True, COR_TEXTO_SEC)
        screen.blit(
            sair, sair.get_rect(center=(dir_x + dir_w // 2, botao_y + botao_h // 2))
        )
