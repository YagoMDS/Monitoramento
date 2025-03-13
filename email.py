import yagmail
import os
from dotenv import load_dotenv 


load_dotenv()  # Carrega as variáveis do .env

def PrecoBaixou():

    email = os.getenv("EMAIL")
    senha = os.getenv("EMAIL_SENHA")

    yag = yagmail.SMTP(email, senha)
    yag.send("yagomds2000@gmail.com", "Preço Atualizado!", "O preço caiu, confira agora!")