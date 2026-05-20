## Histórico de uso de IA generativa

Este documento registra como ferramentas de IA generativa foram utilizadas no desenvolvimento de Fox Crossing, conforme exigido pela disciplina Design de Software do Insper.

### Ferramenta utilizada

Claude (Anthropic) - claude.ai

### Metodologia

- Cada funcionalidade foi planejada antes de ser solicitada à IA.
- Os prompts foram estruturados em etapas pequenas e testáveis.
- O código gerado foi revisado e adaptado antes de ser commitado.
- Bugs foram primeiro analisados pelos autores e depois discutidos com a IA quando necessário.

### Funcionalidades desenvolvidas com auxílio de IA

- Menu principal com opções para jogar e acessar instruções, desenvolvido com auxílio de IA seguindo a metodologia descrita acima.
- Tela de instruções explicando controles e mecânicas, desenvolvida com auxílio de IA seguindo a metodologia descrita acima.
- Sistema de 3 fases com dificuldade crescente, desenvolvido com auxílio de IA seguindo a metodologia descrita acima.
- Sistema de vidas, começando com 3 vidas, desenvolvido com auxílio de IA seguindo a metodologia descrita acima.
- Colisão com carros, perda de vida e reposicionamento da raposa no início, desenvolvida com auxílio de IA seguindo a metodologia descrita acima.
- Zona de chegada, representada pela toca dourada, desenvolvida com auxílio de IA seguindo a metodologia descrita acima.
- Tela de Game Over ao perder todas as vidas, desenvolvida com auxílio de IA seguindo a metodologia descrita acima.
- Tela de Vitória ao completar as 3 fases, desenvolvida com auxílio de IA seguindo a metodologia descrita acima.
- Tela de Pausa acionada pela tecla P, desenvolvida com auxílio de IA seguindo a metodologia descrita acima.
- Sistema de pontuação com 100 pontos na fase 1, 200 na fase 2 e 300 na fase 3, desenvolvido com auxílio de IA seguindo a metodologia descrita acima.
- Recorde persistente salvo em `data/highscore.txt`, desenvolvido com auxílio de IA seguindo a metodologia descrita acima.
- Power-ups de cogumelo vermelho (+1 vida) e trevo verde (invencibilidade por 3 segundos), desenvolvidos com auxílio de IA seguindo a metodologia descrita acima.
- Habilidade especial Instinto com slow-motion por 2 segundos e cooldown de 10 segundos, desenvolvida com auxílio de IA seguindo a metodologia descrita acima.
- Transições suaves de fade entre todas as telas, desenvolvidas com auxílio de IA seguindo a metodologia descrita acima.
- HUD completo com vidas, pontos, recorde, fase atual e barra do Instinto, desenvolvido com auxílio de IA seguindo a metodologia descrita acima.

### Decisões manuais (sem IA)

- Definição do conceito do jogo: raposa, tema floresta/cidade e formato horizontal.
- Estrutura geral de pastas e arquivos.
- Escolha de cores e estética.
- Configurações específicas, incluindo velocidades, número de fases e valores de pontuação.
- Debugging e ajustes finais.
- Testes de gameplay e balanceamento.

### Observações

Todo código gerado foi compreendido pelos autores. Bugs gerados por sugestões da IA foram resolvidos por reanálise dos prompts e debugging manual.
