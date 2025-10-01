import unittest
from src.transacoes_financeiras import TransacaoFinanceira
from src.exceptions.valida_valor_exception import ValorInvalidoException

class TestValidarValor(unittest.TestCase):
    
    def setUp(self):
        self.transacao = TransacaoFinanceira()
    
    def test_validar_valor_positivo_int(self):
        """Testa valor positivo inteiro (sucesso)"""
        correlation_id = "100"
        valor = 100
        
        result = self.transacao._validar_valor(correlation_id, valor)
        self.assertTrue(result)
    
    def test_validar_valor_positivo_float(self):
        """Testa valor positivo float (sucesso)"""
        correlation_id = "101"
        valor = 150.75
        
        result = self.transacao._validar_valor(correlation_id, valor)
        self.assertTrue(result)
    
    def test_validar_valor_zero(self):
        """Testa valor zero (deve falhar)"""
        correlation_id = "102"
        valor = 0
        
        with self.assertRaises(ValorInvalidoException) as context:
            self.transacao._validar_valor(correlation_id, valor)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertEqual(context.exception.valor, valor)
        self.assertIn("valor deve ser positivo", context.exception.mensagem)
    
    def test_validar_valor_negativo(self):
        """Testa valor negativo (deve falhar)"""
        correlation_id = "103"
        valor = -50
        
        with self.assertRaises(ValorInvalidoException) as context:
            self.transacao._validar_valor(correlation_id, valor)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertEqual(context.exception.valor, valor)
        self.assertIn("valor deve ser positivo", context.exception.mensagem)
    
    def test_validar_valor_string(self):
        """Testa valor como string (deve falhar)"""
        correlation_id = "104"
        valor = "100"
        
        with self.assertRaises(ValorInvalidoException) as context:
            self.transacao._validar_valor(correlation_id, valor)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertEqual(context.exception.valor, valor)
        self.assertIn("valor deve ser int ou float", context.exception.mensagem)
    
    def test_validar_valor_lista(self):
        """Testa valor como lista (deve falhar)"""
        correlation_id = "105"
        valor = [100]
        
        with self.assertRaises(ValorInvalidoException) as context:
            self.transacao._validar_valor(correlation_id, valor)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertEqual(context.exception.valor, valor)
        self.assertIn("valor deve ser int ou float", context.exception.mensagem)
    
    def test_validar_valor_none(self):
        """Testa valor None (deve falhar)"""
        correlation_id = "106"
        valor = None
        
        with self.assertRaises(ValorInvalidoException) as context:
            self.transacao._validar_valor(correlation_id, valor)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertEqual(context.exception.valor, valor)
        self.assertIn("valor deve ser int ou float", context.exception.mensagem)