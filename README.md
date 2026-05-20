## 🦊 Fox Crossing

### Sobre o projeto

Fox Crossing é um jogo 2D desenvolvido em PyGame no qual o jogador controla uma raposa que precisa atravessar faixas movimentadas de carros até chegar à sua toca dourada. A cada fase, o desafio aumenta: os carros ficam mais rápidos, há mais obstáculos na tela e o jogador precisa administrar melhor suas vidas, power-ups e habilidade especial.

A narrativa do jogo acompanha a travessia da raposa entre a floresta e a cidade. O objetivo é sobreviver ao caminho urbano, coletar itens especiais e alcançar a zona dourada, que representa a toca segura da raposa.

Este projeto foi desenvolvido como projeto final da disciplina Design de Software do Insper, em 2026, com foco em orientação a objetos, organização modular, máquina de estados e boas práticas de desenvolvimento de jogos.

### Autores

- Andrezza [SOBRENOME]
- Rodrigo [SOBRENOME]

### Vídeo demonstrativo

[PLACEHOLDER: https://youtube.com/SEU_LINK_AQUI]

Veja o jogo em ação clicando no link acima.

### Como rodar o jogo

Requisitos:

- Python 3.10+
- pygame-ce

Passo a passo:

1. Clone o repositório:
   ```bash
   git clone [URL]
   ```
2. Entre na pasta do projeto:
   ```bash
   cd fox-crossing
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o jogo:
   ```bash
   python main.py
   ```

### Controles

| Tecla | Ação |
| --- | --- |
| Setas do teclado | Mover a raposa |
| SHIFT | Ativar Instinto (slow-motion) |
| P | Pausar |
| ENTER | Confirmar / Iniciar |
| I | Ver instruções no menu |
| ESC | Sair |
| M | Voltar ao menu em telas de fim/pausa |

### Como jogar

O objetivo é atravessar a cidade desviando dos carros e alcançar a toca dourada no fim do mapa. A raposa começa com 3 vidas; ao colidir com um carro, perde uma vida e retorna ao início da fase.

O jogo possui 3 fases com dificuldade progressiva. Ao completar cada travessia, o jogador recebe pontos: 100 na fase 1, 200 na fase 2 e 300 na fase 3. Ao completar as três fases, a tela de vitória é exibida.

Durante a partida, é possível coletar power-ups: o cogumelo vermelho concede +1 vida, enquanto o trevo verde deixa a raposa invencível por 3 segundos. A habilidade especial Instinto, ativada com SHIFT, reduz a velocidade dos carros por 2 segundos e possui cooldown de 10 segundos.

### Funcionalidades implementadas

- Menu principal com opções para jogar e acessar instruções.
- Tela de instruções explicando controles e mecânicas.
- Sistema de 3 fases com dificuldade crescente.
- Sistema de vidas, começando com 3 vidas.
- Colisão com carros, perda de vida e reposicionamento da raposa no início.
- Zona de chegada, representada pela toca dourada.
- Tela de Game Over ao perder todas as vidas.
- Tela de Vitória ao completar as 3 fases.
- Tela de Pausa acionada pela tecla P.
- Sistema de pontuação: 100 pontos na fase 1, 200 na fase 2 e 300 na fase 3.
- Recorde persistente salvo em `data/highscore.txt`.
- Power-ups: cogumelo vermelho (+1 vida) e trevo verde (invencibilidade por 3 segundos).
- Habilidade especial Instinto com slow-motion por 2 segundos e cooldown de 10 segundos.
- Transições suaves de fade entre todas as telas.
- HUD completo com vidas, pontos, recorde, fase atual e barra do Instinto.

### Estrutura do projeto

```text
fox-crossing/
├── main.py
├── programa.py
├── requirements.txt
├── README.md
├── assets/
│   ├── fonts/
│   ├── img/
│   └── sounds/
├── data/
│   └── highscore.txt
├── docs/
│   ├── decisoes_design.md
│   └── prompts_ia.md
└── src/
    ├── game.py
    ├── settings.py
    ├── entities/
    │   ├── fox.py
    │   ├── obstacle.py
    │   └── powerup.py
    ├── managers/
    │   ├── level_manager.py
    │   ├── map_manager.py
    │   ├── score_manager.py
    │   ├── sound_manager.py
    │   └── transition_manager.py
    ├── states/
    │   ├── base_state.py
    │   ├── game_over_state.py
    │   ├── game_state.py
    │   ├── instructions_state.py
    │   ├── menu.py
    │   ├── pause_state.py
    │   ├── splash_state.py
    │   └── victory_state.py
    └── utils/
```

### Decisões de design

O jogo utiliza uma máquina de estados para separar claramente as telas principais: menu, instruções, jogo, pausa, game over e vitória. Essa escolha evita condicionais espalhadas pelo loop principal e permite que cada tela controle seus próprios eventos, atualização e desenho.

A lógica foi dividida em managers para manter responsabilidade única. O `MapManager` cuida do mapa e dos elementos da fase, o `ScoreManager` centraliza pontuação e recorde, o `LevelManager` controla progressão e dificuldade, e o `TransitionManager` gerencia os fades entre telas. Assim, o `GameState` permanece focado na experiência de gameplay.

Optamos por fases progressivas em vez de uma fase única infinita para criar sensação clara de avanço e conclusão. O jogador percebe que está vencendo etapas, encontra dificuldade crescente e recebe uma tela de vitória ao final, o que torna a experiência mais completa para uma entrega acadêmica.

### Uso de IA generativa

Utilizamos Claude (Anthropic) durante o desenvolvimento para acelerar a implementação. Cada prompt foi enviado, analisado e o código gerado foi revisado antes de ser commitado.

Bugs encontrados foram resolvidos pelos membros do grupo. Os prompts utilizados estão documentados em `docs/prompts_ia.md`.

Estimativa: aproximadamente 70% do código foi gerado ou sugerido com auxílio de IA, enquanto 30% foi escrito ou modificado manualmente. A estrutura geral, as decisões de arquitetura e o debugging foram conduzidos pelos autores.

### Créditos de assets

Por enquanto, todos os elementos visuais são placeholders coloridos gerados pelo PyGame.

Sprites e sons reais podem ser incorporados em versões futuras. Caso assets externos sejam adicionados, terão crédito apropriado.

### Licença

Projeto acadêmico - uso educacional.
