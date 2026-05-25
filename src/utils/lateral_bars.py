"""Barras laterais decorativas, uma para cada lado e tema das 10 fases.

Cada função recebe (width, height) e devolve uma Surface escalada a partir
de um design original de 48x200, reproduzindo a arte pixel dos SVGs de
referência (uma cena por país: floresta amazônica, Londres à noite, etc.).
"""

import pygame


def _bar_canvas(width, height, design_w=48, design_h=200):
    """Cria a Surface da barra e devolve helpers escalados das coords de design.

    Args:
        width: Largura final da barra em pixels.
        height: Altura final da barra em pixels.
        design_w: Largura do design original (padrão 48).
        design_h: Altura do design original (padrão 200).

    Returns:
        (surf, R, rect_alpha, poly, poly_alpha, line_alpha): a Surface alvo
        mais helpers que escalam coords de design para pixels reais.
    """
    surf = pygame.Surface((width, height))
    sx = width / design_w
    sy = height / design_h

    def R(x, y, w, h):
        return pygame.Rect(
            int(x * sx), int(y * sy), max(1, int(w * sx)), max(1, int(h * sy))
        )

    def rect_alpha(cor, alpha, x, y, w, h):
        r = R(x, y, w, h)
        s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        s.fill((*cor, alpha))
        surf.blit(s, r.topleft)

    def poly(cor, pts):
        scaled = [(int(x * sx), int(y * sy)) for (x, y) in pts]
        pygame.draw.polygon(surf, cor, scaled)

    def poly_alpha(cor, alpha, pts):
        scaled = [(int(x * sx), int(y * sy)) for (x, y) in pts]
        min_x = min(p[0] for p in scaled)
        min_y = min(p[1] for p in scaled)
        max_x = max(p[0] for p in scaled)
        max_y = max(p[1] for p in scaled)
        s = pygame.Surface(
            (max_x - min_x + 1, max_y - min_y + 1), pygame.SRCALPHA
        )
        local = [(p[0] - min_x, p[1] - min_y) for p in scaled]
        pygame.draw.polygon(s, (*cor, alpha), local)
        surf.blit(s, (min_x, min_y))

    def line_alpha(cor, alpha, x1, y1, x2, y2, w=1):
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.line(
            s, (*cor, alpha),
            (int(x1 * sx), int(y1 * sy)),
            (int(x2 * sx), int(y2 * sy)),
            w,
        )
        surf.blit(s, (0, 0))

    return surf, R, rect_alpha, poly, poly_alpha, line_alpha


# ============================== AMAZÔNIA ==============================

def _amazonia_esq(w, h):
    """Barra esquerda do tema AMAZÔNIA: floresta densa, cipós e folhas."""
    surf, R, rect_alpha, poly, _, _ = _bar_canvas(w, h)
    surf.fill((26, 74, 10))
    rect_alpha((42, 106, 16), 128, 8, 0, 4, 200)
    rect_alpha((42, 106, 16), 128, 36, 0, 4, 200)
    # Árvore grande embaixo.
    pygame.draw.rect(surf, (90, 48, 16), R(14, 160, 8, 40))
    pygame.draw.rect(surf, (30, 122, 8), R(4, 130, 28, 36))
    pygame.draw.rect(surf, (37, 146, 10), R(8, 118, 20, 22))
    pygame.draw.rect(surf, (42, 170, 12), R(12, 108, 12, 16))
    # Árvore média.
    pygame.draw.rect(surf, (90, 48, 16), R(18, 80, 6, 30))
    pygame.draw.rect(surf, (30, 122, 8), R(10, 58, 22, 28))
    pygame.draw.rect(surf, (37, 146, 10), R(14, 48, 14, 18))
    pygame.draw.rect(surf, (42, 170, 12), R(17, 40, 8, 12))
    # Folhas pendentes.
    for x, y, ww, hh, cor, a in [
        (2, 20, 10, 6, (37, 146, 10), 205), (34, 35, 10, 6, (42, 170, 12), 205),
        (0, 50, 8, 5, (30, 122, 8), 180), (38, 65, 10, 5, (37, 146, 10), 180),
        (2, 90, 10, 5, (42, 170, 12), 153),
    ]:
        rect_alpha(cor, a, x, y, ww, hh)
    pygame.draw.rect(surf, (45, 106, 16), R(0, 192, 48, 8))
    rect_alpha((255, 68, 136), 230, 6, 186, 4, 4)
    rect_alpha((255, 170, 0), 230, 30, 188, 4, 4)
    return surf


def _amazonia_dir(w, h):
    """Barra direita do tema AMAZÔNIA: árvores variadas, cipós e flores."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    surf.fill((26, 74, 10))
    rect_alpha((42, 106, 16), 128, 6, 0, 4, 200)
    rect_alpha((42, 106, 16), 128, 38, 0, 4, 200)
    # Árvore central baixa.
    pygame.draw.rect(surf, (90, 48, 16), R(20, 155, 8, 45))
    pygame.draw.rect(surf, (30, 122, 8), R(8, 122, 30, 38))
    pygame.draw.rect(surf, (37, 146, 10), R(12, 110, 22, 20))
    pygame.draw.rect(surf, (42, 170, 12), R(16, 100, 14, 14))
    # Árvore alta esquerda.
    pygame.draw.rect(surf, (90, 48, 16), R(4, 60, 6, 42))
    pygame.draw.rect(surf, (30, 122, 8), R(0, 40, 20, 26))
    pygame.draw.rect(surf, (42, 170, 12), R(2, 30, 14, 16))
    # Árvore média direita.
    pygame.draw.rect(surf, (90, 48, 16), R(30, 75, 5, 30))
    pygame.draw.rect(surf, (37, 146, 10), R(26, 56, 18, 24))
    pygame.draw.rect(surf, (42, 170, 12), R(29, 48, 10, 14))
    # Folhas pendentes.
    rect_alpha((37, 146, 10), 205, 36, 18, 10, 6)
    rect_alpha((42, 170, 12), 180, 0, 30, 8, 5)
    rect_alpha((30, 122, 8), 180, 38, 50, 10, 5)
    pygame.draw.rect(surf, (45, 106, 16), R(0, 192, 48, 8))
    rect_alpha((255, 68, 136), 230, 16, 186, 4, 4)
    rect_alpha((255, 170, 0), 230, 36, 188, 4, 4)
    return surf


# ============================== LONDRES ==============================

def _londres_esq(w, h):
    """Barra esquerda do tema LONDRES: edifícios e Big Ben à noite."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    surf.fill((10, 14, 26))
    # Estrelas no céu.
    for x, y, a in [(8, 8, 200), (24, 14, 153), (38, 6, 230), (14, 22, 128), (42, 20, 180)]:
        rect_alpha((255, 255, 255), a, x, y, 2, 2)
    # Camada de neblina.
    rect_alpha((136, 153, 170), 38, 0, 140, 48, 20)
    # Edifício pequeno esquerdo.
    pygame.draw.rect(surf, (26, 32, 48), R(0, 90, 20, 110))
    # Janelas (amarelo/azul aleatórios).
    windows_left = [
        (2, 98, 245, 200), (8, 98, 245, 128), (14, 98, 74, 158, 180),
        (2, 108, 74, 158, 153), (8, 108, 245, 200), (14, 108, 245, 102),
        (2, 118, 245, 178), (14, 118, 74, 158, 205),
    ]
    for entry in windows_left:
        if len(entry) == 4:
            x, y, cor_g, a = entry
            cor = (245, 200, 66) if cor_g == 245 else (74, 158, 255)
            rect_alpha(cor, a, x, y, 4, 4)
        else:
            x, y, _, _, a = entry
            rect_alpha((74, 158, 255), a, x, y, 4, 4)
    # Torre Big Ben central.
    pygame.draw.rect(surf, (34, 40, 56), R(22, 60, 18, 140))
    pygame.draw.rect(surf, (42, 52, 72), R(20, 52, 22, 12))
    pygame.draw.rect(surf, (42, 52, 72), R(24, 44, 14, 12))
    pygame.draw.rect(surf, (51, 61, 80), R(26, 36, 10, 12))
    pygame.draw.rect(surf, (58, 69, 88), R(28, 28, 6, 12))
    # Relógio amarelado.
    rect_alpha((232, 216, 112), 180, 24, 52, 14, 10)
    pygame.draw.rect(surf, (51, 51, 51), R(30, 54, 2, 4))
    pygame.draw.rect(surf, (51, 51, 51), R(28, 56, 4, 2))
    # Agulha.
    pygame.draw.rect(surf, (74, 85, 104), R(30, 20, 2, 10))
    # Chão e lampião.
    pygame.draw.rect(surf, (17, 24, 40), R(0, 192, 48, 8))
    pygame.draw.rect(surf, (74, 74, 90), R(3, 155, 3, 38))
    pygame.draw.rect(surf, (74, 74, 90), R(1, 153, 7, 4))
    rect_alpha((245, 200, 66), 230, 2, 148, 5, 6)
    return surf


def _londres_dir(w, h):
    """Barra direita do tema LONDRES: dois prédios iluminados e neblina."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    surf.fill((12, 16, 32))
    for x, y, a in [(6, 10, 180), (20, 5, 230), (34, 16, 153), (44, 8, 205), (12, 24, 128)]:
        rect_alpha((255, 255, 255), a, x, y, 2, 2)
    # Prédio alto esquerdo.
    pygame.draw.rect(surf, (28, 36, 52), R(4, 70, 22, 130))
    # Janelas em grade.
    cores_jan = [(245, 200, 66), (74, 158, 255), (245, 200, 66)]
    for fila_y in (78, 88, 98, 108):
        for col_x in (6, 12, 18):
            cor = cores_jan[(fila_y + col_x) % 3]
            rect_alpha(cor, 180, col_x, fila_y, 4, 4)
    # Prédio mais baixo direito.
    pygame.draw.rect(surf, (24, 32, 46), R(28, 110, 20, 90))
    for fila_y in (118, 128):
        for col_x in (30, 38):
            cor = cores_jan[(fila_y + col_x) % 3]
            rect_alpha(cor, 180, col_x, fila_y, 4, 4)
    # Neblina suave.
    rect_alpha((136, 153, 170), 26, 0, 150, 48, 15)
    # Lampião direito.
    pygame.draw.rect(surf, (74, 74, 90), R(40, 158, 3, 34))
    pygame.draw.rect(surf, (74, 74, 90), R(38, 156, 7, 4))
    rect_alpha((245, 200, 66), 230, 39, 151, 5, 6)
    pygame.draw.rect(surf, (14, 22, 36), R(0, 192, 48, 8))
    return surf


# ============================== HAVAÍ ==============================

def _havai_esq(w, h):
    """Barra esquerda do tema HAVAÍ: praia com sol, palmeira e mar."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    pygame.draw.rect(surf, (74, 184, 240), R(0, 0, 48, 120))
    pygame.draw.rect(surf, (26, 106, 170), R(0, 120, 48, 80))
    rect_alpha((42, 136, 204), 180, 0, 118, 48, 8)
    # Ondas.
    for x, y, ww in [(0, 130, 20), (24, 138, 20), (0, 150, 16), (28, 162, 16)]:
        rect_alpha((74, 170, 221), 153, x, y, ww, 4)
    # Areia.
    pygame.draw.rect(surf, (232, 200, 112), R(0, 110, 48, 14))
    # Tronco do coqueiro.
    pygame.draw.rect(surf, (139, 90, 32), R(20, 50, 8, 64))
    pygame.draw.rect(surf, (139, 90, 32), R(22, 44, 6, 10))
    # Folhas (4 retângulos largos).
    for x, y, ww, hh, cor in [
        (0, 30, 24, 8, (45, 154, 16)),
        (24, 28, 24, 8, (53, 176, 18)),
        (8, 22, 20, 7, (45, 154, 16)),
        (22, 20, 20, 7, (53, 176, 18)),
    ]:
        pygame.draw.rect(surf, cor, R(x, y, ww, hh))
    # Cocos.
    pygame.draw.rect(surf, (139, 74, 16), R(18, 50, 6, 6))
    # Sol.
    pygame.draw.rect(surf, (255, 224, 51), R(6, 10, 20, 20))
    for x, y, ww, hh in [(2, 18, 6, 4), (28, 18, 6, 4), (14, 6, 8, 4), (14, 30, 8, 4)]:
        rect_alpha((255, 224, 51), 180, x, y, ww, hh)
    return surf


def _havai_dir(w, h):
    """Barra direita do tema HAVAÍ: mar, palmeira, hibisco e nuvem."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    pygame.draw.rect(surf, (90, 196, 248), R(0, 0, 48, 120))
    pygame.draw.rect(surf, (26, 106, 170), R(0, 120, 48, 80))
    rect_alpha((42, 136, 204), 180, 0, 118, 48, 8)
    for x, y, ww in [(4, 128, 18), (26, 140, 18), (2, 156, 14), (30, 168, 14)]:
        rect_alpha((74, 170, 221), 153, x, y, ww, 4)
    pygame.draw.rect(surf, (232, 200, 112), R(0, 110, 48, 14))
    # Hibiscos.
    rect_alpha((255, 68, 102), 230, 4, 104, 8, 8)
    rect_alpha((255, 102, 68), 230, 36, 106, 8, 8)
    # Coqueiro.
    pygame.draw.rect(surf, (139, 90, 32), R(6, 55, 7, 58))
    for x, y, ww, hh, cor in [
        (0, 35, 20, 7, (45, 154, 16)),
        (8, 32, 20, 7, (53, 176, 18)),
        (0, 26, 18, 6, (45, 154, 16)),
        (10, 24, 18, 6, (53, 176, 18)),
    ]:
        pygame.draw.rect(surf, cor, R(x, y, ww, hh))
    pygame.draw.rect(surf, (139, 74, 16), R(4, 56, 6, 6))
    # Nuvem.
    rect_alpha((255, 255, 255), 217, 22, 18, 22, 10)
    rect_alpha((255, 255, 255), 217, 26, 12, 14, 10)
    return surf


# ============================== SUÍÇA ==============================

def _suica_esq(w, h):
    """Barra esquerda do tema SUÍÇA: montanha nevada, pinheiros e chalé."""
    surf, R, rect_alpha, poly, poly_alpha, _ = _bar_canvas(w, h)
    surf.fill((168, 216, 240))
    poly((200, 216, 208), [(0, 160), (24, 70), (48, 160)])
    poly((232, 238, 242), [(0, 160), (24, 80), (48, 160)])
    poly((255, 255, 255), [(14, 95), (24, 70), (34, 95)])
    poly_alpha((184, 204, 212), 180, [(-10, 160), (14, 100), (38, 160)])
    poly_alpha((255, 255, 255), 230, [(6, 118), (14, 100), (22, 118)])
    # Pinheiros.
    for tx, tw, th_top in [(4, 170, 138), (32, 172, 140), (18, 175, 148)]:
        pygame.draw.rect(surf, (90, 48, 16), R(tx, tw, 6, 200 - tw))
        cx = tx + 3
        poly((26, 106, 32), [(cx, th_top), (cx - 6, 170), (cx + 6, 170)])
        poly((37, 136, 10), [(cx, th_top + 12), (cx - 5, 172), (cx + 5, 172)])
    # Chalé.
    pygame.draw.rect(surf, (200, 160, 96), R(10, 178, 18, 16))
    poly((139, 74, 32), [(10, 178), (19, 168), (28, 178)])
    pygame.draw.rect(surf, (107, 48, 16), R(16, 184, 6, 10))
    pygame.draw.rect(surf, (232, 238, 242), R(0, 194, 48, 6))
    return surf


def _suica_dir(w, h):
    """Barra direita do tema SUÍÇA: montanha alta, pinheiros e bandeira."""
    surf, R, rect_alpha, poly, poly_alpha, _ = _bar_canvas(w, h)
    surf.fill((184, 224, 244))
    poly((208, 220, 228), [(-4, 160), (20, 65), (44, 160)])
    poly((238, 242, 246), [(-4, 160), (20, 75), (44, 160)])
    poly((255, 255, 255), [(10, 100), (20, 65), (30, 100)])
    poly_alpha((192, 212, 220), 180, [(16, 160), (36, 95), (56, 160)])
    poly_alpha((255, 255, 255), 230, [(28, 115), (36, 95), (44, 115)])
    # Pinheiros.
    for tx, ty, th_top in [(2, 172, 144), (36, 170, 142)]:
        pygame.draw.rect(surf, (90, 48, 16), R(tx, ty, 6, 200 - ty))
        cx = tx + 3
        poly((26, 106, 32), [(cx, th_top), (cx - 6, ty), (cx + 6, ty)])
        poly((37, 136, 10), [(cx, th_top + 12), (cx - 5, ty), (cx + 5, ty)])
    # Bandeira suíça.
    pygame.draw.rect(surf, (136, 136, 136), R(22, 155, 2, 14))
    pygame.draw.rect(surf, (204, 0, 0), R(24, 155, 8, 6))
    pygame.draw.rect(surf, (255, 255, 255), R(26, 157, 4, 2))
    pygame.draw.rect(surf, (255, 255, 255), R(27, 155, 2, 6))
    pygame.draw.rect(surf, (232, 238, 242), R(0, 194, 48, 6))
    return surf


# ============================== FRANÇA ==============================

def _franca_esq(w, h):
    """Barra esquerda do tema FRANÇA: Mont Blanc alto e pinheiros."""
    surf, R, rect_alpha, poly, poly_alpha, _ = _bar_canvas(w, h)
    surf.fill((106, 180, 224))
    rect_alpha((255, 255, 255), 217, 2, 20, 26, 10)
    rect_alpha((255, 255, 255), 217, 6, 14, 16, 10)
    poly((192, 204, 212), [(-4, 200), (24, 30), (52, 200)])
    poly((216, 228, 236), [(4, 200), (24, 40), (44, 200)])
    poly((255, 255, 255), [(14, 80), (24, 30), (34, 80)])
    poly_alpha((176, 188, 196), 153, [(8, 140), (24, 90), (40, 140)])
    # Pinheiros.
    for tx, ty in [(2, 178), (38, 176), (20, 180)]:
        pygame.draw.rect(surf, (74, 46, 16), R(tx, ty, 6, 200 - ty))
        cx = tx + 3
        poly((26, 90, 24), [(cx, ty - 28), (cx - 5, ty), (cx + 5, ty)])
        poly((34, 106, 30), [(cx, ty - 18), (cx - 4, ty), (cx + 4, ty)])
    pygame.draw.rect(surf, (232, 238, 244), R(0, 194, 48, 6))
    return surf


def _franca_dir(w, h):
    """Barra direita do tema FRANÇA: pico nevado e teleférico."""
    surf, R, rect_alpha, poly, poly_alpha, _ = _bar_canvas(w, h)
    surf.fill((122, 192, 232))
    rect_alpha((255, 255, 255), 217, 18, 16, 28, 10)
    rect_alpha((255, 255, 255), 217, 22, 10, 18, 10)
    poly((184, 200, 208), [(-4, 200), (20, 35), (44, 200)])
    poly((204, 218, 228), [(2, 200), (20, 44), (38, 200)])
    poly((255, 255, 255), [(10, 85), (20, 35), (30, 85)])
    poly_alpha((168, 184, 192), 153, [(6, 145), (20, 95), (34, 145)])
    for tx, ty in [(4, 174), (36, 176)]:
        pygame.draw.rect(surf, (74, 46, 16), R(tx, ty, 6, 200 - ty))
        cx = tx + 3
        poly((26, 90, 24), [(cx, ty - 26), (cx - 5, ty), (cx + 5, ty)])
        poly((34, 106, 30), [(cx, ty - 14), (cx - 4, ty), (cx + 4, ty)])
    # Cabo do teleférico (linha).
    pygame.draw.line(surf, (136, 136, 136), R(0, 100, 1, 1).topleft, R(48, 80, 1, 1).topleft, 1)
    pygame.draw.rect(surf, (204, 17, 17), R(18, 86, 12, 8))
    pygame.draw.rect(surf, (136, 136, 136), R(22, 84, 4, 4))
    pygame.draw.rect(surf, (232, 238, 244), R(0, 194, 48, 6))
    return surf


# ============================== ÁFRICA DO SUL (SAFARI) ==============================

def _africa_esq(w, h):
    """Barra esquerda do tema ÁFRICA DO SUL: pôr do sol na savana com girafa."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    pygame.draw.rect(surf, (232, 120, 32), R(0, 0, 48, 130))
    rect_alpha((192, 80, 16), 128, 0, 80, 48, 50)
    rect_alpha((255, 224, 51), 230, 8, 70, 18, 18)
    rect_alpha((255, 224, 51), 153, 14, 66, 6, 6)
    pygame.draw.rect(surf, (58, 40, 8), R(0, 130, 48, 70))
    rect_alpha((192, 112, 32), 128, 0, 128, 48, 6)
    # Acácia esquerda silhueta.
    pygame.draw.rect(surf, (26, 16, 8), R(2, 90, 5, 44))
    pygame.draw.rect(surf, (26, 16, 8), R(0, 72, 28, 20))
    pygame.draw.rect(surf, (26, 16, 8), R(4, 66, 20, 14))
    # Acácia direita.
    pygame.draw.rect(surf, (26, 16, 8), R(36, 95, 5, 38))
    pygame.draw.rect(surf, (26, 16, 8), R(26, 78, 22, 18))
    pygame.draw.rect(surf, (26, 16, 8), R(30, 72, 14, 12))
    # Tufos de grama.
    for x, y, hh in [(5, 126, 8), (16, 124, 10), (28, 126, 8), (38, 124, 10)]:
        rect_alpha((90, 58, 8), 205, x, y, 4, hh)
    # Girafa silhueta.
    pygame.draw.rect(surf, (26, 16, 8), R(20, 110, 5, 20))
    pygame.draw.rect(surf, (26, 16, 8), R(21, 96, 3, 16))
    pygame.draw.rect(surf, (26, 16, 8), R(19, 95, 7, 6))
    pygame.draw.rect(surf, (26, 16, 8), R(22, 90, 2, 8))
    return surf


def _africa_dir(w, h):
    """Barra direita do tema ÁFRICA DO SUL: savana com elefante."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    pygame.draw.rect(surf, (217, 106, 20), R(0, 0, 48, 130))
    rect_alpha((176, 64, 16), 128, 0, 80, 48, 50)
    rect_alpha((255, 224, 51), 217, 22, 68, 18, 18)
    rect_alpha((255, 224, 51), 153, 28, 64, 6, 6)
    pygame.draw.rect(surf, (58, 40, 8), R(0, 130, 48, 70))
    rect_alpha((184, 104, 24), 128, 0, 128, 48, 6)
    # Acácia central.
    pygame.draw.rect(surf, (26, 16, 8), R(18, 92, 5, 40))
    pygame.draw.rect(surf, (26, 16, 8), R(10, 72, 26, 22))
    pygame.draw.rect(surf, (26, 16, 8), R(14, 65, 18, 14))
    # Elefante silhueta.
    pygame.draw.rect(surf, (26, 16, 8), R(2, 112, 14, 18))
    pygame.draw.rect(surf, (26, 16, 8), R(6, 106, 10, 10))
    for px in (4, 9, 13):
        pygame.draw.rect(surf, (26, 16, 8), R(px, 115, 3, 7))
    pygame.draw.rect(surf, (26, 16, 8), R(7, 104, 2, 8))  # tromba
    # Tufos.
    for x, y, hh in [(8, 126, 8), (24, 124, 10), (38, 126, 8)]:
        rect_alpha((90, 58, 8), 205, x, y, 4, hh)
    return surf


# ============================== EGITO ==============================

def _egito_esq(w, h):
    """Barra esquerda do tema EGITO: deserto com pirâmide e sol forte."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    pygame.draw.rect(surf, (212, 160, 40), R(0, 0, 48, 120))
    rect_alpha((232, 184, 64), 128, 0, 80, 48, 40)
    pygame.draw.rect(surf, (255, 248, 160), R(14, 10, 20, 20))
    for x, y, ww, hh in [(22, 4, 4, 8), (22, 28, 4, 8), (6, 18, 8, 4), (34, 18, 8, 4)]:
        rect_alpha((255, 248, 160), 180, x, y, ww, hh)
    pygame.draw.rect(surf, (200, 150, 14), R(0, 120, 48, 80))
    rect_alpha((224, 168, 32), 180, 0, 118, 48, 8)
    # Dunas (aproximadas com elipses preenchidas).
    pygame.draw.ellipse(surf, (216, 168, 24), R(-6, 116, 36, 12))
    pygame.draw.ellipse(surf, (200, 144, 16), R(22, 122, 32, 10))
    # Pirâmide grande.
    pygame.draw.polygon(surf, (184, 120, 8), [
        (int(2 * w / 48), int(120 * h / 200)),
        (int(16 * w / 48), int(60 * h / 200)),
        (int(30 * w / 48), int(120 * h / 200)),
    ])
    pygame.draw.polygon(surf, (212, 144, 16), [
        (int(4 * w / 48), int(120 * h / 200)),
        (int(16 * w / 48), int(65 * h / 200)),
        (int(28 * w / 48), int(120 * h / 200)),
    ])
    rect_alpha((138, 90, 4), 205, 12, 98, 8, 6)
    # Escaravelho.
    pygame.draw.rect(surf, (26, 26, 96), R(36, 140, 8, 6))
    pygame.draw.rect(surf, (42, 42, 128), R(38, 138, 4, 4))
    # Ondulações na areia.
    for y in (150, 158, 166):
        rect_alpha((176, 112, 8), 128, 2 + (y % 10), y, 18, 2)
    return surf


def _egito_dir(w, h):
    """Barra direita do tema EGITO: deserto com esfinge e pirâmide."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    pygame.draw.rect(surf, (204, 152, 32), R(0, 0, 48, 120))
    rect_alpha((224, 176, 48), 128, 0, 80, 48, 40)
    pygame.draw.rect(surf, (255, 248, 160), R(14, 8, 20, 20))
    for x, y, ww, hh in [(22, 2, 4, 8), (22, 26, 4, 8), (6, 16, 8, 4), (34, 16, 8, 4)]:
        rect_alpha((255, 248, 160), 180, x, y, ww, hh)
    pygame.draw.rect(surf, (192, 144, 16), R(0, 120, 48, 80))
    rect_alpha((216, 160, 24), 180, 0, 118, 48, 8)
    pygame.draw.ellipse(surf, (204, 160, 24), R(-6, 118, 32, 12))
    pygame.draw.ellipse(surf, (184, 138, 14), R(18, 124, 36, 10))
    # Esfinge.
    pygame.draw.rect(surf, (160, 104, 6), R(4, 100, 24, 20))
    pygame.draw.rect(surf, (176, 120, 8), R(22, 88, 12, 14))
    pygame.draw.rect(surf, (160, 104, 6), R(26, 84, 8, 8))
    pygame.draw.rect(surf, (136, 96, 5), R(24, 92, 4, 8))
    # Pirâmide direita.
    pygame.draw.polygon(surf, (176, 112, 6), [
        (int(30 * w / 48), int(120 * h / 200)),
        (int(42 * w / 48), int(76 * h / 200)),
        (int(54 * w / 48), int(120 * h / 200)),
    ])
    pygame.draw.polygon(surf, (200, 136, 24), [
        (int(32 * w / 48), int(120 * h / 200)),
        (int(42 * w / 48), int(80 * h / 200)),
        (int(52 * w / 48), int(120 * h / 200)),
    ])
    for y in (148, 158, 166):
        rect_alpha((160, 112, 6), 128, 2 + (y % 8), y, 20, 2)
    return surf


# ============================== CANADÁ ==============================

def _canada_esq(w, h):
    """Barra esquerda do tema CANADÁ: abetos com neve, flocos e folha de bordo."""
    surf, R, rect_alpha, poly, _, _ = _bar_canvas(w, h)
    surf.fill((184, 204, 216))
    # Nuvens.
    rect_alpha((216, 228, 236), 230, 0, 10, 36, 14)
    rect_alpha((228, 238, 246), 230, 4, 4, 22, 12)
    rect_alpha((208, 220, 232), 230, 22, 18, 26, 12)
    # Flocos.
    flocos = [(6, 35, 230), (18, 28, 205), (30, 40, 230), (42, 32, 180), (12, 48, 205),
              (38, 52, 230), (24, 58, 180), (4, 60, 205), (44, 65, 230), (16, 70, 153)]
    for x, y, a in flocos:
        rect_alpha((255, 255, 255), a, x, y, 2, 2)
    # Abeto grande esquerda.
    pygame.draw.rect(surf, (90, 48, 16), R(4, 150, 8, 44))
    rect_alpha((255, 255, 255), 153, 3, 148, 10, 4)
    for top_y in (72, 85, 100, 115):
        cor = (26, 90, 24) if top_y in (72, 100) else (34, 106, 30)
        poly(cor, [(8, top_y), (-2, top_y + 48), (18, top_y + 48)])
    rect_alpha((255, 255, 255), 180, -2, 118, 20, 4)
    rect_alpha((255, 255, 255), 153, 0, 130, 16, 3)
    # Abeto médio centro.
    pygame.draw.rect(surf, (90, 48, 16), R(20, 158, 6, 36))
    for top_y in (90, 104, 118, 130):
        cor = (26, 90, 24) if top_y in (90, 118) else (34, 106, 30)
        poly(cor, [(23, top_y), (13, top_y + 40), (33, top_y + 40)])
    rect_alpha((255, 255, 255), 180, 13, 128, 20, 4)
    # Abeto direita.
    pygame.draw.rect(surf, (90, 48, 16), R(36, 155, 7, 40))
    for top_y in (80, 94, 108, 122):
        cor = (26, 90, 24) if top_y in (80, 108) else (34, 106, 30)
        poly(cor, [(39, top_y), (30, top_y + 42), (48, top_y + 42)])
    # Chão de neve.
    pygame.draw.rect(surf, (232, 240, 246), R(0, 188, 48, 12))
    pygame.draw.rect(surf, (220, 232, 240), R(0, 184, 48, 6))
    # Folha de bordo.
    rect_alpha((204, 34, 0), 180, 20, 182, 6, 4)
    rect_alpha((204, 34, 0), 180, 22, 180, 2, 2)
    return surf


def _canada_dir(w, h):
    """Barra direita do tema CANADÁ: abetos cobertos de neve e pegadas."""
    surf, R, rect_alpha, poly, _, _ = _bar_canvas(w, h)
    surf.fill((196, 212, 224))
    rect_alpha((220, 232, 240), 230, 10, 8, 38, 14)
    rect_alpha((232, 240, 248), 230, 6, 2, 24, 12)
    rect_alpha((212, 224, 236), 230, 0, 16, 20, 12)
    for x, y, a in [(10, 32, 230), (22, 42, 205), (36, 30, 230), (4, 50, 180),
                    (46, 44, 205), (14, 62, 230), (40, 58, 180), (28, 68, 205)]:
        rect_alpha((255, 255, 255), a, x, y, 2, 2)
    # Abeto esquerda.
    pygame.draw.rect(surf, (90, 48, 16), R(2, 160, 6, 36))
    for top_y in (95, 108, 122, 134):
        cor = (26, 90, 24) if top_y in (95, 122) else (34, 106, 30)
        poly(cor, [(5, top_y), (-4, top_y + 37), (14, top_y + 37)])
    rect_alpha((255, 255, 255), 180, -4, 130, 18, 4)
    # Abeto central grande.
    pygame.draw.rect(surf, (90, 48, 16), R(19, 148, 8, 48))
    rect_alpha((255, 255, 255), 153, 18, 146, 10, 4)
    for top_y in (68, 82, 97, 112):
        cor = (26, 90, 24) if top_y in (68, 97) else (34, 106, 30)
        poly(cor, [(23, top_y), (10, top_y + 50), (36, top_y + 50)])
    rect_alpha((255, 255, 255), 180, 10, 116, 26, 4)
    # Abeto direita pequeno.
    pygame.draw.rect(surf, (90, 48, 16), R(38, 165, 6, 32))
    for top_y in (108, 120, 132):
        cor = (26, 90, 24) if top_y in (108,) else (34, 106, 30)
        poly(cor, [(41, top_y), (33, top_y + 34), (49, top_y + 34)])
    # Chão.
    pygame.draw.rect(surf, (234, 242, 248), R(0, 186, 48, 14))
    pygame.draw.rect(surf, (224, 234, 244), R(0, 182, 48, 6))
    # Pegadas.
    for x in (8, 14, 20, 26):
        pygame.draw.rect(surf, (200, 216, 232), R(x, 185 + (x % 4), 3, 3))
    return surf


# ============================== BÉLGICA ==============================

def _belgica_esq(w, h):
    """Barra esquerda do tema BÉLGICA: casa com fachada escalonada na chuva."""
    surf, R, rect_alpha, _, _, line_alpha = _bar_canvas(w, h)
    surf.fill((74, 82, 96))
    # Nuvens pesadas.
    rect_alpha((58, 64, 80), 230, -4, 0, 36, 16)
    rect_alpha((66, 72, 88), 230, 0, 6, 48, 18)
    rect_alpha((60, 68, 85), 230, 10, 0, 42, 14)
    # Chuva (linhas diagonais geradas em loop).
    for i in range(28):
        x = (i * 7) % 48
        y = 20 + (i * 11) % 80
        line_alpha((122, 154, 176), 153, x, y, x - 2, y + 14, 1)
    # Fachada escalonada.
    pygame.draw.rect(surf, (139, 74, 40), R(0, 108, 22, 82))
    pygame.draw.rect(surf, (122, 62, 32), R(0, 104, 22, 6))
    pygame.draw.rect(surf, (139, 74, 40), R(2, 98, 18, 6))
    pygame.draw.rect(surf, (122, 62, 32), R(4, 92, 14, 6))
    pygame.draw.rect(surf, (139, 74, 40), R(6, 86, 10, 6))
    pygame.draw.rect(surf, (122, 62, 32), R(8, 80, 6, 6))
    pygame.draw.rect(surf, (139, 74, 40), R(10, 74, 2, 6))
    # Janelas.
    for y in (114, 128, 142):
        rect_alpha((184, 204, 212), 180, 2, y, 6, 8)
        rect_alpha((184, 204, 212), 180, 12, y, 6, 8)
    # Porta.
    pygame.draw.rect(surf, (74, 46, 24), R(6, 162, 10, 28))
    pygame.draw.rect(surf, (58, 32, 16), R(7, 162, 8, 14))
    # Calçada.
    pygame.draw.rect(surf, (58, 58, 68), R(0, 190, 48, 10))
    rect_alpha((90, 106, 122), 128, 4, 192, 8, 3)
    rect_alpha((90, 106, 122), 128, 22, 193, 12, 3)
    return surf


def _belgica_dir(w, h):
    """Barra direita do tema BÉLGICA: campanário e casa belga na chuva."""
    surf, R, rect_alpha, _, _, line_alpha = _bar_canvas(w, h)
    surf.fill((80, 88, 104))
    rect_alpha((64, 72, 88), 230, 0, 2, 40, 14)
    rect_alpha((62, 70, 86), 230, 8, 0, 48, 16)
    # Chuva.
    for i in range(28):
        x = (i * 9 + 3) % 48
        y = 18 + (i * 13) % 80
        line_alpha((122, 154, 176), 153, x, y, x - 2, y + 14, 1)
    # Campanário central.
    pygame.draw.rect(surf, (58, 66, 72), R(18, 60, 12, 110))
    rect_alpha((106, 128, 144), 153, 20, 68, 8, 10)
    rect_alpha((106, 128, 144), 128, 20, 84, 8, 10)
    pygame.draw.polygon(surf, (46, 56, 64), [
        (int(18 * w / 48), int(60 * h / 200)),
        (int(24 * w / 48), int(38 * h / 200)),
        (int(30 * w / 48), int(60 * h / 200)),
    ])
    pygame.draw.rect(surf, (74, 85, 96), R(23, 28, 2, 12))
    # Casa esquerda tijolo.
    pygame.draw.rect(surf, (154, 85, 48), R(0, 118, 18, 72))
    pygame.draw.rect(surf, (138, 72, 37), R(0, 114, 18, 6))
    pygame.draw.rect(surf, (154, 85, 48), R(2, 108, 14, 6))
    pygame.draw.rect(surf, (138, 72, 37), R(4, 102, 10, 6))
    pygame.draw.rect(surf, (154, 85, 48), R(6, 96, 6, 6))
    for y in (122, 136, 150):
        rect_alpha((184, 204, 212), 180, 2, y, 5, 7)
        rect_alpha((184, 204, 212), 180, 10, y, 5, 7)
    pygame.draw.rect(surf, (42, 26, 14), R(4, 166, 10, 24))
    # Casa direita verde.
    pygame.draw.rect(surf, (90, 104, 80), R(30, 128, 18, 62))
    pygame.draw.polygon(surf, (72, 86, 64), [
        (int(30 * w / 48), int(128 * h / 200)),
        (int(39 * w / 48), int(106 * h / 200)),
        (int(48 * w / 48), int(128 * h / 200)),
    ])
    for y in (134, 148, 162):
        rect_alpha((184, 204, 212), 180, 32, y, 5, 7)
        rect_alpha((184, 204, 212), 180, 40, y, 5, 7)
    pygame.draw.rect(surf, (42, 30, 16), R(36, 172, 10, 18))
    # Calçada.
    pygame.draw.rect(surf, (56, 56, 68), R(0, 190, 48, 10))
    rect_alpha((90, 106, 122), 128, 2, 193, 10, 3)
    rect_alpha((90, 106, 122), 128, 20, 192, 8, 3)
    rect_alpha((90, 106, 122), 128, 36, 193, 10, 3)
    return surf


# ============================== MILÃO ==============================

def _milao_esq(w, h):
    """Barra esquerda do tema MILÃO: Duomo gótico e prédios laterais."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    surf.fill((90, 142, 192))
    rect_alpha((255, 255, 255), 192, 2, 22, 28, 8)
    rect_alpha((255, 255, 255), 192, 6, 18, 16, 8)
    # Corpo do Duomo.
    pygame.draw.rect(surf, (232, 220, 200), R(8, 110, 32, 80))
    for x in (12, 18, 26, 32):
        rect_alpha((208, 196, 176), 153, x, 110, 2, 80)
    pygame.draw.rect(surf, (122, 106, 88), R(19, 155, 10, 35))
    pygame.draw.rect(surf, (106, 90, 72), R(20, 155, 8, 20))
    # Janelas ogivais laterais.
    for y, a in [(125, 205), (142, 180)]:
        rect_alpha((138, 170, 192), a, 10, y, 6, 12)
        rect_alpha((138, 170, 192), a, 32, y, 6, 12)
    # Torre central (guglia).
    pygame.draw.rect(surf, (221, 208, 188), R(20, 72, 8, 40))
    pygame.draw.rect(surf, (204, 192, 170), R(22, 60, 4, 16))
    pygame.draw.rect(surf, (187, 176, 160), R(23, 50, 2, 14))
    pygame.draw.rect(surf, (200, 168, 48), R(23, 40, 2, 12))
    pygame.draw.rect(surf, (240, 200, 64), R(24, 38, 1, 4))
    # Torres laterais.
    for tx in (10, 32):
        pygame.draw.rect(surf, (221, 208, 188), R(tx, 88, 6, 24))
        pygame.draw.rect(surf, (204, 192, 170), R(tx + 1, 82, 4, 8))
        pygame.draw.rect(surf, (187, 176, 160), R(tx + 2, 76, 2, 8))
        pygame.draw.rect(surf, (200, 168, 48), R(tx + 2, 70, 2, 8))
    pygame.draw.rect(surf, (200, 184, 152), R(0, 188, 48, 12))
    pygame.draw.rect(surf, (184, 168, 136), R(0, 188, 48, 2))
    for x in (4, 16, 28, 40):
        rect_alpha((184, 168, 136), 102, x, 192, 6, 4)
    pygame.draw.rect(surf, (200, 184, 160), R(0, 130, 8, 60))
    pygame.draw.rect(surf, (200, 184, 160), R(40, 135, 8, 55))
    return surf


def _milao_dir(w, h):
    """Barra direita do tema MILÃO: prédios racionalistas e vespa."""
    surf, R, rect_alpha, _, _, _ = _bar_canvas(w, h)
    surf.fill((104, 152, 200))
    rect_alpha((255, 255, 255), 180, 18, 18, 28, 8)
    rect_alpha((255, 255, 255), 180, 22, 12, 18, 8)
    # Prédio alto esquerda.
    pygame.draw.rect(surf, (176, 168, 152), R(0, 50, 18, 140))
    for fila_y in (56, 68, 80, 92, 104, 116, 128):
        for col_x in (2, 10):
            alpha = 180 + (fila_y * col_x) % 70
            rect_alpha((122, 170, 200), min(255, alpha), col_x, fila_y, 5, 6)
    # Prédio clássico centro.
    pygame.draw.rect(surf, (212, 200, 176), R(16, 80, 20, 110))
    pygame.draw.rect(surf, (192, 180, 160), R(14, 78, 24, 4))
    for fila_y in (88, 102, 116, 130, 144):
        for col_x in (20, 28):
            rect_alpha((138, 170, 192), 200, col_x, fila_y, 5, 7)
    pygame.draw.rect(surf, (138, 122, 104), R(22, 163, 8, 27))
    pygame.draw.rect(surf, (122, 106, 88), R(23, 163, 6, 14))
    # Prédio direita moderno.
    pygame.draw.rect(surf, (168, 176, 184), R(34, 65, 14, 125))
    for fila_y in (72, 84, 96, 108, 120, 132):
        for col_x in (36, 42):
            rect_alpha((200, 224, 240), 200, col_x, fila_y, 4, 6)
    # Calçada.
    pygame.draw.rect(surf, (192, 176, 160), R(0, 188, 48, 12))
    pygame.draw.rect(surf, (176, 160, 144), R(0, 188, 48, 2))
    for x in (3, 12, 22, 32, 42):
        rect_alpha((176, 160, 144), 102, x, 192, 5, 4)
    # Vespa vermelha.
    pygame.draw.rect(surf, (204, 34, 0), R(6, 180, 10, 6))
    pygame.draw.rect(surf, (51, 51, 51), R(4, 183, 4, 4))
    pygame.draw.rect(surf, (51, 51, 51), R(14, 183, 4, 4))
    pygame.draw.rect(surf, (170, 26, 0), R(8, 178, 4, 4))
    return surf


# ============================== Registry & dispatcher ==============================

_LATERAL_BARRAS = {
    "amazonia": (_amazonia_esq, _amazonia_dir),
    "londres": (_londres_esq, _londres_dir),
    "havai": (_havai_esq, _havai_dir),
    "suica": (_suica_esq, _suica_dir),
    "franca": (_franca_esq, _franca_dir),
    "africa": (_africa_esq, _africa_dir),
    "egito": (_egito_esq, _egito_dir),
    "canada": (_canada_esq, _canada_dir),
    "belgica": (_belgica_esq, _belgica_dir),
    "milao": (_milao_esq, _milao_dir),
}


def criar_lateral(tema, lado, width, height):
    """Cria a Surface da barra lateral do tema indicado, escalada para (width, height).

    Args:
        tema: Identificador do tema da fase ("amazonia", "londres", "havai"...).
        lado: "esq" para a barra esquerda, "dir" para a direita.
        width: Largura da barra em pixels.
        height: Altura da barra em pixels.

    Returns:
        pygame.Surface opaca com o cenário lateral pixel-art.
    """
    fns = _LATERAL_BARRAS.get(tema, _LATERAL_BARRAS["amazonia"])
    fn = fns[0] if lado == "esq" else fns[1]
    return fn(width, height)
