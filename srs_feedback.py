import pygame
import config
import funcoes
import banco



class VisualizarFeedbacks:
    def __init__(self):
        # Controle de rolagem
        self.scroll_y = 0  # Posição atual do scroll
        self.velocidade_scroll = 20  # Velocidade do scroll ao girar a rodinha

        self.largura = 900
        self.altura_visivel = 660

        self.visivel = False
        self.feedbacks = []

        self.bloco_feedbacks = pygame.Rect(0, 0, self.largura, self.altura_visivel)
        self.bloco_feedbacks.center = (config.centroX, config.altura // 2)

        self.botao_fechar = pygame.Rect(0, 0, 35, 35)
        self.botao_fechar.topright = (self.bloco_feedbacks.right - 15, self.bloco_feedbacks.top + 15)

        self.input_senha = pygame.transform.scale(
            pygame.image.load(funcoes.resource_path("assets/IMAGENS/senha.png")), (250, 125)
        )
        self.input_senha_rect = self.input_senha.get_rect(
            centerx=config.centroX, centery=self.bloco_feedbacks.centery
        )
        self.senha = "faitec"
        self.modo_senha = False
        self.lendo_senha = False

        self.senha_lida = ""

        # ÁREA DE CORTE DO SCROLL
        self.largura_tabela = self.bloco_feedbacks.width - 20
        self.altura_area_linhas = 450  # Espaço vertical disponível para mostrar as linhas
        self.pos_y_tabela = self.bloco_feedbacks.y + 180  # Começa logo abaixo do cabeçalho

        # Pop-up de detalhes da avaliação
        self.popup_visivel = False
        self.popup_texto = ""
        self.popup_jogador = ""
        self.popup_ponto = ""
        self.popup_rect = pygame.Rect(0, 0, 700, 320)
        self.popup_rect.center = (config.centroX, config.altura // 2)
        self.popup_botao_fechar = pygame.Rect(0, 0, 35, 35)
        self.popup_botao_fechar.topright = (self.popup_rect.right - 15, self.popup_rect.top + 15)


    def abrir(self):
        self.visivel = True
        self.modo_senha = True
        self.scroll_y = 0  # Inicia no primeiro
        self.senha_lida = ""
        self.lendo_senha = False
        self.popup_visivel = False

    def gerenciar_eventos(self, evento):
        # Se a tela NÃO estiver aberta, sai imediatamente e libera o Menu
        if not self.visivel:
            return False

        pos_mouse = pygame.mouse.get_pos()

        # Tecla ESC fecha o pop-up de detalhes se ele estiver aberto
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE and self.popup_visivel:
            self.popup_visivel = False
            return True

        # Se o pop-up da avaliação estiver aberto, apenas ele pode receber cliques
        if self.popup_visivel:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                config.click_sound.play()
                if self.popup_botao_fechar.collidepoint(pos_mouse):
                    self.popup_visivel = False
                # Bloqueia qualquer clique de passar para a tela de trás
                return True
            return True

        # Scroll do mouse na lista (bloqueado se o pop-up estiver aberto)
        if evento.type == pygame.MOUSEWHEEL and not self.modo_senha:
            altura_total_dados = len(self.feedbacks) * 75 + 10
            limite_maximo = max(0, altura_total_dados - self.altura_area_linhas)
            self.scroll_y -= evento.y * self.velocidade_scroll
            self.scroll_y = max(0, min(self.scroll_y, limite_maximo))

        # Cliques do mouse na tela de feedback
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.visivel:

            # Botão fechar
            if self.botao_fechar.collidepoint(pos_mouse):
                self.visivel = False
                self.modo_senha = False
                self.lendo_senha = False
                self.senha_lida = ""
                return False  # Sai totalmente do modo feedback

            # Campo de entrada de senha
            if self.modo_senha and self.input_senha_rect.collidepoint(pos_mouse):
                self.lendo_senha = True
                return True  # Foco de digitação ativo
            else:
                self.lendo_senha = False

            # Clique em uma linha de feedback para abrir o popup detalhado
            if not self.modo_senha:
                area_x = self.bloco_feedbacks.x + 10
                area_y = self.pos_y_tabela
                if area_x <= pos_mouse[0] <= area_x + self.largura_tabela and area_y <= pos_mouse[1] <= area_y + self.altura_area_linhas:
                    pos_y_clique = (pos_mouse[1] - area_y) + self.scroll_y
                    indice = pos_y_clique // 75
                    if 0 <= indice < len(self.feedbacks):
                        jogador, ponto_turistico, texto_fb, _ = self.feedbacks[indice]
                        self.popup_jogador = str(jogador)
                        self.popup_ponto = str(ponto_turistico)
                        self.popup_texto = str(texto_fb)
                        self.popup_visivel = True
                        return True

        # Digitação da senha
        if self.lendo_senha and self.modo_senha:
            if evento.type == pygame.TEXTINPUT:
                if len(self.senha_lida) < 6:
                    self.senha_lida += evento.text  # Grava texto na variável
            if evento.type == pygame.KEYDOWN:  # Apaga letra na variável
                if evento.key == pygame.K_BACKSPACE:
                    self.senha_lida = self.senha_lida[:-1]

        # Validação da senha
        if self.modo_senha and self.senha_lida == self.senha:
            self.modo_senha = False
            self.lendo_senha = False
            self.feedbacks = banco.carregar_feedbacks_srs()

        if not self.visivel:
            return False

        return True

    def desenhar(self, tela):
        if not self.visivel:
            self.senha_lida = ""
            return

        fundo_escuro = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
        fundo_escuro.fill((0, 0, 0, 150))
        tela.blit(fundo_escuro, (0, 0))

        pygame.draw.rect(tela, config.bege, self.bloco_feedbacks, border_radius=16)
        pygame.draw.rect(tela, config.amarelo, self.bloco_feedbacks, width=4, border_radius=16)

        titulo = config.fonte_grossa.render("FEEDBACKS SANTA RITA", True, config.preto)
        titulo_rect = titulo.get_rect(centerx=self.bloco_feedbacks.centerx, y=self.bloco_feedbacks.y + 35)
        tela.blit(titulo, titulo_rect)

        if self.modo_senha:
            tela.blit(self.input_senha, self.input_senha_rect)
            senha_escondida = "*" * len(self.senha_lida)
            if self.lendo_senha == True:
                senha_escondida += "|"
            senha_escondida_render = config.fonte_dicas.render(senha_escondida, True, config.branco)
            senha_rect = senha_escondida_render.get_rect(
                centerx=self.input_senha_rect.centerx, centery=self.input_senha_rect.centery + 30
            )
            tela.blit(senha_escondida_render, senha_rect)

        elif self.feedbacks:
            texto_tela_feed = config.fonte_fases.render("Registros de avaliações dos pontos turísticos", True, config.preto)
            texto_tela_feed_rect = texto_tela_feed.get_rect(
                centerx=self.bloco_feedbacks.centerx, y=self.bloco_feedbacks.y + 95
            )
            tela.blit(texto_tela_feed, texto_tela_feed_rect)

            # Cabeçalhos com centros fixos para cada coluna
            pos_x_jogador = self.bloco_feedbacks.x + 95
            pos_x_ponto = self.bloco_feedbacks.x + 295
            pos_x_avaliacao = self.bloco_feedbacks.x + 620

            cabecalho_jog = config.fonte_dicas.render("Jogador", True, config.preto)
            rect_cab_jog = cabecalho_jog.get_rect(centerx=pos_x_jogador, y=self.bloco_feedbacks.y + 145)
            tela.blit(cabecalho_jog, rect_cab_jog)

            cabecalho_pto = config.fonte_dicas.render("Ponto Turístico", True, config.preto)
            rect_cab_pto = cabecalho_pto.get_rect(centerx=pos_x_ponto, y=self.bloco_feedbacks.y + 145)
            tela.blit(cabecalho_pto, rect_cab_pto)

            cabecalho_av = config.fonte_dicas.render("Avaliação", True, config.preto)
            rect_cab_av = cabecalho_av.get_rect(centerx=pos_x_avaliacao, y=self.bloco_feedbacks.y + 145)
            tela.blit(cabecalho_av, rect_cab_av)

            # DESENHO DAS LINHAS COM SCROLL
            altura_total_dados = max(self.altura_area_linhas, len(self.feedbacks) * 75 + 20)
            superficie_linhas = pygame.Surface((self.largura_tabela, altura_total_dados), pygame.SRCALPHA)

            centro_relativo_avaliacao = 620

            L = 0
            y_linha = 5
            for item in self.feedbacks:
                jogador, ponto_turistico, texto_fb, data_reg = item
                linha_rect = pygame.Rect(0, y_linha, self.largura_tabela, 68)

                if L == 0:
                    pygame.draw.rect(superficie_linhas, config.amarelo_pastel, linha_rect, border_radius=6)
                    L = 1
                else:
                    pygame.draw.rect(superficie_linhas, config.verde_pastel, linha_rect, border_radius=6)
                    L = 0

                # Coluna Jogadores
                texto_nome = config.fonte_dicas.render(str(jogador)[:14], True, config.preto)
                rect_nome = texto_nome.get_rect(x=15, y=y_linha + 8)
                superficie_linhas.blit(texto_nome, rect_nome)

                # Coluna Ponto Turístico com quebra
                linhas_ponto = funcoes.formatar_texto_largura(str(ponto_turistico), config.fonte_dicas, 180)
                y_ponto_atual = y_linha + 8
                for lp in linhas_ponto[:2]:
                    render_ponto = config.fonte_dicas.render(lp, True, (60, 30, 10))
                    superficie_linhas.blit(render_ponto, (220, y_ponto_atual))
                    y_ponto_atual += 18

                # Coluna Avaliação centralizada
                linhas_fb = funcoes.formatar_texto_largura(str(texto_fb), config.fonte_dicas, 460)
                y_fb_atual = y_linha + 10
                for lfb in linhas_fb[:2]:
                    render_fb = config.fonte_dicas.render(lfb, True, (30, 30, 30))
                    rect_fb = render_fb.get_rect(centerx=centro_relativo_avaliacao, y=y_fb_atual)
                    superficie_linhas.blit(render_fb, rect_fb)
                    y_fb_atual += 18

                # Data do Registro
                if data_reg:
                    data_formatada = str(data_reg)[:10]
                    txt_data = config.fonte_dicas.render(data_formatada, True, (100, 100, 100))
                    superficie_linhas.blit(txt_data, (15, y_linha + 42))

                y_linha += 75

            # RECORTE DA ÁREA VISÍVEL
            area_corte = pygame.Rect(0, self.scroll_y, self.largura_tabela, self.altura_area_linhas)
            tela.blit(superficie_linhas, (self.bloco_feedbacks.x + 10, self.pos_y_tabela), area_corte)
        else:
            texto_vazio = config.fonte_dicas.render("Nenhum feedback registrado ainda.", True, config.preto)
            tela.blit(texto_vazio, texto_vazio.get_rect(center=self.bloco_feedbacks.center))

        pygame.draw.rect(tela, config.vermelho, self.botao_fechar, border_radius=6)
        fechar = config.fonte_fases_bold.render("X", True, config.branco)
        fechar_rect = fechar.get_rect(center=self.botao_fechar.center)
        tela.blit(fechar, fechar_rect)

        # Pop-up aberto
        if self.popup_visivel:
            self.desenhar_popup(tela)

    def desenhar_popup(self, tela):
        # Fundo escurecido semi-transparente para dar foco exclusivo ao pop-up
        sombra_fundo = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
        sombra_fundo.fill((0, 0, 0, 100))
        tela.blit(sombra_fundo, (0, 0))

        pygame.draw.rect(tela, config.branco, self.popup_rect, border_radius=16)
        pygame.draw.rect(tela, config.amarelo, self.popup_rect, width=4, border_radius=16)

        tit_popup = config.fonte_fases_bold.render("Avaliação Completa", True, config.preto)
        tela.blit(tit_popup, (self.popup_rect.x + 25, self.popup_rect.y + 20))

        sub_popup = config.fonte_dicas.render(f"{self.popup_jogador} - {self.popup_ponto}", True, (90, 90, 90))
        tela.blit(sub_popup, (self.popup_rect.x + 25, self.popup_rect.y + 55))

        linhas = funcoes.formatar_texto_largura(self.popup_texto, config.fonte_dicas, 640)
        y_txt = self.popup_rect.y + 95
        for l in linhas[:8]:
            render_l = config.fonte_dicas.render(l, True, (30, 30, 30))
            tela.blit(render_l, (self.popup_rect.x + 25, y_txt))
            y_txt += 20

        pygame.draw.rect(tela, config.vermelho, self.popup_botao_fechar, border_radius=6)
        fechar_pop = config.fonte_fases_bold.render("X", True, config.branco)
        tela.blit(fechar_pop, fechar_pop.get_rect(center=self.popup_botao_fechar.center))