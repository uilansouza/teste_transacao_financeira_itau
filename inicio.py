class ContasSaldo:
    def __init__(self, conta, saldo):
        self.conta = conta
        self.saldo = saldo

class AcessoDados:
    def __init__(self):
        self.tabela_saldos = [
            ContasSaldo(938485762, 180),
            ContasSaldo(347586970, 1200),
            ContasSaldo(2147483649, 0),
            ContasSaldo(675869708, 4900),
            ContasSaldo(238596054, 478),
            ContasSaldo(573659065, 787),
            ContasSaldo(210385733, 10),
            ContasSaldo(674038564, 400),
            ContasSaldo(563856300, 1200),
           
        ]

    def get_saldo(self, id) -> ContasSaldo | None:
        return next((x for x in self.tabela_saldos if x.conta == id), None)

   

class ExecutarTransacaoFinanceira(AcessoDados):
    def transferir(self, correlation_id: str, conta_origem: int, conta_destino: int, valor: float) -> None:
        if not isinstance(valor, (int, float)):
            print(f"Transacao numero {correlation_id} foi cancelada: valor deve ser int ou float")
            return
        if valor <= 0:
            print(f"Transacao numero {correlation_id} foi cancelada: valor invalido")
            return
        if conta_origem == conta_destino:
            print(f"Transacao numero {correlation_id} foi cancelada: contas de origem e destino sao iguais")
            return
        conta_saldo_origem = self.get_saldo(conta_origem)
        if conta_saldo_origem is None:
            print(f"Transacao numero {correlation_id} foi cancelada: conta origem inexistente")
            return
        if conta_saldo_origem.saldo < valor:
            print(f"Transacao numero {correlation_id} foi cancelada por falta de saldo")
            return
        else:
            conta_saldo_destino = self.get_saldo(conta_destino)
            if conta_saldo_destino is None:
                print(f"Transacao numero {correlation_id} foi cancelada: conta destino inexistente")
                return
            conta_saldo_origem.saldo -= valor
            conta_saldo_destino.saldo += valor
            print(f"Transacao numero {correlation_id} foi efetivada com sucesso! Novos saldos: Conta Origem:{conta_saldo_origem.saldo} | Conta Destino: {conta_saldo_destino.saldo}")

if __name__ == "__main__":
    TRANSACOES = [
        {"correlation_id": 1, "datetime": "09/09/2023 14:15:00", "conta_origem": 938485762, "conta_destino": 2147483649, "VALOR": 150},
        {"correlation_id": 2, "datetime": "09/09/2023 14:15:05", "conta_origem": 2147483649, "conta_destino": 210385733, "VALOR": 149},
        {"correlation_id": 3, "datetime": "09/09/2023 14:15:29", "conta_origem": 347586970, "conta_destino": 238596054, "VALOR": 1100},
        {"correlation_id": 4, "datetime": "09/09/2023 14:17:00", "conta_origem": 675869708, "conta_destino": 210385733, "VALOR": 5300},
        {"correlation_id": 5, "datetime": "09/09/2023 14:18:00", "conta_origem": 238596054, "conta_destino": 674038564, "VALOR": 1489},
        {"correlation_id": 6, "datetime": "09/09/2023 14:18:20", "conta_origem": 573659065, "conta_destino": 563856300, "VALOR": 49},
        {"correlation_id": 7, "datetime": "09/09/2023 14:19:00", "conta_origem": 938485762, "conta_destino": 2147483649, "VALOR": 44},
        {"correlation_id": 8, "datetime": "09/09/2023 14:19:01", "conta_origem": 573659065, "conta_destino": 675869708, "VALOR": 150},
        {"correlation_id": 9, "datetime": "09/09/2023 14:19:02", "conta_origem": 573659077, "conta_destino": 675869722, "VALOR": 150},
    ]

    executor = ExecutarTransacaoFinanceira()
    for item in TRANSACOES:
        executor.transferir(
            item["correlation_id"],
            item["conta_origem"],
            item["conta_destino"],
            item["VALOR"]
        )
    print("Todas as transacoes foram processadas.")

#aqui tinhamos um problema de concorrência onde 