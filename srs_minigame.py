import os
import pygame
import config
import funcoes
from srs_ponto_turistico import PontoTuristico, criar_pontos_santa_rita
from sprite import Personagem


class MinigameSRS:
    def __init__(self, personagem_selecionado):
        # ESTADO INICIAL
        self.estado = "ESCOLHA_IDIOMA"
        self.modo = "pt"

        # VARIÁVEIS DE CONTROLE DE FLUXO / TRANSIÇÃO
        self.proxima_fase = "GAME_SRS"
        self.reiniciar = False
        self.solicitou_pular = False
        self.idioma_selecionado = None

        # BOTÕES DE LINGUAGEM
        y_botoes = config.altura // 2
        
        self.modo_pt_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS_SRS/pt.png")), (200, 40))
        self.modo_pt_rect = self.modo_pt_img.get_rect(centerx=config.centroX - 220, centery=y_botoes)

        self.modo_en_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS_SRS/en.png")), (200, 40))
        self.modo_en_rect = self.modo_en_img.get_rect(centerx=config.centroX, centery=y_botoes)

        self.modo_esp_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS_SRS/esp.png")), (200, 40))
        self.modo_esp_rect = self.modo_esp_img.get_rect(centerx=config.centroX + 220, centery=y_botoes)

        # Recursos visuais e fontes
        caminho_mapa = funcoes.resource_path("assets/IMAGENS_SRS/mapa_srs.png")
        self.mapa_img = pygame.image.load(caminho_mapa).convert()
        self.mapa_img = pygame.transform.scale(self.mapa_img, (config.largura, config.altura))

        self.fonte_titulo = pygame.font.SysFont("Arial", 24, True)
        self.fonte_texto = pygame.font.SysFont("Arial", 18)
        self.fonte_hud = pygame.font.SysFont("Arial", 14, True)

        self.linha_rio_y = 480

        # Botão Reiniciar
        caminho_btn = funcoes.resource_path("assets/IMAGENS/botao_reiniciar.png")
        self.botao_reiniciar = pygame.transform.scale(pygame.image.load(caminho_btn).convert_alpha(), (50, 50))
        self.botao_reiniciar_rect = self.botao_reiniciar.get_rect(x=114, y=2)

        # Botão Pular Minigame
        self.botao_pular_rect = pygame.Rect(config.largura - 140, 10, 120, 36)

        # Rosa dos Ventos
        caminho_rosa_ventos = funcoes.resource_path("assets/IMAGENS_SRS/rosaVentos.png")
        self.rosa_ventos_img = pygame.image.load(caminho_rosa_ventos).convert_alpha()
        self.rosa_ventos_img = pygame.transform.scale(self.rosa_ventos_img, (110, 110))
        self.rosa_ventos_rect = self.rosa_ventos_img.get_rect()
        self.rosa_ventos_rect.topright = (config.largura - 20, self.botao_pular_rect.bottom + 10)

        # MAPA REAL ------------------------
        self.mapa_real = pygame.image.load(funcoes.resource_path("assets/IMAGENS_SRS/mapa_real.png")).convert_alpha()
        self.mapa_real = pygame.transform.scale(self.mapa_real, (800, 500))
        self.mapa_real_rect = self.mapa_real.get_rect(centerx=config.centroX, centery=config.altura // 2)
        
        self.mostrar_mapa_real = False
        self.botao_fechar_mapa_real = pygame.Rect(0, 0, 34, 34)
        self.botao_fechar_mapa_real.topright = (self.mapa_real_rect.right - 10, self.mapa_real_rect.top + 10)

        # Personagem
        self.personagem = Personagem(personagem_selecionado)

        # Variáveis de controle de jogo
        self.rio_apresentado = False
        self.mostrar_popup = True
        self.ponto_atual = None
        self.finalizado = False

        self.pontos = []
        self.total_pontos = 0
        self.entrada_cidade = {}
        self.evento_rio = {}
        self.interface = {}
        self.popup_img = None
        self.popup_qr = None
        self.estatua_img = None
        self.estatua_rect = None

    def iniciar_cenario(self, modo_escolhido):
        self.modo = modo_escolhido
        self.pontos, self.entrada_cidade, self.evento_rio, self.interface = criar_pontos_santa_rita(self.modo)
        self.total_pontos = len(self.pontos)

        # Inicializa o sprite da estátua de entrada
        caminho_estatua = funcoes.resource_path(self.entrada_cidade["imagem_path"])
        self.estatua_img = pygame.image.load(caminho_estatua).convert_alpha()
        self.estatua_img = pygame.transform.scale(self.estatua_img, (90, 90))
        self.estatua_rect = self.estatua_img.get_rect(center=(self.entrada_cidade["x"], self.entrada_cidade["y"]))

        # Posiciona o personagem no ponto de entrada
        self.personagem.rect.center = (self.entrada_cidade["x"], self.entrada_cidade["y"])
        self.pos_y_anterior = self.personagem.rect.y

        # Define os textos e imagens iniciais do pop-up da entrada (com QR code padrão)
        self.popup_nome = self.entrada_cidade["nome"]
        self.popup_texto = self.entrada_cidade["mensagem"]

        caminho_foto_entrada = funcoes.resource_path(self.entrada_cidade["foto_popup_path"])
        self.popup_img = pygame.image.load(caminho_foto_entrada).convert_alpha() if os.path.exists(caminho_foto_entrada) else None

        caminho_qr_entrada = funcoes.resource_path(self.entrada_cidade["qr_path"])
        self.popup_qr = pygame.image.load(caminho_qr_entrada).convert_alpha() if os.path.exists(caminho_qr_entrada) else None

        self.estado = "JOGO"

    def gerenciar_eventos(self, evento):
        pos_mouse = pygame.mouse.get_pos()

        # Escolha inicial de idioma
        if self.estado == "ESCOLHA_IDIOMA":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.modo_pt_rect.collidepoint(pos_mouse):
                    self.idioma_selecionado = "pt"
                elif self.modo_en_rect.collidepoint(pos_mouse):
                    self.idioma_selecionado = "en"
                elif self.modo_esp_rect.collidepoint(pos_mouse):
                    self.idioma_selecionado = "esp"
            return

        # Interações com o Mapa Real aberto
        if self.mostrar_mapa_real:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.botao_fechar_mapa_real.collidepoint(pos_mouse):
                    self.mostrar_mapa_real = False
            elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                self.mostrar_mapa_real = False
            return

        # Cliques em tela normal de jogo
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_reiniciar_rect.collidepoint(pos_mouse):
                self.reiniciar = True
            elif self.botao_pular_rect.collidepoint(pos_mouse):
                self.solicitou_pular = True
            elif self.rosa_ventos_rect.collidepoint(pos_mouse):
                self.mostrar_mapa_real = True

        # Fechamento de pop-ups informativos
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                if self.mostrar_popup:
                    self.mostrar_popup = False
                    if self.ponto_atual is not None:
                        self.ponto_atual.marcar_visitado()
                        self.ponto_atual = None

    def atualizar(self, reiniciar):
        #conta os estados visitados
        contador = 0
        for ponto in self.pontos:
            if ponto.visitado:
                contador += 1
        self.total_visitados = contador


        if self.reiniciar:
            reiniciar = True
            return "MENU", reiniciar, self.modo
        
        if self.solicitou_pular:
            return "JOGO_SRS", reiniciar, self.modo

        if self.estado == "ESCOLHA_IDIOMA":
            if self.idioma_selecionado:
                self.iniciar_cenario(self.idioma_selecionado)
                self.idioma_selecionado = None
            return "GAME_SRS", reiniciar, self.modo
        
        if not self.mostrar_popup and not self.mostrar_mapa_real:
            if self.pontos and all(p.visitado for p in self.pontos):
                return "JOGO_SRS", reiniciar, self.modo

        if self.mostrar_popup or self.mostrar_mapa_real:
            return "GAME_SRS", reiniciar, self.modo

        teclas = pygame.key.get_pressed()
        self.personagem.mover(teclas)
        self.personagem.update()

        # Travessia do Rio Sapucaí
        if not self.rio_apresentado:
            cruzou_subindo = (self.pos_y_anterior >= self.linha_rio_y and self.personagem.rect.y < self.linha_rio_y)
            if cruzou_subindo:
                self.rio_apresentado = True
                self.popup_nome = self.evento_rio["nome"]
                self.popup_texto = self.evento_rio["mensagem"]
                caminho_foto_rio = funcoes.resource_path(self.evento_rio["foto_popup_path"])
                self.popup_img = pygame.image.load(caminho_foto_rio).convert_alpha() if os.path.exists(caminho_foto_rio) else None
                caminho_qr_rio = funcoes.resource_path(self.evento_rio["qr_path"])
                self.popup_qr = pygame.image.load(caminho_qr_rio).convert_alpha() if os.path.exists(caminho_qr_rio) else None
                self.mostrar_popup = True

        self.pos_y_anterior = self.personagem.rect.y

        # Colisão com os pontos turísticos
        for p in self.pontos:
            centro_x = self.personagem.rect.centerx
            centro_y = self.personagem.rect.centery
            if not p.visitado and p.dentro_do_raio(centro_x, centro_y, 32):
                self.ponto_atual = p
                self.popup_nome = p.nome
                self.popup_texto = p.curiosidade
                self.popup_img = p.foto_popup
                self.popup_qr = p.qr_img
                self.mostrar_popup = True
                break

        return "GAME_SRS", reiniciar, self.modo

    def desenhar(self, tela):
        tela.blit(self.mapa_img, (0, 0))

        # Tela de Escolha de Idioma
        if self.estado == "ESCOLHA_IDIOMA":
            escurecer = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
            escurecer.fill((0, 0, 0, 180))
            tela.blit(escurecer, (0, 0))

            caixa_fundo = pygame.Rect(config.centroX - 350, config.altura // 2 - 150, 700, 300)
            pygame.draw.rect(tela, config.bege, caixa_fundo, border_radius=14)
            pygame.draw.rect(tela, (50, 30, 15), caixa_fundo, 4, border_radius=14)

            txt_selecao = self.fonte_titulo.render("Selecione seu Idioma / Select Language", True, (60, 30, 10))
            tela.blit(txt_selecao, txt_selecao.get_rect(centerx=config.centroX, y=caixa_fundo.y + 25))

            tela.blit(self.modo_pt_img, self.modo_pt_rect)
            tela.blit(self.modo_en_img, self.modo_en_rect)
            tela.blit(self.modo_esp_img, self.modo_esp_rect)
            return

        tela.blit(self.estatua_img, self.estatua_rect)
        tela.blit(self.botao_reiniciar, self.botao_reiniciar_rect)

        pos_mouse = pygame.mouse.get_pos()

        # Botão Pular
        texto_pular = self.interface.get("pular", "PULAR")
        cor_pular = (70, 140, 210) if self.botao_pular_rect.collidepoint(pos_mouse) else (40, 90, 200)
        pygame.draw.rect(tela, cor_pular, self.botao_pular_rect, border_radius=6)
        pygame.draw.rect(tela, (50, 30, 15), self.botao_pular_rect, 2, border_radius=6)
        txt_pular = self.fonte_hud.render(texto_pular, True, (255, 255, 255))
        tela.blit(txt_pular, txt_pular.get_rect(center=self.botao_pular_rect.center))

        # Rosa dos Ventos
        tela.blit(self.rosa_ventos_img, self.rosa_ventos_rect)

        # Pontos Turísticos no mapa
        for p in self.pontos:
            if p.imagem:
                tela.blit(p.imagem, p.imagem_rect)
            cor_tag = (46, 204, 113) if p.visitado else (30, 30, 35) #cor sem visitar, cor depois de visitado
            texto_ponto = self.fonte_hud.render(p.nome, True, (255, 255, 255))
            rect_bg = pygame.Rect(p.x - (texto_ponto.get_width() // 2) - 6, p.y + 45, texto_ponto.get_width() + 12, 22)
            pygame.draw.rect(tela, cor_tag, rect_bg, border_radius=4)
            tela.blit(texto_ponto, (p.x - (texto_ponto.get_width() // 2), p.y + 48))

        tela.blit(self.personagem.image, self.personagem.rect)

        # HUD Contador de pontos visitados
        rotulo_hud = self.interface.get("contador", "Pontos Visitados:") #pega do txt, ou deixa O OUTRO COMO DEFAULT    
        texto_hud = self.fonte_hud.render(f"{rotulo_hud} {self.total_visitados}/{self.total_pontos}", True, (25, 25, 25))
        hud_box = pygame.Rect(175, 5, texto_hud.get_width() + 20, 32)
        pygame.draw.rect(tela, (250, 248, 240), hud_box, border_radius=6)
        pygame.draw.rect(tela, (50, 30, 15), hud_box, 2, border_radius=6)
        tela.blit(texto_hud, texto_hud.get_rect(center=hud_box.center))

        # Pop-up de informações se ativo
        if self.mostrar_popup:
            escurecer = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
            escurecer.fill((0, 0, 0, 160))
            tela.blit(escurecer, (0, 0))

            margem_v = 25
            altura_total = config.altura - (margem_v * 2)
            altura_img = altura_total // 2
            altura_caixa = altura_total - altura_img
            largura_popup = min(780, config.largura - 40)

            x_popup = config.centroX - (largura_popup // 2)
            y_inicio = margem_v
            y_caixa = y_inicio + altura_img

            if self.popup_img:
                img_banner = pygame.transform.scale(self.popup_img, (largura_popup, altura_img))
                tela.blit(img_banner, (x_popup, y_inicio))
                borda_img = pygame.Rect(x_popup, y_inicio, largura_popup, altura_img)
                pygame.draw.rect(tela, (50, 30, 15), borda_img, 4)
            else:
                fundo_padrao = pygame.Rect(x_popup, y_inicio, largura_popup, altura_img)
                pygame.draw.rect(tela, (180, 165, 145), fundo_padrao)
                pygame.draw.rect(tela, (50, 30, 15), fundo_padrao, 4)

            caixa = pygame.Rect(x_popup, y_caixa, largura_popup, altura_caixa)
            pygame.draw.rect(tela, (250, 248, 240), caixa, border_bottom_left_radius=14, border_bottom_right_radius=14)
            pygame.draw.rect(tela, (50, 30, 15), caixa, 4, border_bottom_left_radius=14, border_bottom_right_radius=14)

            titulo = self.fonte_titulo.render(self.popup_nome, True, (60, 30, 10))
            tela.blit(titulo, (x_popup + 35, y_caixa + 18))
            pygame.draw.line(tela, (190, 175, 155), (x_popup + 35, y_caixa + 52), (x_popup + largura_popup - 35, y_caixa + 52), 2)

            tam_qr = min(150, altura_caixa - 120)
            if self.popup_qr:
                qr_redimensionado = pygame.transform.scale(self.popup_qr, (tam_qr, tam_qr))
                tela.blit(qr_redimensionado, (x_popup + 35, y_caixa + 68))
            else:
                quadrado_vazio = pygame.Rect(x_popup + 35, y_caixa + 68, tam_qr, tam_qr)
                pygame.draw.rect(tela, (220, 220, 220), quadrado_vazio)
                pygame.draw.rect(tela, (50, 30, 15), quadrado_vazio, 2)

            # Legenda do QR Code padronizada para todos os pontos e entrada
            texto_qr = self.interface.get("qr_aviso", "Escaneie o QR")
            txt_qr = self.fonte_hud.render(texto_qr, True, (80, 50, 20))
            tela.blit(txt_qr, (x_popup + 35 + (tam_qr // 2) - (txt_qr.get_width() // 2), y_caixa + 72 + tam_qr))

            x_texto = x_popup + tam_qr + 60
            largura_util_texto = (x_popup + largura_popup - 35) - x_texto
            palavras = self.popup_texto.split(" ")
            linhas, linha_atual = [], ""
            for p in palavras:
                teste = f"{linha_atual} {p}".strip()
                if self.fonte_texto.size(teste)[0] <= largura_util_texto:
                    linha_atual = teste
                else:
                    linhas.append(linha_atual)
                    linha_atual = p
            if linha_atual:
                linhas.append(linha_atual)

            for i, l in enumerate(linhas):
                texto_linha = self.fonte_texto.render(l, True, (30, 30, 30))
                tela.blit(texto_linha, (x_texto, y_caixa + 70 + (i * 26)))

            texto_instrucao = self.interface.get("instrucao", "Pressione [ESPAÇO] ou [ENTER] para fechar")
            instrucao = self.fonte_hud.render(texto_instrucao, True, (160, 40, 30))
            tela.blit(instrucao, (config.centroX - (instrucao.get_width() // 2), caixa.bottom - 24))

        # Visualização do Mapa Real
        if self.mostrar_mapa_real:
            escurecer_mapa = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
            escurecer_mapa.fill((0, 0, 0, 170))
            tela.blit(escurecer_mapa, (0, 0))

            tela.blit(self.mapa_real, self.mapa_real_rect)
            pygame.draw.rect(tela, (50, 30, 15), self.mapa_real_rect, 4, border_radius=8)

            # Botão [X]
            pygame.draw.rect(tela, (210, 50, 40), self.botao_fechar_mapa_real, border_radius=6)
            pygame.draw.rect(tela, (50, 30, 15), self.botao_fechar_mapa_real, 2, border_radius=6)
            txt_fechar = self.fonte_titulo.render("X", True, (255, 255, 255))
            tela.blit(txt_fechar, txt_fechar.get_rect(center=self.botao_fechar_mapa_real.center))