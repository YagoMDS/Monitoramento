import psycopg2
import os
from dotenv import load_dotenv

load_dotenv("infos.env")

# Conexão com o banco 
def conectar_db():
    os.system('cls')

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
    
def select():
     
    conexao = conectar_db()
    if not conexao:
        return

    try:
        cur = conexao.cursor()

        query = "SELECT id, codproduto, name FROM produtos" 
        cur.execute(query)

        resultado = cur.fetchall()

        print(resultado)

        cur.close()
        conexao.close()

        return print("Seleção realizada com sucesso!")
    
    except psycopg2.Error as e:
        print(f"Erro ao buscar os dados: {e}")
        return None

select()