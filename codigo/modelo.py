#modelo.py
import math

def calcular_heuristica(estacao_atual, destino, coordenadas, velocidade_maxima):
    # Retorna a estimativa admissível de tempo dividindo a distância euclidiana pela velocidade máxima.
    x1, y1 = coordenadas[estacao_atual]
    x2, y2 = coordenadas[destino]
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia / velocidade_maxima

def gerar_sucessores(estado_atual, conexoes, custo_baldeacao):
    # Gera uma lista de estados vizinhos adicionando o custo de viagem e a penalidade por troca de linha.
    estacao_atual, linha_atual = estado_atual
    sucessores = []
    
    if estacao_atual not in conexoes:
        return sucessores
        
    for vizinho, linha_vizinho, tempo in conexoes[estacao_atual]:
        penalidade = custo_baldeacao if (linha_atual is not None and linha_atual != linha_vizinho) else 0
        custo_movimento = tempo + penalidade
        sucessores.append(((vizinho, linha_vizinho), custo_movimento))
        
    return sucessores
