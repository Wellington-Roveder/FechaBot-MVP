import unittest
from unittest.mock import patch

import pandas as pd

from reader.excel_reader import ExcelReader


class ExcelReaderTests(unittest.TestCase):
    def setUp(self):
        self.reader = ExcelReader()

    def test_processar_dados_soma_todas_as_categorias(self):
        dados = pd.DataFrame(
            [
                {"Produto": "Fit 1/2", "Quantidade Vendida": 2},
                {"Produto": "FIT tradicional", "Quantidade Vendida": 3},
                {"Produto": "Pollo 1/2", "Quantidade Vendida": 4},
                {"Produto": "Pollo inteiro", "Quantidade Vendida": 5},
                {"Produto": "Sobrecoxa 1/2", "Quantidade Vendida": 6},
                {"Produto": "Sobrecoxa inteira", "Quantidade Vendida": 7},
                {"Produto": "Mix", "Quantidade Vendida": 8},
                {"Produto": "Asa", "Quantidade Vendida": 9},
                {"Produto": "Produto não reconhecido", "Quantidade Vendida": 100},
            ]
        )

        self.assertEqual(
            self.reader.processar_dados(dados),
            {
                "meia_fit": 2,
                "inteira_fit": 3,
                "meia_pollo": 4,
                "inteira_pollo": 5,
                "meia_sobrecoxa": 6,
                "inteira_sobrecoxa": 7,
                "mix": 8,
                "asa": 9,
            },
        )

    def test_processar_dados_retorna_none_quando_coluna_obrigatoria_falta(self):
        dados = pd.DataFrame({"Produto": ["Fit"]})

        self.assertIsNone(self.reader.processar_dados(dados))

    @patch("reader.excel_reader.pd.read_excel")
    def test_ler_arquivo_retorna_dataframe(self, read_excel):
        esperado = pd.DataFrame({"Produto": ["Mix"], "Quantidade Vendida": [2]})
        read_excel.return_value = esperado

        resultado = self.reader.ler_arquivo("vendas.xlsx")

        read_excel.assert_called_once_with("vendas.xlsx")
        self.assertIs(esperado, resultado)

    @patch("reader.excel_reader.pd.read_excel", side_effect=ValueError("arquivo inválido"))
    def test_ler_arquivo_retorna_none_em_erro_de_leitura(self, read_excel):
        self.assertIsNone(self.reader.ler_arquivo("vendas.xlsx"))
        read_excel.assert_called_once_with("vendas.xlsx")


if __name__ == "__main__":
    unittest.main()
