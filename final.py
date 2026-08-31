import pygame
import banco
import config
import funcoes
from estatisticas import Estatisticas

estatisticas = Estatisticas()

class Final:
    def __init__(self):
        self.top_jogadores = []
        
        self.botao_qr = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_qr.png")), (50, 50))
        self.botao_qr_rect = self.botao_qr.get_rect(x=114, y=2)

        self.botao_estatisticas = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_estatisticas.png")), (50, 50))
        self.botao_estatisticas_rect = self.botao_estatisticas.get_rect(x=108, y=2)

        self.bloco_qr = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/bloco_qr.png")), (400, 600))
        self.bloco_qr_rect = self.bloco_qr.get_rect(centerx = config.centroX, centery = config.altura // 2)

        self.botao_replay = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_jogar.png")), (160, 40))
        self.botao_replay_rect = self.botao_replay.get_rect(x= config.largura - 170, y=7)

        self.qr = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/QR.png")), (200, 200))
        self.qr_rect = self.qr.get_rect(centerx = config.centroX, centery = config.altura // 3)

        self.botao_fechar = pygame.Rect(0, 0, 35, 35)
        self.botao_fechar.topright = (self.bloco_qr_rect.right - 27, self.bloco_qr_rect.top + 32)

        self.reiniciar = False
        self.status_qr = False

    def gerenciar_eventos(self, evento):
        estatisticas.gerenciar_eventos(evento)
        pos_mouse = pygame.mouse.get_pos()
        if self.botao_fechar.collidepoint(pos_mouse) and self.status_qr or self.botao_estatisticas_rect.collidepoint(pos_mouse) or self.botao_qr_rect.collidepoint(pos_mouse) :
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.botao_replay_rect.collidepoint(pos_mouse):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: #ve se foi o botão esquerdo
                config.click_sound.play()
                if self.botao_estatisticas_rect.collidepoint(pos_mouse):
                    estatisticas.abrir()
                elif self.botao_qr_rect.collidepoint(pos_mouse):
                    self.status_qr = True
                elif self.botao_fechar.collidepoint(pos_mouse):
                    self.status_qr = False
                elif self.botao_replay_rect.collidepoint(pos_mouse):
                    self.reiniciar = True

    def atualizar(self, rodar_ranking, reiniciar): #recebe o salvarBD se for true significa que pode salavr uma vez o ranking

        if self.reiniciar:
            reiniciar = True
            return "MENU", reiniciar

        if rodar_ranking:
            banco.salvar_dados(config.nome_jogador, config.idade_jogador, config.acertos_jogador, config.erros_jogador, config.tempo_sobra)
            self.top_jogadores = banco.carregar_ranking()
            # BD.salvar_dados_jogador(config.nome_jogador, config.idade_jogador, config.acertos_jogador, config.erros_jogador, config.tempo_sobra)
            # self.top_jogadores = BD.rankear()
        return "FINAL", reiniciar
    
    def desenhar(self, tela):
        tela.fill((16, 71, 15))
        tela.blit(self.botao_estatisticas, self.botao_estatisticas_rect)
        tela.blit(self.botao_qr, self.botao_qr_rect)
        tela.blit(self.botao_replay, self.botao_replay_rect)

        parabens_texto = f"Parabéns, {config.nome_jogador}!"
        parabens_renderizado = config.fonte_fases.render(parabens_texto, True, config.amarelo)
        rect_parabens = parabens_renderizado.get_rect(centerx=config.centroX, y = 30)
        tela.blit(parabens_renderizado, rect_parabens)

        texto_pontos = f"Acertos: {config.acertos_jogador}  |  Erros: {config.erros_jogador}"
        texto_pontos_renderizado = config.fonte_fases.render(texto_pontos, True, config.branco)
        texto_pontos_renderizado_rect = texto_pontos_renderizado.get_rect(centerx=config.centroX, y = 85)
        tela.blit(texto_pontos_renderizado, texto_pontos_renderizado_rect)

        largura_ranking = 800
        altura_ranking = 550
        rect_ranking = pygame.Rect(config.centroX - (largura_ranking // 2), 120, largura_ranking, altura_ranking)

        pygame.draw.rect(tela, config.bege, rect_ranking, border_radius=12)
        # Borda externa do quadro
        pygame.draw.rect(tela, config.amarelo, rect_ranking, width=3, border_radius=12)

        ranking_texto = config.fonte_fases.render("RANKING", True, config.preto)
        ranking_renderizado = ranking_texto.get_rect(centerx=rect_ranking.centerx, y = rect_ranking.y + 15)
        tela.blit(ranking_texto, ranking_renderizado)

        y_linha = rect_ranking.y + 65
        for pos, jogador in enumerate(self.top_jogadores):
            nome = jogador[0]
            acertos = jogador[2]
            erros = jogador[3]

            #ORGANIZAÇÃO DE BACKGROUND DOS JOGADORES
            blocos_rect = pygame.Rect(0, y_linha, largura_ranking - 15, 45)
            blocos_rect.centerx = config.centroX
            blocos_rect.centery = y_linha
            if pos == 0:
                cor_fundo = config.ouro
                cor_texto = config.preto
            elif pos == 1:
                cor_fundo = config.prata
                cor_texto = config.preto
            elif pos == 2:
                cor_fundo = config.bronze
                cor_texto = config.branco
            elif nome == config.nome_jogador:
                cor_fundo = (123, 252, 3)
                cor_texto = config.preto
            else:
                cor_fundo = config.padrao
                cor_texto = config.preto

            pygame.draw.rect(tela, cor_fundo, blocos_rect, border_radius=5)

            # Monta a frase formatada (Ex: "1º  MATHEUS  -  27 Acertos | 9 Erros")
            texto_linha = f"{pos + 1}º  {nome}  -  {acertos} Acertos | {erros} Erros"
            texto_linha_renderizado = config.fonte_fases.render(texto_linha, True, cor_texto)
            texto_linha_renderizado_rect = texto_linha_renderizado.get_rect(centerx = config.centroX, centery = y_linha)

            tela.blit(texto_linha_renderizado, texto_linha_renderizado_rect)
    
            y_linha += 50

        if self.status_qr:
            tela.blit(self.bloco_qr, self.bloco_qr_rect)
            tela.blit(self.qr, self.qr_rect)
            pygame.draw.rect(tela, config.vermelho, self.botao_fechar, border_radius=6)

            # --- CRÉDITOS DENTRO DO BLOCO QR ---
            creditos_titulo = config.fonte_dicas.render("Desenvolvido por:", True, config.amarelo)
            creditos_titulo_rect = creditos_titulo.get_rect(centerx=config.centroX, y=self.qr_rect.bottom + 200)
            tela.blit(creditos_titulo, creditos_titulo_rect)

            creditos_nomes = config.fonte_dicas.render("Matheus Openheimer,", True, config.amarelo)
            creditos_nomes_rect = creditos_nomes.get_rect(centerx=config.centroX, y=creditos_titulo_rect.bottom + 8)
            tela.blit(creditos_nomes, creditos_nomes_rect)

            creditos_nomes2 = config.fonte_dicas.render("Cecília Alves", True, config.amarelo)
            creditos_nomes2_rect = creditos_nomes2.get_rect(centerx=config.centroX, y=creditos_nomes_rect.bottom + 5)
            tela.blit(creditos_nomes2, creditos_nomes2_rect)

            creditos_nomes3 = config.fonte_dicas.render("e Bruno Siécola", True, config.amarelo)
            creditos_nomes3_rect = creditos_nomes3.get_rect(centerx=config.centroX, y=creditos_nomes2_rect.bottom + 5)
            tela.blit(creditos_nomes3, creditos_nomes3_rect)

            fechar = config.fonte_fases.render("X", True, config.branco)
            fechar_rect = fechar.get_rect(center=self.botao_fechar.center)
            tela.blit(fechar, fechar_rect)

        estatisticas.desenhar(tela)