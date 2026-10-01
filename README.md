# Projeto N1: Itinerário de Transporte Público

**Curso:** Sistemas de Informação — 8º semestre
**Disciplina:** Inteligência Artificial
**Tema:** 6 — Itinerário de transporte público

## 1. Objetivo

O projeto modela uma rede de transporte público como um problema de busca em espaço de estados. O passageiro parte de uma estação, percorre conexões de diferentes linhas e precisa chegar ao destino.

O código compara busca em largura (BFS), busca em profundidade (DFS) e busca A*. Também executa o experimento específico do Tema 6: comparar o trajeto de menor tempo com o trajeto de menor número de baldeações.

## 2. Integrantes e divisão de autoria

| Integrante | Arquivos e funções sob responsabilidade |
| :--- | :--- |
| Samuel Henrique | `codigo/modelo.py`: representação do estado, `gerar_sucessores`, custos de transição e heurística; `codigo/dados.py`: instâncias |
| Marcelo Vaz | `codigo/buscas.py`: `busca_em_largura`, `busca_em_profundidade` e estruturas FIFO/LIFO |
| Gabriel Yan | `codigo/buscas.py`: `busca_a_estrela`, critérios de custo e métricas; `codigo/main.py` e `codigo/experimentos.py`: execução e tabela |



## 3. PEAS e classificação do ambiente

### PEAS

- **P — Desempenho:** minimizar o custo do itinerário; registrar tempo de viagem, número de baldeações, passos, nós gerados, nós expandidos e tempo de execução.
- **E — Ambiente:** rede de estações conectadas por linhas, com tempo de viagem e penalidade de baldeação.
- **A — Atuadores:** deslocar-se para uma estação vizinha usando uma linha disponível.
- **S — Sensores:** estação atual, linha atual e conhecimento da rede de conexões.

### Sete propriedades do ambiente

1. **Totalmente observável:** a rede, as conexões, os tempos e o destino são conhecidos pelo programa.
2. **Agente único:** há apenas um passageiro sendo roteado.
3. **Determinístico:** a mesma estação, linha e ação produzem a mesma próxima situação.
4. **Sequencial:** cada deslocamento altera a estação e a linha disponíveis para os próximos passos.
5. **Estático:** a rede não muda enquanto a busca é executada.
6. **Discreto:** estações, linhas, ações e estados são enumeráveis.
7. **Conhecido:** as regras e os efeitos das conexões são fornecidos antes da busca.

O agente é **baseado em objetivos**: ele planeja uma sequência de ações até uma estação destino, em vez de reagir somente à percepção atual.

## 4. Formulação do problema

- **Estado:** tupla `(estação, linha)`. Por exemplo, `("C", "Linha 2")` representa o passageiro na estação C usando a Linha 2.
- **Estado inicial:** definido em cada instância, atualmente `("A", None)`.
- **Função sucessora:** `gerar_sucessores` retorna as estações vizinhas alcançáveis e o custo da transição.
- **Teste de objetivo:** o estado é objetivo quando sua estação é igual ao destino da instância.
- **Custo de caminho:** no experimento principal, é o tempo de viagem mais a penalidade de baldeação. O código também calcula separadamente tempo puro e quantidade de baldeações.

## 5. Estratégias implementadas

- **BFS:** usa `deque` e `popleft()`, explorando os estados em ordem de descoberta. Encontra o menor número de transições, mas não necessariamente o menor tempo.
- **DFS:** usa uma lista e `pop()`, aprofundando um ramo por vez. Não garante o menor caminho ou menor custo.
- **A*:** usa `heapq` e a prioridade `f(n) = g(n) + h(n)`. Para tempo, a heurística é a distância euclidiana dividida pela velocidade máxima. Para número de baldeações, a heurística é zero, pois o objetivo é minimizar somente as trocas de linha.

O controle de estados descobertos impede ciclos. No A*, `melhor_custo` mantém o menor custo conhecido para cada estado e descarta entradas obsoletas da fila de prioridade.

## 6. Experimento específico do Tema 6

A instância `2_media_conflito` foi construída para produzir objetivos diferentes:

- o trajeto de menor tempo passa por `A -> B -> C -> D`, leva 50 unidades de tempo e possui uma baldeação;
- o trajeto com menos baldeações passa por `A -> C -> D`, possui zero baldeações, mas leva 55 unidades de tempo.

O programa informa os dois resultados e permite discutir se o usuário prefere chegar mais rápido ou evitar a troca de linha.

## 7. Instâncias

As instâncias ficam em `codigo/dados.py`:

1. `1_pequena`: rede simples com uma linha.
2. `2_media_conflito`: rede com duas linhas e conflito entre tempo e baldeações.
3. `3_sem_solucao`: destino isolado, usada para testar o encerramento correto sem solução.

## 8. Métricas

- **Nós gerados:** estados inseridos na fronteira.
- **Nós expandidos:** estados retirados da fronteira e processados.
- **Custo do critério:** custo usado pela estratégia selecionada.
- **Tempo de viagem:** soma dos tempos das conexões, sem penalidade.
- **Baldeações:** quantidade de trocas de linha.
- **Custo com baldeação:** tempo de viagem mais `quantidade de baldeações × custo da baldeação`.
- **Passos:** quantidade de transições do caminho.
- **Tempo de execução:** tempo medido com `time.perf_counter()`.

Mesmo quando não existe solução, a saída informa o status, os nós gerados, os nós expandidos e o tempo de execução.

## 9. Como executar

Na raiz do projeto:

```bash
python codigo/main.py
```

Para executar somente o script de experimentos:

```bash
python codigo/experimentos.py
```

Não são necessárias bibliotecas externas. O projeto usa apenas a biblioteca padrão do Python (`math`, `time`, `heapq` e `collections`).

## 10. Estrutura dos arquivos

```text
codigo/
├── buscas.py          # BFS, DFS, A*, critérios e métricas
├── dados.py           # instâncias de teste
├── experimentos.py    # script que reproduz a tabela
├── main.py            # execução e apresentação dos resultados
└── modelo.py          # sucessores, custos, validações e heurística
```

O pacote final da disciplina ainda deve incluir externamente `artigo.pdf` e `apresentacao.pdf`, além deste código e README.

## 11. Declaração de uso de IA

Foi utilizada uma ferramenta de inteligência artificial como apoio à revisão, organização e correção do código e deste README. O grupo executou o programa, conferiu as métricas, verificou as transições das instâncias e é responsável por compreender e explicar todo o material entregue.

## 12. Checklist antes da entrega

- [ ] Executar `python codigo/main.py` em uma máquina limpa.
- [ ] Conferir a tabela comparativa e os números medidos na execução.
- [ ] Conferir o experimento de menor tempo versus menor número de baldeações.
- [ ] Inserir o artigo científico em `artigo.pdf`.
- [ ] Inserir a apresentação em `apresentacao.pdf`.
- [ ] Ensaiar a explicação da função sucessora, do laço de busca e do controle de estados.
