# dados.py


def carregar_instancias():
    """Retorna instâncias pequenas, conflitantes e sem solução para os experimentos."""
    return {
        "1_pequena": {
            "estado_inicial": ("A", None),
            "destino": "C",
            "coordenadas": {"A": (0, 0), "B": (3, 4), "C": (6, 8)},
            "conexoes": {
                "A": [("B", "Linha 1", 10)],
                "B": [("A", "Linha 1", 10), ("C", "Linha 1", 10)],
                "C": [("B", "Linha 1", 10)],
            },
            "vel_max": 1.0,
            "custo_baldeacao": 15,
        },
        "2_media_conflito": {
            "estado_inicial": ("A", None),
            "destino": "D",
            "coordenadas": {
                "A": (0, 0),
                "B": (10, 0),
                "C": (10, 10),
                "D": (20, 10),
            },
            "conexoes": {
                "A": [("B", "Linha 1", 15), ("C", "Linha 2", 40)],
                "B": [("A", "Linha 1", 15), ("C", "Linha 1", 20)],
                "C": [
                    ("A", "Linha 2", 40),
                    ("B", "Linha 1", 20),
                    ("D", "Linha 2", 15),
                ],
                "D": [("C", "Linha 2", 15)],
            },
            "vel_max": 1.5,
            "custo_baldeacao": 20,
        },
        "3_sem_solucao": {
            "estado_inicial": ("A", None),
            "destino": "C",
            "coordenadas": {"A": (0, 0), "B": (5, 5), "C": (20, 20)},
            "conexoes": {
                "A": [("B", "Linha 1", 10)],
                "B": [("A", "Linha 1", 10)],
                "C": [],
            },
            "vel_max": 1.0,
            "custo_baldeacao": 10,
        },
    }
