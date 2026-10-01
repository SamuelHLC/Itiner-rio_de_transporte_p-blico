# Guia de explicação do projeto

Este documento explica os conceitos utilizados no projeto, o motivo de cada escolha e os pontos que podem ser cobrados na apresentação e na arguição.

Este arquivo é um guia de estudo e documentação complementar. Ele não substitui o artigo científico nem a apresentação exigidos na entrega.

## 1. Problema resolvido

O problema é encontrar um itinerário em uma rede de transporte público. A rede possui:

- estações;
- linhas de transporte;
- conexões entre estações;
- tempo de viagem em cada conexão;
- penalidade quando o passageiro troca de linha.

O projeto foi modelado como busca em espaço de estados porque o passageiro pode estar em diferentes situações e cada deslocamento leva a uma nova situação.

## 2. Agente baseado em objetivos

O programa representa um agente baseado em objetivos. O objetivo é chegar a uma estação destino.

Essa classificação foi usada porque o agente não toma uma decisão isolada apenas olhando para a estação atual. Ele procura uma sequência completa de deslocamentos até atingir a meta.

Um agente reativo simples não seria suficiente, pois ele não compararia caminhos alternativos nem planejaria o custo total da viagem.

## 3. PEAS

### P — Desempenho

O desempenho é avaliado pelo caminho encontrado e pelas métricas da execução:

- tempo total de viagem;
- número de baldeações;
- custo com penalidades;
- número de passos;
- nós gerados;
- nós expandidos;
- tempo de execução.

Essas medidas foram usadas porque um caminho com menos passos não necessariamente é o mais rápido, e um caminho mais rápido pode exigir uma troca de linha.

### E — Ambiente

O ambiente é uma rede fixa de estações e conexões. Cada conexão informa estação de destino, linha utilizada e tempo de viagem.

### A — Atuadores

O atuador do agente é deslocar-se para uma estação vizinha usando uma linha disponível.

### S — Sensores

O programa conhece a estação atual, a linha atual e as conexões disponíveis na rede.

## 4. Sete propriedades do ambiente

1. **Totalmente observável:** o programa conhece a rede, as conexões, os tempos e o destino.
2. **Agente único:** somente um passageiro é roteado.
3. **Determinístico:** uma mesma ação produz sempre a mesma transição.
4. **Sequencial:** cada deslocamento influencia as escolhas seguintes.
5. **Estático:** a rede não se altera durante a execução.
6. **Discreto:** estações, linhas e ações podem ser enumeradas.
7. **Conhecido:** as regras e os custos são informados antes da busca.

Essa classificação justifica o uso de algoritmos de busca determinísticos em um grafo conhecido.

## 5. Formulação em espaço de estados

O projeto segue os cinco componentes da formulação de problemas de busca.

### Estado

O estado é representado por:

```python
(estacao, linha)
```

Exemplo:

```python
("C", "Linha 2")
```

Isso significa que o passageiro está na estação C e está utilizando a Linha 2.

A linha faz parte do estado porque chegar à mesma estação por linhas diferentes muda o custo da próxima ação: trocar de linha pode gerar uma baldeação.

### Estado inicial

Cada instância começa em:

```python
("A", None)
```

O valor `None` representa que o passageiro ainda não está utilizando uma linha antes do primeiro deslocamento.

### Função sucessora

A função `gerar_sucessores` procura todas as conexões que saem da estação atual e cria os próximos estados possíveis.

Ela também calcula se houve troca de linha e define o custo da transição conforme o critério escolhido:

- `tempo`: considera somente o tempo da conexão;
- `tempo_com_baldeacao`: soma tempo e penalidade de troca;
- `baldeacoes`: considera somente se houve troca de linha.

### Teste de objetivo

O estado é considerado objetivo quando sua estação é igual ao destino. A linha atual não precisa ser igual a nenhuma linha específica.

### Custo de caminho

O projeto mede três custos diferentes:

1. tempo puro de viagem;
2. tempo mais penalidade de baldeação;
3. quantidade de baldeações.

Essa separação permite cumprir a exigência específica do Tema 6, que pede a comparação entre menor tempo e menor número de baldeações.

## 6. Representação dos dados

As instâncias ficam em `codigo/dados.py`.

O dicionário de conexões tem este formato:

```python
"A": [("B", "Linha 1", 15)]
```

Isso representa uma conexão da estação A para a estação B, usando a Linha 1, com tempo 15.

Essa estrutura foi escolhida porque permite consultar diretamente os vizinhos de uma estação e evita bibliotecas externas de grafos.

## 7. Busca em largura — BFS

A BFS usa uma fila FIFO implementada com `deque`.

```python
estado = fronteira.popleft()
```

`popleft()` retira o estado mais antigo. Por isso, a BFS explora primeiro todos os estados mais rasos e depois avança para níveis mais profundos.

### Por que foi usada

A BFS é uma busca não informada exigida pelo conteúdo da disciplina. Ela permite comparar o menor número de transições com os custos obtidos pelas outras estratégias.

### Garantia

A BFS encontra o caminho com menor número de passos quando todas as ações têm o mesmo custo. Como as conexões deste projeto possuem tempos diferentes, ela não garante o menor tempo.

## 8. Busca em profundidade — DFS

A DFS usa uma lista como pilha LIFO.

```python
estado = fronteira.pop()
```

`pop()` retira o último estado inserido. Assim, a busca aprofunda um ramo antes de explorar as alternativas.

### Por que foi usada

A DFS também é uma busca não informada ensinada na disciplina. Ela permite mostrar que uma estratégia pode encontrar uma solução válida sem encontrar a melhor solução.

### Limitação

A DFS não garante o menor número de passos nem o menor custo. A ordem dos sucessores pode fazer com que ela encontre primeiro um caminho mais longo.

## 9. Busca A*

A* usa uma fila de prioridade implementada com `heapq`. A prioridade é:

```text
f(n) = g(n) + h(n)
```

- `g(n)` é o custo acumulado desde o início;
- `h(n)` é a estimativa do custo restante;
- `f(n)` é a prioridade total do estado.

### Por que foi usada

A* é uma busca informada exigida pelo projeto. Ela utiliza conhecimento sobre a distância até o destino e tende a expandir menos estados que uma busca sem informação.

### Heurística

Para objetivos relacionados a tempo, a heurística é:

```text
distância euclidiana / velocidade máxima
```

Ela é admissível nas instâncias utilizadas porque estima um limite inferior do tempo restante. A penalidade de baldeação não reduz o custo real, portanto ignorá-la na heurística não faz a estimativa ultrapassar o custo verdadeiro.

Para o objetivo de minimizar baldeações, a heurística é zero. Nesse caso, o A* funciona como uma busca de custo uniforme sobre o número de trocas.

## 10. Fronteira e estados descobertos

### Fronteira

A fronteira contém estados gerados que ainda aguardam expansão.

- BFS: `deque` com `popleft()`;
- DFS: lista com `pop()`;
- A*: lista de prioridade com `heapq.heappop()`.

### Estados descobertos

O conjunto `descobertos` impede inserir repetidamente o mesmo estado na BFS e na DFS.

Sem esse controle, as conexões de retorno poderiam produzir ciclos como:

```text
A -> B -> A -> B -> A
```

No A*, o dicionário `melhor_custo` guarda o menor custo conhecido para cada estado e descarta caminhos piores para o mesmo estado.

## 11. Reconstrução do caminho

Cada item da fronteira guarda a lista completa do caminho até aquele estado:

```python
caminho + [vizinho]
```

Quando o destino é encontrado, essa lista já contém a sequência de estados desde a origem.

Essa decisão simplifica a implementação e facilita a explicação em sala. O custo é que várias listas de caminho podem ocupar mais memória do que uma estrutura separada de predecessores.

## 12. Controle de casos-limite

O código trata os seguintes casos:

- destino inalcançável;
- estação inicial inválida;
- destino inexistente;
- conexões malformadas;
- tempo de conexão inválido;
- velocidade máxima inválida;
- custo de baldeação negativo;
- limite máximo de expansões.

Na instância `3_sem_solucao`, todas as estratégias terminam e informam os nós gerados e expandidos, em vez de executar indefinidamente.

## 13. Experimento do Tema 6

Na instância `2_media_conflito` existem duas escolhas relevantes:

| Critério | Caminho | Tempo | Baldeações |
| :--- | :--- | ---: | ---: |
| Menor tempo | A → B → C → D | 50 | 1 |
| Menos baldeações | A → C → D | 55 | 0 |

O resultado mostra que a melhor rota depende da medida de desempenho escolhida. Um usuário com urgência pode preferir 50 unidades de tempo; outro pode preferir evitar a baldeação mesmo levando 5 unidades a mais.

## 14. Métricas da execução

- **Nós gerados:** estados inseridos na fronteira.
- **Nós expandidos:** estados retirados da fronteira e processados.
- **Passos:** quantidade de transições do caminho.
- **Tempo de viagem:** soma dos tempos das conexões.
- **Baldeações:** quantidade de trocas de linha.
- **Custo com baldeação:** tempo mais penalidades.
- **Tempo de execução:** duração medida pelo relógio de alta resolução.

Os números da tabela devem ser obtidos executando `codigo/experimentos.py`, não digitados manualmente.

## 15. O que cada integrante deve saber explicar

### Samuel Henrique

- por que o estado possui estação e linha;
- como `gerar_sucessores` identifica uma baldeação;
- como a heurística é calculada;
- por que a heurística não deve superestimar o custo.

### Marcelo Vaz

- diferença entre fila e pilha;
- efeito de `popleft()` e `pop()`;
- diferença entre estado descoberto e expandido;
- motivo do conjunto `descobertos`.

### Gabriel Yan

- significado de `g`, `h` e `f` no A*;
- funcionamento do `heapq`;
- diferença entre nós gerados e expandidos;
- comparação entre tempo e baldeações.

## 16. O que deve estar no README?

O enunciado exige que o README contenha principalmente:

- instruções de execução;
- PEAS;
- divisão de autoria;
- declaração de uso de IA.

O enunciado também exige que o código tenha comentários ou documentação de uma linha por função.

Não há uma exigência explícita dizendo que toda a explicação linha a linha, todos os pseudocódigos e toda a justificativa técnica precisam estar no README.

Essas explicações são exigidas principalmente na seção de implementação do artigo e na leitura de código durante a apresentação. Este arquivo serve para organizar o estudo e pode ser mantido como documentação complementar.

## 17. Arquivos que ainda serão entregues externamente

O pacote final da disciplina deve incluir:

```text
codigo/
README.md
artigo.pdf
apresentacao.pdf
```

Este guia não substitui `artigo.pdf` nem `apresentacao.pdf`.
