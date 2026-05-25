"""Gera as sprite sheets da raposa (4 direções x 3 frames) em pygame.draw.

Cada arquivo é uma faixa horizontal de 3 frames de 48x64. Os arquivos finais
ficam em ``assets/img/fox{0..3}.png``, onde:

- fox0.png = direção UP   (raposa vista de costas)
- fox1.png = direção RIGHT (perfil olhando à direita)
- fox2.png = direção DOWN  (raposa vista de frente)
- fox3.png = direção LEFT  (perfil olhando à esquerda)

Rode com ``python tools/generate_fox_sprites.py`` para regenerar os PNGs.
"""

from pathlib import Path

import pygame


FRAME_W = 48
FRAME_H = 64
N_FRAMES = 3

# Paleta da raposa.
LARANJA = (208, 110, 48)
LARANJA_ESC = (160, 78, 30)
BRANCO = (245, 240, 230)
PRETO = (38, 32, 28)
ROSA_OR = (236, 180, 170)
SOMBRA = (140, 70, 28)


def _new_frame():
    """Cria uma Surface transparente do tamanho de um frame."""
    return pygame.Surface((FRAME_W, FRAME_H), pygame.SRCALPHA)


def _draw_paw(surf, x, y):
    """Desenha uma pata (retângulo escuro) na posição dada."""
    pygame.draw.rect(surf, PRETO, (x, y, 5, 6))


def fox_down(frame):
    """Raposa vista de frente (DOWN), olhando pra câmera; 3 frames de animação."""
    surf = _new_frame()
    # Bob sutil do corpo.
    bob = 0 if frame == 1 else (-1 if frame == 0 else 1)

    # Cauda atrás (visível acima do corpo, com ponta branca).
    pygame.draw.rect(surf, LARANJA, (20, 30 + bob, 8, 14))
    pygame.draw.rect(surf, BRANCO, (21, 28 + bob, 6, 4))

    # Corpo principal.
    pygame.draw.rect(surf, LARANJA, (12, 28 + bob, 24, 26))
    # Barriga branca.
    pygame.draw.rect(surf, BRANCO, (16, 36 + bob, 16, 16))
    # Sombra lateral pra dar volume.
    pygame.draw.rect(surf, SOMBRA, (12, 28 + bob, 2, 26))
    pygame.draw.rect(surf, SOMBRA, (34, 28 + bob, 2, 26))

    # Cabeça.
    pygame.draw.rect(surf, LARANJA, (10, 10 + bob, 28, 20))
    # Bochechas brancas.
    pygame.draw.rect(surf, BRANCO, (12, 18 + bob, 24, 8))
    # Sombra lateral cabeça.
    pygame.draw.rect(surf, SOMBRA, (10, 10 + bob, 2, 20))
    pygame.draw.rect(surf, SOMBRA, (36, 10 + bob, 2, 20))

    # Orelhas pontudas.
    pygame.draw.polygon(surf, LARANJA, [(11, 12 + bob), (10, 0 + bob), (18, 10 + bob)])
    pygame.draw.polygon(surf, LARANJA, [(37, 12 + bob), (38, 0 + bob), (30, 10 + bob)])
    pygame.draw.polygon(surf, ROSA_OR, [(13, 10 + bob), (12, 4 + bob), (17, 9 + bob)])
    pygame.draw.polygon(surf, ROSA_OR, [(35, 10 + bob), (36, 4 + bob), (31, 9 + bob)])

    # Olhos (almonds pretas).
    pygame.draw.rect(surf, PRETO, (15, 18 + bob, 4, 3))
    pygame.draw.rect(surf, PRETO, (29, 18 + bob, 4, 3))
    # Pontinho branco no olho.
    pygame.draw.rect(surf, BRANCO, (16, 18 + bob, 1, 1))
    pygame.draw.rect(surf, BRANCO, (30, 18 + bob, 1, 1))

    # Nariz preto.
    pygame.draw.rect(surf, PRETO, (22, 23 + bob, 4, 3))

    # Patas (4 — andam alternando entre os frames).
    if frame == 0:
        _draw_paw(surf, 13, 54)
        _draw_paw(surf, 30, 56)
        _draw_paw(surf, 15, 58)
        _draw_paw(surf, 28, 56)
    elif frame == 1:
        _draw_paw(surf, 13, 56)
        _draw_paw(surf, 30, 56)
        _draw_paw(surf, 15, 56)
        _draw_paw(surf, 28, 56)
    else:
        _draw_paw(surf, 13, 56)
        _draw_paw(surf, 30, 54)
        _draw_paw(surf, 15, 56)
        _draw_paw(surf, 28, 58)

    return surf


def fox_up(frame):
    """Raposa vista de costas (UP); câmera olha pela nuca dela."""
    surf = _new_frame()
    bob = 0 if frame == 1 else (-1 if frame == 0 else 1)

    # Cauda agora aparece NA BASE do sprite (atrás = embaixo na visão UP).
    pygame.draw.rect(surf, LARANJA, (20, 50 + bob, 8, 14))
    pygame.draw.rect(surf, BRANCO, (21, 60 + bob, 6, 4))

    # Corpo.
    pygame.draw.rect(surf, LARANJA, (12, 28 + bob, 24, 26))
    pygame.draw.rect(surf, SOMBRA, (12, 28 + bob, 2, 26))
    pygame.draw.rect(surf, SOMBRA, (34, 28 + bob, 2, 26))

    # Cabeça (de costas).
    pygame.draw.rect(surf, LARANJA, (10, 10 + bob, 28, 20))
    pygame.draw.rect(surf, SOMBRA, (10, 10 + bob, 2, 20))
    pygame.draw.rect(surf, SOMBRA, (36, 10 + bob, 2, 20))

    # Orelhas pontudas (sem interior visível porque é de costas).
    pygame.draw.polygon(surf, LARANJA, [(11, 12 + bob), (10, 0 + bob), (18, 10 + bob)])
    pygame.draw.polygon(surf, LARANJA, [(37, 12 + bob), (38, 0 + bob), (30, 10 + bob)])
    pygame.draw.polygon(surf, LARANJA_ESC, [(13, 10 + bob), (12, 4 + bob), (17, 9 + bob)])
    pygame.draw.polygon(surf, LARANJA_ESC, [(35, 10 + bob), (36, 4 + bob), (31, 9 + bob)])

    # Patas (parcialmente visíveis dos lados do corpo).
    if frame == 0:
        _draw_paw(surf, 13, 30)
        _draw_paw(surf, 30, 32)
        _draw_paw(surf, 13, 46)
        _draw_paw(surf, 30, 48)
    elif frame == 1:
        _draw_paw(surf, 13, 32)
        _draw_paw(surf, 30, 32)
        _draw_paw(surf, 13, 48)
        _draw_paw(surf, 30, 48)
    else:
        _draw_paw(surf, 13, 32)
        _draw_paw(surf, 30, 30)
        _draw_paw(surf, 13, 48)
        _draw_paw(surf, 30, 46)

    return surf


def fox_right(frame):
    """Raposa em perfil olhando à direita; 3 frames de animação."""
    surf = _new_frame()
    bob = 0 if frame == 1 else (-1 if frame == 0 else 1)

    # Cauda atrás (esquerda).
    pygame.draw.rect(surf, LARANJA, (4, 24 + bob, 14, 14))
    pygame.draw.rect(surf, BRANCO, (2, 22 + bob, 6, 6))

    # Corpo (horizontal).
    pygame.draw.rect(surf, LARANJA, (12, 22 + bob, 24, 18))
    # Barriga branca embaixo.
    pygame.draw.rect(surf, BRANCO, (14, 32 + bob, 20, 6))
    # Sombra topo.
    pygame.draw.rect(surf, SOMBRA, (12, 22 + bob, 24, 2))

    # Cabeça (direita).
    pygame.draw.rect(surf, LARANJA, (30, 14 + bob, 16, 16))
    pygame.draw.rect(surf, SOMBRA, (30, 14 + bob, 16, 2))

    # Focinho pontudo à direita.
    pygame.draw.polygon(surf, LARANJA, [(44, 18 + bob), (47, 24 + bob), (44, 27 + bob)])
    pygame.draw.rect(surf, BRANCO, (44, 24 + bob, 3, 3))
    pygame.draw.rect(surf, PRETO, (46, 23 + bob, 2, 2))  # nariz

    # Orelha (visível só uma — outra atrás).
    pygame.draw.polygon(surf, LARANJA, [(31, 14 + bob), (34, 4 + bob), (38, 14 + bob)])
    pygame.draw.polygon(surf, ROSA_OR, [(33, 13 + bob), (35, 7 + bob), (37, 13 + bob)])

    # Olho.
    pygame.draw.rect(surf, PRETO, (38, 20 + bob, 3, 3))
    pygame.draw.rect(surf, BRANCO, (39, 20 + bob, 1, 1))

    # Patas (2 visíveis no perfil, andando).
    if frame == 0:
        _draw_paw(surf, 14, 40)  # frente avança
        _draw_paw(surf, 28, 42)
    elif frame == 1:
        _draw_paw(surf, 16, 42)
        _draw_paw(surf, 28, 42)
    else:
        _draw_paw(surf, 18, 42)
        _draw_paw(surf, 26, 40)  # traseira avança

    return surf


def fox_left(frame):
    """Raposa em perfil olhando à esquerda — espelhamento de fox_right."""
    right_surf = fox_right(frame)
    return pygame.transform.flip(right_surf, True, False)


DIR_FUNCS = {0: fox_up, 1: fox_right, 2: fox_down, 3: fox_left}


def build_sheet(direction):
    """Monta o sprite sheet (3 frames lado a lado) de uma direção."""
    sheet = pygame.Surface((FRAME_W * N_FRAMES, FRAME_H), pygame.SRCALPHA)
    fn = DIR_FUNCS[direction]
    for i in range(N_FRAMES):
        sheet.blit(fn(i), (i * FRAME_W, 0))
    return sheet


def build_preview():
    """Monta uma imagem grande com todas as direções e frames pra revisão visual."""
    padding = 8
    scale = 4  # 4x maior pra dar pra ver os pixels
    w = FRAME_W * N_FRAMES * scale + padding * 2
    h = FRAME_H * 4 * scale + padding * 5
    canvas = pygame.Surface((w, h))
    canvas.fill((40, 60, 50))
    nomes = ["UP (fox0)", "RIGHT (fox1)", "DOWN (fox2)", "LEFT (fox3)"]
    font = pygame.font.SysFont(None, 22, bold=True)
    for direction in range(4):
        sheet = build_sheet(direction)
        big = pygame.transform.scale(sheet, (sheet.get_width() * scale, sheet.get_height() * scale))
        y = padding + direction * (FRAME_H * scale + padding)
        canvas.blit(big, (padding, y))
        label = font.render(nomes[direction], True, (255, 220, 120))
        canvas.blit(label, (padding, y + FRAME_H * scale - 22))
    return canvas


def save_sheets(out_dir):
    """Salva os 4 PNGs em out_dir/foxN.png."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for direction in range(4):
        sheet = build_sheet(direction)
        pygame.image.save(sheet, str(out_dir / f"fox{direction}.png"))


def main():
    """Entry-point: gera os PNGs em assets/img/."""
    pygame.init()
    pygame.display.set_mode((1, 1))
    out_dir = Path(__file__).resolve().parent.parent / "assets" / "img"
    save_sheets(out_dir)
    print(f"Salvo: {out_dir / 'fox0.png'} (+ fox1..3)")
    pygame.quit()


if __name__ == "__main__":
    main()
