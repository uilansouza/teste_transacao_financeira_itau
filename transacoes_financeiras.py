from acessa_dados import AcessoDados
class TransacaoFinanceira(AcessoDados):
    def __init__(self):
        super().__init__()

    def transferir(self, correlation_id: str, conta_origem: int, conta_destino: int, valor: float) -> None:
        valor_valido = self.valida_valor(correlation_id, valor)
        if not valor_valido:
            return
        conta_saldo_origem, conta_saldo_destino  = self.valida_conta(correlation_id, conta_origem, conta_destino)

        if conta_saldo_origem is None or conta_saldo_destino is None:
            return

        if conta_saldo_origem.saldo < valor:
            print(f"Transacao numero {correlation_id} foi cancelada por falta de saldo")
            return
        conta_saldo_origem.saldo -= valor
        conta_saldo_destino.saldo += valor
        print(f"Transacao numero {correlation_id} foi efetivada com sucesso! Novos saldos: Conta Origem:{conta_saldo_origem.saldo} | Conta Destino: {conta_saldo_destino.saldo}")

    

    def valida_conta(self, correlation_id: str, conta_origem: int, conta_destino: int) -> list:
        if conta_origem == conta_destino:
            print(f"Transacao numero {correlation_id} foi cancelada: contas de origem e destino sao iguais")
            return None, None
        conta_saldo_origem = self.get_saldo(conta_origem)
        if conta_saldo_origem is None:
            print(f"Transacao numero {correlation_id} foi cancelada: conta origem inexistente")
            return None, None
        conta_saldo_destino = self.get_saldo(conta_destino)
        if conta_saldo_destino is None:
            print(f"Transacao numero {correlation_id} foi cancelada: conta destino inexistente")
            return None, None
       
        return conta_saldo_origem, conta_saldo_destino
    
    def valida_valor(self, correlation_id: str, valor: float) -> bool:
        if not isinstance(valor, (int, float)):
            print(f"Transacao numero {correlation_id} foi cancelada: valor deve ser int ou float")
            return False
        if valor <= 0:
            print(f"Transacao numero {correlation_id} foi cancelada: valor invalido")
            return False
        return True