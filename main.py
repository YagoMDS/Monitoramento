import requests
import time
import os
import psycopg2
from dotenv import load_dotenv 

# Carregar o arquivo .env
load_dotenv("infos.env")

def conectar_db():

    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        return conn
    except Exception as e:
        print(f"Erro na conexão com o banco de dados: {e}")
        return None

# Gera um novo Token para consulta na API
def GerarToken():
    os.system('cls')
    url_token = "https://api.mercadolibre.com/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": os.getenv("ML_CLIENT_ID"),  # Pegando de variável de ambiente
        "client_secret": os.getenv("ML_CLIENT_SECRET"),
        "refresh_token": os.getenv("ML_REFRESH_TOKEN")
    }
    headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url_token, headers=headers, data=payload)
        response.raise_for_status()  # Garante que não houve erro na requisição

        return response.json()  # Retorna como JSON (dicionário Python)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição:")
        return None

    
# Realiza uma consulta dos detalhes do produto
def ConsultaItemDetalhes(produto_id):
    url = f"https://api.mercadolibre.com/items/{produto_id}"
    token = os.getenv('ML_ACCESS_TOKEN')
    headers = {'Authorization': f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        detalhes_produto = response.json()
        if detalhes_produto is None:
            return 
        else:
            title = detalhes_produto["title"]
            last_updated = detalhes_produto["last_updated"]
            last_updated = last_updated[0:10]
        return title, last_updated
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar o produto: {e}")
        return None
    
# Realiza uma consulta dos preços do produto
def ConsultarPrecoPromoc(produto_id):

    url = f"https://api.mercadolibre.com/items/{produto_id}/prices"
    token = os.getenv('ML_ACCESS_TOKEN')
    headers = {'Authorization': f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar o produto: {e}")
        return None
    
# Insere dados na tabela 
def insert(*args):

    conexao = conectar_db()
    if not conexao:
        return

    try:
        cur = conexao.cursor()

        query = "INSERT INTO precos(id_produto, price_default, price_promotion, last_updated) VALUES (%s, %s, %s, %s)" 
        cur.execute(query, args)

        conexao.commit()  # Confirma a transação
        cur.close()
        conexao.close()

        return print("Inserção realizada com sucesso!")
    
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados: {e}")
        return None

    

def main():
    response_token = GerarToken()

    if response_token and "refresh_token" in response_token:
        token = response_token["refresh_token"]  # Pega o token diretamente do JSON
        print(f"Token gerado: {token}")
    else:
        print("Erro ao gerar o token.")
    
    print()

    if response_token and "access_token" in response_token:
        access_token = response_token["access_token"]  # Pega o access_token diretamente do JSON
        print(f"Access_token: {access_token}")
    else:
        print("Erro ao gerar Access.")

    print()


    produto = "MLB3930037419"
    intervalo = 3600
    promocional = ConsultarPrecoPromoc(produto)
    
    if promocional is None:
        return
    else:
        standard = []
        for price in promocional["prices"]:
            if price["type"] == "standard": 
                standard.append(price["amount"])
                standard = str(standard[0])
        promotion = []
        for price in promocional["prices"]:
            if price["type"] == "promotion":
                promotion.append(price["amount"])
                promotion = str(promotion[0])

    detalhes_produto = ConsultaItemDetalhes(produto)
    """nome_produto = detalhes_produto[0] # Várialvel que pega o nome do produto"""
    last_update = detalhes_produto[1] # Várialvel que pega a última atualização do produto
    
    insert(1,standard, promotion, last_update)

main()