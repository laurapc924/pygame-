"""Tela de instruções e tutorial do Fox Crossing."""

import pygame

from src.settings import (
    COR_DOURADO,
    COR_TEXTO,
    COR_TEXTO_SEC,
    COR_VERDE_CLARO,
    HEIGHT,
    WIDTH,
)
from src.states.base_state import BaseState
from src.utils.fonts import get_font
from src.utils.sprite_factory import (
    criar_background_floresta_dia,
    criar_cogumelo,
    criar_raposa_estatica,
    criar_trevo,
    desenhar_painel,
    desenhar_titulo_estilizado,
)


# Dimensões padrão de um painel de seção.
PAINEL_W = 460
PAINEL_H = 200


class InstructionsState(BaseState):
    """Exibe o tutorial: objetivo, controles, itens especiais e habilidade."""

    def __init__(self, game):
        """Inicializa fontes, background, nuvens animadas e ícones decorativos."""
        super().__init__(game)
        self.font_titulo = get_font(58, bold=True)
        self.font_secao = get_font(26, bold=True)
        self.font_texto = get_font(21)
        self.font_tecla = get_font(18, bold=True)
        self.font_rodape = get_font(19)

        self.background = criar_background_floresta_dia(WIDTH, HEIGHT)

        self.icone_cogumelo = criar_cogumelo(30)
        self.icone_trevo = criar_trevo(30)
        self.raposa = criar_raposa_estatica(70, 70)

    def _desenhar_tecla(self, screen, rect, texto):
        """Desenha uma tecla em formato de chip dentro das instrucoes."""
        pygame.draw.rect(screen, (18, 28, 24, 220), rect, border_radius=9)
        pygame.draw.rect(screen, COR_DOURADO, rect, 1, border_radius=9)
        surf = self.font_tecla.render(texto, True, COR_DOURADO)
        screen.blit(surf, surf.get_rect(center=rect.center))

    def _desenhar_linha_controle(self, screen, x, y, tecla, texto):
        """Desenha uma linha de controle com tecla separada da descricao."""
        tecla_rect = pygame.Rect(x, y, 72, 30)
        self._desenhar_tecla(screen, tecla_rect, tecla)
        texto_surf = self.font_texto.render(texto, True, COR_TEXTO)
        screen.blit(texto_surf, texto_surf.get_rect(midleft=(x + 88, y + 15)))

    def handle_events(self):
        """Processa eventos: M ou ESC voltam ao menu."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_m, pygame.K_ESCAPE):
                    from src.states.menu import MenuState

                    self.game.change_state(MenuState(self.game))

    def update(self, dt):
        """Tela estática: nada a atualizar."""
        pass

    def _desenhar_secao(self, screen, px, py, titulo, linhas):
        """Desenha um painel com título de seção e linhas de texto centralizadas.

        Args:
            screen: Surface destino.
            px: X do canto superior esquerdo do painel.
            py: Y do canto superior esquerdo do painel.
            titulo: Texto do título da seção.
            linhas: Lista de strings exibidas abaixo do título.
        """
        desenhar_painel(screen, px, py, PAINEL_W, PAINEL_H)
        centro_x = px + PAINEL_W // 2
        titulo_surf = self.font_secao.render(titulo, True, COR_VERDE_CLARO)
        screen.blit(titulo_surf, titulo_surf.get_rect(center=(centro_x, py + 34)))
        for i, linha in enumerate(linhas):
            linha_surf = self.font_texto.render(linha, True, COR_TEXTO)
            screen.blit(
                linha_surf, linha_surf.get_rect(center=(centro_x, py + 86 + i * 38))
            )

    def _desenhar_controles(self, screen, px, py):
        """Desenha controles com chips de tecla para melhorar a leitura."""
        desenhar_painel(screen, px, py, PAINEL_W, PAINEL_H)
        titulo_surf = self.font_secao.render("CONTROLES", True, COR_VERDE_CLARO)
        screen.blit(
            titulo_surf, titulo_surf.get_rect(center=(px + PAINEL_W // 2, py + 34))
        )
        self._desenhar_linha_controle(screen, px + 48, py + 70, "SETAS", "Mover")
        self._desenhar_linha_controle(screen, px + 48, py + 112, "SHIFT", "Instinto")
        self._desenhar_linha_controle(screen, px + 48, py + 154, "P", "Pausar")

    def _desenhar_itens(self, screen, px, py):
        """Desenha o painel 'ITENS ESPECIAIS' com os ícones de cogumelo e trevo.

        Args:
            screen: Surface destino.
            px: X do canto superior esquerdo do painel.
            py: Y do canto superior esquerdo do painel.
        """
        desenhar_painel(screen, px, py, PAINEL_W, PAINEL_H)
        titulo_surf = self.font_secao.render("ITENS ESPECIAIS", True, COR_VERDE_CLARO)
        screen.blit(
            titulo_surf, titulo_surf.get_rect(center=(px + PAINEL_W // 2, py + 34))
        )
        itens = [
            (self.icone_cogumelo, "Cogumelo: +1 vida"),
            (self.icone_trevo, "Trevo: invencível por 3 segundos"),
        ]
        for i, (icone, texto) in enumerate(itens):
            linha_y = py + 78 + i * 50
            screen.blit(icone, (px + 36, linha_y))
            texto_surf = self.font_texto.render(texto, True, COR_TEXTO)
            screen.blit(texto_surf, (px + 82, linha_y + 4))

    def draw(self, screen):
        """Desenha o fundo, o título, a raposa e os painéis de instruções."""
        screen.blit(self.background, (0, 0))

        screen.blit(self.raposa, (40, 12))
        desenhar_titulo_estilizado(
            screen, "COMO JOGAR", self.font_titulo, WIDTH // 2, 44, COR_DOURADO
        )

        x_esq = 42
        x_dir = WIDTH - 42 - PAINEL_W
        y_cima = 78
        y_baixo = 292

        self._desenhar_secao(
            screen,
            x_esq,
            y_cima,
            "OBJETIVO",
            [
                "Ajude a raposa a atravessar a cidade",
                "e chegar na zona dourada (a toca).",
            ],
        )
        self._desenhar_controles(screen, x_dir, y_cima)
        self._desenhar_itens(screen, x_esq, y_baixo)
        self._desenhar_secao(
            screen,
            x_dir,
            y_baixo,
            "HABILIDADE: INSTINTO",
            [
                "SHIFT reduz a velocidade dos carros.",
                "Dura 2s e recarrega em 10s.",
            ],
        )

        rodape_w, rodape_h = 460, 48
        rodape_x = WIDTH // 2 - rodape_w // 2
        rodape_y = HEIGHT - 60
        desenhar_painel(screen, rodape_x, rodape_y, rodape_w, rodape_h)
        rodape_surf = self.font_rodape.render(
            "M ou ESC para voltar ao menu", True, COR_TEXTO_SEC
        )
        screen.blit(
            rodape_surf,
            rodape_surf.get_rect(center=(WIDTH // 2, rodape_y + rodape_h // 2)),
        )
