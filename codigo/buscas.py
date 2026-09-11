#buscas.py
import time
import heapq
from collections import deque

def busca_em_largura(estado_inicial, destino, grafo):
    # Explora o grafo nivel por nivel usando uma fila (deque) para encontrar o caminho com menos arestas.
    tempo_inicio = time.time()
    fronteira = deque([(estado_inicial, [estado_inicial], 0)])
    visitados = set([estado_inicial])
    nos_gerados = 1
    nos_expandidos = 0
    
    while fronteira:
        estado_atual, caminho, custo_acumulado = fronteira.popleft()
        estacao_atual, _ = estado_atual
        nos_expandidos += 1
        
        if estacao_atual == destino:
            return formatar_saida(caminho, custo_acumulado, nos_gerados, nos_expandidos, tempo_inicio)
            
        for vizinho, custo_mov in gerar_sucessores(estado_atual, grafo["conexoes"], grafo["custo_baldeacao"]):
            if vizinho not in visitados:
                visitados.add(vizinho)
                nos_gerados += 1
                fronteira.append((vizinho, caminho + [vizinho], custo_acumulado + custo_mov))
                
    return None

def busca_a_estrela(estado_inicial, destino, grafo):
    # Encontra o caminho de menor custo total usando uma fila de prioridade guiada pela função f(n) = g(n) + h(n).
    tempo_inicio = time.time()
    contador = 0 
    fronteira = []
    heapq.heappush(fronteira, (0, 0, contador, estado_inicial, [estado_inicial]))
    visitados = {}
    nos_gerados = 1
    nos_expandidos = 0
    
    while fronteira:
        _, custo_g, _, estado_atual, caminho = heapq.heappop(fronteira)
        estacao_atual, _ = estado_atual
        
        if estado_atual in visitados and visitados[estado_atual] <= custo_g:
            continue
            
        visitados[estado_atual] = custo_g
        nos_expandidos += 1
        
        if estacao_atual == destino:
            return formatar_saida(caminho, custo_g, nos_gerados, nos_expandidos, tempo_inicio)
            
        for vizinho, custo_mov in gerar_sucessores(estado_atual, grafo["conexoes"], grafo["custo_baldeacao"]):
            novo_custo_g = custo_g + custo_mov
            if vizinho not in visitados or novo_custo_g < visitados[vizinho]:
                nos_gerados += 1
                contador += 1
                heuristica = calcular_heuristica(vizinho[0], destino, grafo["coordenadas"], grafo["vel_max"])
                custo_f = novo_custo_g + heuristica
                heapq.heappush(fronteira, (custo_f, novo_custo_g, contador, vizinho, caminho + [vizinho]))
                
    return None

def formatar_saida(caminho, custo, gerados, expandidos, tempo_inicio):
    # Empacota os contadores obrigatórios da instrumentação em um dicionário para leitura simplificada.
    return {
        "caminho": caminho,
        "custo_solucao": custo,
        "passos": len(caminho) - 1,
        "nos_gerados": gerados,
        "nos_expandidos": expandidos,
        "tempo_execucao": time.time() - tempo_inicio
    }
