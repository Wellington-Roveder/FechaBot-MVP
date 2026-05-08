import tkinter as tk
from reader.excel_reader import ExcelReader
from tkinter import filedialog as fd
from tkinter import messagebox
import re


class APP:

    def __init__(self):
        self.dados = None
        self.excel_reader = ExcelReader()

        self.janela = tk.Tk()
        self.janela.title("SOMA FRANGO")
        self.janela.geometry("600x400")

        # INPUTS
        tk.Label(text="Insira a Janta").pack(pady=5)
        self.janta_entry = tk.Entry(width=30)
        self.janta_entry.pack(pady=5)

        tk.Label(text="Insira a cortesia").pack(pady=5)
        self.cortesia_entry = tk.Entry(width=30)
        self.cortesia_entry.pack(pady=5)

        tk.Label(text="Insira a Data").pack(pady=5)
        self.data_entry = tk.Entry(width=30)
        self.data_entry.pack(pady=10)

        # BOTÕES
        tk.Button(text="Ler o arquivo", command=self.ler_arquivo).pack(pady=5)
        tk.Button(text="Copiar Mensagem", command=self.inserir_consumo).pack(pady=5)

        self.janela.mainloop()

  

    def ler_arquivo(self):
        path = fd.askopenfilename()
        if not path:
            return

        arquivo = self.excel_reader.ler_arquivo(path)
        if arquivo is None:
            messagebox.showerror("Erro", "Não foi possível ler o arquivo.\nVerifique se o arquivo é um .xlsx válido.")
            return

        self.dados = self.excel_reader.processar_dados(arquivo)
        if self.dados is None:
            messagebox.showerror("Erro", "Coluna não encontrada na planilha.\nVerifique se a planilha está no formato correto.")
            return

        messagebox.showinfo("Arquivo carregado", "Planilha lida com sucesso!")
   

    def validar_data(self, data):
        return bool(re.fullmatch(r'^\d{2}/\d{2}$', data))

    def validar_itens(self, texto):
        if not texto.strip():
            return True, ""

        for item in texto.split(","):
            item = item.strip()
            if not item:
                continue
            if not re.match(r"^[0-9/ a-zA-ZçÇ]+:\d+$", item):
                return False, f"Item inválido: '{item}'\nUse o formato: nome:quantidade"

        return True, ""

  

    def formatar_itens(self, texto):
        if not texto.strip():
            return ""

        resultado = []
        for item in texto.split(","):
            item = item.strip()
            if ":" in item:
                k, v = item.split(":", 1)
                resultado.append(f"{k.strip().capitalize()}: {v.strip()}")

        return "\n".join(resultado)



    def inserir_consumo(self):
        if not self.dados:
            messagebox.showerror("Erro", "Carregue o arquivo primeiro!")
            return

        janta_raw = self.janta_entry.get()
        cortesia_raw = self.cortesia_entry.get()

        ok, erro = self.validar_itens(janta_raw)
        if not ok:
            messagebox.showerror("Erro na Janta", erro)
            return

        ok, erro = self.validar_itens(cortesia_raw)
        if not ok:
            messagebox.showerror("Erro na Cortesia", erro)
            return

        data = self.data_entry.get()
        if not self.validar_data(data):
            messagebox.showerror("Erro", "Data inválida. Use o formato dd/mm")
            return

        janta = self.formatar_itens(janta_raw)
        cortesia = self.formatar_itens(cortesia_raw)

        dados = self.dados.copy()
        dados.update({"janta": janta, "cortesia": cortesia})
        dados = {k: int(v) if isinstance(v, float) else v for k, v in dados.items()}

        mensagem = f"""data {data}
*INTEIRA*
Fit: {dados['inteira_fit']}
Pollo: {dados['inteira_pollo']}
Sobrecoxa: {dados['inteira_sobrecoxa']}
Mix: {dados['mix']}
Asa: {dados['asa']}

*MEIA*
1/2 Pollo: {dados['meia_pollo']}
1/2 fit: {dados['meia_fit']}
1/2 sobrecoxa: {dados['meia_sobrecoxa']}

*JANTA*
{dados['janta']}

*CORTESIA*
{dados['cortesia']}
"""
        try:
            self.janela.clipboard_clear()
            self.janela.clipboard_append(mensagem)
            self.janela.update()
            messagebox.showinfo("Sucesso!", "Relatório gerado e COPIADO!\nAgora é só dar Ctrl+V no WhatsApp.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao copiar: {e}")