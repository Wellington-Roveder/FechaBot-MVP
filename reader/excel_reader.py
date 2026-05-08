import pandas as pd
from utils.logger import configurar_logger



logger = configurar_logger()

class ExcelReader:
    


    def ler_arquivo(self,caminho):
        try:
            df = pd.read_excel(caminho)
            logger.info("Sucesso na leitura")
            return df
            #por logger de info aqui
            
        except Exception as e:
            logger.error(f"Erro na leitura do arquivo {e}")
            return None
            
            
            
    def processar_dados(self, df):
        try:
            fit_meia = df[df['Produto'].str.contains('fit', case=False) &   df['Produto'].str.contains('1/2', case=False)]
            pollo_meia = df[df['Produto'].str.contains('pollo', case=False) & df['Produto'].str.contains('1/2', case=False)]
            sobrecoxa_meia = df[df['Produto'].str.contains('sobrecoxa', case=False) & df['Produto'].str.contains('1/2', case=False)]
        
            pollo_inteira = df[df['Produto'].str.contains('pollo', case=False) & ~df['Produto'].str.contains('1/2', case=False)]
            sobrecoxa_inteira = df[df['Produto'].str.contains('sobrecoxa', case=False) & ~df['Produto'].str.contains('1/2', case=False)]
            fit_inteira = df[df['Produto'].str.contains('fit', case=False) & ~df['Produto'].str.contains('1/2', case=False)]

            mix = df[df['Produto'].str.contains('mix', case=False)]
            asa = df[df['Produto'].str.contains('asa', case=False)]

            soma_meia_fit = fit_meia['Quantidade Vendida'].sum()
            soma_meia_pollo = pollo_meia['Quantidade Vendida'].sum()
            soma_meia_sobrecoxa = sobrecoxa_meia['Quantidade Vendida'].sum()

            soma_inteira_fit = fit_inteira['Quantidade Vendida'].sum()
            soma_inteira_pollo = pollo_inteira['Quantidade Vendida'].sum()
            soma_inteira_sobrecoxa = sobrecoxa_inteira['Quantidade Vendida'].sum()
        
            soma_mix = mix['Quantidade Vendida'].sum()
            soma_asa = asa['Quantidade Vendida'].sum()

            dict_soma = {"meia_fit":soma_meia_fit, "inteira_fit":soma_inteira_fit, "meia_pollo":soma_meia_pollo, "inteira_pollo":soma_inteira_pollo, "meia_sobrecoxa":soma_meia_sobrecoxa, "inteira_sobrecoxa":soma_inteira_sobrecoxa, "mix":soma_mix, "asa":soma_asa}
            logger.info("Todos os campos Somados")
            return  dict_soma

        except KeyError as e:
            logger.error(f"Coluna não encontrada na planilha: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao processar dados: {e}") 
            return None   