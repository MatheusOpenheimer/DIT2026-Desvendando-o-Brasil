import os
import pygame
import funcoes


def carregar_informacoes_txt(modo="pt"):
    if modo == "pt":
        nome_arquivo = "srs_pontos.txt"
    elif modo == "en":
        nome_arquivo = "srs_pontos_en.txt"
    elif modo == "esp":
        nome_arquivo = "srs_pontos_esp.txt"
    else:
        nome_arquivo = "srs_pontos.txt"

    caminho = funcoes.resource_path(os.path.join("dados", nome_arquivo))
    dados = {"INTERFACE": {}}
    id_atual = None
    linhas_bloco = []

    if not os.path.exists(caminho):
        return dados

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha_limpa = linha.strip()
            if not linha_limpa:
                continue

            if linha_limpa.startswith("[") and linha_limpa.endswith("]"):
                if id_atual and id_atual != "INTERFACE" and len(linhas_bloco) >= 1:
                    nome = linhas_bloco[0]
                    texto = " ".join(linhas_bloco[1:]).strip() if len(linhas_bloco) > 1 else ""
                    dados[id_atual] = {"nome": nome, "texto": texto}
                
                id_atual = linha_limpa[1:-1].strip()
                linhas_bloco = []
                continue

            if id_atual == "INTERFACE":
                if ":" in linha_limpa:
                    k, v = linha_limpa.split(":", 1)
                    dados["INTERFACE"][k.strip()] = v.strip()
            elif id_atual:
                linhas_bloco.append(linha_limpa)

        if id_atual and id_atual != "INTERFACE" and len(linhas_bloco) >= 1:
            nome = linhas_bloco[0]
            texto = " ".join(linhas_bloco[1:]).strip() if len(linhas_bloco) > 1 else ""
            dados[id_atual] = {"nome": nome, "texto": texto}

    return dados


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

        caminho_img = funcoes.resource_path(self.imagem_path)
        if os.path.exists(caminho_img):
            img_carregada = pygame.image.load(caminho_img).convert_alpha()
            self.imagem = pygame.transform.scale(img_carregada, (90, 90))
            self.imagem_rect = self.imagem.get_rect(center=(self.x, self.y))
        else:
            self.imagem = pygame.Surface((90, 90), pygame.SRCALPHA)
            pygame.draw.circle(self.imagem, (220, 80, 50), (45, 45), 35)
            self.imagem_rect = self.imagem.get_rect(center=(self.x, self.y))

        caminho_foto = funcoes.resource_path(self.foto_popup_path)
        if os.path.exists(caminho_foto):
            self.foto_popup = pygame.image.load(caminho_foto).convert_alpha()
        else:
            self.foto_popup = None

        caminho_qr = funcoes.resource_path(self.qr_path)
        if os.path.exists(caminho_qr):
            self.qr_img = pygame.image.load(caminho_qr).convert_alpha()
        else:
            self.qr_img = None

    def dentro_do_raio(self, px, py, tamanho_jogador=32):
        rect_jogador = pygame.Rect(px - 10, py - 10, 20, 20)
        if self.imagem_rect:
            return self.imagem_rect.colliderect(rect_jogador)
        return False

    def marcar_visitado(self):
        self.visitado = True

    def resetar(self):
        self.visitado = False


def criar_pontos_santa_rita(modo="pt"):
    info = carregar_informacoes_txt(modo)


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