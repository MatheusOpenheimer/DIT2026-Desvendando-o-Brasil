import os
import sqlite3

# Garante que a pasta dados exista no diretório do executável antes de conectar
if not os.path.exists("dados"):
    os.makedirs("dados", exist_ok=True)

banco = os.path.join("dados", "GameData.db")

def criar_banco():
    conexao = sqlite3.connect(banco) #pega a conexao com o banco
    cursor = conexao.cursor() # cria uma variavel pra gerenciar o cursor no banco conectado

    cursor.execute('''CREATE TABLE IF NOT EXISTS ranking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT, idade INTEGER,
                    acertos INTEGER, erros INTEGER,
                    tempo INTEGER)''')

    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS estatisticas_erros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Nome TEXT, Norte INTEGER, Nordeste INTEGER,
                    Centro_oeste INTEGER,
                    Sudeste INTEGER,
                    Sul INTEGER)
    ''')

    conexao.commit()
    conexao.close()

def salvar_dados(nome, idade, acertos, erros, tempo):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    cursor.execute('''INSERT INTO ranking (
                    nome,
                    idade,
                    acertos,
                    erros,
                    tempo)
                    VALUES (?, ?, ?, ?, ?)''',
                    (nome, int(idade), int(acertos), int(erros), int(tempo)))
    conexao.commit()
    conexao.close()

def carregar_ranking():
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    cursor.execute('''SELECT 
                        nome, idade, acertos, erros, tempo 
                        FROM ranking ORDER BY acertos DESC, erros ASC LIMIT 10''') #o SELECT busca dados e deixa na memória temporaria do cursor

        #o fetchall pega o que está na memória temporária do cursor e retorna. Sem select antes daria erro, pois não encontraria nada
    top_jogadores = cursor.fetchall() #retorna umas lista de tuplas, cada linha dentro de uma tupla
    conexao.close()

    return top_jogadores

def salvar_estatisticas(nome, norte, nordeste, centrooeste, sudeste, sul):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    cursor.execute('''INSERT INTO estatisticas_erros (
                        Nome,
                        Norte,
                        Nordeste,
                        Centro_oeste,
                        Sudeste,
                        Sul)
                        VALUES (?,?,?,?,?, ?)''',
                        (nome, int(norte), int(nordeste), int(centrooeste), int(sudeste), int(sul)))
    conexao.commit()
    conexao.close()

def carregar_estatisticas():
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    cursor.execute('''SELECT 
                    Nome, Norte, Nordeste, Centro_oeste, Sudeste, Sul
                    FROM estatisticas_erros ORDER BY id DESC''')
    estatisticas = cursor.fetchall()
    conexao.close()
    return estatisticas