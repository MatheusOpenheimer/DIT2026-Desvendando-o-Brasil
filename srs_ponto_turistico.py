import os
import pygame
import funcoes

#config para executavel
def obter_caminho_dados(nome_arquivo):
    # Caminho padrão na pasta 'dados' do projeto
    caminho_local = os.path.join("dados", nome_arquivo)

    # Se o arquivo existir na pasta local, usa ele
    if os.path.exists(caminho_local):
        return caminho_local

    # Se não encontrar localmente, usa a função para buscar no executável
    return funcoes.obter_caminho_arquivo(caminho_local)


def carregar_informacoes_txt(modo="pt"):
    # Escolhe o arquivo certo com base no idioma que o jogador selecionou
    if modo == "pt":
        nome_arquivo = "srs_pontos.txt"
    elif modo == "en":
        nome_arquivo = "srs_pontos_en.txt"
    elif modo == "esp":
        nome_arquivo = "srs_pontos_esp.txt"
    else:
        nome_arquivo = "srs_pontos.txt"

    caminho_arquivo = obter_caminho_dados(nome_arquivo)

    # Dicionário que vai guardar tudo o que for lido do arquivo
    dados_carregados = {"INTERFACE": {}}
    secao_atual = None
    linhas_do_ponto = []

    # Se o arquivo não existir, já devolve a estrutura básica vazia pra não dar erro
    if not os.path.exists(caminho_arquivo):
        return dados_carregados

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo_txt:
        for linha in arquivo_txt:
            linha_limpa = linha.strip()

            # Pula linhas em branco para não atrapalhar a leitura
            if not linha_limpa:
                continue

            # Identifica quando começa uma nova seção (ex: [CRISTO] ou [INTERFACE])
            if linha_limpa.startswith("[") and linha_limpa.endswith("]"):
                # Antes de mudar de seção, salva o ponto turístico que acabou de ler
                if secao_atual and secao_atual != "INTERFACE" and len(linhas_do_ponto) >= 1:
                    nome_ponto = linhas_do_ponto[0]
                    
                    # Junta o restante das linhas para formar o texto explicativo
                    if len(linhas_do_ponto) > 1:
                        descricao_ponto = " ".join(linhas_do_ponto[1:]).strip()
                    else:
                        descricao_ponto = ""

                    dados_carregados[secao_atual] = {
                        "nome": nome_ponto,
                        "texto": descricao_ponto
                    }

                # Pega o nome da nova seção tirando os colchetes '[' e ']'
                secao_atual = linha_limpa[1:-1].strip()
                linhas_do_ponto = []
                continue

            # Se estiver dentro da seção de interface, separa em chave e valor pelo ':'
            if secao_atual == "INTERFACE":
                if ":" in linha_limpa:
                    chave, valor = linha_limpa.split(":", 1)
                    dados_carregados["INTERFACE"][chave.strip()] = valor.strip()

            # Se for um ponto turístico normal, vai guardando as linhas de texto dele
            elif secao_atual:
                linhas_do_ponto.append(linha_limpa)

        # Salva o último ponto turístico do arquivo após terminar o laço
        if secao_atual and secao_atual != "INTERFACE" and len(linhas_do_ponto) >= 1:
            nome_ponto = linhas_do_ponto[0]
            
            if len(linhas_do_ponto) > 1:
                descricao_ponto = " ".join(linhas_do_ponto[1:]).strip() #junta as linhas usando " " pra separar
            else:
                descricao_ponto = ""

            dados_carregados[secao_atual] = {
                "nome": nome_ponto,
                "texto": descricao_ponto
            }

    return dados_carregados


class PontoTuristico:
    def __init__(self, nome, x, y, curiosidade, imagem_path, foto_popup_path, qr_path):
        self.nome = nome
        self.x = x
        self.y = y
        self.curiosidade = curiosidade
        self.imagem_path = imagem_path
        self.foto_popup_path = foto_popup_path
        self.qr_path = qr_path
        self.visitado = False

        caminho_img = funcoes.obter_caminho_arquivo(self.imagem_path)
        if os.path.exists(caminho_img): #desenha a imagem
            img_carregada = pygame.image.load(caminho_img).convert_alpha()
            self.imagem = pygame.transform.scale(img_carregada, (90, 90))
            self.imagem_rect = self.imagem.get_rect(center=(self.x, self.y))
        else: #se não tiver cria um ponto
            self.imagem = pygame.Surface((90, 90), pygame.SRCALPHA)
            pygame.draw.circle(self.imagem, (220, 80, 50), (45, 45), 35)
            self.imagem_rect = self.imagem.get_rect(center=(self.x, self.y))

        caminho_foto = funcoes.obter_caminho_arquivo(self.foto_popup_path)
        if os.path.exists(caminho_foto): #mesma lógica pro pop-up
            self.foto_popup = pygame.image.load(caminho_foto).convert_alpha()
        else:
            self.foto_popup = None

        caminho_qr = funcoes.obter_caminho_arquivo(self.qr_path)
        if os.path.exists(caminho_qr): #mesma lógica pro qr code
            self.qr_img = pygame.image.load(caminho_qr).convert_alpha()
        else:
            self.qr_img = None

    def dentro_do_raio(self, px, py, tamanho_jogador=20):
        # Cria o retângulo do jogador usando o tamanho real e centralizando nas coordenadas px e py
        metade_tamanho = tamanho_jogador // 2
        rect_jogador = pygame.Rect(
            px - metade_tamanho, 
            py - metade_tamanho, 
            tamanho_jogador, 
            tamanho_jogador
        )
        
        if self.imagem_rect:
            return self.imagem_rect.colliderect(rect_jogador)
        return False

    def marcar_visitado(self):
        self.visitado = True

def criar_pontos_santa_rita(modo="pt"):
    info = carregar_informacoes_txt(modo)

    interface = info.get("INTERFACE", {})

    item_entrada = info.get("ENTRADA_CIDADE", {})
    entrada_cidade = {
        "nome": item_entrada.get("nome", "Estátua de Santa Rita - Entrada da Cidade"),
        "x": 1051,
        "y": 750,
        "imagem_path": "assets/IMAGENS_SRS/santa_estatua.png",
        "foto_popup_path": "assets/IMAGENS_SRS/srs.png",
        "qr_path": "assets/IMAGENS_SRS/qr_guiaTuristico.png",
        "mensagem": item_entrada.get("texto", "")
    }

    # Dados do Evento do Rio Sapucaí
    item_rio = info.get("EVENTO_RIO_SAPUCAI", {})
    evento_rio = {
        "nome": item_rio.get("nome", "Travessia do Rio Sapucaí"),
        "foto_popup_path": "assets/IMAGENS_SRS/img_rio.png",
        "qr_path": "assets/IMAGENS_SRS/qr_rio.png",
        "mensagem": item_rio.get("texto", "")
    }

    # Lista com todos os Pontos Turísticos
    pontos = [
        PontoTuristico(
            nome=info.get("SANTUARIO", {}).get("nome", "Santuário Santa Rita de Cássia"),
            x=851, y=216,
            curiosidade=info.get("SANTUARIO", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/igreja.png",
            foto_popup_path="assets/IMAGENS_SRS/img_igreja.png",
            qr_path="assets/IMAGENS_SRS/qr_igreja.png"
        ),
        PontoTuristico(
            nome=info.get("TEATRO", {}).get("nome", "Teatro Municipal"),
            x=957, y=320,
            curiosidade=info.get("TEATRO", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/teatro.png",
            foto_popup_path="assets/IMAGENS_SRS/img_teatro.jpg",
            qr_path="assets/IMAGENS_SRS/qr_teatro.png"
        ),
        PontoTuristico(
            nome=info.get("MERCADO", {}).get("nome", "Mercado Municipal"),
            x=1075, y=210,
            curiosidade=info.get("MERCADO", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/mercadao.png",
            foto_popup_path="assets/IMAGENS_SRS/img_mercadao.png",
            qr_path="assets/IMAGENS_SRS/qr_mercado.png"
        ),
        PontoTuristico(
            nome=info.get("EVENTOS", {}).get("nome", "Centro de Eventos e Festivais"),
            x=205, y=380,
            curiosidade=info.get("EVENTOS", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/eventos.png",
            foto_popup_path="assets/IMAGENS_SRS/img_eventos.png",
            qr_path="assets/IMAGENS_SRS/qr_eventos.png"
        ),
        PontoTuristico(
            nome=info.get("MUSEU", {}).get("nome", "Museu Histórico Dr. Delfim Moreira"),
            x=328, y=734,
            curiosidade=info.get("MUSEU", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/museu.png",
            foto_popup_path="assets/IMAGENS_SRS/img_museu.png",
            qr_path="assets/IMAGENS_SRS/qr_museu.png"
        ),
        PontoTuristico(
            nome=info.get("ETE", {}).get("nome", "ETE FMC"),
            x=1152, y=344,
            curiosidade=info.get("ETE", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/ete.png",
            foto_popup_path="assets/IMAGENS_SRS/img_ete.png",
            qr_path="assets/IMAGENS_SRS/qr_ete.png"
        ),
        PontoTuristico(
            nome=info.get("FAI", {}).get("nome", "FAI Centro de Ensino Superior"),
            x=1437, y=266,
            curiosidade=info.get("FAI", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/fai.png",
            foto_popup_path="assets/IMAGENS_SRS/img_fai.png",
            qr_path="assets/IMAGENS_SRS/qr_fai.png"
        ),
        PontoTuristico(
            nome=info.get("INATEL", {}).get("nome", "INATEL"),
            x=1157, y=101,
            curiosidade=info.get("INATEL", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/inatel.png",
            foto_popup_path="assets/IMAGENS_SRS/img_inatel.png",
            qr_path="assets/IMAGENS_SRS/qr_inatel.png"
        ),
        PontoTuristico(
            nome=info.get("CRUZEIRO", {}).get("nome", "Morro do Cruzeiro"),
            x=705, y=65,
            curiosidade=info.get("CRUZEIRO", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/morro.png",
            foto_popup_path="assets/IMAGENS_SRS/img_morro.png",
            qr_path="assets/IMAGENS_SRS/qr_morro.png"
        ),
        PontoTuristico(
            nome=info.get("GAAU", {}).get("nome", "GAAU - Galeria Aberta de Arte Urbana"),
            x=960, y=490,
            curiosidade=info.get("GAAU", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/ponto.png",
            foto_popup_path="assets/IMAGENS_SRS/img_gaau.png",
            qr_path="assets/IMAGENS_SRS/qr_gaau.png"
        ),
        PontoTuristico(
            nome=info.get("VOO_LIVRE", {}).get("nome", "Rampa de Voo Livre"),
            x=95, y=300,
            curiosidade=info.get("VOO_LIVRE", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/ponto.png",
            foto_popup_path="assets/IMAGENS_SRS/img_voo.png",
            qr_path="assets/IMAGENS_SRS/qr_voo.png"
        ),
        PontoTuristico(
            nome=info.get("PARQUE", {}).get("nome", "Parque Mun. Natural Dr. Cyro de Luna Dias"),
            x=160, y=195,
            curiosidade=info.get("PARQUE", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/ponto.png",
            foto_popup_path="assets/IMAGENS_SRS/img_parque.png",
            qr_path="assets/IMAGENS_SRS/qr_parque.png"
        ),
        PontoTuristico(
            nome=info.get("REBIO", {}).get("nome", "REBIO - Reserva Biológica Profª. Dra. Mítzi"),
            x=185, y=95,
            curiosidade=info.get("REBIO", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/ponto.png",
            foto_popup_path="assets/IMAGENS_SRS/img_rebio.png",
            qr_path="assets/IMAGENS_SRS/qr_rebio.png"
        ),
        PontoTuristico(
            nome=info.get("RODOVIARIA", {}).get("nome", "Terminal Rodoviário"),
            x=840, y=750,
            curiosidade=info.get("RODOVIARIA", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/rodoviaria.png",
            foto_popup_path="assets/IMAGENS_SRS/img_rodoviaria.jpg",
            qr_path="assets/IMAGENS_SRS/qr_rodoviaria.png"
    ),
        PontoTuristico(
            nome=info.get("CARNAVAL", {}).get("nome", "Carnaval e Tradições"),
            x=420, y=250,
            curiosidade=info.get("CARNAVAL", {}).get("texto", ""),
            imagem_path="assets/IMAGENS_SRS/info.png",
            foto_popup_path="assets/IMAGENS_SRS/carnaval.jpg",
            qr_path="assets/IMAGENS_SRS/qr_carnaval.png"
        )
    ]

    return pontos, entrada_cidade, evento_rio, interface