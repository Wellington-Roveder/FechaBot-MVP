# FechaBot

Aplicação desktop para automatizar o fechamento diário de vendas de uma loja de alimentos. O sistema lê uma planilha Excel, consolida as quantidades vendidas por categoria e copia um relatório formatado para envio no WhatsApp.

## Visão geral

O FechaBot reduz o trabalho manual no fechamento da loja:

- leitura de arquivos `.xlsx`;
- consolidação das vendas por produto e modalidade;
- inclusão de itens de janta e cortesia;
- validação dos dados informados na interface;
- geração e cópia do relatório para a área de transferência;
- registro das operações e dos erros em arquivos de log.

O processamento é realizado localmente. As planilhas não são enviadas para nenhum serviço externo pela aplicação.

## Requisitos

- Python 3.9 ou superior;
- Windows, Linux ou macOS com suporte ao Tkinter;
- arquivo Excel `.xlsx` no formato esperado pelo sistema.

No Windows, o Tkinter normalmente já acompanha a instalação oficial do Python. Em distribuições Linux, pode ser necessário instalar o pacote `python3-tk`.

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/Wellington-Roveder/FechaBot-MVP.git
cd FechaBot-MVP
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Com o ambiente virtual ativado, execute:

```bash
python main.py
```

Na interface:

1. Informe os itens de **Janta**, separados por vírgula, no formato `nome:quantidade`.
2. Informe os itens de **Cortesia** no mesmo formato, se necessário.
3. Informe a data no formato `dd/mm`.
4. Clique em **Ler o arquivo** e selecione a planilha do dia.
5. Clique em **Copiar Mensagem**.
6. Cole o relatório no WhatsApp usando `Ctrl+V`.

Os campos de janta e cortesia podem ficar vazios. Exemplos de valores aceitos:

```text
pollo:3, mix:4, 1/2 fit:6
```

## Formato da planilha

A planilha deve conter, no mínimo, as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `Produto` | Nome ou descrição do produto vendido |
| `Quantidade Vendida` | Quantidade total vendida |

A identificação das categorias é feita por texto, sem diferenciar letras maiúsculas e minúsculas. O processamento reconhece:

- produtos `fit`, `pollo` e `sobrecoxa` nas modalidades inteira e meia;
- produtos `mix`;
- produtos `asa`.

Para a classificação como meia, a descrição do produto deve conter `1/2`. Produtos sem essa indicação são tratados como inteiros nas categorias correspondentes.

## Relatório gerado

O relatório é copiado para a área de transferência no seguinte formato:

```text
data 28/04
*INTEIRA*
Fit: 42
Pollo: 89
Sobrecoxa: 15
Mix: 34
Asa: 22

*MEIA*
1/2 Pollo: 67
1/2 fit: 38
1/2 sobrecoxa: 12

*JANTA*
Pollo: 3
Mix: 4
1/2 Fit: 6

*CORTESIA*
Fit: 2
```

## Estrutura do projeto

```text
.
├── assets/                 # Imagens usadas na documentação
├── reader/
│   ├── __init__.py
│   └── excel_reader.py     # Leitura e consolidação dos dados da planilha
├── UI/
│   └── interface.py        # Interface gráfica e validação dos campos
├── utils/
│   └── logger.py           # Configuração dos registros da aplicação
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências Python
└── .gitignore
```

## Funcionamento interno

1. `main.py` instancia a aplicação gráfica.
2. `UI/interface.py` coleta os dados, valida a data e os itens adicionais e controla o fluxo da interface.
3. `reader/excel_reader.py` carrega a planilha com `pandas` e soma as quantidades por categoria.
4. O relatório é montado e copiado para a área de transferência pelo Tkinter.
5. `utils/logger.py` registra leituras, processamento e erros.

## Logs

Os logs são gravados no diretório `logs/`, que é ignorado pelo Git. O logger utiliza rotação diária e mantém os registros recentes para facilitar diagnóstico e suporte.

Erros comuns exibidos pela aplicação:

- arquivo não selecionado ou inválido;
- colunas obrigatórias ausentes;
- data fora do formato `dd/mm`;
- item de janta ou cortesia fora do formato `nome:quantidade`;
- tentativa de gerar o relatório antes de carregar a planilha.

## Distribuição como executável

O projeto pode ser empacotado para distribuição como executável usando uma ferramenta de empacotamento Python, como o PyInstaller. O executável deve ser gerado e testado no mesmo sistema operacional de destino. A configuração de empacotamento não faz parte das dependências de execução listadas em `requirements.txt`.

## Privacidade e dados

Arquivos de planilha, logs, ambientes virtuais, builds e executáveis estão configurados para não serem versionados. Não inclua dados reais de clientes, vendas ou credenciais no repositório.

## Contribuição

Para contribuir:

1. crie uma branch a partir da versão atual;
2. faça uma alteração pequena e específica;
3. valide a execução com uma planilha de teste sem dados sensíveis;
4. descreva no pull request o problema corrigido e como a alteração foi validada.

## Autor

**Wellington Roveder**

- [GitHub](https://github.com/Wellington-Roveder)
- [LinkedIn](https://www.linkedin.com/in/wellington-roveder-04637b37b/)
