import pygame
import banco
import config
import funcoes

class Estatisticas():
    def __init__(self):

        # Controle de rolagem
        self.scroll_y = 0         # Posição atual do scroll
        self.velocidade_scroll = 20 # Velocidade do scroll ao girar a rodinha

        self.largura = 900
        self.altura_visivel = 660
        
        self.visivel = False
        self.estatisticas = []

        self.bloco_estatisticas = pygame.Rect(0, 0, self.largura, self.altura_visivel)
        self.bloco_estatisticas.center = (config.centroX, config.altura // 2)

        self.botao_fechar_estatisticas = pygame.Rect(0, 0, 35, 35)
        self.botao_fechar_estatisticas.topright = (self.bloco_estatisticas.right - 15, self.bloco_estatisticas.top + 15)

        self.input_senha = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/senha.png")), (250, 125))
        self.input_senha_rect = self.input_senha.get_rect(centerx = config.centroX, centery = self.bloco_estatisticas.centery)
        self.senha = "faitec"
        self.modo_senha = False
        self.lendo_senha = False

        self.senha_lida = ""

        #ÁREA DE CORTE DO SCROLL
        self.largura_tabela = self.bloco_estatisticas.width - 20
        self.altura_area_linhas = 450  # Espaço vertical disponível para mostrar as linhas
        self.pos_y_tabela = self.bloco_estatisticas.y + 180  # Começa logo abaixo do cabeçalho

    def abrir(self):
        #self.estatisticas = banco.carregar_estatisticas()
        self.visivel = True
        self.modo_senha = True
        self.scroll_y = 0 #inicia no primeiro

    def gerenciar_eventos(self, evento):
        pos_mouse = pygame.mouse.get_pos()

        if evento.type == pygame.MOUSEWHEEL and self.visivel and not self.modo_senha:
            #altura total necessária para todas as linhas (38px por linha + margem)
            altura_total_dados = len(self.estatisticas) * 38 + 10
            limite_maximo = max(0, altura_total_dados - self.altura_area_linhas)
            # Atualiza o scroll
            self.scroll_y -= evento.y * self.velocidade_scroll
            self.scroll_y = max(0, min(self.scroll_y, limite_maximo))

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            config.click_sound.play()
            if self.botao_fechar_estatisticas.collidepoint(pos_mouse):
                self.visivel = False
                return False #sai do modo senha

            if self.modo_senha and self.input_senha_rect.collidepoint(pos_mouse):
                self.lendo_senha = True
                return True #modo senha
            else:
                self.lendo_senha = False

        if self.lendo_senha:
            if evento.type == pygame.TEXTINPUT:
                if len(self.senha_lida) < 6:
                    self.senha_lida += evento.text #grava texto na variavel
            if evento.type == pygame.KEYDOWN: #apaga letra na variavel
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

        fundo_escuro = pygame.Surface((config.largura, config.altura), pygame.SRCALPHA)
        fundo_escuro.fill((0, 0, 0, 150))
        tela.blit(fundo_escuro, (0, 0))

        pygame.draw.rect(tela, config.bege, self.bloco_estatisticas, border_radius=16)
        pygame.draw.rect(tela, config.amarelo, self.bloco_estatisticas, width=4, border_radius=16)

        titulo = config.fonte_grossa.render("ESTATÍSTICAS DO JOGADOR", True, config.preto)
        titulo_rect = titulo.get_rect(centerx=self.bloco_estatisticas.centerx, y=self.bloco_estatisticas.y + 35)
        tela.blit(titulo, titulo_rect)
        
        if self.modo_senha:
            tela.blit(self.input_senha, self.input_senha_rect)
            senha_escondida = "*" * len(self.senha_lida)
            if self.lendo_senha == True:
                senha_escondida += "|"
            senha_escondida = config.fonte_input.render(senha_escondida, True, config.branco)
            senha_rect = senha_escondida.get_rect(centerx = self.input_senha_rect.centerx, centery = self.input_senha_rect.centery + 30)
            tela.blit(senha_escondida, senha_rect)

        elif self.estatisticas:
            texto_tela_est = config.fonte_fases.render("Porcentagem de erros por região", True, config.preto)
            texto_tela_est_rect = texto_tela_est.get_rect(centerx=self.bloco_estatisticas.centerx, y=self.bloco_estatisticas.y + 95)
            tela.blit(texto_tela_est, texto_tela_est_rect)
    
            colunas = ["Nome", "Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
    
            posicoes_x = [
                self.bloco_estatisticas.x + 120,self.bloco_estatisticas.x + 290,
                self.bloco_estatisticas.x + 410,self.bloco_estatisticas.x + 555,
                self.bloco_estatisticas.x + 700,self.bloco_estatisticas.x + 800
            ]
    
            for i in range(len(colunas)):
                cabecalho = config.fonte_media.render(colunas[i], False, config.preto)
                cabecalho_rect = cabecalho.get_rect(centerx=posicoes_x[i], y=self.bloco_estatisticas.y + 145)
                tela.blit(cabecalho, cabecalho_rect)

            #DESENHO DAS LINHAS COM SCROLL (Superfície Virtual)
            altura_total_dados = max(self.altura_area_linhas, len(self.estatisticas) * 38 + 20)
            superficie_linhas = pygame.Surface((self.largura_tabela, altura_total_dados), pygame.SRCALPHA)
            posicoes_x_relativas = [
                110, 280, 400, 545, 690, 790
            ]
            L = 0
            y_linha = 5
            for jogador in self.estatisticas:
                linha_rect = pygame.Rect(0, y_linha - 5, self.largura_tabela, 30)
                if L == 0:
                    pygame.draw.rect(superficie_linhas, config.amarelo_pastel, linha_rect, border_radius=5)
                    L = 1
                else:
                    pygame.draw.rect(superficie_linhas, config.verde_pastel, linha_rect, border_radius=5)
                    L = 0

                # 1. Nome do Jogador (sem %)
                texto_nome = config.fonte_fases.render(str(jogador[0]), True, config.preto)
                rect_nome = texto_nome.get_rect(centerx=posicoes_x_relativas[0], y=y_linha)
                superficie_linhas.blit(texto_nome, rect_nome)

                # 2. Regiões (Norte até Sul, com %)
                for i in range(1, len(posicoes_x_relativas)):
                    texto_regiao = config.fonte_dicas.render(f"{jogador[i]}%", False, config.preto)
                    rect_regiao = texto_regiao.get_rect(centerx=posicoes_x_relativas[i], y=y_linha)
                    superficie_linhas.blit(texto_regiao, rect_regiao)

                y_linha += 38

            #RECORTE DA ÁREA VISÍVEL
            # Define qual pedaço da superfície de dados vai ser exibido
            area_corte = pygame.Rect(0, self.scroll_y, self.largura_tabela, self.altura_area_linhas)
            # Desenha apenas a fatia visível dentro do card bege
            tela.blit(superficie_linhas, (self.bloco_estatisticas.x + 10, self.pos_y_tabela), area_corte)

        pygame.draw.rect(tela, config.vermelho, self.botao_fechar_estatisticas, border_radius=6)

        fechar = config.fonte_fases.render("X", True, config.branco)
        fechar_rect = fechar.get_rect(center=self.botao_fechar_estatisticas.center)
        tela.blit(fechar, fechar_rect)