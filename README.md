# 8-Puzzle — Busca em Espaço de Estados

Implementação em Python dos algoritmos BFS, DFS e A* para resolver o 8-Puzzle,
usando o template da atividade de Serginho Tanaka.

## Executar

Requer Python 3.10 ou superior. A execução usa apenas a biblioteca padrão.

```bash
python main.py
```

O programa executa os três algoritmos e mostra os movimentos, o custo, a
profundidade, os nós expandidos, os nós gerados e o tamanho máximo da fronteira.

## Tabuleiro e movimentos

O tabuleiro é uma tupla de nove números. O valor `0` representa o espaço vazio.
O objetivo é chegar a `(1, 2, 3, 4, 5, 6, 7, 8, 0)`.

As ações `UP`, `DOWN`, `LEFT` e `RIGHT` indicam o movimento do espaço vazio.
Cada movimento tem custo 1. Para experimentar outro tabuleiro, altere a variável
`initial` em `main.py`.

## Algoritmos

| Algoritmo | Funcionamento |
| --- | --- |
| BFS | Usa uma fila e encontra uma solução com o menor número de movimentos. |
| DFS | Usa uma pilha e busca até o limite de profundidade, que por padrão é 50. |
| A* | Usa uma fila de prioridade com o custo acumulado mais a distância Manhattan. |

A DFS pode encontrar um caminho mais longo que a BFS e o A*. Ela permite
revisitar um tabuleiro quando ele é alcançado em uma profundidade menor.

A distância Manhattan soma as distâncias de cada peça até sua posição final,
sem incluir o espaço vazio. É uma heurística admissível, então o A* também
encontra uma solução com o menor número de movimentos. A classe `AStar` aceita
uma função heurística opcional no construtor.

Quando a busca termina sem solução, o resultado tem `found=False`, uma lista
de ações vazia e custo -1. No caso da DFS, isso também pode indicar que a solução
exige uma profundidade maior que o limite configurado.

## Métricas

- Nós expandidos: estados cujos vizinhos foram gerados.
- Nós gerados: inclui o estado inicial e todos os vizinhos produzidos, mesmo os repetidos que são descartados.
- Fronteira máxima: maior quantidade de entradas aguardando processamento na fila, pilha ou fila de prioridade.
- Profundidade: quantidade de movimentos do estado inicial até a solução.

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes verificam movimentos válidos, reconstrução de caminhos, soluções
mínimas, limites da DFS, heurística, métricas e um tabuleiro sem solução.

## Estrutura

```
├── puzzle/
│   ├── state.py
│   ├── result.py
│   └── base_search.py
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   └── a_star.py
├── tests/
│   └── test_search.py
├── main.py
└── pyproject.toml
```

As interfaces originais de `puzzle/base_search.py` e `puzzle/result.py` foram
preservadas.
