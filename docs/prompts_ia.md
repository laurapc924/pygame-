# Histórico de uso de IA generativa

Este documento registra como ferramentas de IA generativa foram utilizadas no
desenvolvimento de **Fox Crossing**, conforme exigido pela disciplina Design
de Software do Insper.

## Ferramenta utilizada

- **Claude (Anthropic)** — modelo Opus 4.x, via Claude Code (integração com
  o editor) e via interface claude.ai.

## Metodologia

1. **Planejamento manual**: cada feature foi pensada pelos autores antes de
   ser solicitada à IA. Definíamos o que precisava ser feito, em qual arquivo
   e como deveria se integrar ao resto do projeto.
2. **Prompts estruturados**: ao pedir código novo, especificávamos:
   - Contexto (qual módulo já existe, quais constantes estão disponíveis)
   - Objetivo claro (o que a função/classe precisa fazer)
   - Convenções (docstrings, nomes em português, separação de responsabilidades)
3. **Revisão antes de commitar**: todo código sugerido foi lido, testado em
   runtime e ajustado pelos autores antes de virar commit.
4. **Bugs**: analisávamos primeiro o que estava errado e, quando necessário,
   passávamos pra IA junto com o traceback ou screenshot.

## Histórico cronológico das principais sessões

Abaixo está o resumo do que foi desenvolvido em cada sessão de prompts. O
detalhamento (prompts exatos) está nas conversas exportadas linkadas no topo.

### 1. Fundação do jogo

- Setup do loop principal de pygame com máquina de estados (BaseState +
  subclasses para menu, gameplay, pausa, etc).
- Sprite da raposa controlada pelas setas com colisão, vidas e zona de chegada.
- Sistema de carros (`Obstacle`) que se movem em faixas alternadas, com
  loop infinito ao sair da tela.
- `MapManager` desenhando 3 faixas de rua e laterais de grama.

### 2. HUD, pontuação e tela final

- HUD com vidas, pontos, recorde e fase atual.
- `ScoreManager` com recorde persistente em `data/highscore.txt`.
- Telas de Game Over e Vitória com retorno ao menu.

### 3. Animação da raposa

- Carregamento da sprite sheet (3 colunas × 4 linhas).
- Sistema de animação com `frame_index` e `animation_timer` (0.15s/frame).
- Raposa muda de direção ao apertar setas e fica em idle quando parada.

### 4. Sons gerados por código

- `tools/generate_sounds.py` que gera 4 arquivos `.wav` usando apenas
  `wave` + `math` + `struct` (sem dependência externa).
- `SoundManager` centralizando música + SFX, com fallback silencioso se
  arquivos não carregarem.

### 5. Cenário lateral com decorações

- `criar_arvore`, `criar_grama_textura`, `criar_asfalto_textura` em
  `sprite_factory.py`.
- Posicionamento de árvores em slots verticais não-sobrepostos nas
  laterais do mapa.

### 6. Polimento das telas de UI

- Reescrita do menu, instruções, game over, vitória e pausa com:
  - Backgrounds em gradiente
  - Painéis translúcidos com borda dourada
  - Títulos com sombra (efeito 3D)
  - Animações sutis (raposa quicando, confete, estrelas piscando)
- Paleta de cores oficial centralizada em `settings.py`.

### 7. Raposa decorativa mais realista

- Reescrita de `criar_raposa_estatica` de uma versão front-view "cub" pra
  uma versão side-profile com cauda peluda, focinho pontudo e meias pretas.

### 8. Expansão para 6 fases temáticas

- `LevelManager` expandido com nome, subtítulo, cores e config de carros
  por fase.
- Efeitos especiais: neve (Suíça), faróis (Londres à noite).

### 9. Cenários distintos por fase

- Cada fase recebeu sua própria decoração lateral (`criar_arvore`,
  `criar_poste`, `criar_coqueiro`, `criar_pinheiro`, `criar_pedra`, `criar_cerca`).

### 10. Backgrounds das telas de início, instruções, vitória e perda

- A partir de SVGs de referência criadas em colaboração com Claude,
  transcrevemos as cenas em pygame.draw:
  - Menu: cidade pixel-art com céu azul, sol, prédios, rua, carros, raposa.
  - Instruções / Vitória: floresta de dia com montanhas, raposa indo à toca.
  - Game Over: floresta noturna com aurora dourada e estrelas tênues.

### 11. Expansão para 10 fases temáticas (países)

- `LevelManager` atualizado pra 10 fases nomeadas por país (Amazônia,
  Inglaterra, Havaí, Suíça, França, África do Sul, Egito, Canadá, Bélgica,
  Itália).
- `src/utils/lateral_bars.py` novo com **20 barras laterais** (10 países × 2
  lados) transcritas dos SVGs de referência.
- `map_manager` refatorado pra renderizar a barra inteira de uma vez (em vez
  de sprites isolados).
- Efeito de chuva adicionado pra fase Bélgica.

### 12. Bandeiras nas transições

- `criar_bandeira(tema, w, h)` com 10 bandeiras simplificadas pixel-art.
- Tela de transição entre fases mostra bandeira + nome do país.

### 13. Balanceamento iterativo de dificuldade

- Várias rodadas de ajuste fino testando a curva de dificuldade — o boss
  (fase 10) terminou definido pela velocidade máxima e não pela densidade
  de carros, pra garantir que sempre haja buracos pra raposa passar.

### 14. Documentação final

- Auditoria de docstrings em todos os arquivos.
- README reescrito seguindo o molde do freeCodeCamp.
- Este documento atualizado pra refletir as 10 fases e o estado real do
  projeto.

## Estimativa de uso

A estimativa por componente está na tabela do README. Resumo:

- **~80% do código** foi gerado ou refinado com auxílio de IA.
- **~20%** foi escrito ou ajustado manualmente, principalmente:
  - Integração entre módulos quando o código sugerido não encaixava direto
  - Balanceamento das fases (velocidade, densidade de carros, pontuação)
  - Ajustes finos de layout (posições de painéis, tamanhos de fonte)
  - Decisões de arquitetura (separar em states/managers/entities/utils)
  - Debugging de bugs específicos de runtime

## Decisões manuais (sem IA)

- Conceito do jogo: raposa atravessando 10 países do mundo.
- Lista dos países e qual decoração temática cada um teria.
- Curva final de dificuldade (após testar IRL várias iterações).
- Estética geral (paleta dourada/verde, vibe pixel-art).
- Escolha de testar tudo no Windows com PyGame 2.6.

## Observações

- Todo código gerado foi compreendido pelos autores antes de ser commitado.
- Bugs gerados por sugestões da IA foram resolvidos por re-prompt com
  contexto adicional (traceback, screenshot, descrição do comportamento
  inesperado).
- As conversas inteiras estão exportadas e linkadas no topo do documento
  para auditoria do professor.
