import os
import sqlite3

# Garante que a pasta dados exista no diretório antes de conectar
if not os.path.exists("dados"):
    os.makedirs("dados", exist_ok=True)

# CAMINHOS DOS BANCOS SQLITE
banco = os.path.join("dados", "GameData.db")
banco_srs = os.path.join("dados", "SRSDATA.db")



# JOGO PRINCIPAL (BRASIL)

def criar_banco():
    conexao = sqlite3.connect(banco) #pega a conexao com o banco
    cursor = conexao.cursor() # cria uma variavel pra gerenciar o cursor no banco conectado

    cursor.execute('''CREATE TABLE IF NOT EXISTS ranking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    idade INTEGER,
                    acertos INTEGER,
                    erros INTEGER)''')

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


def salvar_dados(nome, idade, acertos, erros):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    cursor.execute('''INSERT INTO ranking (
                    nome,
                    idade,
                    acertos,
                    erros)
                    VALUES (?, ?, ?, ?)''',
                    (nome, int(idade), int(acertos), int(erros)))
    conexao.commit()
    conexao.close()


def carregar_ranking():
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()

    cursor.execute('''SELECT 
                        nome, idade, acertos, erros
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



# JOGO SANTA RITA DO SAPUCAÍ (SRS)

def criar_banco_srs():
    conexao = sqlite3.connect(banco_srs)
    cursor = conexao.cursor()

    # Tabela de Feedbacks dos Pontos Turísticos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador TEXT,
            ponto_turistico TEXT,
            feedback TEXT,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de Ranking do Quiz de Santa Rita
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ranking_srs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            acertos INTEGER,
            erros INTEGER,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conexao.commit()
    conexao.close()


def salvar_feedback_srs(jogador, ponto_nome, texto):
    if jogador == "":
        jogador = "Explorador"

    conexao = sqlite3.connect(banco_srs)
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO feedbacks (jogador, ponto_turistico, feedback)
        VALUES (?, ?, ?)
    ''', (jogador, ponto_nome, texto))
    conexao.commit()
    conexao.close()


def carregar_feedbacks_srs():
    conexao = sqlite3.connect(banco_srs)
    cursor = conexao.cursor()
    # Garante que a tabela exista antes de consultar
    criar_banco_srs()
    cursor.execute('''
        SELECT jogador, ponto_turistico, feedback, data_registro 
        FROM feedbacks ORDER BY id DESC
    ''')
    dados = cursor.fetchall()
    conexao.close()
    return dados


def salvar_ranking_srs(nome, acertos, erros):
    if nome == "":
        nome = "Explorador"

    conexao = sqlite3.connect(banco_srs)
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO ranking_srs (nome, acertos, erros)
        VALUES (?, ?, ?)
    ''', (nome, int(acertos), int(erros)))
    conexao.commit()
    conexao.close()


def carregar_ranking_srs():
    conexao = sqlite3.connect(banco_srs)
    cursor = conexao.cursor()
    # Garante que a tabela exista antes de consultar
    criar_banco_srs()
    cursor.execute('''
        SELECT nome, acertos, erros 
        FROM ranking_srs 
        ORDER BY acertos DESC, erros ASC 
        LIMIT 10
    ''')
    top_jogadores = cursor.fetchall()
    conexao.close()
    return top_jogadores