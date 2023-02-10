# INF01048 - Turma  A

## Participantes
 - Rodrigo Murillo Boesche       00313543
 - Arthur Loiferman Jawetz       00288612
 
## Algoritmo
Para a implementação da busca para o jogo Othello é utilizado o algoritmo MINIMAX com poda alpha-beta.
A estratégia de parada é composta por uma profundidade variável começando em 5 e aumentada ao longo da partida. Se o jogo contém menos de 30 casas vagas é utilizado a profundidade máxima 6, porém ao longo do jogo – especificamente após sobrarem somente 10 lugares vazios -, o algoritmo consegue processar mais caminhos do algoritmo devido a menor quantidade de jogadas possíveis, incrementado a profundidade máxima de 6. É importante ressaltar que se o tempo de processamento estiver terminando o algoritmo encera o processamento e retorna a melhor jogada calculada até o momento.

## Heurística 
A heurística é baseada em dois fatores: uma tabela estática e no número de peças no tabuleiro do agente. A Tabela estática consiste em atribuir um peso a cada casa do tabuleiro, definindo sua importância para a vitória do jogo. O grupo analisou diversas tabelas (indicadas na referência) para definir quais casa são mais relevantes, sendo, por exemplo, definido que as quinas do tabuleiro são fundamentais para a vitória do jogo. O número de peças do nosso agente comparado ao do oponente tem um fator mais decisivo ao decorrer do jogo, uma vez que as melhores casas são sendo pegas.

## Referência
- Vaishnavi Sannidhanam, Muthukaruppan Annamalai. [An Analysis of Heuristics in Othello](https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf). 
-   Reversi, arminkz [\[Source code\]](https://github.com/arminkz/Reversi).
