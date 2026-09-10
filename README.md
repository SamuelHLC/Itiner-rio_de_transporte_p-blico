# Projeto N1: Itinerário de Transporte Público (Agentes de IA)

**Curso:** Sistemas de Informação (8º Semestre)  
**Disciplina:** Inteligência Artificial  
**Tema:** 6 — Itinerário de transporte público  

---

## 1. Integrantes e Divisão de Autoria

> *Esta seção define a atribuição individual para a arguição oral.*

| Integrante | Responsabilidade no Código / Módulos |
| :--- | :--- |
| **[Samuel Henrique]** | Modelagem do estado `(estação, linha)`, Função Sucessora e Heurística |
| **[Marcelo Vaz]** | Busca em Largura (BFS) e Estruturas da Fronteira (deque) |
| **[Samuel/Marcelo]** | Busca A*, Instrumentação (Métricas) e Script de Experimentos |

---

## 2. Propriedades do Ambiente (PEAS)

* **P (Desempenho):** Minimizar tempo total de viagem e/ou quantidade de baldeações.
* **E (Ambiente):** Rede de transporte com estações, conexões por linha e penalidades.
* **A (Atuadores):** Mover para estação seguinte na mesma linha ou trocar de linha.
* **S (Sensores):** Estação atual, linha atual e tempo decorrido.

---

## 3. Instruções de Execução

```bash
python codigo/main.py
