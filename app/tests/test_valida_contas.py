import unittest
from src.transacoes_financeiras import TransacaoFinanceira

from src.exceptions.conta_exception import ValidacaoContaException

class TestValidarContas(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para cada teste"""
        self.transacao = TransacaoFinanceira()
        
    def test_validar_contas_sucesso(self):
        """Testa validação bem-sucedida com contas válidas"""
        # Configura
        correlation_id = "123"
        conta_origem = 938485762
        conta_destino = 347586970
        
        # Executa
        conta_origem_obj, conta_destino_obj = self.transacao._validar_contas(
            correlation_id, conta_origem, conta_destino
        )
        
        # Verifica
        self.assertEqual(conta_origem_obj.conta, conta_origem)
        self.assertEqual(conta_destino_obj.conta, conta_destino)
        self.assertIsNotNone(conta_origem_obj)
        self.assertIsNotNone(conta_destino_obj)
    
    def test_validar_contas_iguais(self):
        """Testa quando conta origem e destino são iguais"""
        # Configura
        correlation_id = "124"
        conta_origem = 938485762
        conta_destino = 938485762
        
        # Executa & Verifica
        with self.assertRaises(ValidacaoContaException) as context:
            self.transacao._validar_contas(correlation_id, conta_origem, conta_destino)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertEqual(context.exception.mensagem, "contas de origem e destino sao iguais")
        self.assertEqual(context.exception.conta_origem, conta_origem)
        self.assertEqual(context.exception.conta_destino, conta_destino)
    
    def test_validar_conta_origem_inexistente(self):
        """Testa quando conta origem não existe"""
        # Configura
        correlation_id = "125"
        conta_origem = 999999999  # Conta que não existe
        conta_destino = 938485762
        
        # Executa & Verifica
        with self.assertRaises(ValidacaoContaException) as context:
            self.transacao._validar_contas(correlation_id, conta_origem, conta_destino)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertEqual(context.exception.mensagem, "conta origem inexistente")
        self.assertEqual(context.exception.conta_origem, conta_origem)
        self.assertEqual(context.exception.conta_destino, conta_destino)
    
    def test_validar_conta_destino_inexistente(self):
        """Testa quando conta destino não existe"""
        # Configura
        correlation_id = "126"
        conta_origem = 938485762
        conta_destino = 999999999  # Conta que não existe
        
        # Executa & Verifica
        with self.assertRaises(ValidacaoContaException) as context:
            self.transacao._validar_contas(correlation_id, conta_origem, conta_destino)
        
        self.assertEqual(context.exception.correlation_id, correlation_id)
        self.assertEqual(context.exception.mensagem, "conta destino inexistente")
        self.assertEqual(context.exception.conta_origem, conta_origem)
        self.assertEqual(context.exception.conta_destino, conta_destino)
    
    def test_validar_ambas_contas_inexistentes(self):
        """Testa quando ambas contas não existem"""
        # Configura
        correlation_id = "127"
        conta_origem = 888888888  # Não existe
        conta_destino = 999999999  # Não existe
        
        # Executa & Verifica
        with self.assertRaises(ValidacaoContaException) as context:
            self.transacao._validar_contas(correlation_id, conta_origem, conta_destino)
        
        # Deve falhar na conta origem primeiro
        self.assertEqual(context.exception.mensagem, "conta origem inexistente")
        self.assertEqual(context.exception.conta_origem, conta_origem)

if __name__ == '__main__':
    unittest.main()