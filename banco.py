import os
from datetime import datetime

# Garante a existência da pasta 'jogador' no projeto
if not os.path.exists("jogador"):
    os.makedirs("jogador", exist_ok=True)

# Definição dos caminhos para cada arquivo de texto plano (.txt)
#Fiz assim pra imitar a lógica de um banco de dados e não ficar baguynçado
CAMINHO_RANKING_BRASIL = os.path.join("jogador", "ranking_brasil.txt")
CAMINHO_ESTATISTICAS_BRASIL = os.path.join("jogador", "estatisticas_brasil.txt")
CAMINHO_FEEDBACKS_SRS = os.path.join("jogador", "feedbacks_srs.txt")
CAMINHO_RANKING_SRS = os.path.join("jogador", "ranking_srs.txt")


#FUNÇÕES DE CRITÉRIO DE ORDENAÇÃO
#Recebe a tupla: (nome, idade, acertos, erros).
    #Retorna a prioridade de ordenação:
      #1º: -acertos -> o sinal de menos inverte para o maior número vir primeiro.
      #2º: erros    -> menor quantidade de erros desempata primeiro.
      #3º: idade    -> menor idade desempata primeiro. (Foco nas crianças)
def regra_ordenacao_brasil(jogador):
    nome, idade, acertos, erros = jogador
    return (-acertos, erros, idade)


def regra_ordenacao_srs(jogador):
    nome, idade, acertos, erros = jogador
    return (-acertos, erros, idade)



#JOGO PRINCIPAL (MODO BRASIL)
def criar_banco():
    #Garante a existência dos arquivos de texto do jogo Brasil sem sobrescrever conteúdos existentes
    arquivos_jogo_brasil = [CAMINHO_RANKING_BRASIL, CAMINHO_ESTATISTICAS_BRASIL]

    for caminho_arquivo in arquivos_jogo_brasil:
        if not os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_txt:
                pass


def salvar_dados(nome_jogador, idade_jogador, total_acertos, total_erros):
   #Grava o registro da partida no arquivo .txt usando ';' como delimitador.
    with open(CAMINHO_RANKING_BRASIL, "a", encoding="utf-8") as arquivo_ranking:
        linha_registro = f"{nome_jogador};{int(idade_jogador)};{int(total_acertos)};{int(total_erros)}\n"
        arquivo_ranking.write(linha_registro)


def carregar_ranking():
    #Lê o arquivo de ranking, ordena usando a função 'regra_ordenacao_brasil' e retorna o Top 10.
    if not os.path.exists(CAMINHO_RANKING_BRASIL):
        return []

    lista_jogadores = []

    with open(CAMINHO_RANKING_BRASIL, "r", encoding="utf-8") as arquivo_ranking:
        for linha in arquivo_ranking:
            campos = linha.strip().split(";")

            # Confirma se a linha tem os 4 campos esperados
            if len(campos) == 4:
                nome, idade, acertos, erros = campos
                dados_jogador = (nome, int(idade), int(acertos), int(erros))
                lista_jogadores.append(dados_jogador)

    # Ordena usando a função
    lista_jogadores.sort(key=regra_ordenacao_brasil)

    return lista_jogadores[:10]


def salvar_estatisticas(nome_jogador,erros_norte,erros_nordeste,erros_centrooeste,erros_sudeste,erros_sul):
    #Salva a quantidade de erros do jogador por região geográfica para fins pedagógicos
    with open(CAMINHO_ESTATISTICAS_BRASIL, "a", encoding="utf-8") as arquivo_estatisticas:
        linha_registro = (
            f"{nome_jogador};{int(erros_norte)};{int(erros_nordeste)};"
            f"{int(erros_centrooeste)};{int(erros_sudeste)};{int(erros_sul)}\n")
        arquivo_estatisticas.write(linha_registro)


def carregar_estatisticas():
    #Lê o histórico de erros geográficos, retornando as jogadas mais recentes primeiro.
    if not os.path.exists(CAMINHO_ESTATISTICAS_BRASIL):
        return []

    historico_estatisticas = []

    with open(CAMINHO_ESTATISTICAS_BRASIL, "r", encoding="utf-8") as arquivo_estatisticas:
        for linha in arquivo_estatisticas:
            campos = linha.strip().split(";")

            if len(campos) == 6:
                nome, norte, nordeste, centro, sudeste, sul = campos
                dados_estatistica = (
                    nome,
                    int(norte),
                    int(nordeste),
                    int(centro),
                    int(sudeste),
                    int(sul),
                )
                historico_estatisticas.append(dados_estatistica)

    # Inverte a lista para que o último registro salvo apareça no topo
    return list(reversed(historico_estatisticas))



#JOGO SANTA RITA DO SAPUCAÍ (SRS)
def criar_banco_srs():
    #Cria os arquivos de texto do módulo de Santa Rita caso ainda não existam.
    arquivos_modulo_srs = [CAMINHO_FEEDBACKS_SRS, CAMINHO_RANKING_SRS]

    for caminho_arquivo in arquivos_modulo_srs:
        if not os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_txt:
                pass


def salvar_feedback_srs(nome_jogador, nome_ponto_turistico, texto_avaliacao):
    #Salva as avaliações dos atrativos turísticos higienizando o texto contra quebras de linha.
    jogador_identificado = nome_jogador if nome_jogador else "Explorador"

    #Substitui quebras de linha e ponto e vírgula para não corromper as colunas do .txt
    texto_sanitizado = (
        texto_avaliacao.replace("\n", " ")
        .replace("\r", " ")
        .replace(";", ",")
        .strip()
    )
    data_hora_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CAMINHO_FEEDBACKS_SRS, "a", encoding="utf-8") as arquivo_feedback:
        linha_registro = f"{jogador_identificado};{nome_ponto_turistico};{texto_sanitizado};{data_hora_registro}\n"
        arquivo_feedback.write(linha_registro)


def carregar_feedbacks_srs():
    #Carrega todos os feedbacks registrados exibindo os mais recentes primeiro.
    if not os.path.exists(CAMINHO_FEEDBACKS_SRS):
        return []

    lista_feedbacks = []

    with open(CAMINHO_FEEDBACKS_SRS, "r", encoding="utf-8") as arquivo_feedback:
        for linha in arquivo_feedback:
            campos = linha.strip().split(";")

            if len(campos) >= 4:
                jogador, ponto_turistico, texto, data_registro = (
                    campos[0],
                    campos[1],
                    campos[2],
                    campos[3],
                )
                dados_feedback = (
                    jogador,
                    ponto_turistico,
                    texto,
                    data_registro,
                )
                lista_feedbacks.append(dados_feedback)

    return list(reversed(lista_feedbacks))


def salvar_ranking_srs(nome_jogador, idade_jogador, total_acertos, total_erros):
    #Salva os pontos do jogo srs
    jogador_identificado = nome_jogador if nome_jogador else "Explorador"

    with open(CAMINHO_RANKING_SRS, "a", encoding="utf-8") as arquivo_ranking_srs:
        linha_registro = f"{jogador_identificado};{int(idade_jogador)};{int(total_acertos)};{int(total_erros)}\n"
        arquivo_ranking_srs.write(linha_registro)


def carregar_ranking_srs():
    #Lê e retorna o Top 10 de srs usando a regra_ordenacao_srs.
    if not os.path.exists(CAMINHO_RANKING_SRS):
        return []

    lista_jogadores_srs = []

    with open(CAMINHO_RANKING_SRS, "r", encoding="utf-8") as arquivo_ranking_srs:
        for linha in arquivo_ranking_srs:
            campos = linha.strip().split(";")

            if len(campos) == 4:
                nome, idade, acertos, erros = campos
                dados_jogador = (nome, int(idade), int(acertos), int(erros))
                lista_jogadores_srs.append(dados_jogador)

    # Ordena com a função dedicada
    lista_jogadores_srs.sort(key=regra_ordenacao_srs)

    return lista_jogadores_srs[:10]