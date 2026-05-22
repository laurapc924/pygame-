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
    """Cria a Surface de uma raposa fofa de frente, para usar como decoração.

    Args:
        width: Largura da Surface em pixels.
        height: Altura da Surface em pixels.
        olhos_fechados: Se True, desenha olhos fechados (raposa triste).

    Returns:
        pygame.Surface com fundo transparente contendo a raposa.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    laranja = (230, 130, 50)
    branco = (240, 240, 235)
    preto = (30, 30, 30)

    cx = width // 2

    # Cauda peluda atrás do corpo, com a ponta branca.
    cauda_r = width // 5
    cauda_x = cx - int(width * 0.3)
    cauda_y = int(height * 0.66)
    pygame.draw.circle(surf, laranja, (cauda_x, cauda_y), cauda_r)
    pygame.draw.circle(
        surf, laranja, (cauda_x - cauda_r // 2, cauda_y + cauda_r // 2), cauda_r
    )
    pygame.draw.circle(
        surf, branco, (cauda_x - cauda_r, cauda_y + cauda_r), cauda_r // 2
    )

    # Corpo: oval laranja.
    corpo = pygame.Rect(0, 0, int(width * 0.52), int(height * 0.44))
    corpo.center = (cx, int(height * 0.74))
    pygame.draw.ellipse(surf, laranja, corpo)

    # Barriga branca menor.
    barriga = pygame.Rect(0, 0, int(width * 0.28), int(height * 0.30))
    barriga.center = (cx, int(height * 0.80))
    pygame.draw.ellipse(surf, branco, barriga)

    # Cabeça: círculo laranja.
    cabeca_r = int(width * 0.28)
    cabeca_y = int(height * 0.40)
    pygame.draw.circle(surf, laranja, (cx, cabeca_y), cabeca_r)

    # Orelhas triangulares (apontando pra cima e pra fora) com interior branco.
    for lado in (-1, 1):
        base_int = (cx + lado * int(cabeca_r * 0.20), cabeca_y - int(cabeca_r * 0.70))
        base_ext = (cx + lado * int(cabeca_r * 1.00), cabeca_y - int(cabeca_r * 0.35))
        ponta = (cx + lado * int(cabeca_r * 0.72), cabeca_y - int(cabeca_r * 1.55))
        pygame.draw.polygon(surf, laranja, [base_int, base_ext, ponta])
        # Interior branco: triângulo menor encolhido em direção à ponta.
        meio_base = (
            (base_int[0] + base_ext[0]) // 2,
            (base_int[1] + base_ext[1]) // 2,
        )
        meio_int = ((base_int[0] + ponta[0]) // 2, (base_int[1] + ponta[1]) // 2)
        meio_ext = ((base_ext[0] + ponta[0]) // 2, (base_ext[1] + ponta[1]) // 2)
        pygame.draw.polygon(surf, branco, [meio_base, meio_int, meio_ext])

    # Focinho branco em volta do nariz.
    focinho = pygame.Rect(0, 0, int(cabeca_r * 1.1), int(cabeca_r * 0.85))
    focinho.center = (cx, cabeca_y + cabeca_r // 3)
    pygame.draw.ellipse(surf, branco, focinho)

    # Olhos.
    olho_dx = cabeca_r // 2
    olho_y = cabeca_y - cabeca_r // 6
    olho_r = max(2, width // 22)
    if olhos_fechados:
        for lado in (-1, 1):
            ex = cx + lado * olho_dx
            pygame.draw.line(
                surf, preto, (ex - olho_r, olho_y), (ex + olho_r, olho_y), 3
            )
    else:
        for lado in (-1, 1):
            pygame.draw.circle(surf, preto, (cx + lado * olho_dx, olho_y), olho_r)

    # Nariz preto pequeno no centro do focinho.
    pygame.draw.circle(
        surf, preto, (cx, cabeca_y + cabeca_r // 3), max(2, width // 20)
    )

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
