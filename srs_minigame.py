import os
import pygame
import config
import funcoes
from srs_ponto_turistico import PontoTuristico, criar_pontos_santa_rita, ENTRADA_CIDADE, EVENTO_RIO_SAPUCAI
from sprite import Personagem


class MinigameSRS:
    def __init__(self):
        # 1. Carrega imagens e fontes
        caminho_mapa = funcoes.resource_path("assets/IMAGENS_SRS/mapa_srs.png")
        self.mapa_img = pygame.image.load(caminho_mapa).convert()
        self.mapa_img = pygame.transform.scale(self.mapa_img, (config.largura, config.altura))

        self.fonte_titulo = pygame.font.SysFont("Arial", 24, True)
        self.fonte_texto = pygame.font.SysFont("Arial", 18)
        self.fonte_hud = pygame.font.SysFont("Arial", 14, True)

        self.linha_rio_y = 480

        caminho_estatua = funcoes.resource_path(ENTRADA_CIDADE["imagem_path"])
        self.estatua_img = pygame.image.load(caminho_estatua).convert_alpha()
        self.estatua_img = pygame.transform.scale(self.estatua_img, (90, 90))
        self.estatua_rect = self.estatua_img.get_rect(center=(ENTRADA_CIDADE["x"], ENTRADA_CIDADE["y"]))

        self.pontos = criar_pontos_santa_rita()
        self.total_pontos = len(self.pontos)

        # Botão Reiniciar Oficial
        caminho_btn = funcoes.resource_path("assets/IMAGENS/botao_reiniciar.png")
        self.botao_reiniciar = pygame.transform.scale(pygame.image.load(caminho_btn).convert_alpha(), (50, 50))
        self.botao_reiniciar_rect = self.botao_reiniciar.get_rect(x=114, y=2)

        # Botão Pular Minigame (canto superior direito)
        self.botao_pular_rect = pygame.Rect(config.largura - 140, 10, 120, 36)

        # Instanciação do Personagem animado
        self.personagem = Personagem()
        self.personagem.rect.center = (ENTRADA_CIDADE["x"], ENTRADA_CIDADE["y"])

        # 2. Variáveis de início de partida
        self.pos_y_anterior = self.personagem.rect.y
        self.rio_apresentado = False
        self.eh_entrada = True
        self.mostrar_popup = True
        self.ponto_atual = None
        self.reiniciar = False
        self.finalizado = False

        self.popup_nome = ENTRADA_CIDADE["nome"]
        self.popup_texto = ENTRADA_CIDADE["mensagem"]
        
        caminho_foto_entrada = funcoes.resource_path(ENTRADA_CIDADE["foto_popup_path"])
        self.popup_img = pygame.image.load(caminho_foto_entrada).convert_alpha() if os.path.exists(caminho_foto_entrada) else None

        caminho_icone_entrada = funcoes.resource_path(ENTRADA_CIDADE.get("icone_lateral_path", ENTRADA_CIDADE["imagem_path"]))
        self.popup_qr = pygame.image.load(caminho_icone_entrada).convert_alpha() if os.path.exists(caminho_icone_entrada) else None

    def gerenciar_eventos(self, evento):
        pos_mouse = pygame.mouse.get_pos()

        # Clique nos botões
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.botao_reiniciar_rect.collidepoint(pos_mouse):
                self.reiniciar = True
                return "GAME_SRS"

            # Clique para Pular o Minigame
            if self.botao_pular_rect.collidepoint(pos_mouse):
                return "JOGO_SRS"

        # Teclas de controle do pop-up
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                if self.mostrar_popup:
                    self.mostrar_popup = False
                    if self.ponto_atual is not None:
                        self.ponto_atual.marcar_visitado()
                        self.ponto_atual = None

                    # Se todos foram visitados, aciona a troca de tela direto
                    todos_visitados = all(p.visitado for p in self.pontos)
                    if todos_visitados:
                        return "JOGO_SRS"

        return "GAME_SRS"

    def atualizar(self, reiniciar):
        if self.reiniciar:
            reiniciar = True
            return "MENU", reiniciar

        if self.mostrar_popup:
            return "GAME_SRS", reiniciar

        # Movimentação e atualização do sprite do personagem
        teclas = pygame.key.get_pressed()
        self.personagem.mover(teclas)
        self.personagem.update()

        # Gatilho da Linha do Rio Sapucaí
        if not self.rio_apresentado:
            cruzou_subindo = (self.pos_y_anterior >= self.linha_rio_y and self.personagem.rect.y < self.linha_rio_y)
            cruzou_descendo = (self.pos_y_anterior <= self.linha_rio_y and self.personagem.rect.y > self.linha_rio_y)
            if cruzou_subindo or cruzou_descendo:
                self.rio_apresentado = True
                self.eh_entrada = False
                self.popup_nome = EVENTO_RIO_SAPUCAI["nome"]
                self.popup_texto = EVENTO_RIO_SAPUCAI["mensagem"]
                caminho_foto_rio = funcoes.resource_path(EVENTO_RIO_SAPUCAI["foto_popup_path"])
                self.popup_img = pygame.image.load(caminho_foto_rio).convert_alpha() if os.path.exists(caminho_foto_rio) else None
                caminho_qr_rio = funcoes.resource_path(EVENTO_RIO_SAPUCAI["qr_path"])
                self.popup_qr = pygame.image.load(caminho_qr_rio).convert_alpha() if os.path.exists(caminho_qr_rio) else None
                self.mostrar_popup = True

        self.pos_y_anterior = self.personagem.rect.y

        # Colisão com Pontos Turísticos
        for p in self.pontos:
            centro_x = self.personagem.rect.centerx
            centro_y = self.personagem.rect.centery
            if not p.visitado and p.dentro_do_raio(centro_x, centro_y, 32):
                self.ponto_atual = p
                self.eh_entrada = False
                self.popup_nome = p.nome
                self.popup_texto = p.curiosidade
                self.popup_img = p.foto_popup
                self.popup_qr = p.qr_img
                self.mostrar_popup = True
                break

        return "GAME_SRS", reiniciar

    def desenhar(self, tela):
        tela.blit(self.mapa_img, (0, 0))
        tela.blit(self.estatua_img, self.estatua_rect)
        tela.blit(self.botao_reiniciar, self.botao_reiniciar_rect)

        pos_mouse = pygame.mouse.get_pos()

        # Botão Pular
        cor_pular = (70, 140, 210) if self.botao_pular_rect.collidepoint(pos_mouse) else (40, 90, 200)
        pygame.draw.rect(tela, cor_pular, self.botao_pular_rect, border_radius=6)
        pygame.draw.rect(tela, (50, 30, 15), self.botao_pular_rect, 2, border_radius=6)
        txt_pular = self.fonte_hud.render("PULAR", True, (255, 255, 255))
        tela.blit(txt_pular, txt_pular.get_rect(center=self.botao_pular_rect.center))

        visitados = sum(1 for p in self.pontos if p.visitado)
        for p in self.pontos:
            if p.imagem:
                tela.blit(p.imagem, p.imagem_rect)
            cor_tag = (46, 204, 113) if p.visitado else (30, 30, 35)
            texto_ponto = self.fonte_hud.render(p.nome, True, (255, 255, 255))
            rect_bg = pygame.Rect(p.x - (texto_ponto.get_width() // 2) - 6, p.y + 45, texto_ponto.get_width() + 12, 22)
            pygame.draw.rect(tela, cor_tag, rect_bg, border_radius=4)
            tela.blit(texto_ponto, (p.x - (texto_ponto.get_width() // 2), p.y + 48))

        # Desenha o sprite do personagem
        tela.blit(self.personagem.image, self.personagem.rect)

        # HUD Contador
        texto_hud = self.fonte_hud.render(f"Pontos Visitados: {visitados}/{self.total_pontos}", True, (25, 25, 25))
        hud_box = pygame.Rect(175, 5, texto_hud.get_width() + 20, 32)
        pygame.draw.rect(tela, (250, 248, 240), hud_box, border_radius=6)
        pygame.draw.rect(tela, (50, 30, 15), hud_box, 2, border_radius=6)
        tela.blit(texto_hud, texto_hud.get_rect(center=hud_box.center))

        # Pop-up
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

            if not self.eh_entrada:
                txt_qr = self.fonte_hud.render("Escaneie o QR", True, (80, 50, 20))
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

            instrucao = self.fonte_hud.render("Pressione [ESPAÇO] ou [ENTER] para fechar", True, (160, 40, 30))
            tela.blit(instrucao, (config.centroX - (instrucao.get_width() // 2), caixa.bottom - 24))