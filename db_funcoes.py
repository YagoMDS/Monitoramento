import psycopg2
from database import conectar_db

# Insere dados na tabela PRECO
def insertpreco(*args):

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

        return print("Inserção realizada com sucesso!\n")
    
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados: {e}")
        return None
    
# Insere dados na tabela PRECO
def insertproduto(*args):

    conexao = conectar_db()
    if not conexao:
        return

    try:
        cur = conexao.cursor()

        query = "INSERT INTO produtos(codproduto, name) VALUES (%s, %s)" 
        cur.execute(query, args)

        conexao.commit()  # Confirma a transação
        cur.close()
        conexao.close()

        return print("Inserção realizada com sucesso!\n")
    
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados: {e}")
        return None
    
def consultaProdutos():
     
    conexao = conectar_db()
    if not conexao:
        return

    try:
        cur = conexao.cursor()

        query = f"SELECT id, codproduto, name FROM produtos" 
        cur.execute(query)

        produtos = cur.fetchall()


        cur.close()
        conexao.close()

        return produtos
    
    except psycopg2.Error as e:
        print(f"Erro ao buscar os dados: {e}")
        return None
    
def dadosparaografico():

    query = "SELECT " \
        "p.id_produto, " \
        "prod.codproduto, " \
        "p.price_default, " \
        "p.price_promotion, " \
        "p.last_updated " \
        "FROM precos p " \
        "INNER JOIN produtos prod " \
        "ON p.id_produto = prod.id "\
        "ORDER BY id_produto, last_updated;"
    
    return query


def buscaUltimos(id):

    conexao = conectar_db()
    if not conexao:
        return

    try:
        cur = conexao.cursor()

        query = f"SELECT p.id_produto as ID, prod.name as Nome, p.price_promotion as Promocao, p.last_updated as DataAtualizacao FROM precos as p INNER JOIN produtos as prod ON p.id_produto = prod.id WHERE prod.id = {id} ORDER BY SEQUENCIAL DESC LIMIT 1;"
        cur.execute(query)

        ultimos = cur.fetchall()


        cur.close()
        conexao.close()

        return ultimos
    
    except psycopg2.Error as e:
        print(f"Erro ao buscar os ultimos dados: {e}")
        return None