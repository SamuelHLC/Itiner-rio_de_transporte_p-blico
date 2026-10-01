# modelo.py
import math


CRITERIOS_CUSTO = {"tempo", "tempo_com_baldeacao", "baldeacoes"}


def validar_criterio(criterio):
    """Valida o critério usado para ordenar ou medir uma busca."""
    if criterio not in CRITERIOS_CUSTO:
        criterios = ", ".join(sorted(CRITERIOS_CUSTO))
        raise ValueError(f"Critério inválido: {criterio}. Use: {criterios}.")


def validar_problema(estado_inicial, destino, grafo):
    """Valida os dados mínimos do problema antes de iniciar a busca."""
    if not isinstance(grafo, dict):
        raise ValueError("O grafo deve ser um dicionário de configuração.")
    if not isinstance(estado_inicial, tuple) or len(estado_inicial) != 2:
        raise ValueError("O estado inicial deve ser uma tupla (estação, linha).")

    estacao_inicial, _ = estado_inicial
    coordenadas = grafo.get("coordenadas", {})
    conexoes = grafo.get("conexoes", {})
    velocidade = grafo.get("vel_max")

    if estacao_inicial not in coordenadas or estacao_inicial not in conexoes:
        raise ValueError(f"Estação inicial inválida: {estacao_inicial}.")
    if destino not in coordenadas:
        raise ValueError(f"Destino inválido: {destino}.")
    if not isinstance(velocidade, (int, float)) or velocidade <= 0:
        raise ValueError("A velocidade máxima deve ser um número positivo.")
    if grafo.get("custo_baldeacao", 0) < 0:
        raise ValueError("O custo de baldeação não pode ser negativo.")
    for estacao, conexoes_estacao in conexoes.items():
        if estacao not in coordenadas or not isinstance(conexoes_estacao, list):
            raise ValueError(f"Conexões inválidas para a estação {estacao}.")
        for conexao in conexoes_estacao:
            if len(conexao) != 3:
                raise ValueError("Cada conexão deve ter destino, linha e tempo.")
            destino_conexao, linha, tempo = conexao
            if destino_conexao not in coordenadas or not isinstance(linha, str):
                raise ValueError("Conexão contém estação ou linha inválida.")
            if not isinstance(tempo, (int, float)) or tempo <= 0:
                raise ValueError("O tempo de cada conexão deve ser positivo.")


def calcular_heuristica(estacao_atual, destino, coordenadas, velocidade_maxima):
    """Estima o tempo restante pela distância euclidiana e velocidade máxima."""
    x1, y1 = coordenadas[estacao_atual]
    x2, y2 = coordenadas[destino]
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distancia / velocidade_maxima


def calcular_custo_movimento(tempo, houve_baldeacao, custo_baldeacao, criterio):
    """Calcula o custo de uma transição conforme o objetivo da busca."""
    validar_criterio(criterio)
    if criterio == "tempo":
        return tempo
    if criterio == "baldeacoes":
        return int(houve_baldeacao)
    return tempo + (custo_baldeacao if houve_baldeacao else 0)


def gerar_sucessores(
    estado_atual,
    conexoes,
    custo_baldeacao,
    criterio="tempo_com_baldeacao",
):
    """Gera os estados vizinhos e o custo de cada transição."""
    validar_criterio(criterio)
    estacao_atual, linha_atual = estado_atual
    sucessores = []

    if estacao_atual not in conexoes:
        return sucessores

    for vizinho, linha_vizinho, tempo in conexoes[estacao_atual]:
        houve_baldeacao = (
            linha_atual is not None and linha_atual != linha_vizinho
        )
        custo_movimento = calcular_custo_movimento(
            tempo, houve_baldeacao, custo_baldeacao, criterio
        )
        sucessores.append(((vizinho, linha_vizinho), custo_movimento))

    return sucessores


def analisar_caminho(caminho, grafo):
    """Calcula tempo, baldeações e custo combinado de um caminho encontrado."""
    if caminho is None:
        return {
            "tempo_viagem": None,
            "baldeacoes": None,
            "custo_com_baldeacao": None,
        }

    tempo_total = 0
    quantidade_baldeacoes = 0
    conexoes = grafo["conexoes"]
    custo_baldeacao = grafo["custo_baldeacao"]

    for estado_atual, proximo_estado in zip(caminho, caminho[1:]):
        estacao_atual, linha_atual = estado_atual
        estacao_seguinte, linha_seguinte = proximo_estado
        conexao = next(
            (
                item
                for item in conexoes.get(estacao_atual, [])
                if item[0] == estacao_seguinte and item[1] == linha_seguinte
            ),
            None,
        )
        if conexao is None:
            raise ValueError(
                f"Transição inválida no caminho: {estado_atual} -> {proximo_estado}."
            )

        _, _, tempo = conexao
        houve_baldeacao = (
            linha_atual is not None and linha_atual != linha_seguinte
        )
        tempo_total += tempo
        quantidade_baldeacoes += int(houve_baldeacao)

    return {
        "tempo_viagem": tempo_total,
        "baldeacoes": quantidade_baldeacoes,
        "custo_com_baldeacao": tempo_total
        + quantidade_baldeacoes * custo_baldeacao,
    }
