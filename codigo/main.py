# main.py
from buscas import (
    busca_a_estrela,
    busca_em_largura,
    busca_em_profundidade,
    busca_menor_numero_baldeacoes,
    busca_menor_tempo,
)
from dados import carregar_instancias


def resumir_resultado(resultado):
    """Converte um resultado de busca em uma linha curta para a tabela."""
    if resultado["caminho"] is None:
        caminho = resultado["status"]
    else:
        caminho = " -> ".join(
            f"{estacao}/{linha or '-'}"
            for estacao, linha in resultado["caminho"]
        )

    return {
        "status": resultado["status"],
        "caminho": caminho,
        "custo": resultado["custo_solucao"],
        "passos": resultado["passos"],
        "tempo_viagem": resultado["tempo_viagem"],
        "baldeacoes": resultado["baldeacoes"],
        "gerados": resultado["nos_gerados"],
        "expandidos": resultado["nos_expandidos"],
        "tempo_execucao": resultado["tempo_execucao"],
    }


def imprimir_resultado(nome, resultado):
    """Imprime caminho, status e todas as métricas de uma busca."""
    resumo = resumir_resultado(resultado)
    print(f"{nome}: {resumo['status']}")
    print(f"  Caminho: {resumo['caminho']}")
    print(f"  Custo do critério: {resumo['custo']}")
    print(f"  Tempo de viagem: {resumo['tempo_viagem']}")
    print(f"  Baldeações: {resumo['baldeacoes']}")
    print(f"  Passos: {resumo['passos']}")
    print(
        f"  Nós gerados: {resumo['gerados']} | "
        f"Nós expandidos: {resumo['expandidos']}"
    )
    print(f"  Tempo de execução: {resumo['tempo_execucao']:.6f} segundos")


def imprimir_tabela(resultados):
    """Imprime uma tabela comparativa com números produzidos pela execução."""
    cabecalho = (
        f"{'Estratégia':<12} {'Status':<15} {'Custo':>8} {'Passos':>8} "
        f"{'Tempo':>8} {'Bald.':>7} {'Gerados':>9} {'Expandidos':>11}"
    )
    print(cabecalho)
    print("-" * len(cabecalho))
    for nome, resultado in resultados:
        resumo = resumir_resultado(resultado)
        print(
            f"{nome:<12} {resumo['status']:<15} "
            f"{str(resumo['custo']):>8} {str(resumo['passos']):>8} "
            f"{str(resumo['tempo_viagem']):>8} "
            f"{str(resumo['baldeacoes']):>7} "
            f"{resumo['gerados']:>9} {resumo['expandidos']:>11}"
        )


def executar_experimentos():
    """Executa BFS, DFS e A* em todas as instâncias e imprime a tabela."""
    instancias = carregar_instancias()
    resultados_por_instancia = {}

    for nome, grafo in instancias.items():
        estado_inicial = grafo["estado_inicial"]
        destino = grafo["destino"]
        resultados = [
            ("BFS", busca_em_largura(estado_inicial, destino, grafo)),
            ("DFS", busca_em_profundidade(estado_inicial, destino, grafo)),
            ("A*", busca_a_estrela(estado_inicial, destino, grafo)),
        ]
        resultados_por_instancia[nome] = resultados

        print(f"\n{'=' * 80}\nInstância: {nome}\n{'=' * 80}")
        imprimir_tabela(resultados)
        for estrategia, resultado in resultados:
            imprimir_resultado(estrategia, resultado)

    return resultados_por_instancia


def comparar_tempo_e_baldeacoes():
    """Compara, no cenário conflitante, menor tempo e menor número de baldeações."""
    grafo = carregar_instancias()["2_media_conflito"]
    estado_inicial = grafo["estado_inicial"]
    destino = grafo["destino"]
    menor_tempo = busca_menor_tempo(estado_inicial, destino, grafo)
    menos_baldeacoes = busca_menor_numero_baldeacoes(
        estado_inicial, destino, grafo
    )

    print(f"\n{'=' * 80}\nComparação do Tema 6\n{'=' * 80}")
    imprimir_resultado("Menor tempo", menor_tempo)
    imprimir_resultado("Menos baldeações", menos_baldeacoes)
    print(
        "\nInterpretação: o menor tempo pode exigir uma baldeação; "
        "o menor número de baldeações pode aceitar um tempo maior."
    )

    return menor_tempo, menos_baldeacoes


if __name__ == "__main__":
    executar_experimentos()
    comparar_tempo_e_baldeacoes()
