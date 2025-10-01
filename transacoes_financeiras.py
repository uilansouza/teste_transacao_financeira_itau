from acessa_dados import AcessoDados
from exceptions.valida_valor_exception import ValorInvalidoException
from exceptions.conta_exception import (
    ContasIguaisException,
    ContaOrigemInexistenteException,
    ContaDestinoInexistenteException,
    ValidacaoContaException
)   
class TransacaoFinanceira(AcessoDados):
    def __init__(self):
        super().__init__()

    def transferir(self, correlation_id: str, conta_origem: int, conta_destino: int, valor: float) -> None:
        try:
            self.valida_valor(correlation_id, valor)
            conta_saldo_origem, conta_saldo_destino  = self.valida_conta(correlation_id, conta_origem, conta_destino)
            if conta_saldo_origem.saldo < valor:
                print(f"Transacao numero {correlation_id} foi cancelada por falta de saldo")
                return
            conta_saldo_origem.saldo -= valor
            conta_saldo_destino.saldo += valor
            print(f"Transacao numero {correlation_id} foi efetivada com sucesso! Novos saldos: Conta Origem:{conta_saldo_origem.saldo} | Conta Destino: {conta_saldo_destino.saldo}")
        except ContasIguaisException as e:
            print(f"Erro: {e}")
        except ContaOrigemInexistenteException as e:
            print(f"Erro: {e}")
        except ContaDestinoInexistenteException as e:
            print(f"Erro: {e}")
        except ValidacaoContaException as e:
            print(f"Erro de validação: {e}")
        except Exception as e:
            print(f"Transacao numero {correlation_id} falhou por erro inesperado: {e}")

    

    def valida_conta(self, correlation_id: str, conta_origem: int, conta_destino: int) -> list:
        if conta_origem == conta_destino:
            raise ContasIguaisException(correlation_id, conta_origem, conta_destino)
        conta_saldo_origem = self.get_saldo(conta_origem)
        if conta_saldo_origem is None:
            raise ContaOrigemInexistenteException(correlation_id, conta_origem)
        conta_saldo_destino = self.get_saldo(conta_destino)
        if conta_saldo_destino is None:
            raise ContaDestinoInexistenteException(correlation_id, conta_destino)
        return conta_saldo_origem, conta_saldo_destino
    
    def valida_valor(self, correlation_id: str, valor: float) -> bool:
        if not isinstance(valor, (int, float)):
            raise ValorInvalidoException(
                correlation_id, 
                valor, 
                f"Transacao numero {correlation_id} foi cancelada: valor deve ser int ou float"
            )
        
        if valor <= 0:
            raise ValorInvalidoException(correlation_id, valor)
        
        return True