from src.contas_saldo import ContasSaldo
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