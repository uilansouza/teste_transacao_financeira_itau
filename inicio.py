from transacoes_financeiras import TransacaoFinanceira

if __name__ == "__main__":
    TRANSACOES = [
        {"correlation_id": 1, "datetime": "09/09/2023 14:15:00", "conta_origem": 938485762, "conta_destino": 214748364777, "VALOR": 100},
        {"correlation_id": 2, "datetime": "09/09/2023 14:15:05", "conta_origem": 2147483649, "conta_destino": 210385733, "VALOR": 149},
        {"correlation_id": 3, "datetime": "09/09/2023 14:15:29", "conta_origem": 347586970, "conta_destino": 238596054, "VALOR": 1100},
        {"correlation_id": 4, "datetime": "09/09/2023 14:17:00", "conta_origem": 675869708, "conta_destino": 210385733, "VALOR": 5300},
        {"correlation_id": 5, "datetime": "09/09/2023 14:18:00", "conta_origem": 238596054, "conta_destino": 674038564, "VALOR": 1489},
        {"correlation_id": 6, "datetime": "09/09/2023 14:18:20", "conta_origem": 573659065, "conta_destino": 563856300, "VALOR": 49},
        {"correlation_id": 7, "datetime": "09/09/2023 14:19:00", "conta_origem": 938485762, "conta_destino": 2147483649, "VALOR": 44},
        {"correlation_id": 8, "datetime": "09/09/2023 14:19:01", "conta_origem": 573659065, "conta_destino": 675869708, "VALOR": 150},
        {"correlation_id": 9, "datetime": "09/09/2023 14:19:02", "conta_origem": 573659077, "conta_destino": 675869722, "VALOR": 150},
    ]

    executor = TransacaoFinanceira()
    for item in TRANSACOES:
        executor.transferir(
            item["correlation_id"],
            item["conta_origem"],
            item["conta_destino"],
            item["VALOR"]
        )
    print("Todas as transacoes foram processadas.")

#aqui tinhamos um problema de concorrência onde 