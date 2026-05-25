# 🦊 Fox Crossing

Um jogo 2D estilo Frogger feito em PyGame onde uma raposa precisa atravessar rodovias em 10 cidades do mundo (da Amazônia até a Itália) desviando de carros, coletando power-ups e usando a habilidade especial **Instinto**
(slow-motion) para chegar viva à toca dourada no fim do mapa.

![Status](https://img.shields.io/badge/status-jogo%20completo-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyGame](https://img.shields.io/badge/pygame-2.6-orange)

## Sumário

- [Descrição](#descrição)
- [Como instalar e rodar](#como-instalar-e-rodar)
- [Como jogar](#como-jogar)
- [Fases](#fases)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Decisões de design](#decisões-de-design)
- [Uso de IA generativa](#uso-de-ia-generativa)
- [Créditos](#créditos)
- [Licença](#licença)

## Descrição

Fox Crossing é o projeto final de **Design de Software** do Insper (2026). O jogador controla uma raposa que precisa atravessar 10 fases temáticas ambientadas em diferentes países (Amazônia, Inglaterra, Havaí, Suíça, França,
África do Sul, Egito, Canadá, Bélgica e Itália). Cada fase tem cenário próprio em pixel art, dificuldade crescente (mais velocidade e densidade de carros) e a transição entre elas mostra a bandeira + nome do país visitado.

O projeto foi um exercício de orientação a objetos, organização modular, máquina de estados e boas práticas de desenvolvimento de jogos. Todo o cenário, sprites de raposa, decorações das fases, bandeiras e efeitos climáticos (neve, chuva, faróis, vagalumes, confete) são desenhados
procedurmente em runtime com `pygame.draw` — não dependemos de assets externos fora dos sprites de carros (Kenney) e dos sons gerados por código.

### Features

- **10 fases temáticas** com cenário, cores e dificuldade próprios.
- **Máquina de estados** (menu, instruções, jogo, pausa, vitória, game over).
- **Sistema de vidas, pontuação e recorde persistente** (`data/highscore.txt`).
- **Power-ups**: cogumelo (+1 vida) e trevo (3s de invencibilidade).
- **Habilidade Instinto** (slow-motion dos carros, com cooldown).
- **Efeitos climáticos por fase**: neve (Suíça e Canadá), chuva (Bélgica),
  faróis dos carros (Inglaterra à noite).
- **Animações**: raposa caminha em 4 direções com 3 frames; estrelas, confete,
  vagalumes e bandeiras pulsantes nas telas.
- **HUD completo**: vidas, pontos, recorde, fase atual e barra do Instinto.
- **Sons gerados por código** (música de menu/jogo, SFX de colisão/vitória).
- **Tela de transição entre fases** com bandeira + título do país + subtítulo.

## Como instalar e rodar

### Requisitos

- Python 3.10 ou superior
- PyGame 2.6+

### Passo a passo

1. Clone o repositório:
   ```bash
   git clone https://github.com/<USUARIO>/fox-crossing.git
   cd fox-crossing
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode o jogo:
   ```bash
   python main.py
   ```

## Como jogar

### Controles

| Tecla              | Ação                                          |
| ------------------ | --------------------------------------------- |
| Setas (↑ ↓ ← →)    | Mover a raposa                                |
| SHIFT              | Ativar Instinto (slow-motion por 2s)          |
| P                  | Pausar / despausar durante o jogo             |
| ENTER              | Confirmar / iniciar / voltar ao menu          |
| I                  | Abrir instruções no menu principal            |
| M                  | Voltar ao menu (em pausa, fim ou instruções)  |
| ESC                | Sair do jogo                                  |

### Objetivo

Atravessar todas as faixas de carros e chegar à **zona dourada** (toca da raposa) no extremo direito da tela. A raposa começa com **3 vidas**; ao colidir, perde uma vida e volta ao começo da fase.

Ao chegar à toca, ganha pontos e avança pra próxima fase. Completar todas as 10 fases dispara a tela de vitória. Perder todas as vidas leva ao Game Over.

### Pontuação por fase

| # | País                | Subtítulo            | Velocidade | Carros/faixa | Pontos |
| - | ------------------- | -------------------- | ---------- | ------------ | ------ |
| 1 | 🇧🇷 AMAZÔNIA        | Floresta             | 110–200    | 2            | 100    |
| 2 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 INGLATERRA       | Cidade à noite       | 130–220    | 2            | 150    |
| 3 | 🌺 HAVAÍ            | Praia                | 150–240    | 2            | 200    |
| 4 | 🇨🇭 SUÍÇA           | Neve                 | 170–260    | 3            | 250    |
| 5 | 🇫🇷 FRANÇA          | Montanha             | 180–280    | 3            | 350    |
| 6 | 🇿🇦 ÁFRICA DO SUL   | Safari               | 200–300    | 3            | 450    |
| 7 | 🇪🇬 EGITO           | Deserto              | 210–295    | 3            | 600    |
| 8 | 🇨🇦 CANADÁ          | Bosque               | 225–310    | 3            | 750    |
| 9 | 🇧🇪 BÉLGICA         | Cidade com chuva     | 240–325    | 3            | 900    |
| 10| 🇮🇹 ITÁLIA          | Cidade               | 255–345    | 3            | 1200   |

### Power-ups e habilidade

- **🍄 Cogumelo (vermelho)**: +1 vida.
- **🍀 Trevo (verde)**: invencibilidade por 3 segundos (raposa pisca).
- **⚡ Instinto (SHIFT)**: reduz a velocidade dos carros para 30% durante 2s; recarrega em 10s. A barra azul na lateral mostra o estado.

## Fases

Cada fase tem decoração lateral própria (esquerda e direita do mapa) desenhada em pixel art:

| País             | Decoração lateral                            | Efeito especial         |
| ---------------- | -------------------------------------------- | ----------------------- |
| Amazônia         | Floresta densa, cipós, flores tropicais      | —                       |
| Inglaterra       | Big Ben, prédios iluminados, lampião         | Faróis dos carros 💡    |
| Havaí            | Coqueiros, sol, mar, hibiscos                | —                       |
| Suíça            | Montanha nevada, chalé, bandeira             | Neve caindo ❄️          |
| França           | Mont Blanc + teleférico                      | —                       |
| África do Sul    | Acácias, girafa, elefante, pôr do sol        | —                       |
| Egito            | Pirâmide, esfinge, dunas, sol forte          | —                       |
| Canadá           | Pinheiros nevados, folha de bordo, pegadas   | Neve caindo ❄️          |
| Bélgica          | Casas com gevel, campanário, paralelepípedo  | Chuva diagonal 🌧️       |
| Itália           | Duomo, prédios racionalistas, vespa          | —                       |

## Vídeo demonstrativo



## Estrutura do projeto

```text
fox-crossing/
├── main.py                  # Entrypoint
├── requirements.txt
├── README.md
├── data/
│   └── highscore.txt        # Recorde persistente
├── assets/
│   ├── fonts/
│   ├── img/
│   │   ├── fox0..3.png      # Sprite sheets da raposa por direção
│   │   └── cars/            # Sprites de carros (Kenney)
│   └── sounds/              # Música de menu/jogo + SFX
└── src/
    ├── game.py              # Loop principal e troca de estados
    ├── settings.py          # Constantes globais (WIDTH, HEIGHT, cores)
    ├── entities/
    │   ├── fox.py           # Raposa controlável (com animação)
    │   ├── obstacle.py      # Carros (sprite + movimento + colisão)
    │   └── powerup.py       # Cogumelo e trevo
    ├── managers/
    │   ├── level_manager.py    # Configurações das 10 fases
    │   ├── map_manager.py      # Cenário, faixas, obstáculos, efeitos climáticos
    │   ├── score_manager.py    # Pontuação e recorde persistente
    │   ├── sound_manager.py    # Música e SFX
    │   └── transition_manager.py  # Fades entre telas
    ├── states/
    │   ├── base_state.py       # Classe base da máquina de estados
    │   ├── menu.py             # Tela inicial (cidade pixel-art)
    │   ├── instructions_state.py
    │   ├── game_state.py       # Gameplay principal
    │   ├── pause_state.py
    │   ├── splash_state.py
    │   ├── victory_state.py    # Floresta dia + raposa na toca
    │   └── game_over_state.py  # Floresta noturna + aurora
    └── utils/
        ├── fonts.py
        ├── sprite_factory.py   # Sprites e backgrounds procedurais
        └── lateral_bars.py     # 20 barras laterais (10 países × 2 lados)
```

## Decisões de design

- **Máquina de estados**: cada tela (menu, instruções, jogo, pausa, vitória,
  game over) é uma subclasse de `BaseState` com `handle_events`, `update(dt)` e
  `draw(screen)` próprios. Isso evita uma cadeia gigante de `if`s no loop
  principal e isola responsabilidades.
- **Managers separados**: a fase (configs), o mapa (cenário e obstáculos), a
  pontuação, o som e as transições têm cada um seu manager dedicado. O
  `GameState` apenas orquestra — não conhece detalhes de pintura ou som.
- **Tudo em pygame.draw**: o cenário inteiro (céu, montanhas, prédios, árvores,
  carros, raposa decorativa, bandeiras, efeitos climáticos) é desenhado por
  código a partir de SVGs de referência. Isso evita dependência de arquivos
  externos e mantém o repositório leve. O único asset externo são os sprites
  de carros do Kenney (livres).
- **Sprite factory + lateral_bars**: para cada elemento gráfico criamos uma
  função em `sprite_factory.py` ou `lateral_bars.py` (no caso das barras
  laterais). Isso permite recolorir/redimensionar cada peça pela fase atual.
- **Curva de dificuldade**: o jogo tem 10 fases com aumento gradual de
  velocidade. A densidade de carros sobe lentamente (2 → 3 carros/faixa) e o
  pulo grande pra 3 acontece já na fase 4 pra dar tempo de praticar. O boss
  (fase 10) é definido pela velocidade máxima (255–345) e não por densidade,
  pra garantir que sempre haja buracos entre carros.
- **Efeitos especiais por país**: faróis (Inglaterra), neve (Suíça/Canadá) e
  chuva (Bélgica) são ativados pelo tema da fase via `decoration` key.
- **Asfalto sujo só onde tem clima ruim**: na chuva e na neve o asfalto tem
  manchas e pixels claros (parece molhado/desgastado); nas outras fases o
  chão fica limpo.

## Uso de IA generativa

Esse projeto foi desenvolvido com auxílio extensivo do **Claude (Anthropic)** —
todos os prompts foram revisados pelos autores antes do código ser commitado e o entendimento das decisões de arquitetura, da rubrica e do design das fases foi feito pelos membros do grupo.

**Estimativa: ~80% do código foi gerado ou refinado com auxílio de IA**, e
~20% foi escrito/ajustado manualmente (principalmente integração, balanceamento das fases e ajustes finos de layout).

Detalhamento por área:

| Componente                                | % IA | Observações                                            |
| ----------------------------------------- | ---- | ------------------------------------------------------ |
| Máquina de estados + game loop            | 70%  | Estrutura sugerida pela IA, integração feita manualmente |
| Sprites procedurais (raposa, árvores etc.) | 95%  | Geradas a partir de SVGs de referência via Claude       |
| 20 barras laterais (`lateral_bars.py`)    | 95%  | Transcritas dos SVGs de referência via Claude           |
| 10 bandeiras simplificadas                | 100% | Geradas integralmente pela IA                          |
| Backgrounds (menu, vitória, game over)    | 95%  | A partir de SVGs anexados ao prompt                    |
| Balanceamento das 10 fases                | 50%  | Várias iterações pelo grupo testando jogabilidade       |
| Lógica de física dos carros               | 40%  | Boa parte escrita à mão pelos autores                   |
| Sons gerados por código                   | 100% | Geração via stdlib (`wave` + `math`) sugerida pela IA   |
| README + docstrings                       | 95%  | Estrutura inicial e refinamentos via IA                 |

Detalhamento completo das sessões com Claude e da metodologia está em [docs/prompts_ia.md](docs/prompts_ia.md).

## Créditos

### Assets externos

- **🚗 Sprites de carros** — [Kenney Car Kit](https://kenney.nl/assets/car-kit),
  licença [CC0](https://creativecommons.org/publicdomain/zero/1.0/) (uso
  livre, inclusive comercial). Arquivos em `assets/img/cars/`.

- **🦊 Sprite sheet da raposa** — desenhada proceduralmente em
  [tools/generate_fox_sprites.py](tools/generate_fox_sprites.py) usando
  `pygame.draw`. Gera 4 PNGs (`fox0.png` UP, `fox1.png` RIGHT, `fox2.png` DOWN,
  `fox3.png` LEFT) com 3 frames de animação cada (48×64 por frame). Rode
  `python tools/generate_fox_sprites.py` para regenerar. Arte 100% autoral
  do grupo.

### Geradas internamente

- **🎵 Sons** — música de menu/jogo e efeitos sonoros (colisão, vitória)
  são gerados em `tools/generate_sounds.py` usando apenas `wave`, `struct` e
  `math` da stdlib do Python. Roda `python tools/generate_sounds.py` para
  regenerar.

- **🎨 Cenários e elementos visuais** — todos os backgrounds (menu, instruções,
  vitória, game over), as 20 barras laterais (10 países × 2 lados), as 10
  bandeiras, as decorações e a raposa de perfil são desenhados
  proceduralmente em `pygame.draw` a partir de referências SVG criadas em
  colaboração com Claude. Código em [src/utils/sprite_factory.py](src/utils/sprite_factory.py)
  e [src/utils/lateral_bars.py](src/utils/lateral_bars.py).

## Autores

- Andrezza Rutkowski Coelho
- Camila Frid Buniac
- Laura Pimentel Cots

## Licença

Projeto acadêmico — uso educacional. Sprites de carros do Kenney sob CC0.
