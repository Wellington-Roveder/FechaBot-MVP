import unittest
from unittest.mock import Mock, patch

from UI.interface import APP


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        self.app = APP.__new__(APP)

    def test_validar_data_aceita_apenas_mes_e_dia_com_dois_digitos(self):
        self.assertTrue(self.app.validar_data("28/04"))
        self.assertFalse(self.app.validar_data("28/4"))
        self.assertFalse(self.app.validar_data("2024/04"))
        self.assertFalse(self.app.validar_data("28-04"))

    def test_validar_itens_aceita_lista_e_vazio(self):
        self.assertEqual(self.app.validar_itens("pollo:3, mix:4, 1/2 fit:6"), (True, ""))
        self.assertEqual(self.app.validar_itens(""), (True, ""))
        self.assertEqual(self.app.validar_itens("   "), (True, ""))

    def test_validar_itens_rejeita_formato_invalido(self):
        valido, erro = self.app.validar_itens("pollo:3, mix")

        self.assertFalse(valido)
        self.assertIn("mix", erro)

    def test_formatar_itens_normaliza_itens(self):
        self.assertEqual(
            self.app.formatar_itens("pollo:3, mix: 4, 1/2 fit:6"),
            "Pollo: 3\nMix: 4\n1/2 fit: 6",
        )
        self.assertEqual(self.app.formatar_itens(""), "")

    @patch("UI.interface.messagebox.showinfo")
    def test_inserir_consumo_monta_e_copia_relatorio(self, showinfo):
        self.app.dados = {
            "inteira_fit": 3.0,
            "inteira_pollo": 5,
            "inteira_sobrecoxa": 7.0,
            "mix": 8,
            "asa": 9,
            "meia_pollo": 4,
            "meia_fit": 2.0,
            "meia_sobrecoxa": 6,
        }
        self.app.janta_entry = Mock()
        self.app.janta_entry.get.return_value = "pollo:3, mix:4"
        self.app.cortesia_entry = Mock()
        self.app.cortesia_entry.get.return_value = "fit:2"
        self.app.data_entry = Mock()
        self.app.data_entry.get.return_value = "28/04"
        self.app.janela = Mock()

        self.app.inserir_consumo()

        mensagem = self.app.janela.clipboard_append.call_args.args[0]
        self.assertIn("data 28/04", mensagem)
        self.assertIn("Fit: 3", mensagem)
        self.assertIn("Sobrecoxa: 7", mensagem)
        self.assertIn("Pollo: 3\nMix: 4", mensagem)
        self.assertIn("Fit: 2", mensagem)
        self.app.janela.clipboard_clear.assert_called_once_with()
        self.app.janela.update.assert_called_once_with()
        showinfo.assert_called_once()

    @patch("UI.interface.messagebox.showerror")
    def test_inserir_consumo_exige_arquivo_carregado(self, showerror):
        self.app.dados = None

        self.app.inserir_consumo()

        showerror.assert_called_once_with("Erro", "Carregue o arquivo primeiro!")

    @patch("UI.interface.messagebox.showinfo")
    @patch("UI.interface.messagebox.showerror")
    @patch("UI.interface.fd.askopenfilename", return_value="")
    def test_ler_arquivo_ignora_selecao_cancelada(
        self, askopenfilename, showerror, showinfo
    ):
        self.app.excel_reader = Mock()
        self.app.ler_arquivo()

        askopenfilename.assert_called_once_with()
        self.app.excel_reader.ler_arquivo.assert_not_called()
        showerror.assert_not_called()
        showinfo.assert_not_called()


if __name__ == "__main__":
    unittest.main()
