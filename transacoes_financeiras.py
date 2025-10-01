from acessa_dados import AcessoDados
from exceptions.valida_valor_exception import ValorInvalidoException
from exceptions.conta_exception import ValidacaoContaException

class TransacaoFinanceira(AcessoDados):
    def __init__(self):
        super().__init__()

    def transferir(self, correlation_id: str, conta_origem: int, conta_destino: int, valor: float) -> None:
        try:
            self._validar_valor(correlation_id, valor)
            conta_saldo_origem, conta_saldo_destino = self._validar_contas(correlation_id, conta_origem, conta_destino)
            self._validar_saldo(correlation_id, conta_saldo_origem, valor)
            
            # Efetivar transação
            conta_saldo_origem.saldo -= valor
            conta_saldo_destino.saldo += valor
            
            print(f"Transacao numero {correlation_id} foi efetivada com sucesso! "
                  f"Novos saldos: Conta Origem: {conta_saldo_origem.saldo} | "
                  f"Conta Destino: {conta_saldo_destino.saldo}")
                  
        except (ValorInvalidoException, ValidacaoContaException) as e:
            print(f"Transacao numero {correlation_id} cancelada: {e}")
        except Exception as e:
            print(f"Transacao numero {correlation_id} falhou por erro inesperado: {e}")

    def _validar_contas(self, correlation_id: str, conta_origem: int, conta_destino: int) -> tuple:
        """Valida as contas e retorna os objetos ContasSaldo."""
        if conta_origem == conta_destino:
            raise ValidacaoContaException(
                correlation_id,
                "contas de origem e destino sao iguais",
                conta_origem,
                conta_destino
            )
        
        conta_saldo_origem = self.get_saldo(conta_origem)
        if conta_saldo_origem is None:
            raise ValidacaoContaException(
                correlation_id,
                "conta origem inexistente",
                conta_origem,
                conta_destino
            )
        
        conta_saldo_destino = self.get_saldo(conta_destino)
        if conta_saldo_destino is None:
            raise ValidacaoContaException(
                correlation_id, 
                "conta destino inexistente",
                conta_origem,
                conta_destino
            )
        
        return conta_saldo_origem, conta_saldo_destino

    def _validar_valor(self, correlation_id: str, valor: float) -> bool:
        """Valida o valor da transação."""
        if not isinstance(valor, (int, float)):
            raise ValorInvalidoException(
                correlation_id, 
                valor, 
                f"valor deve ser int ou float"
            )
        
        if valor <= 0:
            raise ValorInvalidoException(
                correlation_id, 
                valor, 
                f"valor deve ser positivo"
            )
        
        return True

    def _validar_saldo(self, correlation_id: str, conta_origem, valor: float) -> None:
        """Valida se há saldo suficiente na conta origem."""
        if conta_origem.saldo < valor:
            raise ValidacaoContaException(
                correlation_id,
                f"saldo insuficiente. Saldo atual: {conta_origem.saldo}, valor solicitado: {valor}",
                conta_origem.conta
            )