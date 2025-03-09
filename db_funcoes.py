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

        return print("Inserção realizada com sucesso!")
    
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

        return print("Inserção realizada com sucesso!")
    
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