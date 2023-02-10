### INF01048 turma B

## Participantes

Kairan Mateus Lara Morandin     00275608
Leonardo Droves Silveira        00296968
Pedro Koinaski de Paiva         00302515

## Minimax com poda alpha-beta e limite de profundade


O nosso algoritmo jogador de Othello foi implementado utilizando a busca MINIMAX com poda alpha-beta e limite de profundidade. O nosso limite de profundidade é variável: no início do jogo ele começa com um limite de 5 e aumenta a profundidade ao longo do desenvolvimento da partida caso identifique que a última jogada foi realizada rapidamente. Faltando 20 movimentos, ele começa a dar um "Burst", aumenta em 2 o limite de profundidade caso a jogada tenha ocorrida em menos de 0.3 segundos. Nas jogadas finais, ele procura até o fim do jogo, escolhendo uma joga ótima.


## Heurística

A nossa heurística é baseada em três fatores que têm seus pesos alterados ao longo do desenvolvimento da partida. O primeiro fator é uma tabela de custo estático de cada uma das casas do tabuleiro. O segundo fator é a mobilidade, um valor que compara o número de jogadas possíveis do agente e do oponente, buscando maximizar as nossas jogadas e minimizar as do oponente. O terceiro fator é um valor que compara o número de peças do agente e do oponente no tabuleiro. No início do jogo, o custo estático das casas do tabuleiro é o único que influencia. Com menos de 20 casas livres, o fator de mobilidade começa a ser considerado com 1/3 do peso. Com menos de 10 casas livres o custo das casas para de ser utilizado e começamos a considerar apenas o fator de mobilidade e de número de peças de cada jogador. Esse esquema teve inspiração num artigo que encontramos, o link está no fim do arquivo.


## Referências

Vaishnavi Sannidhanam, Muthukaruppan Annamalai. An Analysis of Heuristics in Othello
Disponível em: https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
