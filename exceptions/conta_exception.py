# exceptions/conta_exception.py
class ValidacaoContaException(Exception):
    """Exception base para todos os erros de validação de conta."""
    
    def __init__(self, correlation_id: str, mensagem: str, conta_origem: int = None, conta_destino: int = None):
        self.correlation_id = correlation_id
        self.mensagem = mensagem
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        super().__init__(self.mensagem)