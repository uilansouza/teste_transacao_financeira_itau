import unittest
from unittest.mock import patch
from src.transacoes_financeiras import TransacaoFinanceira
class TestTransferir(unittest.TestCase):
    
    def setUp(self):
        self.transacao = TransacaoFinanceira()
    
    def test_transferir_sucesso(self):
        """Testa transferência bem-sucedida"""
        correlation_id = "300"
        conta_origem = 938485762  # Saldo: 180
        conta_destino = 210385733  # Saldo: 10
        valor = 50
        
        # Captura saldos iniciais
        saldo_origem_inicial = self.transacao.get_saldo(conta_origem).saldo
        saldo_destino_inicial = self.transacao.get_saldo(conta_destino).saldo
        
        # Executa
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica saldos atualizados
        saldo_origem_final = self.transacao.get_saldo(conta_origem).saldo
        saldo_destino_final = self.transacao.get_saldo(conta_destino).saldo
        
        self.assertEqual(saldo_origem_final, saldo_origem_inicial - valor)
        self.assertEqual(saldo_destino_final, saldo_destino_inicial + valor)
        
        # Verifica mensagem de sucesso
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} foi efetivada com sucesso! "
            f"Novos saldos: Conta Origem: {saldo_origem_final} | "
            f"Conta Destino: {saldo_destino_final}"
        )
    
    def test_transferir_valor_invalido_zero(self):
        """Testa transferência com valor zero"""
        correlation_id = "301"
        conta_origem = 938485762
        conta_destino = 210385733
        valor = 0
        
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica mensagem de erro
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} cancelada: valor deve ser positivo"
     
        )
    
    def test_transferir_valor_invalido_negativo(self):
        """Testa transferência com valor negativo"""
        correlation_id = "302"
        conta_origem = 938485762
        conta_destino = 210385733
        valor = -100
        
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica mensagem de erro
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} cancelada: valor deve ser positivo"
     
        )
    
    def test_transferir_contas_iguais(self):
        """Testa transferência para a mesma conta"""
        correlation_id = "303"
        conta_origem = 938485762
        conta_destino = 938485762  # Mesma conta
        valor = 50
        
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica mensagem de erro
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} cancelada: contas de origem e destino sao iguais"
        )
    
    def test_transferir_conta_origem_inexistente(self):
        """Testa transferência com conta origem inexistente"""
        correlation_id = "304"
        conta_origem = 999999999  # Não existe
        conta_destino = 210385733
        valor = 50
        
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica mensagem de erro
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} cancelada: conta origem inexistente"
        )
    
    def test_transferir_conta_destino_inexistente(self):
        """Testa transferência com conta destino inexistente"""
        correlation_id = "305"
        conta_origem = 938485762
        conta_destino = 999999999  # Não existe
        valor = 50
        
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica mensagem de erro
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} cancelada: conta destino inexistente"
        )
    
    def test_transferir_saldo_insuficiente(self):
        """Testa transferência com saldo insuficiente"""
        correlation_id = "306"
        conta_origem = 938485762  # Saldo: 180
        conta_destino = 210385733
        valor = 200  # Maior que saldo
        
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica mensagem de erro
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} cancelada: "
            f"saldo insuficiente. Saldo atual: 180, valor solicitado: 200"
        )
    
    def test_transferir_conta_saldo_zero(self):
        """Testa transferência de conta com saldo zero"""
        correlation_id = "307"
        conta_origem = 2147483649  # Saldo: 0
        conta_destino = 210385733
        valor = 50
        
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica mensagem de erro
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} cancelada: "
            f"saldo insuficiente. Saldo atual: 0, valor solicitado: 50"
        )
    
    @patch.object(TransacaoFinanceira, '_validar_valor')
    def test_transferir_erro_inesperado(self, mock_validar_valor):
        """Testa tratamento de erro inesperado"""
        correlation_id = "308"
        conta_origem = 938485762
        conta_destino = 210385733
        valor = 50
        
        # Simula um erro inesperado
        mock_validar_valor.side_effect = Exception("Erro inesperado no banco de dados")
        
        with patch('builtins.print') as mock_print:
            self.transacao.transferir(correlation_id, conta_origem, conta_destino, valor)
        
        # Verifica mensagem de erro genérico
        mock_print.assert_called_with(
            f"Transacao numero {correlation_id} falhou por erro inesperado: "
            f"Erro inesperado no banco de dados"
        )
    
    def test_transferir_fluxo_completo_saldos_corretos(self):
        """Testa se os saldos são atualizados corretamente em transferência bem-sucedida"""
        correlation_id = "309"
        conta_origem_num = 573659065  # Saldo: 787
        conta_destino_num = 674038564  # Saldo: 400
        valor = 150
        
        # Obtém objetos das contas
        conta_origem = self.transacao.get_saldo(conta_origem_num)
        conta_destino = self.transacao.get_saldo(conta_destino_num)
        
        saldo_origem_inicial = conta_origem.saldo
        saldo_destino_inicial = conta_destino.saldo
        
        # Executa transferência
        self.transacao.transferir(correlation_id, conta_origem_num, conta_destino_num, valor)
        
        # Verifica saldos atualizados
        self.assertEqual(conta_origem.saldo, saldo_origem_inicial - valor)
        self.assertEqual(conta_destino.saldo, saldo_destino_inicial + valor)

if __name__ == '__main__':
    unittest.main()