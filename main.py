import requests
import os

def GerarToken():

    url = "https://api.mercadolibre.com/oauth/token"

    payload = 'grant_type=refresh_token&client_id=3360521794976032&client_secret=j2Jjei34DEUK1I2kt4ArRfbD5u2mVAkK&refresh_token=TG-67b767e7038f9e0001ae9c83-391581891'
    headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    os.system('cls')

    return(response.text)

def main():
    response = GerarToken()
    token = []

    print()
    print(response)
    
    for i in range(len(response) - 1):  # Garante que podemos acessar i+1
        if response[i] == 'T' and response[i + 1] == 'G' and response[i + 2] == '-':  # Verifica 'T' seguido de 'G'
            token = "".join(response[i + 3:])  # Pega tudo depois de 'TG'
            break  # Para a busca
        
    print(token)


main()