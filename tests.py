import unittest
import os
from unittest.mock import patch, MagicMock
from datetime import date
from main import DOUClient, DOUError

class TestDOUClient(unittest.TestCase):
    def setUp(self):
        self.client = DOUClient()
        # Garantir que o diretório de cache existe
        os.makedirs(".cache", exist_ok=True)
    
    def test_obter_data_sem_parametro(self):
        """Testa a obtenção da data atual quando nenhum parâmetro é fornecido"""
        hoje = date.today()
        ano, mes, dia, data_completa = self.client.obter_data()
        
        self.assertEqual(ano, hoje.strftime("%Y"))
        self.assertEqual(mes, hoje.strftime("%m"))
        self.assertEqual(dia, hoje.strftime("%d"))
        self.assertEqual(data_completa, hoje.strftime("%Y-%m-%d"))
    
    def test_obter_data_com_parametro(self):
        """Testa a obtenção da data a partir de uma string"""
        ano, mes, dia, data_completa = self.client.obter_data("01-02-2023")
        
        self.assertEqual(ano, "2023")
        self.assertEqual(mes, "02")
        self.assertEqual(dia, "01")
        self.assertEqual(data_completa, "2023-02-01")
    
    def test_obter_data_formato_invalido(self):
        """Testa a obtenção da data com formato inválido"""
        with self.assertRaises(ValueError):
            self.client.obter_data("2023-02-01")  # Formato errado
    
    @patch('main.requests.Session')
    def test_get_cookie_sucesso(self, mock_session):
        """Testa a obtenção do cookie com sucesso"""
        # Configura o mock
        mock_instance = mock_session.return_value
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_instance.post.return_value = mock_response
        mock_instance.cookies.get.return_value = "test_cookie"
        
        # Executa o método
        with patch('main.DOU_LOGIN', 'test@example.com'), patch('main.DOU_PASSWORD', 'password'):
            cookie = self.client._get_cookie()
        
        # Verifica o resultado
        self.assertEqual(cookie, "test_cookie")
        mock_instance.post.assert_called_once()
    
    @patch('main.requests.Session')
    def test_get_cookie_sem_credenciais(self, mock_session):
        """Testa a obtenção do cookie sem credenciais configuradas"""
        # Executa o método
        with patch('main.DOU_LOGIN', None), patch('main.DOU_PASSWORD', None):
            with self.assertRaises(DOUError):
                self.client._get_cookie()

if __name__ == '__main__':
    unittest.main()