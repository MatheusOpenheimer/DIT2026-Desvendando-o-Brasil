import pygame
import config
import funcoes
from estatisticas import Estatisticas
from srs_feedback import VisualizarFeedbacks

estatisticas = Estatisticas()
visualizar_feedbacks = VisualizarFeedbacks()

class Menu:
    def __init__(self):
        self.fundo = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/fundomapa.png")), (config.largura, config.altura))
        self.fundo_rect = self.fundo.get_rect(centerx = config.centroX, centery = config.altura // 2)

        # LOGO
        self.desvendando_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/desvendando.png")), (500, 140))
        self.desvendando_rect = self.desvendando_img.get_rect(centerx = config.centroX, centery = 30)

        self.oBrasil_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/oBrasil.png")), (500, 140))
        self.oBrasil_rect = self.desvendando_img.get_rect(centerx = config.centroX, centery = 70)

        self.bandeira_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/bandeira.png")), (250, 150))
        self.bandeira_rect = self.bandeira_img.get_rect()
        self.bandeira_rect.centerx = config.largura / 2
        self.bandeira_rect.centery = 160

        self.bandeira_estado = "DESCENDO"
        self.alvo_y = 190

        # BOTÕES
        self.input_name_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/input_name.png")), (config.tamanho_botao))
        self.input_name_rect = self.input_name_img.get_rect(centerx = config.centroX, y = config.posicoes_botao_y[0])

        self.input_idade_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/input_idade.png")), (config.tamanho_botao))
        self.input_idade_rect = self.input_idade_img.get_rect(centerx = config.centroX, y = config.posicoes_botao_y[1])

        self.botao_iniciar_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_iniciar.png")), (230, 100))
        self.botao_iniciar_rect = self.botao_iniciar_img.get_rect(centerx = config.centroX, y = config.posicoes_botao_y[2])
        self.iniciar_clicado_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/iniciar_clicado.png")), (230, 100))

        self.alerta_menu_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/alerta_menu.png")), (500, 250))
        self.alerta_menu_rect = self.alerta_menu_img.get_rect(centerx = config.centroX, centery = config.altura / 2)

        # Botão Estatísticas (x=58)
        self.botao_estatisticas = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_estatisticas.png")), (50, 50))
        self.botao_estatisticas_rect = self.botao_estatisticas.get_rect(x =114, y = 2)

        # Botão Feedbacks (x=114) com a imagem feedback.png
        self.botao_feedback = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS_SRS/feedback.png")), (50, 50))
        self.botao_feedback_rect = self.botao_feedback.get_rect(x = 174, y = 2)

        # GERENCIAMENTO DE ESTADOS
        self.nome_usuario = ""
        self.idade_usuario = ""
        self.status_input_name = False
        self.status_input_idade = False
        self.confirmacao = False

        self.SUMIR_ALERTA_EVENTO = pygame.USEREVENT + 1
        self.segurando_mouse = False

    def gerenciar_eventos(self, evento):
        modo_estatisticas = estatisticas.gerenciar_eventos(evento)
        modo_feedback = visualizar_feedbacks.gerenciar_eventos(evento)
        pos_mouse = pygame.mouse.get_pos()

        if modo_estatisticas or modo_feedback:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            if self.input_idade_rect.collidepoint(pos_mouse) or \
               self.input_name_rect.collidepoint(pos_mouse) or \
               self.botao_iniciar_rect.collidepoint(pos_mouse) or \
               self.botao_estatisticas_rect.collidepoint(pos_mouse) or \
               self.botao_feedback_rect.collidepoint(pos_mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
        if evento.type == self.SUMIR_ALERTA_EVENTO:
            self.confirmacao = False
            pygame.time.set_timer(self.SUMIR_ALERTA_EVENTO, 0)

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            config.click_sound.play()

            if not modo_estatisticas and not modo_feedback:
                if self.botao_estatisticas_rect.collidepoint(pos_mouse):
                    estatisticas.abrir()

                elif self.botao_feedback_rect.collidepoint(pos_mouse):
                    visualizar_feedbacks.abrir()

                elif self.input_name_rect.collidepoint(evento.pos):
                    self.status_input_name = True
                    self.status_input_idade = False

                elif self.input_idade_rect.collidepoint(evento.pos):
                    self.status_input_name = False
                    self.status_input_idade = True

                else:
                    self.status_input_name = False
                    self.status_input_idade = False

                if self.botao_iniciar_rect.collidepoint(evento.pos):
                    self.segurando_mouse = True
                    if self.nome_usuario == "" or self.idade_usuario == "":
                        self.confirmacao = True
                        pygame.time.set_timer(self.SUMIR_ALERTA_EVENTO, 2000, loops=1)
                    else:
                        config.nome_jogador = self.nome_usuario
                        config.idade_jogador = self.idade_usuario
                        return "INTRO"

        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.segurando_mouse = False
                        
        if self.status_input_name and not modo_estatisticas and not modo_feedback:
            if evento.type == pygame.TEXTINPUT:
                if len(self.nome_usuario) < 14:
                    self.nome_usuario += evento.text
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    self.nome_usuario = self.nome_usuario[:-1]

        elif self.status_input_idade and not modo_estatisticas and not modo_feedback:
            if evento.type == pygame.TEXTINPUT:
                if evento.text.isnumeric():
                    if len(self.idade_usuario) < 2:
                        self.idade_usuario += evento.text
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    self.idade_usuario = self.idade_usuario[:-1]
                    
        return "MENU"
                    
    def desenhar(self, tela):   
        tela.blit(self.fundo, self.fundo_rect)
        tela.blit(self.botao_estatisticas, self.botao_estatisticas_rect)
        tela.blit(self.botao_feedback, self.botao_feedback_rect)
        
        tela.blit(self.desvendando_img, self.desvendando_rect)
        tela.blit(self.oBrasil_img, self.oBrasil_rect)

        self.bandeira_estado = funcoes.movimento1(self.bandeira_estado, self.bandeira_rect, self.alvo_y)
        tela.blit(self.bandeira_img, self.bandeira_rect)

        tela.blit(self.input_name_img, self.input_name_rect)
        tela.blit(self.input_idade_img, self.input_idade_rect)
        if self.segurando_mouse:
            tela.blit(self.iniciar_clicado_img, self.botao_iniciar_rect)
        else:
            tela.blit(self.botao_iniciar_img, self.botao_iniciar_rect)

        # Nome
        nome_na_tela = self.nome_usuario
        if self.status_input_name:
            nome_na_tela = self.nome_usuario + "|"
        nome_renderizado = config.fonte_input.render(nome_na_tela, False, config.branco)
        nome_renderizado_rect = nome_renderizado.get_rect()
        nome_renderizado_rect.centerx = self.input_name_rect.centerx + 8
        nome_renderizado_rect.y = self.input_name_rect.y + 64
        tela.blit(nome_renderizado, nome_renderizado_rect)

        # Idade
        idade_na_tela = self.idade_usuario    
        if self.status_input_idade:
            idade_na_tela = self.idade_usuario + "|"
        idade_renderizada = config.fonte_input.render(idade_na_tela, True, config.branco)
        idade_renderizada_rect = idade_renderizada.get_rect()
        idade_renderizada_rect.centerx = self.input_idade_rect.centerx
        idade_renderizada_rect.y = self.input_idade_rect.y + 62
        tela.blit(idade_renderizada, idade_renderizada_rect)

        if self.confirmacao:
            tela.blit(self.alerta_menu_img, self.alerta_menu_rect)

        estatisticas.desenhar(tela)
        visualizar_feedbacks.desenhar(tela)