import yagmail
import os
from dotenv import load_dotenv 


# Carregar o arquivo .env
load_dotenv("infos.env")

def PrecoBaixou(nome):

    email = os.getenv("EMAIL")
    senha = os.getenv("EMAILSENHA")

    yag = yagmail.SMTP(email, senha)
    yag.send(to="emaildestiono@gmail.com", subject="Preço Atualizado!", contents=f"O preço do item{nome} mudou, confira agora!")

    return None
