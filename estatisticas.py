import pygame
import banco
import config
import funcoes


class Estatisticas:
    def __init__(self):
        # Controle de rolagem
        self.scroll_y = 0  # Posição atual do scroll
        self.velocidade_scroll = 20  # Velocidade do scroll ao girar a rodinha

        # Dimensões da Janela Principal
        self.largura = 1100
        self.altura_visivel = 660

        self.visivel = False
        self.estatisticas = []

        self.bloco_estatisticas = pygame.Rect(0, 0, self.largura, self.altura_visivel)
        self.bloco_estatisticas.center = (config.centroX, config.altura // 2)

        self.botao_fechar_estatisticas = pygame.Rect(0, 0, 35, 35)
        self.botao_fechar_estatisticas.topright = (
            self.bloco_estatisticas.right - 15,
            self.bloco_estatisticas.top + 15,
        )

        self.input_senha = pygame.transform.scale(
            pygame.image.load(funcoes.obter_caminho_arquivo("assets/IMAGENS/senha.png")),
            (250, 125),
        )
        self.input_senha_rect = self.input_senha.get_rect(
            centerx=config.centroX, centery=self.bloco_estatisticas.centery
        )
        self.senha = "faitec"
        self.modo_senha = False
        self.lendo_senha = False

        self.senha_lida = ""

        # Área de corte do Scroll
        self.largura_tabela = self.bloco_estatisticas.width - 40
        self.altura_area_linhas = 450
        self.pos_y_tabela = self.bloco_estatisticas.y + 180

        # ESTADOS E RECTS DO POP-UP DE DETALHES DO JOGADOR
        self.popup_jogador_visivel = False
        self.jogador_selecionado = None

        self.largura_popup = 520
        self.altura_popup = 480
        self.bloco_popup = pygame.Rect(0, 0, self.largura_popup, self.altura_popup)
        self.bloco_popup.center = (config.centroX, config.altura // 2)

        self.botao_fechar_popup = pygame.Rect(0, 0, 120, 38)
        self.botao_fechar_popup.centerx = self.bloco_popup.centerx
        self.botao_fechar_popup.bottom = self.bloco_popup.bottom - 20

    def abrir(self):
        self.visivel = True
        self.modo_senha = True
        self.scroll_y = 0
        self.popup_jogador_visivel = False
        self.jogador_selecionado = None

    def gerenciar_eventos(self, evento):
        pos_mouse = pygame.mouse.get_pos()

        # 1. INTERCEPTAÇÕES QUANDO O POP-UP DO JOGADOR ESTÁ ABERTO
        if self.popup_jogador_visivel:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                config.click_sound.play()
                self.popup_jogador_visivel = False
                return True

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.botao_fechar_popup.collidepoint(pos_mouse):
                    config.click_sound.play()
                    self.popup_jogador_visivel = False
                return True

            # Bloqueia qualquer outra interação de cliques com a tabela de fundo
            return True

        # 2. EVENTOS PADRÃO DA TELA DE ESTATÍSTICAS
        if evento.type == pygame.MOUSEWHEEL and self.visivel and not self.modo_senha:
            altura_total_dados = len(self.estatisticas) * 38 + 10
            limite_maximo = max(0, altura_total_dados - self.altura_area_linhas)
            self.scroll_y -= evento.y * self.velocidade_scroll
            self.scroll_y = max(0, min(self.scroll_y, limite_maximo))

        if self.visivel and evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            config.click_sound.play()
            if self.botao_fechar_estatisticas.collidepoint(pos_mouse):
                self.visivel = False
                return False

            if self.modo_senha and self.input_senha_rect.collidepoint(pos_mouse):
                self.lendo_senha = True
                return True
            else:
                self.lendo_senha = False

            # Clique em uma linha da tabela para abrir o Pop-up
            if not self.modo_senha and self.estatisticas:
                area_tabela_rect = pygame.Rect(
                    self.bloco_estatisticas.x + 20,
                    self.pos_y_tabela,
                    self.largura_tabela,
                    self.altura_area_linhas,
                )

                if area_tabela_rect.collidepoint(pos_mouse):
                    y_relativo_clique = pos_mouse[1] - self.pos_y_tabela + self.scroll_y
                    indice_jogador = y_relativo_clique // 38

                    if 0 <= indice_jogador < len(self.estatisticas):
                        self.jogador_selecionado = self.estatisticas[int(indice_jogador)]
                        self.popup_jogador_visivel = True
                        return True

        if self.lendo_senha:
            if evento.type == pygame.TEXTINPUT:
                if len(self.senha_lida) < 6:
                    self.senha_lida += evento.text
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    self.senha_lida = self.senha_lida[:-1]

        if self.senha_lida == self.senha:
            self.modo_senha = False
            self.estatisticas = banco.carregar_estatisticas()

        if not self.visivel:
            return False

        return True

    def desenhar(self, tela):
        if not self.visivel:
            self.senha_lida = ""
            return

        # Fundo escurecido semi-transparente base
        fundo_escuro = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
        fundo_escuro.fill((0, 0, 0, 150))
        tela.blit(fundo_escuro, (0, 0))

        # Painel bege principal
        pygame.draw.rect(tela, config.bege, self.bloco_estatisticas, border_radius=16)
        pygame.draw.rect(tela, config.amarelo, self.bloco_estatisticas, width=4, border_radius=16)

        titulo = config.fonte_grossa.render("ESTATÍSTICAS DO JOGADOR", True, config.preto)
        titulo_rect = titulo.get_rect(
            centerx=self.bloco_estatisticas.centerx, y=self.bloco_estatisticas.y + 35
        )
        tela.blit(titulo, titulo_rect)

        if self.modo_senha:
            tela.blit(self.input_senha, self.input_senha_rect)
            senha_escondida = "*" * len(self.senha_lida)
            if self.lendo_senha: senha_escondida += "|"
            senha_escondida_render = config.fonte_input.render(senha_escondida, True, config.branco)
            senha_rect = senha_escondida_render.get_rect(centerx=self.input_senha_rect.centerx, centery=self.input_senha_rect.centery + 30)
            tela.blit(senha_escondida_render, senha_rect)

        elif self.estatisticas:
            texto_tela_est = config.fonte_fases.render("Porcentagem de erros por região", True, config.preto)
            texto_tela_est_rect = texto_tela_est.get_rect(centerx=self.bloco_estatisticas.centerx, y=self.bloco_estatisticas.y + 95)
            tela.blit(texto_tela_est, texto_tela_est_rect)

            colunas = ["Nome", "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

            posicoes_x = [
                self.bloco_estatisticas.x + 150,
                self.bloco_estatisticas.x + 360,
                self.bloco_estatisticas.x + 510,
                self.bloco_estatisticas.x + 690,
                self.bloco_estatisticas.x + 860,
                self.bloco_estatisticas.x + 980,
            ]

            for indice_coluna in range(len(colunas)):
                cabecalho = config.fonte_media.render(colunas[indice_coluna], False, config.preto)
                cabecalho_rect = cabecalho.get_rect(
                    centerx=posicoes_x[indice_coluna], y=self.bloco_estatisticas.y + 145
                )
                tela.blit(cabecalho, cabecalho_rect)

            altura_total_dados = max(self.altura_area_linhas, len(self.estatisticas) * 38 + 20)
            superficie_linhas = pygame.Surface(
                (self.largura_tabela, altura_total_dados), pygame.SRCALPHA
            )

            posicoes_x_relativas = [130, 340, 490, 670, 840, 960]

            cor_alternada = 0
            posicao_y_linha = 5
            for jogador in self.estatisticas:
                linha_rect = pygame.Rect(0, posicao_y_linha - 5, self.largura_tabela, 30)
                if cor_alternada == 0:
                    pygame.draw.rect(superficie_linhas, config.amarelo_pastel, linha_rect, border_radius=5)
                    cor_alternada = 1
                else:
                    pygame.draw.rect(superficie_linhas, config.verde_pastel, linha_rect, border_radius=5)
                    cor_alternada = 0

                # Nome do Jogador
                texto_nome = config.fonte_fases.render(str(jogador[0]), True, config.preto)
                rect_nome = texto_nome.get_rect(centerx=posicoes_x_relativas[0], y=posicao_y_linha)
                superficie_linhas.blit(texto_nome, rect_nome)

                # Regiões
                for indice_regiao in range(1, len(posicoes_x_relativas)):
                    if jogador[indice_regiao] == "0% (0/0)":
                        dados_na_tela = "Não jogada"
                    else:
                        dados_na_tela = jogador[indice_regiao]
                        
                    texto_regiao = config.fonte_dicas.render(f"{dados_na_tela}", False, config.preto)
                    rect_regiao = texto_regiao.get_rect(centerx=posicoes_x_relativas[indice_regiao], y=posicao_y_linha)
                    superficie_linhas.blit(texto_regiao, rect_regiao)

                posicao_y_linha += 38

            area_corte = pygame.Rect(0, self.scroll_y, self.largura_tabela, self.altura_area_linhas)
            tela.blit(superficie_linhas, (self.bloco_estatisticas.x + 20, self.pos_y_tabela), area_corte)
        else:
            texto_vazio = config.fonte_dicas.render("Nenhuma estatística registrada ainda.", True, config.preto)
            tela.blit(texto_vazio, texto_vazio.get_rect(center=self.bloco_estatisticas.center))

        # Botão Fechar Janela Principal (X)
        pygame.draw.rect(tela, config.vermelho, self.botao_fechar_estatisticas, border_radius=6)
        texto_fechar = config.fonte_fases.render("X", True, config.branco)
        rect_texto_fechar = texto_fechar.get_rect(center=self.botao_fechar_estatisticas.center)
        tela.blit(texto_fechar, rect_texto_fechar)

        # 3. RENDERIZAÇÃO DO POP-UP DO JOGADOR
        if self.popup_jogador_visivel and self.jogador_selecionado:
            self._desenhar_popup_jogador(tela)

    def _desenhar_popup_jogador(self, tela):
        # Fundo escurecido extra para focar no Pop-up
        fundo_pop = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
        fundo_pop.fill((0, 0, 0, 140))
        tela.blit(fundo_pop, (0, 0))

        # Aumentada a largura do pop-up para caber os 5 itens por linha sem espremer
        largura_popup_detalhes = 620
        altura_popup_detalhes = 500
        bloco_popup_detalhes = pygame.Rect(0, 0, largura_popup_detalhes, altura_popup_detalhes)
        bloco_popup_detalhes.center = (config.centroX, config.altura // 2)

        # Atualiza a posição do botão fechar para acompanhar a nova largura
        self.botao_fechar_popup.centerx = bloco_popup_detalhes.centerx
        self.botao_fechar_popup.bottom = bloco_popup_detalhes.bottom - 15

        # Caixa do Pop-up
        pygame.draw.rect(tela, config.bege, bloco_popup_detalhes, border_radius=16)
        pygame.draw.rect(tela, config.amarelo, bloco_popup_detalhes, width=4, border_radius=16)

        # Nome do Jogador
        nome_jogador = str(self.jogador_selecionado[0]).upper()
        titulo_popup = config.fonte_grossa.render(f"JOGADOR: {nome_jogador}", True, config.preto)
        titulo_popup_rect = titulo_popup.get_rect(
            centerx=bloco_popup_detalhes.centerx, y=bloco_popup_detalhes.y + 20
        )
        tela.blit(titulo_popup, titulo_popup_rect)

        # Cabeçalho da Lista
        cabecalhos = ["Região", "Jogadas", "Erros", "Acertos", "Porcentagem"]
        posicoes_x_cabecalho = [
            bloco_popup_detalhes.x + 80,
            bloco_popup_detalhes.x + 200,
            bloco_popup_detalhes.x + 300,
            bloco_popup_detalhes.x + 400,
            bloco_popup_detalhes.x + 520
        ]

        for idx, item in enumerate(cabecalhos):
            txt_cab = config.fonte_dicas.render(item, True, config.preto)
            txt_cab_rect = txt_cab.get_rect(centerx=posicoes_x_cabecalho[idx], y=bloco_popup_detalhes.y + 70)
            tela.blit(txt_cab, txt_cab_rect)

        pygame.draw.line(
            tela,
            config.preto,
            (bloco_popup_detalhes.x + 20, bloco_popup_detalhes.y + 95),
            (bloco_popup_detalhes.right - 20, bloco_popup_detalhes.y + 95),
            2,
        )

        regioes_nomes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
        total_erros_geral = 0
        total_jogadas_geral = 0

        pos_y = bloco_popup_detalhes.y + 110

        # Detalhes de cada região em formato de tabela/lista
        for i, regiao in enumerate(regioes_nomes):
            dado = str(self.jogador_selecionado[i + 1])
            
            porcentagem_str = "0%"
            erros = 0
            jogadas = 0
            acertos = 0

            if dado != "0% (0/0)":
                # Exemplo de dado: "12% (1/8)"
                porcentagem_str, fracao = dado.split(" (")
                erros, jogadas = map(int, fracao.rstrip(")").split("/"))

                acertos = max(0, jogadas - erros)
                total_erros_geral += erros
                total_jogadas_geral += jogadas

            # Renders de cada coluna
            txt_reg = config.fonte_media.render(regiao, True, config.preto)
            txt_jog = config.fonte_fases.render(str(jogadas), True, config.preto)
            txt_err = config.fonte_fases.render(str(erros), True, config.preto)
            txt_ace = config.fonte_fases.render(str(acertos), True, config.preto)
            txt_por = config.fonte_fases.render(porcentagem_str, True, config.preto)

            tela.blit(txt_reg, txt_reg.get_rect(centerx=posicoes_x_cabecalho[0], y=pos_y))
            tela.blit(txt_jog, txt_jog.get_rect(centerx=posicoes_x_cabecalho[1], y=pos_y))
            tela.blit(txt_err, txt_err.get_rect(centerx=posicoes_x_cabecalho[2], y=pos_y))
            tela.blit(txt_ace, txt_ace.get_rect(centerx=posicoes_x_cabecalho[3], y=pos_y))
            tela.blit(txt_por, txt_por.get_rect(centerx=posicoes_x_cabecalho[4], y=pos_y))

            pos_y += 38

        # Linha Divisória Inferior
        pygame.draw.line(tela,config.preto,(bloco_popup_detalhes.x + 20, pos_y + 10),(bloco_popup_detalhes.right - 20, pos_y + 10),2,)
        # Resumo Acumulado Geral
        pos_y += 25
        total_acertos_geral = max(0, total_jogadas_geral - total_erros_geral)

        txt_resumo = config.fonte_dicas.render(
            f"Total de Questões: {total_jogadas_geral}  |  Erros: {total_erros_geral}  |  Acertos: {total_acertos_geral}",
            True,
            config.preto,
        )
        txt_resumo_rect = txt_resumo.get_rect(centerx=bloco_popup_detalhes.centerx, y=pos_y)
        tela.blit(txt_resumo, txt_resumo_rect)

        # Botão Fechar
        pygame.draw.rect(tela, config.vermelho, self.botao_fechar_popup, border_radius=8)
        pygame.draw.rect(tela, config.preto, self.botao_fechar_popup, width=2, border_radius=8)

        txt_btn = config.fonte_fases.render("FECHAR", True, config.branco)
        txt_btn_rect = txt_btn.get_rect(center=self.botao_fechar_popup.center)
        tela.blit(txt_btn, txt_btn_rect)