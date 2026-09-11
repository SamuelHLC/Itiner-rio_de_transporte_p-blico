#main.py
def executar_experimentos():
    # Executa as duas estratégias de busca em todas as instâncias e imprime a instrumentação no terminal.
    instancias = carregar_instancias()
    
    for nome, grafo in instancias.items():
        print(f"\n{'='*40}\nInstância: {nome}\n{'='*40}")
        estado_inicial = ("A", None)
        # O destino é C nas instâncias 1 e 3, e D na instância 2
        destino = "C" if nome != "2_media_baldeacao" else "D"
        
        print("--- Busca em Largura (BFS) ---")
        resultado_bfs = busca_em_largura(estado_inicial, destino, grafo)
        imprimir_resultado(resultado_bfs)
        
        print("\n--- Busca A* ---")
        resultado_a_estrela = busca_a_estrela(estado_inicial, destino, grafo)
        imprimir_resultado(resultado_a_estrela)

def imprimir_resultado(resultado):
    # Formata a impressão legível do caminho encontrado e das métricas, ou avisa se não houver solução.
    if resultado is None:
        print("Resultado: Nenhuma solução encontrada.")
    else:
        print(f"Caminho: {resultado['caminho']}")
        print(f"Custo total: {resultado['custo_solucao']}")
        print(f"Número de passos: {resultado['passos']}")
        print(f"Nós gerados: {resultado['nos_gerados']} | Nós expandidos: {resultado['nos_expandidos']}")
        print(f"Tempo de execução: {resultado['tempo_execucao']:.6f} segundos")

# Executa o laço principal de testes
executar_experimentos()
