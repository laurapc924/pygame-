# Decisões de design

Este documento registra as principais decisões de arquitetura e design tomadas
durante o desenvolvimento de **Fox Crossing**. Cada seção explica uma escolha
e o motivo dela.

## Formato horizontal

Escolhemos o formato horizontal para diferenciar Fox Crossing do Frogger
clássico e reforçar a ideia narrativa de travessia. Em vez de subir pela tela,
a raposa avança lateralmente, como atravessando estradas em diferentes países.

Essa escolha também facilita a leitura visual da progressão: a raposa começa
na lateral esquerda e precisa alcançar a zona dourada à direita. O
deslocamento horizontal cria sensação clara de início, percurso e chegada.

## Máquina de estados

Usamos máquina de estados em vez de flags booleanas (`is_in_menu`,
`is_playing`, `is_paused`) porque cada tela tem comportamento próprio. Menu,
instruções, gameplay, pausa, vitória e game over processam eventos, atualizam
lógica e desenham elementos de formas diferentes.

Com estados separados (`BaseState` + subclasses), o loop principal fica
simples e cada classe encapsula sua própria lógica. Isso reduz o risco de
combinações inválidas de flags e facilita adicionar novas telas.

## Divisão em managers

Dividimos responsabilidades em managers para evitar que o `GameState`
acumulasse toda a lógica do jogo:

- **`LevelManager`** — configurações das 10 fases (velocidade, densidade,
  cores, decoração temática).
- **`MapManager`** — cenário (barras laterais, faixas, gradiente), spawn de
  carros e power-ups, efeitos climáticos.
- **`ScoreManager`** — pontuação corrente e recorde persistente.
- **`SoundManager`** — música e SFX, com fallback silencioso.
- **`TransitionManager`** — fades entre telas.

Cada classe tem um motivo principal pra existir e mudar (Single Responsibility
Principle). Quando precisamos ajustar a curva de dificuldade, mexemos só no
`LevelManager`. Quando trocamos um efeito sonoro, mexemos só no `SoundManager`.

## 10 fases temáticas em vez de fase infinita

Optamos por **10 fases progressivas** representando países (Amazônia,
Inglaterra, Havaí, Suíça, França, África do Sul, Egito, Canadá, Bélgica,
Itália) em vez de uma fase única infinita. Razões:

- **Sensação de progressão**: o jogador vê o mundo mudar visualmente a cada
  travessia e tem uma meta clara (chegar à fase 10).
- **Variedade visual**: cada fase tem cenário, paleta e efeitos próprios —
  cada uma sente como um capítulo novo.
- **Balanceamento controlado**: dá pra calibrar dificuldade fase a fase
  (curva controlada), em vez de uma escalada exponencial até morrer.
- **Fim definido**: a tela de Vitória dá um closure narrativo (a raposa
  chegou em casa) — importante pra uma entrega acadêmica.

## Tudo desenhado em pygame.draw

Em vez de depender de uma biblioteca grande de assets, **todo o cenário
(céu, montanhas, prédios, árvores, raposa decorativa, bandeiras, efeitos
climáticos) é desenhado proceduralmente** com `pygame.draw`. Isso significa:

- Repositório mais leve (não tem imagens pesadas).
- Fácil recolorir/redimensionar qualquer elemento por fase.
- Sem dependências externas além do PyGame.
- Cada elemento gráfico é uma função pura em `sprite_factory.py` ou
  `lateral_bars.py`, fácil de testar isoladamente.

As exceções são:
- Sprites de carros (Kenney, CC0)
- Sprite sheet da raposa (assets/img/foxN.png — origem documentada no README)

## Power-ups e habilidade Instinto

Adicionamos power-ups (cogumelo, trevo) e a habilidade especial Instinto para
diferenciar de uma recriação genérica de Frogger:

- **Cogumelo** (+1 vida): incentivo a explorar todas as faixas.
- **Trevo** (3s de invencibilidade): momento de respiro em fases difíceis.
- **Instinto** (slow-motion dos carros por 2s, cooldown 10s): escolha
  estratégica — o jogador decide quando ativar.

O jogador não depende só de reflexo: pode usar recursos pra contornar
situações difíceis. Isso torna o balanceamento mais flexível porque podemos
fazer fases mais "intensas" sabendo que existem ferramentas pra escapar.

## Curva de dificuldade

A curva final tem três princípios:

1. **Velocidade cresce gradualmente** (+15–20 px/s por fase) em vez de
   saltar drasticamente.
2. **Densidade de carros sobe lentamente** (2 → 3 carros/faixa cedo,
   mantida em 3 até o fim).
3. **A fase final (Itália) é o boss pela velocidade**, não pela densidade —
   sempre tem buraco entre carros pra raposa passar.

Antes desse formato, tínhamos pulado pra 4 e 5 carros/faixa nas fases
finais, mas isso reduzia o espaço entre carros pra ~52px (raposa tem 64px) —
era estatisticamente impossível. Aprendemos que **densidade tem um teto
estrutural** mais limitante que velocidade.

## Efeitos climáticos por tema

Algumas fases têm efeito climático que combina com o tema:

- **Suíça** e **Canadá**: neve caindo (50 partículas).
- **Bélgica**: chuva diagonal (80 partículas).
- **Inglaterra (noite)**: faróis amarelos atrás dos carros.

O asfalto também muda: nas fases com chuva/neve, ele fica com manchas
escuras e pixels claros (parece molhado/desgastado). Nas outras, fica liso.

## Bandeiras nas transições

Na tela de transição entre fases mostramos a bandeira do país ao lado do
nome. Razão: reforça a identidade visual de cada fase como um país distinto
e dá um pequeno momento contemplativo antes da próxima travessia começar.

As bandeiras são desenhadas em `sprite_factory.py` em 10 funções privadas
(uma por país), todas no mesmo tamanho/proporção, simplificadas pra leitura
em pixel art.
