from functools import wraps
def transacao_segura(func):
    """Decorator para tornar o processamento de transações resiliente"""
    @wraps(func)
    def wrapper(executor, item):
        try:
            # Verifica campos mínimos
            campos_necessarios = ["correlation_id", "conta_origem", "conta_destino", "VALOR"]
            for campo in campos_necessarios:
                if campo not in item:
                    raise KeyError(f"Campo '{campo}' não encontrado")
            
            return func(executor, item)
            
        except KeyError as e:
            correlation_id = item.get("correlation_id", "ID_DESCONHECIDO")
            print(f"❌ Transação {correlation_id} ignorada: {e}")
            return None
        except Exception as e:
            correlation_id = item.get("correlation_id", "ID_DESCONHECIDO")
            print(f"⚠️ Erro inesperado na transação {correlation_id}: {e}")
            return None
    return wrapper

@transacao_segura
def processar_transacao(executor, item):
    executor.transferir(
        item["correlation_id"],
        item["conta_origem"],
        item["conta_destino"],
        item["VALOR"]
    )