import requests
import time
import os
from db_funcoes import insertpreco, consultaProdutos, insertproduto
from dotenv import load_dotenv 

# Carregar o arquivo .env
load_dotenv("infos.env")

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
def ConsultaItemDetalhes(produto_id, access_token):
    url = f"https://api.mercadolibre.com/items/{produto_id}"
    token = access_token
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
def ConsultarPrecoPromoc(produto_id, access_token):

    url = f"https://api.mercadolibre.com/items/{produto_id}/prices"
    token = access_token
    headers = {'Authorization': f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar o produto: {e}")
        return None
    
# Verifica se o código do produto existe na tabela PRODUTOS 
def verificaCodigo(codprod, nome):

    produto = consultaProdutos()
    
    if not produto:  # Se não encontrar o produto
        # Insere o produto na tabela Produtos e retorna o id
        id_produto = insertproduto(codprod, nome)
        return id_produto
    else:
        print("Produto já existe na tabela")
        return produto[0]  # Retorna o id do produto encontrado

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



    # Consulta todos os produtos da tabela
    produtos = consultaProdutos()

    if not produtos:
        print("Nenhum produto encontrado na tabela.")
        return


     # Para cada produto encontrado na tabela, consulta os detalhes e preços
    for produto in produtos:
        id = produto[0]
        codprod = produto[1]  # O código do produto está na segunda posição
        nome_produto = produto[2]  # O nome do produto está na terceira posição
        
        # Coleta as informações do produto
        detalhes_produto = ConsultaItemDetalhes(codprod, access_token)
        
        if detalhes_produto is None:
            print(f"Erro ao obter detalhes do produto {nome_produto} ({codprod}).")
            continue  # Pula para o próximo produto

        last_update = detalhes_produto[1]  # Última atualização do produto
        
        # Verifica o código do produto e retorna a tupla com o id_produto
        id_produto = verificaCodigo(codprod, nome_produto)
        
        # Coleta os preços promocionais e padrões
        promocional = ConsultarPrecoPromoc(codprod, access_token)
        
        if promocional is None:
            print(f"Erro ao obter preços do produto {nome_produto} ({codprod}). Tentando novamente...")
            continue

        # Preços padrão e promocional
        standard = next((price["amount"] for price in promocional["prices"] if price["type"] == "standard"), "0")
        promotion = next((price["amount"] for price in promocional["prices"] if price["type"] == "promotion"), "0")

        print(f"Produto: {nome_produto}")
        print(f"Preço padrão: {standard} / Preço promocional: {promotion}")
        print(f"Última atualização: {last_update}")

        # Inserir ou atualizar os preços no banco de dados
        insertpreco(id, standard, promotion, last_update)

main()