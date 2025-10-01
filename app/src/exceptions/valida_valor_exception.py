class ValorInvalidoException(Exception):
    """Exception levantada quando um valor é inválido para operações financeiras."""
    
    def __init__(self, correlation_id: str, valor: float, mensagem: str = None):
        self.correlation_id = correlation_id
        self.valor = valor
        self.mensagem = mensagem or f"Transacao numero {correlation_id} foi cancelada: valor invalido"
        super().__init__(self.mensagem)