import math
import pygame
import config
import os
import sys


def resource_path(relative_path):
  try:
    # O PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")

  return os.path.join(base_path, relative_path)

#REGIÕES-------------------------
norte = (0, 128, 1)
nordeste = (254, 215, 0)
centro_oeste = (255, 69, 0)
sudeste = (30, 144, 255)
sul = (138, 43, 225)

#ESTADOS----------------------------------
amazonas = (2, 98, 8)
para = (128, 254, 4)
mato_grosso = (254, 99, 71)
minas_gerais = (1, 0, 138)
bahia = (209, 180, 140)
sergipe = (245, 206, 165)
alagoas = (220, 174, 114)
tocantins = (148, 99, 15)
goias = (255, 69, 0)
rio_grande_do_sul = (186, 86, 212)
maranhao = (255, 253, 6)
piaui = (135, 206, 234)
mato_grosso_do_sul = (255, 139, 0)
roraima = (108, 143, 25)
rondonia = (63, 224, 208)
sao_paulo = (0, 0, 204)
acre = (2, 127, 129)
amapa = (173, 255, 48)
ceara = (178, 223, 229)
rio_grande_do_norte = (70, 70, 70)
paraiba = (153, 0, 48)
pernambuco = (65, 134, 175)
espirito_santo = (30, 144, 255)
rio_de_janeiro = (0, 3, 252)
distrito_federal = (87, 28, 3)
parana = (138, 43, 225)
santa_catarina = (130, 0, 127)

def checar_cor_proxima(cor_clicada, cor_alvo, margem=17):
        #Funçao que calcula se a cor clicada está dentro da margem de erro da cor alvo.
        
        # Calcula a distância matemática entre as duas cores
        distancia = math.sqrt(
            (cor_clicada[0] - cor_alvo[0])**2 + 
            (cor_clicada[1] - cor_alvo[1])**2 + 
            (cor_clicada[2] - cor_alvo[2])**2
        )
        # Se a cor clicada tiver a distância menor que a margem de cor proxima, retorna True (está perto o suficiente é uma cor parecida)
        return distancia < margem

def obter_regiao_por_cor(rgb):
    #Limpa o clique anterior antes de testar a nova cor pq
    #se não for nenhuma das cores ele continua vazio
    if checar_cor_proxima(rgb, norte):
        return "Norte"
    elif checar_cor_proxima(rgb, nordeste):
        return "Nordeste"
    elif checar_cor_proxima(rgb, centro_oeste):
        return "Centro-Oeste"
    elif checar_cor_proxima(rgb, sudeste):
        return "Sudeste"
    elif checar_cor_proxima(rgb, sul):
        return "Sul"    
        
    return None

def obter_estado_por_cor(rgb):
    # Limpa o clique anterior antes de testar a nova cor pq
    # se não for nenhuma das cores ele continua vazio
    if checar_cor_proxima(rgb, amazonas):
       return "Amazonas"
    elif checar_cor_proxima(rgb, para):
       return "Pará"
    elif checar_cor_proxima(rgb, mato_grosso):
       return "Mato Grosso"
    elif checar_cor_proxima(rgb, minas_gerais):
       return "Minas Gerais"
    elif checar_cor_proxima(rgb, bahia):
       return "Bahia"
    elif checar_cor_proxima(rgb, sergipe):
       return "Sergipe"
    elif checar_cor_proxima(rgb, alagoas):
       return "Alagoas"
    elif checar_cor_proxima(rgb, tocantins):
       return "Tocantins"
    elif checar_cor_proxima(rgb, goias):
       return "Goiás"
    elif checar_cor_proxima(rgb, rio_grande_do_sul):
       return "Rio Grande do Sul"
    elif checar_cor_proxima(rgb, maranhao):
       return "Maranhão"
    elif checar_cor_proxima(rgb, piaui):
       return "Piauí"
    elif checar_cor_proxima(rgb, mato_grosso_do_sul):
       return "Mato Grosso do Sul"
    elif checar_cor_proxima(rgb, roraima):
       return "Roraima"
    elif checar_cor_proxima(rgb, rondonia):
       return "Rondônia"
    elif checar_cor_proxima(rgb, sao_paulo):
       return "São Paulo"
    elif checar_cor_proxima(rgb, acre):
       return "Acre"
    elif checar_cor_proxima(rgb, amapa):
       return "Amapá"
    elif checar_cor_proxima(rgb, ceara):
       return "Ceará"
    elif checar_cor_proxima(rgb, rio_grande_do_norte):
       return "Rio Grande do Norte"
    elif checar_cor_proxima(rgb, paraiba):
       return "Paraíba"
    elif checar_cor_proxima(rgb, pernambuco):
       return "Pernambuco"
    elif checar_cor_proxima(rgb, espirito_santo):
       return "Espírito Santo"
    elif checar_cor_proxima(rgb, rio_de_janeiro):
       return "Rio de Janeiro"
    elif checar_cor_proxima(rgb, distrito_federal):
       return "Distrito Federal"
    elif checar_cor_proxima(rgb, parana):
       return "Paraná"
    elif checar_cor_proxima(rgb, santa_catarina):
       return "Santa Catarina"
    
    return None

def animacao(objeto_estado, objeto_rect, alvo_y, duracao_espera, tempo_inicio_espera ): 
      
   if objeto_estado == "ENTRANDO": #vira tipo um while

      distancia = alvo_y - objeto_rect.centery
            
      # Calcula a velocidade pra andar no mínimo 1 pixel por frame
      velocidade = int(distancia * 0.1)
      if velocidade == 0 and distancia > 0:
         velocidade = 1
         
      if abs(distancia) > 2:
         objeto_rect.centery += velocidade
            
      else: #significa que a distancia é pouca e ta chegando onde eu quero
         objeto_rect.centery = alvo_y
         objeto_estado = "ESPERANDO"
         tempo_inicio_espera = pygame.time.get_ticks()   
                            # Marca o momento exato em milissegundos do início da pausa
         
   elif objeto_estado == "ESPERANDO":

      tempo_real = pygame.time.get_ticks() #fica mudando o tempo para o atual
      if tempo_real - tempo_inicio_espera >= duracao_espera: #ve se deu o tempo que que quero que fique na tela
         objeto_estado = "SAINDO"

   elif objeto_estado == "SAINDO":
      alvo_saida = config.altura + 300
      distancia = alvo_saida - objeto_rect.centery

      velocidade = int(distancia * 0.12)
      if velocidade == 0 and distancia > 0:
         velocidade = 1

      if abs(distancia) > 10:
         objeto_rect.centery += velocidade
      else:  
         objeto_estado = "FIM"   
   
   return objeto_estado, tempo_inicio_espera

def movimento1(objeto_estado, objeto_rect, alvo_y): 
      
   if objeto_estado == "DESCENDO":

      distancia = alvo_y - objeto_rect.centery
            
      velocidade = int(distancia * 0.03)
      if velocidade == 0 and distancia > 0:
         velocidade = 1
         
      if abs(distancia) > 2:
         objeto_rect.centery += velocidade
            
      else:
         objeto_rect.centery = alvo_y
         objeto_estado = "SUBINDO"   

   elif objeto_estado == "SUBINDO":
      alvo_subida = 160
      distancia = alvo_subida - objeto_rect.centery

      velocidade = int(distancia * 0.03)
      if velocidade == 0 and distancia < 0:
         velocidade = -1

      if abs(distancia) > 10:
         objeto_rect.centery += velocidade
      else:  
         objeto_estado = "DESCENDO"
   
   return objeto_estado



def animacao2(objeto_estado, objeto_rect, alvo_y, duracao_espera, tempo_inicio_espera, variavelcontrole, liberar ): 
 
   if objeto_estado == "ENTRANDO":

      distancia = alvo_y - objeto_rect.centery
            
      velocidade = int(distancia * 0.1)
      if velocidade == 0 and distancia > 0:
         velocidade = 1
         
      if abs(distancia) > 2:
         objeto_rect.centery += velocidade
            
      else:
         objeto_rect.centery = alvo_y
         objeto_estado = "ESPERANDO"
         tempo_inicio_espera = pygame.time.get_ticks()   
         
   elif objeto_estado == "ESPERANDO":

      tempo_real = pygame.time.get_ticks()
      if tempo_real - tempo_inicio_espera >= duracao_espera:
         objeto_estado = "SAINDO"

   elif objeto_estado == "SAINDO":
      alvo_saida = config.altura + 300
      distancia = alvo_saida - objeto_rect.centery

      velocidade = int(distancia * 0.12)
      if velocidade == 0 and distancia > 0:
         velocidade = 1

      if abs(distancia) > 10:
         objeto_rect.centery += velocidade
      else:  
         objeto_estado = "FIM"
         variavelcontrole = False
         liberar = True 
           
   
   return objeto_estado, tempo_inicio_espera, variavelcontrole, liberar


def animacao_entrar(objeto_estado, objeto_rect, alvo_y): 
      
   if objeto_estado == "SUBINDO":

      distancia = alvo_y - objeto_rect.centery
            
      velocidade = int(distancia * 0.1)
      if velocidade == 0 and distancia > 0:
         velocidade = 1
         
      if abs(distancia) > 5:
         objeto_rect.centery += velocidade
            
      else:
         objeto_rect.centery = alvo_y
         objeto_estado = "PARAR"   
   
   return objeto_estado

def formatar_texto_largura(texto, fonte, largura_maxima):
  palavras = texto.split(' ')
  linhas = []
  linha_atual = ''

  for palavra in palavras:
    # Testa como ficaria a linha com a nova palavra adicionada
    test_linha = f'{linha_atual} {palavra}'.strip()

    # Mede a largura em pixels da linha testada
    if fonte.size(test_linha)[0] <= largura_maxima:
      linha_atual = test_linha
    else:
      # Se estourar a largura, salva a linha atual e começa uma nova
      if linha_atual:
        linhas.append(linha_atual)
      linha_atual = palavra

  # Adiciona a última linha restante
  if linha_atual:
    linhas.append(linha_atual)

  return linhas



import re
def carregar_questoes_txt(caminho_arquivo):
    # Dicionário retornado caso o arquivo divida o conteúdo por estado (ex: Modo Brasil)
    dados_finais = {}
    # Lista retornada caso o arquivo seja uma sequência contínua de questões sem a marcação 'Estado:'
    lista_simples = []

    # Trava de segurança: impede que o jogo trave se o arquivo não existir
    if not os.path.exists(caminho_arquivo):
        print(f"Aviso: Arquivo de questões não encontrado em: {caminho_arquivo}")
        return lista_simples

    estado_atual = None
    questao_atual = {}
    tem_estados = False

    # Abre o arquivo garantindo suporte aos acentos (UTF-8)
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            # Remove espaços em branco e quebras de linha nas pontas
            linha = linha.strip()

            # Ignora linhas totalmente em branco
            if not linha:
                continue

            # Se encontrar a tag "Estado:", ativa o agrupamento por Unidade Federativa
            if linha.lower().startswith("estado:"):
                tem_estados = True

                # Se já havia uma questão em leitura antes desta linha, armazena no estado anterior
                if estado_atual and questao_atual:
                    dados_finais[estado_atual].append(questao_atual)
                    questao_atual = {}

                # Extrai o nome do estado após os dois pontos
                estado_atual = linha.split(":", 1)[1].strip()

                # Garante que a lista daquele estado esteja criada no dicionário
                if estado_atual not in dados_finais:
                    dados_finais[estado_atual] = []

            elif linha.lower().startswith("pergunta:"):
                # Ao iniciar uma nova pergunta, descarrega a anterior que ainda estava aberta
                if questao_atual:
                    if tem_estados and estado_atual:
                        dados_finais[estado_atual].append(questao_atual)
                    else:
                        lista_simples.append(questao_atual) #se entrou aqui era simples não tem separação de estados
                    questao_atual = {}

                # Guarda o enunciado da questão
                questao_atual["pergunta"] = linha.split(":", 1)[1].strip()

            elif linha.lower().startswith("região:") or linha.lower().startswith("regiao:"):
                # Guarda a região geográfica correspondente
                questao_atual["regiao"] = linha.split(":", 1)[1].strip()

            elif linha.lower().startswith("dicas:"):
                # Separa as dicas caso venham delimitadas por ponto e vírgula
                texto_dicas = linha.split(":", 1)[1].strip()
                questao_atual["dicas"] = [dica.strip() for dica in texto_dicas.split(";")] #strip remove espaços, slipt corta o testo após o ;

            elif linha.lower().startswith("opções:") or linha.lower().startswith("opcoes:"):
                texto_opcoes = linha.split(":", 1)[1].strip()

                # Prioriza a divisão direta por ponto e vírgula se existente
                if ";" in texto_opcoes:
                    questao_atual["opcoes"] = [opcao.strip() for opcao in texto_opcoes.split(";")]
                else:
                    # Alternativa: separa usando expressões regulares identificando letras no estilo A), B), C), D)
                    opcoes_divididas = re.split(r"(?=[A-D]\))", texto_opcoes)
                    opcoes_limpas = [
                        opcao.strip(", ").strip()
                        for opcao in opcoes_divididas
                        if opcao.strip()
                    ]

                    # Se o texto não estiver formatado com letras A) a D), divide por vírgula simples
                    if len(opcoes_limpas) < 2:
                        opcoes_limpas = [
                            opcao.strip()
                            for opcao in texto_opcoes.split(",")[:4]
                        ]

                    # Limita a lista às 4 opções padrão do jogo
                    questao_atual["opcoes"] = opcoes_limpas[:4]

            elif linha.lower().startswith("correta:"):
                # Converte o índice da alternativa correta para número inteiro (ex: 0, 1, 2 ou 3)
                questao_atual["correta"] = int(linha.split(":", 1)[1].strip())

        # Salva a última questão pendente ao final do arquivo
        if questao_atual:
            if tem_estados and estado_atual:
                dados_finais[estado_atual].append(questao_atual)
            else:
                lista_simples.append(questao_atual)

    # Retorna o dicionário agrupado por estado ou a lista simples sequencial
    return dados_finais if tem_estados else lista_simples


def carregar_curiosidades_txt(caminho_arquivo):
    curiosidades = {}

    # Evita falhas críticas caso o arquivo de curiosidades não esteja acessível
    if not os.path.exists(caminho_arquivo):
        print(
            f"Aviso: Arquivo de curiosidades não encontrado em: {caminho_arquivo}"
        )
        return curiosidades

    estado_atual = None
    linhas_texto = []

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha_limpa = linha.strip()

            if not linha_limpa:
                continue

            # Ao encontrar um novo estado, une todas as linhas do parágrafo do estado anterior e gurada no estado anterior
            if linha_limpa.lower().startswith("estado:"):
                if estado_atual and linhas_texto:
                    curiosidades[estado_atual] = " ".join(linhas_texto).strip()
                    linhas_texto = []# Esvazia a lista temporária para começar a guardar as frases do próximo estado
               
                estado_atual = linha_limpa.split(":", 1)[1].strip() # split(":", 1) divide a string apenas no primeiro dois-pontos.
                # O [1] pega a segunda parte (o nome do estado) e o .strip() remove o espaço após os dois-pontos

            # Se a linha não é o cabeçalho 'Estado:', mas já temos um estado ativo, adiciona a frase à lista
            elif estado_atual:
                linhas_texto.append(linha_limpa)

        # Salva o texto do último estado lido antes de encerrar o arquivo
        if estado_atual and linhas_texto:
            curiosidades[estado_atual] = " ".join(linhas_texto).strip()

    return curiosidades


# FUNÇÕES SANTA RITA LER TEXTO


def carregar_textos_srs(modo="pt"):
    # Seleção do arquivo conforme o idioma selecionado
    if modo == "pt":
        arquivo = "srs_pontos.txt"
    elif modo == "en":
        arquivo = "srs_pontos_en.txt"
    elif modo == "esp":
        arquivo = "srs_pontos_esp.txt"
    else:
        arquivo = "srs_pontos.txt"

    caminho = resource_path(os.path.join("dados", arquivo))
    dados = {"INTERFACE": {}}
    chave_atual = None
    linhas_bloco = []

    if not os.path.exists(caminho):
        return dados

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha_limpa = linha.strip()

            if not linha_limpa:
                continue

            # Reconhece blocos delimitados por colchetes, como [SANTUARIO] ou [INTERFACE]
            if linha_limpa.startswith("[") and linha_limpa.endswith("]"):
                # Se não for a tag de interface, a primeira linha é o nome e as demais formam o texto
                if (
                    chave_atual
                    and chave_atual != "INTERFACE"
                    and len(linhas_bloco) >= 1
                ):
                    nome = linhas_bloco[0]
                    texto = (" ".join(linhas_bloco[1:]).strip() if len(linhas_bloco) > 1 else "")
                    dados[chave_atual] = {"nome": nome, "texto": texto}

                # Atualiza para o novo identificador de bloco e limpa o buffer
                chave_atual = linha_limpa[1:-1].strip()
                linhas_bloco = []
                continue

            # Bloco [INTERFACE]: mapeia labels de botões e avisos como par chave:valor
            if chave_atual == "INTERFACE":
                if ":" in linha_limpa:
                    chave_config, valor_config = linha_limpa.split(":", 1)
                    dados["INTERFACE"][chave_config.strip()] = (
                        valor_config.strip()
                    )
            # Blocos de pontos turísticos: acumula as linhas descritivas
            elif chave_atual:
                linhas_bloco.append(linha_limpa)

        # Salva o último ponto turístico do arquivo
        if chave_atual and chave_atual != "INTERFACE" and len(linhas_bloco) >= 1:
            nome = linhas_bloco[0]
            texto = (" ".join(linhas_bloco[1:]).strip() if len(linhas_bloco) > 1 else "")
   #se tiver mais de 1 linha no bloco une elas e separa com espaço, se tiver só uma mostra só ela e o testo vira nada
            dados[chave_atual] = {"nome": nome, "texto": texto}

    return dados