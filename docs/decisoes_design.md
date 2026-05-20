# Decisões de design

## Formato horizontal

Escolhemos o formato horizontal para diferenciar Fox Crossing do Frogger clássico e reforçar a ideia narrativa de travessia da floresta até a cidade e, finalmente, até a toca. Em vez de apenas subir pela tela, o jogador avança lateralmente, como se estivesse atravessando um caminho urbano.

Essa escolha também facilita a leitura visual da progressão: a raposa começa em uma extremidade e precisa alcançar a zona dourada na outra. O deslocamento horizontal cria uma sensação clara de início, percurso e chegada.

## Divisão em managers

Dividimos responsabilidades em managers para evitar que o `GameState` acumulasse toda a lógica do jogo. O `MapManager` organiza mapa, obstáculos e power-ups; o `ScoreManager` cuida de pontuação e recorde; o `LevelManager` define a dificuldade das fases; e o `TransitionManager` gerencia as transições visuais.

Essa separação torna o código mais fácil de ler, testar e modificar. Também segue o princípio de responsabilidade única, no qual cada classe tem um motivo principal para existir e mudar.

## Máquina de estados

Usamos máquina de estados em vez de várias flags booleanas, como `is_in_menu`, `is_playing` ou `is_paused`, porque cada tela do jogo possui comportamento próprio. Menu, instruções, gameplay, pausa, vitória e game over processam eventos, atualizam lógica e desenham elementos de formas diferentes.

Com estados separados, o loop principal fica simples e cada classe encapsula sua própria lógica. Isso reduz o risco de combinações inválidas de flags e facilita adicionar novas telas, como instruções e pausa.

## Power-ups e habilidade especial

O sistema de power-ups e a habilidade Instinto foram adicionados para diferenciar Fox Crossing de uma recriação genérica de Frogger. O cogumelo, o trevo e o slow-motion criam escolhas estratégicas e momentos de recuperação durante a partida.

Essas mecânicas também tornam o jogo mais interessante para balanceamento. O jogador não depende apenas de reflexos: ele pode usar invencibilidade, ganhar vidas extras e escolher o melhor momento para ativar o Instinto.
