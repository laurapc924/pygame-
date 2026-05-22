"""Funções que criam sprites em pixel art usando pygame.draw."""

import random

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


def criar_arvore(width, height):
    """Cria a Surface de uma árvore (tronco marrom + copa verde).

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface com fundo transparente contendo a árvore.
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Tronco: retângulo marrom centralizado na base.
    tronco_w = max(6, width // 4)
    tronco_h = max(10, height // 3)
    tronco_x = (width - tronco_w) // 2
    tronco_y = height - tronco_h
    pygame.draw.rect(surface, (101, 67, 33), (tronco_x, tronco_y, tronco_w, tronco_h))

    # Copa: círculos verdes sobrepostos preenchendo a metade superior.
    copa_r = max(8, width // 3)
    centro_x = width // 2
    base_y = height - tronco_h
    pygame.draw.circle(surface, (34, 110, 34), (centro_x, base_y - copa_r), copa_r)
    pygame.draw.circle(
        surface, (40, 130, 40), (centro_x - copa_r // 2, base_y - 2 * copa_r), copa_r
    )
    pygame.draw.circle(
        surface, (40, 130, 40), (centro_x + copa_r // 2, base_y - 2 * copa_r), copa_r
    )

    return surface


def criar_grama_textura(width, height):
    """Cria uma textura de grama: verde escuro com pontinhos e tufos claros.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface opaca com a textura de grama.
    """
    surface = pygame.Surface((width, height))
    surface.fill((30, 80, 30))

    # Pontinhos verde claro espalhados aleatoriamente.
    num_pontos = (width * height) // 30
    for _ in range(num_pontos):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        surface.set_at((x, y), (50, 130, 50))

    # Tufos de grama: linhas verticais curtas verde claro.
    num_tufos = (width * height) // 1500
    for _ in range(num_tufos):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 5)
        altura_tufo = random.randint(3, 4)
        pygame.draw.line(surface, (60, 150, 60), (x, y), (x, y + altura_tufo))

    return surface


def criar_asfalto_textura(width, height):
    """Cria uma textura de asfalto: cinza com manchas escuras e pixels claros.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface opaca com a textura de asfalto.
    """
    surface = pygame.Surface((width, height))
    surface.fill((80, 80, 85))

    # Manchas mais escuras pra dar textura ao asfalto.
    num_manchas = (width * height) // 400
    for _ in range(num_manchas):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        raio = random.randint(2, 5)
        pygame.draw.circle(surface, (60, 60, 65), (x, y), raio)

    # Pixels mais claros: aspecto de asfalto desgastado.
    num_claros = (width * height) // 50
    for _ in range(num_claros):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        surface.set_at((x, y), (100, 100, 105))

    return surface
