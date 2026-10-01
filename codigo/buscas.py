# buscas.py
import heapq
import time
from collections import deque

from modelo import (
    analisar_caminho,
    calcular_heuristica,
    gerar_sucessores,
    validar_criterio,
    validar_problema,
)


def formatar_saida(
    caminho,
    custo,
    gerados,
    expandidos,
    tempo_inicio,
    grafo,
    criterio,
    status="solucao",
):
    """Empacota caminho, status, métricas e critérios em um resultado uniforme."""
    metricas_caminho = analisar_caminho(caminho, grafo)
    return {
        "status": status,
        "criterio": criterio,
        "caminho": caminho,
        "custo_solucao": custo,
        "passos": None if caminho is None else len(caminho) - 1,
        "tempo_viagem": metricas_caminho["tempo_viagem"],
        "baldeacoes": metricas_caminho["baldeacoes"],
        "custo_com_baldeacao": metricas_caminho["custo_com_baldeacao"],
        "nos_gerados": gerados,
        "nos_expandidos": expandidos,
        "tempo_execucao": time.perf_counter() - tempo_inicio,
    }


def _preparar_busca(estado_inicial, destino, grafo, criterio):
    """Valida entradas comuns e devolve o critério normalizado."""
    validar_criterio(criterio)
    validar_problema(estado_inicial, destino, grafo)


def busca_em_largura(
    estado_inicial,
    destino,
    grafo,
    criterio="tempo_com_baldeacao",
    limite_expansoes=None,
):
    """Explora níveis com FIFO e encontra o caminho com menos transições."""
    _preparar_busca(estado_inicial, destino, grafo, criterio)
    tempo_inicio = time.perf_counter()
    fronteira = deque([(estado_inicial, [estado_inicial], 0)])
    descobertos = {estado_inicial}
    nos_gerados = 1
    nos_expandidos = 0

    while fronteira:
        estado_atual, caminho, custo_acumulado = fronteira.popleft()
        nos_expandidos += 1

        if estado_atual[0] == destino:
            return formatar_saida(
                caminho,
                custo_acumulado,
                nos_gerados,
                nos_expandidos,
                tempo_inicio,
                grafo,
                criterio,
            )

        if limite_expansoes is not None and nos_expandidos >= limite_expansoes:
            return formatar_saida(
                None,
                None,
                nos_gerados,
                nos_expandidos,
                tempo_inicio,
                grafo,
                criterio,
                status="limite_expansoes",
            )

        for vizinho, custo_movimento in gerar_sucessores(
            estado_atual,
            grafo["conexoes"],
            grafo["custo_baldeacao"],
            criterio,
        ):
            if vizinho not in descobertos:
                descobertos.add(vizinho)
                nos_gerados += 1
                fronteira.append(
                    (
                        vizinho,
                        caminho + [vizinho],
                        custo_acumulado + custo_movimento,
                    )
                )

    return formatar_saida(
        None,
        None,
        nos_gerados,
        nos_expandidos,
        tempo_inicio,
        grafo,
        criterio,
        status="sem_solucao",
    )


def busca_em_profundidade(
    estado_inicial,
    destino,
    grafo,
    criterio="tempo_com_baldeacao",
    limite_expansoes=None,
):
    """Explora um ramo com LIFO e evita revisitar estados descobertos."""
    _preparar_busca(estado_inicial, destino, grafo, criterio)
    tempo_inicio = time.perf_counter()
    fronteira = [(estado_inicial, [estado_inicial], 0)]
    descobertos = {estado_inicial}
    nos_gerados = 1
    nos_expandidos = 0

    while fronteira:
        estado_atual, caminho, custo_acumulado = fronteira.pop()
        nos_expandidos += 1

        if estado_atual[0] == destino:
            return formatar_saida(
                caminho,
                custo_acumulado,
                nos_gerados,
                nos_expandidos,
                tempo_inicio,
                grafo,
                criterio,
            )

        if limite_expansoes is not None and nos_expandidos >= limite_expansoes:
            return formatar_saida(
                None,
                None,
                nos_gerados,
                nos_expandidos,
                tempo_inicio,
                grafo,
                criterio,
                status="limite_expansoes",
            )

        sucessores = gerar_sucessores(
            estado_atual,
            grafo["conexoes"],
            grafo["custo_baldeacao"],
            criterio,
        )
        for vizinho, custo_movimento in reversed(sucessores):
            if vizinho not in descobertos:
                descobertos.add(vizinho)
                nos_gerados += 1
                fronteira.append(
                    (
                        vizinho,
                        caminho + [vizinho],
                        custo_acumulado + custo_movimento,
                    )
                )

    return formatar_saida(
        None,
        None,
        nos_gerados,
        nos_expandidos,
        tempo_inicio,
        grafo,
        criterio,
        status="sem_solucao",
    )


def _heuristica_para_criterio(estado, destino, grafo, criterio):
    """Escolhe uma heurística admissível para cada objetivo de otimização."""
    if criterio == "baldeacoes":
        return 0
    return calcular_heuristica(
        estado[0], destino, grafo["coordenadas"], grafo["vel_max"]
    )


def busca_a_estrela(
    estado_inicial,
    destino,
    grafo,
    criterio="tempo_com_baldeacao",
    limite_expansoes=None,
):
    """Ordena a fronteira por f(n)=g(n)+h(n) para o critério escolhido."""
    _preparar_busca(estado_inicial, destino, grafo, criterio)
    tempo_inicio = time.perf_counter()
    contador = 0
    fronteira = []
    custo_inicial = 0
    heuristica_inicial = _heuristica_para_criterio(
        estado_inicial, destino, grafo, criterio
    )
    heapq.heappush(
        fronteira,
        (
            custo_inicial + heuristica_inicial,
            custo_inicial,
            contador,
            estado_inicial,
            [estado_inicial],
        ),
    )
    melhor_custo = {estado_inicial: custo_inicial}
    nos_gerados = 1
    nos_expandidos = 0

    while fronteira:
        _, custo_g, _, estado_atual, caminho = heapq.heappop(fronteira)
        if custo_g != melhor_custo.get(estado_atual):
            continue

        nos_expandidos += 1
        if estado_atual[0] == destino:
            return formatar_saida(
                caminho,
                custo_g,
                nos_gerados,
                nos_expandidos,
                tempo_inicio,
                grafo,
                criterio,
            )

        if limite_expansoes is not None and nos_expandidos >= limite_expansoes:
            return formatar_saida(
                None,
                None,
                nos_gerados,
                nos_expandidos,
                tempo_inicio,
                grafo,
                criterio,
                status="limite_expansoes",
            )

        for vizinho, custo_movimento in gerar_sucessores(
            estado_atual,
            grafo["conexoes"],
            grafo["custo_baldeacao"],
            criterio,
        ):
            novo_custo_g = custo_g + custo_movimento
            if novo_custo_g >= melhor_custo.get(vizinho, float("inf")):
                continue

            melhor_custo[vizinho] = novo_custo_g
            contador += 1
            heuristica = _heuristica_para_criterio(
                vizinho, destino, grafo, criterio
            )
            heapq.heappush(
                fronteira,
                (
                    novo_custo_g + heuristica,
                    novo_custo_g,
                    contador,
                    vizinho,
                    caminho + [vizinho],
                ),
            )
            nos_gerados += 1

    return formatar_saida(
        None,
        None,
        nos_gerados,
        nos_expandidos,
        tempo_inicio,
        grafo,
        criterio,
        status="sem_solucao",
    )


def busca_menor_tempo(estado_inicial, destino, grafo, limite_expansoes=None):
    """Busca o itinerário com menor tempo de viagem, sem penalidade artificial."""
    return busca_a_estrela(
        estado_inicial,
        destino,
        grafo,
        criterio="tempo",
        limite_expansoes=limite_expansoes,
    )


def busca_menor_numero_baldeacoes(
    estado_inicial, destino, grafo, limite_expansoes=None
):
    """Busca o itinerário com menor número de baldeações."""
    return busca_a_estrela(
        estado_inicial,
        destino,
        grafo,
        criterio="baldeacoes",
        limite_expansoes=limite_expansoes,
    )
