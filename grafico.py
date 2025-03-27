import pandas as pd
import matplotlib.pyplot as plt
from database import conectar_db 
from db_funcoes import dadosparaografico

def criargrafico():
    
    conexao = conectar_db()

    query = dadosparaografico()
    df = pd.read_sql(query, conexao)

    conexao.close()

    # Converter a coluna 'data' para datetime
    df['last_updated'] = pd.to_datetime(df['last_updated'])

    # Criar gráfico
    plt.figure(figsize=(12, 8))
    for produto, dados_produto in df.groupby('id_produto'):
        plt.plot(dados_produto['last_updated'], dados_produto['price_promotion'], marker="o", label=produto)

    plt.xlabel("Data") # Nomeia o eixo X como "Data"
    plt.ylabel("Preço (R$)") # Nomeia o eixo Y como "Preço (R$)"
    plt.title("Variação de Preços dos Produtos") # Define o título do gráfico
    plt.legend(["Luva","iPhone 16","S23","TV SANSUNG"])# Adiciona uma legenda com os nomes dos produtos.
    plt.grid() # Adiciona uma grade ao gráfico para facilitar a leitura.
    plt.xticks(rotation=45) # Rotaciona as datas no eixo X para melhor visualização.
    plt.show()

# Se o arquivo for executado diretamente, exibe o gráfico
if __name__ == "__main__":
    criargrafico()