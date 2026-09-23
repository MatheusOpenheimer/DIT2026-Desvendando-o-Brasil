import os
from datetime import datetime

# Garante a existência da pasta 'jogador' no projeto
if not os.path.exists("jogador"):
    os.makedirs("jogador", exist_ok=True)

# Definição dos caminhos para cada arquivo de texto plano (.txt)
CAMINHO_RANKING_BRASIL = os.path.join("jogador", "ranking_brasil.txt")
CAMINHO_ESTATISTICAS = os.path.join("jogador", "estatisticas_brasil.txt")
CAMINHO_FEEDBACKS_SRS = os.path.join("jogador", "feedbacks_srs.txt")
CAMINHO_RANKING_SRS = os.path.join("jogador", "ranking_srs.txt")


# FUNÇÕES DE CRITÉRIO DE ORDENAÇÃO
def regra_ordenacao_brasil(jogador):
    nome, idade, acertos, erros = jogador
    return (-acertos, erros, idade)


def regra_ordenacao_srs(jogador):
    nome, idade, acertos, erros = jogador
    return (-acertos, erros, idade)


# JOGO PRINCIPAL (MODO BRASIL)
def criar_banco():
    arquivos_jogo_brasil = [CAMINHO_RANKING_BRASIL, CAMINHO_ESTATISTICAS]

    for caminho_arquivo in arquivos_jogo_brasil:
        if not os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_txt:
                pass


def salvar_dados(nome_jogador, idade_jogador, total_acertos, total_erros):
    with open(CAMINHO_RANKING_BRASIL, "a", encoding="utf-8") as arquivo_ranking:
        linha_registro = f"{nome_jogador};{int(idade_jogador)};{int(total_acertos)};{int(total_erros)}\n"
        arquivo_ranking.write(linha_registro)


def carregar_ranking():
    if not os.path.exists(CAMINHO_RANKING_BRASIL):
        return []

    lista_jogadores = []

    with open(CAMINHO_RANKING_BRASIL, "r", encoding="utf-8") as arquivo_ranking:
        for linha in arquivo_ranking:
            campos = linha.strip().split(";")

            if len(campos) == 4:
                nome, idade, acertos, erros = campos
                dados_jogador = (nome, int(idade), int(acertos), int(erros))
                lista_jogadores.append(dados_jogador)

    lista_jogadores.sort(key=regra_ordenacao_brasil)

    return lista_jogadores[:10]


def salvar_estatisticas(nome, estatisticas_regioes):
    os.makedirs("jogador", exist_ok=True)
    dados_formatados = ";".join(estatisticas_regioes)
    linha = f"{nome};{dados_formatados}\n"
    
    with open(CAMINHO_ESTATISTICAS, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def carregar_estatisticas():
    if not os.path.exists(CAMINHO_ESTATISTICAS):
        return []
    
    dados = []
    with open(CAMINHO_ESTATISTICAS, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split(";")
            if len(partes) >= 6:
                dados.append(partes[:6]) 
    return dados


# JOGO SANTA RITA DO SAPUCAÍ (SRS)
def criar_banco_srs():
    arquivos_modulo_srs = [CAMINHO_FEEDBACKS_SRS, CAMINHO_RANKING_SRS]

    for caminho_arquivo in arquivos_modulo_srs:
        if not os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_txt:
                pass


def salvar_feedback_srs(nome_jogador, nome_ponto_turistico, texto_avaliacao, estrelas=5):
    """Salva a avaliação e a quantidade de estrelas (1-5) no arquivo .txt."""
    jogador_identificado = nome_jogador if nome_jogador else "Explorador"

    texto_sanitizado = (
        texto_avaliacao.replace("\n", " ")
        .replace("\r", " ")
        .replace(";", ",")
        .strip()
    )
    data_hora_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CAMINHO_FEEDBACKS_SRS, "a", encoding="utf-8") as arquivo_feedback:
        # Formato gravado: Nome;Ponto;Texto;Data;Estrelas
        linha_registro = f"{jogador_identificado};{nome_ponto_turistico};{texto_sanitizado};{data_hora_registro};{int(estrelas)}\n"
        arquivo_feedback.write(linha_registro)


def carregar_feedbacks_srs():
    """Carrega os feedbacks garantindo compatibilidade com registros antigos e novos."""
    if not os.path.exists(CAMINHO_FEEDBACKS_SRS):
        return []

    lista_feedbacks = []

    with open(CAMINHO_FEEDBACKS_SRS, "r", encoding="utf-8") as arquivo_feedback:
        for linha in arquivo_feedback:
            campos = linha.strip().split(";")

            if len(campos) >= 4:
                jogador = campos[0]
                ponto_turistico = campos[1]
                texto = campos[2]
                data_registro = campos[3]
                
                # Se tiver a 5ª coluna de estrelas, lê ela; caso contrário, assume o valor padrão 5
                estrelas = int(campos[4]) if len(campos) >= 5 and campos[4].isdigit() else 5

                dados_feedback = (
                    jogador,
                    ponto_turistico,
                    texto,
                    data_registro,
                    estrelas,
                )
                lista_feedbacks.append(dados_feedback)

    return list(reversed(lista_feedbacks))


def salvar_ranking_srs(nome_jogador, idade_jogador, total_acertos, total_erros):
    jogador_identificado = nome_jogador if nome_jogador else "Explorador"

    with open(CAMINHO_RANKING_SRS, "a", encoding="utf-8") as arquivo_ranking_srs:
        linha_registro = f"{jogador_identificado};{int(idade_jogador)};{int(total_acertos)};{int(total_erros)}\n"
        arquivo_ranking_srs.write(linha_registro)


def carregar_ranking_srs():
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

    lista_jogadores_srs.sort(key=regra_ordenacao_srs)

    return lista_jogadores_srs[:10]