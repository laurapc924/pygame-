"""Funções que criam sprites em pixel art usando pygame.draw."""

import pygame


def criar_cogumelo(size=30):
    """Cria um cogumelo estilo Mario: chapéu vermelho com bolinhas brancas e caule creme."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)

    cx = size // 2
    caule_w = size * 14 // 30
    caule_h = size * 11 // 30
    caule_x = cx - caule_w // 2
    caule_y = size - caule_h

    # Caule creme
    pygame.draw.rect(surf, (240, 230, 200), (caule_x, caule_y, caule_w, caule_h))
    # Contorno do caule
    pygame.draw.rect(surf, (40, 20, 10), (caule_x, caule_y, caule_w, caule_h), 1)

    # Chapéu: elipse vermelha cobrindo os dois terços superiores
    chapeu_h = size * 22 // 30
    chapeu_rect = pygame.Rect(0, 0, size, chapeu_h + size // 6)
    pygame.draw.ellipse(surf, (220, 50, 50), chapeu_rect)
    # Contorno do chapéu
    pygame.draw.ellipse(surf, (40, 20, 10), chapeu_rect, 1)

    # 3 bolinhas brancas no chapéu
    dot_r = max(2, size * 3 // 30)
    pygame.draw.circle(surf, (255, 255, 255), (cx, size * 6 // 30), dot_r)
    pygame.draw.circle(surf, (255, 255, 255), (size * 7 // 30, size * 13 // 30), dot_r)
    pygame.draw.circle(surf, (255, 255, 255), (size * 23 // 30, size * 13 // 30), dot_r)

    return surf


def criar_trevo(size=30):
    """Cria um trevo de 4 folhas: quatro elipses verdes em cruz com caule pequeno."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)

    cx = size // 2
    cy = size // 2
    folha_w = size * 13 // 30
    folha_h = size * 13 // 30
    cor_folha = (50, 150, 70)
    cor_borda = (30, 100, 45)
    cor_nervura = (80, 190, 100)

    offsets = [
        (cx - folha_w // 2, cy - folha_h),          # cima
        (cx - folha_w // 2, cy),                     # baixo
        (cx - folha_w, cy - folha_h // 2),           # esquerda
        (cx, cy - folha_h // 2),                     # direita
    ]

    for ox, oy in offsets:
        r = pygame.Rect(ox, oy, folha_w, folha_h)
        pygame.draw.ellipse(surf, cor_folha, r)
        pygame.draw.ellipse(surf, cor_borda, r, 1)

    # Nervura central em cada folha (linha mais clara)
    pygame.draw.line(surf, cor_nervura, (cx, cy - folha_h + 2), (cx, cy - 2), 1)
    pygame.draw.line(surf, cor_nervura, (cx, cy + 2), (cx, cy + folha_h - 2), 1)
    pygame.draw.line(surf, cor_nervura, (cx - folha_w + 2, cy), (cx - 2, cy), 1)
    pygame.draw.line(surf, cor_nervura, (cx + 2, cy), (cx + folha_w - 2, cy), 1)

    # Caule verde pequeno centralizado embaixo
    caule_w = max(2, size * 4 // 30)
    caule_h = size * 5 // 30
    caule_x = cx - caule_w // 2
    pygame.draw.rect(surf, (40, 120, 60), (caule_x, size - caule_h, caule_w, caule_h))

    return surf
