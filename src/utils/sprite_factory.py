"""Funções que criam sprites em pixel art usando pygame.draw."""

import math
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


def desenhar_gradiente_vertical(surface, cor_topo, cor_baixo):
    """Cria um gradiente vertical na surface, do topo para a base.

    Para cada linha y, interpola linearmente entre cor_topo (y=0) e
    cor_baixo (y=height) e desenha uma linha horizontal nessa cor.

    Args:
        surface: pygame.Surface preenchida in-place.
        cor_topo: Cor (R, G, B) usada no topo.
        cor_baixo: Cor (R, G, B) usada na base.
    """
    width = surface.get_width()
    height = surface.get_height()

    def interpolar(inicio, fim, fracao):
        """Interpola um canal de cor entre inicio e fim pela fração dada."""
        return int(inicio + (fim - inicio) * fracao)

    for y in range(height):
        fracao = y / height
        cor = (
            interpolar(cor_topo[0], cor_baixo[0], fracao),
            interpolar(cor_topo[1], cor_baixo[1], fracao),
            interpolar(cor_topo[2], cor_baixo[2], fracao),
        )
        pygame.draw.line(surface, cor, (0, y), (width, y))


def desenhar_painel(
    surface, x, y, largura, altura, cor=(45, 100, 55, 200), borda_cor=(255, 215, 0)
):
    """Desenha um painel semi-transparente arredondado com borda.

    Args:
        surface: Surface destino.
        x: Coordenada X do canto superior esquerdo do painel.
        y: Coordenada Y do canto superior esquerdo do painel.
        largura: Largura do painel em pixels.
        altura: Altura do painel em pixels.
        cor: Cor RGBA de preenchimento (o 4º canal controla a transparência).
        borda_cor: Cor RGB da borda.
    """
    painel = pygame.Surface((largura, altura), pygame.SRCALPHA)
    pygame.draw.rect(painel, cor, (0, 0, largura, altura), border_radius=15)
    pygame.draw.rect(
        painel, borda_cor, (0, 0, largura, altura), width=3, border_radius=15
    )
    surface.blit(painel, (x, y))


def desenhar_titulo_estilizado(
    surface, texto, font, x, y, cor_principal=(255, 215, 0), cor_sombra=(0, 0, 0)
):
    """Desenha um texto centralizado em (x, y) com sombra projetada (efeito 3D).

    A sombra é desenhada 3px deslocada e o texto principal por cima.

    Args:
        surface: Surface destino.
        texto: String a renderizar.
        font: pygame.font.Font usada na renderização.
        x: Coordenada X do centro do texto.
        y: Coordenada Y do centro do texto.
        cor_principal: Cor RGB do texto principal.
        cor_sombra: Cor RGB da sombra.
    """
    sombra = font.render(texto, True, cor_sombra)
    surface.blit(sombra, sombra.get_rect(center=(x + 3, y + 3)))

    principal = font.render(texto, True, cor_principal)
    surface.blit(principal, principal.get_rect(center=(x, y)))


def desenhar_estrela(surface, cx, cy, raio, cor):
    """Desenha uma estrela de 5 pontas preenchida, centrada em (cx, cy).

    Args:
        surface: Surface destino.
        cx: Coordenada X do centro da estrela.
        cy: Coordenada Y do centro da estrela.
        raio: Raio externo (das pontas) da estrela.
        cor: Cor RGB de preenchimento.
    """
    pontos = []
    for i in range(10):
        angulo = math.pi / 2 + i * math.pi / 5
        r = raio if i % 2 == 0 else raio * 0.45
        pontos.append((cx + r * math.cos(angulo), cy - r * math.sin(angulo)))
    pygame.draw.polygon(surface, cor, pontos)


def criar_raposa_estatica(width=80, height=80, olhos_fechados=False):
    """Cria a Surface de uma raposa em perfil, para usar como decoração.

    Desenha uma raposa sentada vista de lado (focinho voltado à direita),
    com cauda peluda de ponta branca, orelhas pontudas e patas escuras.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.
        olhos_fechados: Se True, desenha o olho fechado (raposa triste).

    Returns:
        pygame.Surface com fundo transparente contendo a raposa.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    laranja = (203, 106, 42)
    laranja_esc = (158, 78, 30)
    branco = (244, 240, 232)
    preto = (38, 32, 30)
    w, h = width, height

    def pt(fx, fy):
        """Converte coordenadas fracionárias (0 a 1) em pixels da surface."""
        return (int(w * fx), int(h * fy))

    # Cauda peluda atrás do corpo, drapeada para baixo, com a ponta branca.
    for fx, fy, fr in [
        (0.23, 0.44, 0.15),
        (0.15, 0.58, 0.17),
        (0.13, 0.74, 0.17),
        (0.19, 0.89, 0.15),
    ]:
        pygame.draw.circle(surf, laranja, pt(fx, fy), int(w * fr))
    pygame.draw.circle(surf, branco, pt(0.20, 0.93), int(w * 0.115))

    # Corpo e ancas (raposa sentada).
    corpo = pygame.Rect(0, 0, int(w * 0.54), int(h * 0.54))
    corpo.center = pt(0.45, 0.63)
    pygame.draw.ellipse(surf, laranja, corpo)

    # Pata dianteira esguia até o chão e patas escuras (as "meias" da raposa).
    perna = pygame.Rect(int(w * 0.54), int(h * 0.55), int(w * 0.12), int(h * 0.38))
    pygame.draw.rect(surf, laranja, perna, border_radius=int(w * 0.05))
    pygame.draw.ellipse(
        surf, preto, (int(w * 0.31), int(h * 0.85), int(w * 0.21), int(h * 0.12))
    )
    pygame.draw.ellipse(
        surf, preto, (int(w * 0.52), int(h * 0.86), int(w * 0.16), int(h * 0.11))
    )

    # Peito/pescoço ligando o corpo à cabeça, com babado branco.
    pygame.draw.polygon(
        surf, laranja, [pt(0.48, 0.40), pt(0.74, 0.34), pt(0.71, 0.74), pt(0.45, 0.66)]
    )
    pygame.draw.polygon(
        surf, branco, [pt(0.58, 0.45), pt(0.69, 0.43), pt(0.66, 0.74), pt(0.57, 0.70)]
    )

    # Cabeça.
    cabeca = pt(0.66, 0.30)
    cabeca_r = int(w * 0.165)
    pygame.draw.circle(surf, laranja, cabeca, cabeca_r)

    # Orelhas pontudas: a de trás mais escura, a da frente com interior preto.
    pygame.draw.polygon(
        surf, laranja_esc, [pt(0.71, 0.21), pt(0.82, 0.02), pt(0.84, 0.25)]
    )
    pygame.draw.polygon(surf, laranja, [pt(0.52, 0.25), pt(0.57, 0.00), pt(0.71, 0.19)])
    pygame.draw.polygon(
        surf, preto, [pt(0.565, 0.215), pt(0.585, 0.07), pt(0.665, 0.175)]
    )

    # Focinho pontudo voltado à direita, com a mandíbula inferior branca.
    pygame.draw.polygon(surf, laranja, [pt(0.70, 0.22), pt(0.72, 0.43), pt(0.99, 0.34)])
    pygame.draw.polygon(
        surf, branco, [pt(0.72, 0.37), pt(0.74, 0.46), pt(0.99, 0.355)]
    )

    # Olho.
    olho = pt(0.69, 0.28)
    if olhos_fechados:
        raio = max(2, int(w * 0.045))
        pygame.draw.line(
            surf,
            preto,
            (olho[0] - raio, olho[1]),
            (olho[0] + raio, olho[1]),
            max(2, int(w * 0.025)),
        )
    else:
        pygame.draw.circle(surf, preto, olho, max(2, int(w * 0.038)))

    # Nariz preto na ponta do focinho.
    pygame.draw.circle(surf, preto, pt(0.97, 0.34), max(2, int(w * 0.042)))

    return surf


def _clarear(cor, fator):
    """Clareia uma cor RGB misturando-a com branco pelo fator dado (0 a 1)."""
    return tuple(min(255, int(c + (255 - c) * fator)) for c in cor[:3])


def _escurecer(cor, fator):
    """Escurece uma cor RGB multiplicando cada canal por (1 - fator)."""
    return tuple(max(0, int(c * (1 - fator))) for c in cor[:3])


def criar_grama_textura_colorida(width, height, cor_base):
    """Cria uma textura de grama na cor dada, com pontinhos e tufos mais claros.

    Igual a criar_grama_textura, mas usando cor_base como base em vez de uma
    cor fixa; pontinhos e tufos são versões clareadas de cor_base.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.
        cor_base: Cor (R, G, B) de base da grama.

    Returns:
        pygame.Surface opaca com a textura de grama.
    """
    surface = pygame.Surface((width, height))
    surface.fill(cor_base)
    cor_pontos = _clarear(cor_base, 0.3)
    cor_tufos = _clarear(cor_base, 0.5)

    num_pontos = (width * height) // 30
    for _ in range(num_pontos):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        surface.set_at((x, y), cor_pontos)

    num_tufos = (width * height) // 1500
    for _ in range(num_tufos):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 5)
        altura_tufo = random.randint(3, 4)
        pygame.draw.line(surface, cor_tufos, (x, y), (x, y + altura_tufo))

    return surface


def criar_asfalto_textura_colorida(width, height, cor_base):
    """Cria uma textura de asfalto na cor dada, com manchas escuras e pixels claros.

    Igual a criar_asfalto_textura, mas usando cor_base; as manchas são versões
    escurecidas e os pixels desgastados são versões clareadas de cor_base.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.
        cor_base: Cor (R, G, B) de base do asfalto.

    Returns:
        pygame.Surface opaca com a textura de asfalto.
    """
    surface = pygame.Surface((width, height))
    surface.fill(cor_base)
    cor_manchas = _escurecer(cor_base, 0.2)
    cor_claros = _clarear(cor_base, 0.25)

    num_manchas = (width * height) // 400
    for _ in range(num_manchas):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        raio = random.randint(2, 5)
        pygame.draw.circle(surface, cor_manchas, (x, y), raio)

    num_claros = (width * height) // 50
    for _ in range(num_claros):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        surface.set_at((x, y), cor_claros)

    return surface


def criar_poste(width, height):
    """Cria a Surface de um poste de luz (mastro cinza + luminária acesa no topo).

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface com fundo transparente contendo o poste.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    cinza = (95, 95, 105)
    cinza_escuro = (55, 55, 65)
    luz = (255, 235, 150)
    cx = width // 2
    topo_y = height // 5

    # Halo de luz ao redor da luminária.
    halo = pygame.Surface((width, width), pygame.SRCALPHA)
    pygame.draw.circle(halo, (255, 235, 150, 80), (width // 2, width // 2), width // 2)
    surf.blit(halo, (cx - width // 2, topo_y - width // 2))

    # Mastro vertical e base.
    mastro_w = max(5, width // 9)
    pygame.draw.rect(
        surf, cinza, (cx - mastro_w // 2, topo_y, mastro_w, height - topo_y - 4)
    )
    pygame.draw.rect(surf, cinza_escuro, (cx - mastro_w, height - 8, mastro_w * 2, 8))

    # Luminária no topo.
    pygame.draw.ellipse(surf, cinza_escuro, (cx - 11, topo_y - 9, 22, 14))
    pygame.draw.circle(surf, luz, (cx, topo_y + 2), 7)

    return surf


def criar_coqueiro(width, height):
    """Cria a Surface de um coqueiro (tronco marrom + folhas de palmeira + cocos).

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface com fundo transparente contendo o coqueiro.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    marrom = (140, 100, 60)
    verde = (40, 140, 60)
    verde_claro = (65, 175, 85)
    cx = width // 2
    topo_y = int(height * 0.34)

    # Tronco em segmentos levemente ondulados.
    seg_h = (height - topo_y) // 5
    for i in range(5):
        desloc = int(4 * math.sin(i))
        pygame.draw.rect(
            surf, marrom, (cx - 5 + desloc, topo_y + i * seg_h, 10, seg_h + 1)
        )

    # Folhas de palmeira: triângulos largos radiando e caindo do topo.
    dirs = [
        (-1.0, -0.15),
        (-0.75, 0.35),
        (-0.35, 0.55),
        (0.35, 0.55),
        (0.75, 0.35),
        (1.0, -0.15),
    ]
    comprimento = width * 0.62
    for j, (dx, dy) in enumerate(dirs):
        norm = math.hypot(dx, dy)
        ux, uy = dx / norm, dy / norm
        tip = (cx + ux * comprimento, topo_y + uy * comprimento)
        # Base da folha perpendicular à sua direção.
        px, py = -uy, ux
        b1 = (cx + px * 7, topo_y + py * 7)
        b2 = (cx - px * 7, topo_y - py * 7)
        cor = verde if j % 2 == 0 else verde_claro
        pygame.draw.polygon(surf, cor, [b1, b2, tip])

    # Cocos sob as folhas.
    pygame.draw.circle(surf, marrom, (cx - 5, topo_y + 5), 4)
    pygame.draw.circle(surf, marrom, (cx + 5, topo_y + 5), 4)

    return surf


def criar_pinheiro(width, height):
    """Cria a Surface de um pinheiro nevado (camadas triangulares verdes com neve).

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface com fundo transparente contendo o pinheiro.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    marrom = (90, 60, 40)
    verde = (30, 95, 58)
    neve = (240, 245, 250)
    cx = width // 2

    tronco_h = height // 7
    pygame.draw.rect(surf, marrom, (cx - 5, height - tronco_h, 10, tronco_h))
    area_h = height - tronco_h

    # 3 camadas triangulares: i=0 é a base (larga e baixa).
    camadas = []
    for i in range(3):
        base_y = area_h * (1 - i * 0.30)
        apex_y = area_h * (0.45 - i * 0.225)
        meia_largura = (width // 2) * (1 - i * 0.18)
        camadas.append((apex_y, base_y, meia_largura))
        pygame.draw.polygon(
            surf,
            verde,
            [
                (cx, apex_y),
                (cx - meia_largura, base_y),
                (cx + meia_largura, base_y),
            ],
        )

    # Capas de neve no topo de cada camada (desenhadas por cima do verde).
    for apex_y, base_y, meia_largura in camadas:
        neve_base = apex_y + (base_y - apex_y) * 0.42
        pygame.draw.polygon(
            surf,
            neve,
            [
                (cx, apex_y),
                (cx - meia_largura * 0.5, neve_base),
                (cx + meia_largura * 0.5, neve_base),
            ],
        )

    return surf


def criar_pedra(width, height):
    """Cria a Surface de uma pedra/rocha cinzenta arredondada.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface com fundo transparente contendo a rocha.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    cinza = (122, 122, 130)
    cinza_claro = (162, 162, 170)
    cinza_escuro = (85, 85, 95)

    rocha_h = int(height * 0.55)
    # Rocha principal ocupando a base da surface.
    pygame.draw.ellipse(
        surf, cinza, (width // 8, height - rocha_h, width - width // 4, rocha_h)
    )
    # Pedra menor ao lado, dando volume.
    pygame.draw.ellipse(
        surf, cinza_escuro, (0, height - rocha_h // 2, width // 2, rocha_h // 2)
    )
    # Brilho no topo da rocha principal.
    pygame.draw.ellipse(
        surf,
        cinza_claro,
        (width // 3, height - rocha_h + 4, width // 3, rocha_h // 3),
    )

    return surf


def criar_cerca(width, height):
    """Cria a Surface de um trecho de cerca de madeira (postes e travessas).

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface com fundo transparente contendo a cerca.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    madeira = (150, 100, 55)
    madeira_escura = (110, 70, 38)
    topo = int(height * 0.38)
    poste_w = max(6, width // 7)

    # Dois postes verticais.
    for px in (int(width * 0.18), int(width * 0.82) - poste_w):
        pygame.draw.rect(surf, madeira, (px, topo, poste_w, height - topo))
        pygame.draw.rect(surf, madeira_escura, (px, topo, poste_w, height - topo), 1)

    # Duas travessas horizontais.
    trav_h = max(5, height // 12)
    for ty in (topo + (height - topo) // 4, topo + (height - topo) * 3 // 5):
        pygame.draw.rect(surf, madeira, (4, ty, width - 8, trav_h))
        pygame.draw.rect(surf, madeira_escura, (4, ty, width - 8, trav_h), 1)

    return surf


def criar_lua(raio):
    """Cria a Surface de uma lua cheia pálida com um halo suave.

    Args:
        raio: Raio do disco da lua em pixels.

    Returns:
        pygame.Surface transparente contendo a lua e seu halo.
    """
    tam = int(raio * 3.4)
    centro = tam // 2
    surf = pygame.Surface((tam, tam), pygame.SRCALPHA)
    # Halo difuso ao redor da lua.
    pygame.draw.circle(surf, (235, 235, 200, 45), (centro, centro), int(raio * 1.6))
    # Disco da lua.
    pygame.draw.circle(surf, (240, 240, 212), (centro, centro), raio)
    # Crateras.
    cratera = (216, 216, 182)
    pygame.draw.circle(surf, cratera, (centro + raio // 3, centro - raio // 4), raio // 5)
    pygame.draw.circle(surf, cratera, (centro - raio // 3, centro + raio // 4), raio // 6)
    pygame.draw.circle(surf, cratera, (centro + raio // 5, centro + raio // 2), raio // 8)
    return surf


def desenhar_gradiente_multicolor(surface, stops):
    """Gradiente vertical com múltiplos pontos de cor (color stops).

    Args:
        surface: pygame.Surface preenchida in-place.
        stops: Lista de tuplas (t, (r, g, b)) ordenada por t crescente,
               onde t=0.0 é o topo e t=1.0 é a base.
    """
    w = surface.get_width()
    h = surface.get_height()
    for y in range(h):
        t = y / h
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                frac = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
                cor = tuple(int(c0[j] + (c1[j] - c0[j]) * frac) for j in range(3))
                pygame.draw.line(surface, cor, (0, y), (w, y))
                break


def criar_arvore_silhueta(width, height, cor=(15, 22, 18)):
    """Cria uma árvore como silhueta sólida, para planos de fundo.

    Args:
        width: Largura da Surface.
        height: Altura da Surface.
        cor: Cor RGB da silhueta.

    Returns:
        pygame.Surface com fundo transparente contendo a silhueta.
    """
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    tronco_w = max(4, width // 5)
    tronco_h = max(8, height // 4)
    tronco_x = (width - tronco_w) // 2
    tronco_y = height - tronco_h
    pygame.draw.rect(surface, cor, (tronco_x, tronco_y, tronco_w, tronco_h))
    copa_r = max(8, width // 3)
    base_y = height - tronco_h
    cx = width // 2
    pygame.draw.circle(surface, cor, (cx, base_y - copa_r), copa_r)
    pygame.draw.circle(surface, cor, (cx - copa_r // 2, base_y - 2 * copa_r), copa_r)
    pygame.draw.circle(surface, cor, (cx + copa_r // 2, base_y - 2 * copa_r), copa_r)
    return surface


def desenhar_titulo_glow(surface, texto, font, x, y, cor_principal, cor_glow, passos=4):
    """Texto centralizado com efeito de brilho (glow) suave ao redor.

    Args:
        surface: Surface destino.
        texto: String a renderizar.
        font: pygame.font.Font usada na renderização.
        x: Coordenada X do centro do texto.
        y: Coordenada Y do centro do texto.
        cor_principal: Cor RGB do texto em destaque.
        cor_glow: Cor RGB do halo de brilho.
        passos: Intensidade do glow (4 = suave, 8 = intenso).
    """
    glow_surf = font.render(texto, True, cor_glow)
    for raio in range(passos, 0, -1):
        alpha = int(80 * (raio / passos) ** 1.8)
        g = glow_surf.copy()
        g.set_alpha(alpha)
        for dx, dy in [
            (-raio, 0), (raio, 0), (0, -raio), (0, raio),
            (-raio, -raio), (raio, -raio), (-raio, raio), (raio, raio),
        ]:
            surface.blit(g, g.get_rect(center=(x + dx, y + dy)))
    sombra = font.render(texto, True, (0, 0, 0))
    surface.blit(sombra, sombra.get_rect(center=(x + 3, y + 3)))
    principal = font.render(texto, True, cor_principal)
    surface.blit(principal, principal.get_rect(center=(x, y)))


def criar_background_menu_cidade(width, height):
    """Cria o background pixel-art do menu: cidade de dia com céu, prédios, rua e árvores.

    Reproduz a cena de assets/img/menu_bg.svg usando pygame.draw, escalada
    proporcionalmente do design original 1280x720 para o tamanho pedido.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface opaca contendo o cenário do menu.
    """
    surf = pygame.Surface((width, height))
    sx = width / 1280.0
    sy = height / 720.0

    def R(x, y, w, h):
        """Retorna um pygame.Rect escalado das coordenadas de design (1280x720)."""
        return pygame.Rect(int(x * sx), int(y * sy), max(1, int(w * sx)), max(1, int(h * sy)))

    def rect_alpha(cor, alpha, x, y, w, h):
        """Desenha um retângulo semi-transparente no destino."""
        r = R(x, y, w, h)
        s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        s.fill((*cor, alpha))
        surf.blit(s, r.topleft)

    # Céu: gradiente azul de 3 paradas (topo claro -> turquesa -> mais claro).
    azul_topo = (74, 184, 240)
    azul_meio = (125, 212, 248)
    azul_baixo = (168, 230, 255)
    for j in range(height):
        f = j / max(1, height - 1)
        if f < 0.6:
            t = f / 0.6
            cor = tuple(int(azul_topo[k] + (azul_meio[k] - azul_topo[k]) * t) for k in range(3))
        else:
            t = (f - 0.6) / 0.4
            cor = tuple(int(azul_meio[k] + (azul_baixo[k] - azul_meio[k]) * t) for k in range(3))
        pygame.draw.line(surf, cor, (0, j), (width, j))

    # Sol no canto superior direito.
    pygame.draw.rect(surf, (255, 224, 51), R(1060, 55, 56, 56))
    rect_alpha((255, 241, 118), 128, 1070, 63, 36, 20)
    for rx, ry, rw, rh in [(1084, 38, 8, 14), (1084, 114, 8, 14), (1040, 78, 14, 8), (1118, 78, 14, 8)]:
        rect_alpha((255, 224, 51), 180, rx, ry, rw, rh)
    for rx, ry in [(1046, 47), (1116, 47), (1046, 110), (1116, 110)]:
        rect_alpha((255, 224, 51), 128, rx, ry, 10, 10)

    # Nuvens pixel-art (clusters de retângulos brancos translúcidos).
    nuvens = [
        [(80, 60, 100, 30), (60, 72, 140, 28), (90, 50, 60, 24)],
        [(400, 40, 80, 26), (385, 50, 110, 24)],
        [(800, 55, 120, 30), (780, 65, 160, 26), (820, 46, 70, 22)],
        [(1100, 45, 90, 26), (1085, 55, 120, 24)],
    ]
    for cluster in nuvens:
        for cx, cy, cw, ch in cluster:
            rect_alpha((255, 255, 255), 225, cx, cy, cw, ch)

    # Prédios da cidade no horizonte (esquerda e direita).
    janela_cor = (126, 207, 245)
    predios = [
        ((176, 190, 197), 0, 240, 80, 260),
        ((141, 158, 170), 70, 160, 60, 340),
        ((160, 176, 188), 120, 300, 70, 200),
        ((154, 172, 184), 1060, 200, 90, 300),
        ((176, 190, 197), 1150, 180, 110, 320),
    ]
    for cor, px, py, pw, ph in predios:
        pygame.draw.rect(surf, cor, R(px, py, pw, ph))
    # Antena do prédio alto.
    pygame.draw.rect(surf, (96, 125, 139), R(97, 150, 4, 14))
    pygame.draw.rect(surf, (96, 125, 139), R(93, 154, 12, 2))
    # Janelas (grades regulares em cada prédio).
    janelas = [
        (10, 260, 320, [10, 30], 12, 8, 20),
        (78, 175, 250, [0, 18, 36], 10, 8, 20),
        (130, 315, 350, [0, 22], 14, 10, 20),
        (1070, 215, 270, [0, 20, 42], 12, 9, 20),
        (1160, 195, 250, [0, 22, 44], 14, 10, 21),
    ]
    for bx, y_ini, y_fim, colunas, jw, jh, passo in janelas:
        for y in range(y_ini, y_fim, passo):
            for col in colunas:
                rect_alpha(janela_cor, 200, bx + col, y, jw, jh)

    # Grama (faixa verde com um destaque mais claro em cima).
    pygame.draw.rect(surf, (58, 138, 34), R(0, 500, 1280, 30))
    pygame.draw.rect(surf, (74, 170, 42), R(0, 500, 1280, 12))

    # Rua em 3 faixas com tons de cinza.
    pygame.draw.rect(surf, (85, 85, 102), R(0, 530, 1280, 60))
    pygame.draw.rect(surf, (74, 74, 90), R(0, 590, 1280, 50))
    pygame.draw.rect(surf, (85, 85, 102), R(0, 640, 1280, 80))
    # Faixas brancas tracejadas + linha amarela central tracejada.
    for x in range(0, 1280, 80):
        rect_alpha((255, 255, 255), 180, x, 557, 60, 6)
    for x in range(20, 1280, 80):
        rect_alpha((245, 200, 66), 150, x, 610, 50, 5)

    # Árvores pixel-art em 3 camadas de tom de verde (mais escura embaixo).
    arvores_pos = [(210, 460, 56), (310, 468, 50), (410, 455, 62), (810, 462, 56), (920, 465, 50), (1020, 458, 62)]
    for tx, ty_trunk, copa in arvores_pos:
        tronco_w = max(14, copa // 4)
        pygame.draw.rect(surf, (107, 68, 35), R(tx, ty_trunk, tronco_w, copa - 6))
        cx = tx + tronco_w // 2
        for w_copa, cor, dy in [(copa, (45, 138, 14), -copa + 6), ((copa * 5) // 7, (53, 160, 16), -copa - 2), ((copa * 3) // 7, (61, 184, 18), -copa - 10)]:
            pygame.draw.rect(surf, cor, R(cx - w_copa // 2, ty_trunk + dy, w_copa, w_copa))

    # Raposa pixel-art na grama, à esquerda (igual à da referência).
    fx, fy = 50, 440
    fox_laranja = (224, 90, 10)
    fox_laranja_claro = (240, 144, 80)
    fox_orelha_int = (240, 120, 48)
    fox_perna = (192, 72, 0)
    fox_preto = (26, 26, 26)
    # Corpo, cabeça, orelhas externas.
    pygame.draw.rect(surf, fox_laranja, R(fx + 10, fy + 24, 50, 30))
    pygame.draw.rect(surf, fox_laranja, R(fx + 40, fy + 8, 30, 26))
    pygame.draw.rect(surf, fox_laranja, R(fx + 44, fy, 10, 12))
    pygame.draw.rect(surf, fox_laranja, R(fx + 62, fy, 10, 12))
    # Interior das orelhas.
    pygame.draw.rect(surf, fox_orelha_int, R(fx + 46, fy + 2, 6, 8))
    pygame.draw.rect(surf, fox_orelha_int, R(fx + 64, fy + 2, 6, 8))
    # Focinho/face mais claro.
    pygame.draw.rect(surf, fox_laranja_claro, R(fx + 44, fy + 16, 20, 16))
    # Olho com pontinho branco e nariz.
    pygame.draw.rect(surf, fox_preto, R(fx + 62, fy + 12, 6, 6))
    pygame.draw.rect(surf, (255, 255, 255), R(fx + 64, fy + 13, 2, 2))
    pygame.draw.rect(surf, fox_preto, R(fx + 68, fy + 20, 4, 4))
    # Cauda com ponta clara.
    pygame.draw.rect(surf, fox_laranja, R(fx, fy + 20, 18, 16))
    pygame.draw.rect(surf, fox_laranja_claro, R(fx, fy + 18, 14, 8))
    # Quatro patas (laranja mais escuro).
    for lx in (14, 28, 42, 56):
        pygame.draw.rect(surf, fox_perna, R(fx + lx, fy + 50, 10, 16))
    # Barriga.
    pygame.draw.rect(surf, fox_orelha_int, R(fx + 16, fy + 30, 36, 18))

    # Carros pixel-art (vermelho, azul e amarelo) sobre as faixas.
    carros = [
        ((204, 34, 34), (153, 34, 17), 100, 535, 70, 28, 110, 528, 48, 16, 100, 560, 154, 560),
        ((34, 68, 204), (17, 34, 136), 900, 592, 70, 28, 912, 585, 46, 16, 900, 617, 954, 617),
        ((232, 192, 32), (192, 160, 16), 550, 638, 65, 26, 562, 631, 42, 14, 550, 661, 601, 661),
    ]
    for (corpo, teto, bx, by, bw, bh, tx, ty, tw, th, r1x, r1y, r2x, r2y) in carros:
        pygame.draw.rect(surf, corpo, R(bx, by, bw, bh))
        pygame.draw.rect(surf, teto, R(tx, ty, tw, th))
        # Duas janelas no teto.
        rect_alpha((200, 238, 255), 230, tx + 4, ty + 2, (tw - 14) // 2, th - 4)
        rect_alpha((200, 238, 255), 230, tx + (tw // 2) + 2, ty + 2, (tw - 14) // 2, th - 4)
        # Rodas.
        pygame.draw.rect(surf, (34, 34, 34), R(r1x, r1y, 16, 8))
        pygame.draw.rect(surf, (34, 34, 34), R(r2x, r2y, 16, 8))

    return surf


def criar_background_floresta_dia(width, height):
    """Cria o background pixel-art de floresta de dia: sol, montanhas, rua, raposa na toca.

    Reproduz a cena de assets/img/end_bg.svg usando pygame.draw, escalada
    proporcionalmente do design original 1310x730 para o tamanho pedido.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.

    Returns:
        pygame.Surface opaca contendo o cenário final.
    """
    surf = pygame.Surface((width, height))
    sx = width / 1310.0
    sy = height / 730.0

    def R(x, y, w, h):
        """Retorna um pygame.Rect escalado das coordenadas de design (1310x730)."""
        return pygame.Rect(int(x * sx), int(y * sy), max(1, int(w * sx)), max(1, int(h * sy)))

    def rect_alpha(cor, alpha, x, y, w, h):
        """Desenha um retângulo semi-transparente."""
        r = R(x, y, w, h)
        s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        s.fill((*cor, alpha))
        surf.blit(s, r.topleft)

    def poly_alpha(cor, alpha, pts):
        """Desenha um polígono semi-transparente com pontos em coords de design."""
        scaled = [(int(x * sx), int(y * sy)) for (x, y) in pts]
        min_x = min(p[0] for p in scaled)
        min_y = min(p[1] for p in scaled)
        max_x = max(p[0] for p in scaled)
        max_y = max(p[1] for p in scaled)
        s = pygame.Surface((max_x - min_x + 1, max_y - min_y + 1), pygame.SRCALPHA)
        local = [(p[0] - min_x, p[1] - min_y) for p in scaled]
        pygame.draw.polygon(s, (*cor, alpha), local)
        surf.blit(s, (min_x, min_y))

    # Céu gradiente azul de 3 paradas.
    azul_topo = (42, 160, 232)
    azul_meio = (109, 205, 245)
    azul_baixo = (160, 224, 255)
    for j in range(height):
        f = j / max(1, height - 1)
        if f < 0.55:
            t = f / 0.55
            cor = tuple(int(azul_topo[k] + (azul_meio[k] - azul_topo[k]) * t) for k in range(3))
        else:
            t = (f - 0.55) / 0.45
            cor = tuple(int(azul_meio[k] + (azul_baixo[k] - azul_meio[k]) * t) for k in range(3))
        pygame.draw.line(surf, cor, (0, j), (width, j))

    # Sol no canto superior esquerdo (com halo e raios).
    pygame.draw.rect(surf, (255, 224, 51), R(160, 55, 56, 56))
    rect_alpha((255, 241, 118), 128, 170, 63, 36, 20)
    for rx, ry, rw, rh in [(184, 36, 8, 14), (184, 114, 8, 14), (136, 78, 14, 8), (214, 78, 14, 8)]:
        rect_alpha((255, 224, 51), 180, rx, ry, rw, rh)
    for rx, ry in [(144, 46), (214, 46)]:
        rect_alpha((255, 224, 51), 128, rx, ry, 10, 10)

    # Nuvens (3 clusters).
    for cluster in [
        [(300, 50, 120, 34), (280, 62, 160, 30), (320, 40, 70, 26)],
        [(700, 40, 100, 30), (680, 52, 140, 28)],
        [(1050, 55, 90, 28), (1030, 65, 130, 26)],
    ]:
        for cx, cy, cw, ch in cluster:
            rect_alpha((255, 255, 255), 230, cx, cy, cw, ch)

    # Base verde sob as montanhas (fecha o gap antes da grama).
    pygame.draw.rect(surf, (42, 122, 12), R(0, 340, 1260, 145))

    # 5 montanhas principais.
    for pts, cor in [
        ([(0, 380), (150, 240), (300, 380)], (30, 96, 8)),
        ([(180, 380), (360, 225), (540, 380)], (46, 138, 16)),
        ([(420, 380), (600, 230), (780, 380)], (52, 140, 18)),
        ([(660, 380), (840, 235), (1020, 380)], (46, 138, 16)),
        ([(900, 380), (1080, 228), (1260, 380)], (42, 122, 12)),
    ]:
        scaled = [(int(x * sx), int(y * sy)) for (x, y) in pts]
        pygame.draw.polygon(surf, cor, scaled)

    # 5 montanhas da segunda camada, mais claras e semi-transparentes (preenchem vales).
    for pts, cor in [
        ([(80, 380), (230, 280), (380, 380)], (53, 150, 14)),
        ([(310, 380), (480, 265), (650, 380)], (47, 136, 14)),
        ([(560, 380), (720, 258), (880, 380)], (53, 150, 14)),
        ([(800, 380), (960, 270), (1120, 380)], (47, 136, 14)),
        ([(1060, 380), (1180, 272), (1300, 380)], (53, 150, 14)),
    ]:
        poly_alpha(cor, 217, pts)

    # Grama (gradiente verde + faixa mais clara no topo).
    grama_top = (58, 154, 26)
    grama_bot = (42, 112, 16)
    g_y0 = int(480 * sy)
    g_y1 = min(height, int(720 * sy))
    for j in range(g_y0, g_y1):
        t = (j - g_y0) / max(1, g_y1 - g_y0)
        cor = tuple(int(grama_top[k] + (grama_bot[k] - grama_top[k]) * t) for k in range(3))
        pygame.draw.line(surf, cor, (0, j), (width, j))
    pygame.draw.rect(surf, (74, 184, 32), R(0, 480, 1260, 14))

    # Rua: 3 faixas de asfalto + faixa de grama no rodapé.
    pygame.draw.rect(surf, (85, 85, 102), R(0, 510, 1260, 55))
    pygame.draw.rect(surf, (74, 74, 90), R(0, 565, 1260, 45))
    pygame.draw.rect(surf, (85, 85, 102), R(0, 610, 1260, 40))
    pygame.draw.rect(surf, (58, 138, 26), R(0, 650, 1260, 70))
    rect_alpha((245, 200, 66), 128, 0, 508, 1260, 4)
    for x in range(0, 1260, 75):
        rect_alpha((255, 255, 255), 180, x, 535, 55, 5)
    for x in range(20, 1260, 80):
        rect_alpha((245, 200, 66), 150, x, 585, 50, 5)

    # 8 árvores: 4 à esquerda e 4 à direita, com camadas de verde mais claras pra cima.
    arvores = [
        # (tronco_x, tronco_y, tronco_w, tronco_h, [(folha_x, y, w, h, cor)...])
        ((0, 450, 18, 60), [(0, 390, 80, 70, (45, 138, 14)), (8, 378, 64, 56, (53, 160, 16)), (16, 366, 48, 44, (61, 184, 18)), (24, 354, 32, 32, (72, 204, 22))]),
        ((70, 455, 16, 55), [(54, 400, 64, 62, (45, 138, 14)), (62, 390, 48, 48, (53, 160, 16)), (70, 380, 32, 32, (61, 184, 18))]),
        ((140, 458, 14, 52), [(124, 406, 58, 60, (45, 138, 14)), (132, 396, 42, 44, (53, 160, 16)), (140, 386, 26, 28, (61, 184, 18))]),
        ((220, 460, 16, 50), [(202, 408, 60, 60, (53, 160, 16)), (210, 398, 44, 46, (61, 184, 18)), (218, 388, 28, 28, (72, 204, 22))]),
        ((980, 458, 16, 52), [(964, 406, 60, 60, (45, 138, 14)), (972, 396, 44, 46, (53, 160, 16)), (980, 386, 28, 28, (61, 184, 18))]),
        ((1060, 454, 18, 56), [(1042, 398, 66, 66, (45, 138, 14)), (1050, 386, 50, 52, (53, 160, 16)), (1058, 374, 34, 34, (61, 184, 18))]),
        ((1148, 456, 16, 54), [(1132, 402, 62, 62, (45, 138, 14)), (1140, 392, 46, 48, (53, 160, 16)), (1148, 382, 30, 30, (61, 184, 18))]),
        ((1220, 450, 18, 60), [(1200, 390, 60, 70, (45, 138, 14)), (1208, 380, 44, 54, (53, 160, 16)), (1216, 370, 28, 36, (61, 184, 18))]),
    ]
    for (tx, ty, tw, th), camadas in arvores:
        pygame.draw.rect(surf, (107, 68, 35), R(tx, ty, tw, th))
        for fx, fy, fw, fh, cor in camadas:
            pygame.draw.rect(surf, cor, R(fx, fy, fw, fh))

    # Toca da raposa: morro marrom com buraco escuro.
    pygame.draw.rect(surf, (90, 58, 10), R(570, 475, 120, 35))
    pygame.draw.rect(surf, (107, 74, 24), R(590, 480, 80, 28))
    pygame.draw.rect(surf, (42, 24, 0), R(610, 468, 40, 30))
    pygame.draw.rect(surf, (26, 15, 0), R(612, 470, 36, 26))

    # Raposa vitoriosa em frente à toca (translated +490, +430 no SVG original).
    fx, fy = 490, 430
    laranja = (224, 90, 10)
    laranja_claro = (240, 144, 80)
    laranja_orelha = (240, 120, 48)
    laranja_perna = (192, 72, 0)
    preto = (26, 26, 26)
    pygame.draw.rect(surf, laranja, R(fx + 10, fy + 28, 44, 26))
    pygame.draw.rect(surf, laranja, R(fx + 30, fy + 4, 28, 28))
    pygame.draw.rect(surf, laranja, R(fx + 32, fy, 10, 12))
    pygame.draw.rect(surf, laranja, R(fx + 48, fy, 10, 12))
    pygame.draw.rect(surf, laranja_orelha, R(fx + 34, fy + 2, 6, 8))
    pygame.draw.rect(surf, laranja_orelha, R(fx + 50, fy + 2, 6, 8))
    pygame.draw.rect(surf, laranja_claro, R(fx + 32, fy + 16, 22, 14))
    pygame.draw.rect(surf, preto, R(fx + 34, fy + 12, 6, 5))
    pygame.draw.rect(surf, preto, R(fx + 48, fy + 12, 6, 5))
    pygame.draw.rect(surf, (255, 255, 255), R(fx + 36, fy + 13, 2, 2))
    pygame.draw.rect(surf, (255, 255, 255), R(fx + 50, fy + 13, 2, 2))
    pygame.draw.rect(surf, preto, R(fx + 52, fy + 22, 4, 4))
    pygame.draw.rect(surf, laranja_orelha, R(fx + 14, fy + 32, 28, 18))
    pygame.draw.rect(surf, laranja, R(fx, fy + 10, 14, 30))
    pygame.draw.rect(surf, laranja_claro, R(fx, fy + 8, 12, 12))
    for lx in (12, 26, 40):
        pygame.draw.rect(surf, laranja_perna, R(fx + lx, fy + 50, 10, 14))

    # Borboletas (rosa à esquerda, azul à direita).
    rect_alpha((255, 136, 204), 205, 350, 430, 8, 6)
    rect_alpha((255, 136, 204), 205, 360, 426, 8, 6)
    rect_alpha((170, 102, 0), 180, 355, 432, 4, 10)
    rect_alpha((136, 204, 255), 205, 870, 418, 8, 6)
    rect_alpha((136, 204, 255), 205, 880, 414, 8, 6)
    rect_alpha((170, 102, 0), 180, 875, 420, 4, 10)

    return surf
