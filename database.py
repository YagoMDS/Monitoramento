import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("infos.env")

# Conexão com o banco 
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