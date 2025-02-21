import requests
import os
from dotenv import load_dotenv 

# Carregar o arquivo .env
load_dotenv("infos.env")

def GerarToken():

    url = "https://api.mercadolibre.com/oauth/token"

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
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Garante que não houve erro na requisição
        os.system('cls')

        return response.json()  # Retorna como JSON (dicionário Python)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def main():
    response = GerarToken()

    if response and "refresh_token" in response:
        token = response["refresh_token"]  # Pega o token diretamente do JSON
        print(f"Token gerado: {token}")
    else:
        print("Erro ao gerar o token.")

main()