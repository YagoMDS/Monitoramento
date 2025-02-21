import requests
import os
import json
from dotenv import load_dotenv 

# Carregar o arquivo .env
load_dotenv("infos.env")

def ConsultarPreco():

    url = "https://api.mercadolibre.com/items/MLB3930037419/prices"
    headers = {
    'Authorization': f'Bearer {os.getenv('ML_ACCESS_TOKEN')}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print("Erro ao buscar o produto")
        return None
    

def GerarToken():

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
        os.system('cls')

        return response.json()  # Retorna como JSON (dicionário Python)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição:")
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

    response_item = ConsultarPreco()
    
    if response_item is None:
        return
    else:
        standard = []
        for price in response_item["prices"]:
            if price["type"] == "standard": 
                standard.append(price["amount"])
                standard = str(standard[0])

        promotion = []
        for price in response_item["prices"]:
            if price["type"] == "promotion":
                promotion.append(price["amount"])
                promotion = str(promotion[0])

        print(promotion) # preço promocional
        print(standard) # valor indicado pelo vendedor sem promoções
    
main()