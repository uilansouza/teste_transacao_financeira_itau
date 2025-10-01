import unittest
from src.transacoes_financeiras import TransacaoFinanceira
from src.exceptions.conta_exception import ValidacaoContaException
from src.contas_saldo import ContasSaldo

class TestValidarSaldo(unittest.TestCase):
    
    def setUp(self):
        self.transacao = TransacaoFinanceira()
    
    def test_validar_saldo_suficiente(self):
        """Testa quando há saldo suficiente"""
        correlation_id = "200"
        conta_origem = ContasSaldo(938485762, 180)  # Saldo: 180
        valor = 100  # Valor menor que saldo
        
        # Não deve lançar exceção
        self.transacao._validar_saldo(correlation_id, conta_origem, valor)
    
    def test_validar_saldo_exato(self):
        """Testa quando valor é exatamente igual ao saldo"""
        correlation_id = "201"
        conta_origem = ContasSaldo(938485762, 180)  # Saldo: 180
        valor = 180  # Valor igual ao saldo
        
        # Não deve lançar exceção
        self.transacao._validar_saldo(correlation_id, conta_origem, valor)
    
    def test_validar_saldo_insuficiente(self):
        """Testa quando saldo é insuficiente"""
        correlation_id = "202"
        conta_origem = ContasSaldo(938485762, 180)  # Saldo: 180
        valor = 200  # Valor maior que saldo
        
        with self.assertRaises(ValidacaoContaException) as context:
            self.transacao._validar_saldo(correlation_id, conta_origem, valor)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertIn("saldo insuficiente", context.exception.mensagem)
        self.assertIn("Saldo atual: 180", context.exception.mensagem)
        self.assertIn("valor solicitado: 200", context.exception.mensagem)
        self.assertEqual(context.exception.conta_origem, conta_origem.conta)
    
    def test_validar_saldo_conta_zero(self):
        """Testa quando conta tem saldo zero"""
        correlation_id = "203"
        conta_origem = ContasSaldo(2147483649, 0)  # Saldo: 0
        valor = 50  # Qualquer valor positivo
        
        with self.assertRaises(ValidacaoContaException) as context:
            self.transacao._validar_saldo(correlation_id, conta_origem, valor)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertIn("saldo insuficiente", context.exception.mensagem)
        self.assertIn("Saldo atual: 0", context.exception.mensagem)
    
    def test_validar_saldo_valor_muito_alto(self):
        """Testa quando valor é muito superior ao saldo"""
        correlation_id = "204"
        conta_origem = ContasSaldo(573659065, 787)  # Saldo: 787
        valor = 5000  # Valor muito maior
        
        with self.assertRaises(ValidacaoContaException) as context:
            self.transacao._validar_saldo(correlation_id, conta_origem, valor)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertIn("saldo insuficiente", context.exception.mensagem)
        self.assertIn("Saldo atual: 787", context.exception.mensagem)
        self.assertIn("valor solicitado: 5000", context.exception.mensagem)