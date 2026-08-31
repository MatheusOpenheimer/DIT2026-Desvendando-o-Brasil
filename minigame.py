import pygame
import config
import estados
from sprite import Personagem
import funcoes
import os


class Minigame:

    def __init__(self):
        self.curiosidades_estados = funcoes.carregar_curiosidades_txt(os.path.join("dados", "curiosidades.txt"))


        # Carrega e ajusta o tamanho da imagem de fundo para a resolução do jogo
        self.fundo_img = pygame.image.load(funcoes.resource_path("assets/IMAGENS/fundo_game.png")).convert_alpha()
        self.fundo_img = pygame.transform.scale(self.fundo_img, (config.largura, config.altura))
        # INTRO ----------------------------------------------------------------
        self.intro_img = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/minigame.png")), (600, 400))
        self.intro_rect = self.intro_img.get_rect(centerx=config.centroX, centery=-300)
        
        self.intro_estado = "ENTRANDO"
        self.alvo_y = config.altura // 2
        self.tempo_inicio_espera = 0
        self.duracao_espera = 1000

        #------------------------------------------------------------------------------------
        self.largura = config.largura
        self.altura = config.altura

        self.fonte_escrita = pygame.font.SysFont("arial", 11, bold=True)
        self.fonte_popup = pygame.font.SysFont("arial", 20, bold=True)
        self.fonte_curiosidades = pygame.font.Font(funcoes.resource_path("assets/FONTES/Afonte.ttf"), 11)

        self.blocos_estados = []
        self._criar_mapa_estados_quadrado()

        self.todas_sprites = pygame.sprite.Group()
        self.personagem = Personagem()
        self.todas_sprites.add(self.personagem)

        self.botao_skip = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/skip.png")), (150, 54))
        self.botao_skip_rect = self.botao_skip.get_rect(x = config.largura - 290, y = config.altura - 70)

        self.janela_skip = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/skip_pop.png")), (400, 400))
        self.janela_skip_rect = self.janela_skip.get_rect(centerx = config.centroX, centery = config.altura // 2)
        self.botao_sair = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/pular.png")), (155, 80))
        self.botao_sair_rect = self.botao_sair.get_rect(centerx = config.centroX - 85, y = self.janela_skip_rect.y + 250)
        self.botao_continuar = pygame.transform.scale(pygame.image.load(funcoes.resource_path("assets/IMAGENS/botao_continuar.png")), (155, 80))
        self.botao_continuar_rect = self.botao_continuar.get_rect(centerx = config.centroX + 85, y = self.botao_sair_rect.y)

        self.estado_atual_colisao = None
        self.confirmacao_fase1 = False
        self.mudar_fase = False
        self.clicou_ficar = False

    def _criar_mapa_estados_quadrado(self):
        largura_img, altura_img = 50, 40
        margem = 25
        posicoes = []

        # 1. TOPO (8 estados)
        for i in range(8):
            x = margem + i * ((self.largura - (2 * margem) - largura_img) // 8)
            posicoes.append((x + 70, margem - 20))

        # 2. DIREITA (6 estados)
        for i in range(6):
            y = 80 + i * ((self.altura - 160 - altura_img) // 5)
            posicoes.append((self.largura - largura_img - margem - 15, y))

        # 3. BASE
        offset_x_base = 100
        for i in range(6):
            x = margem + offset_x_base + i * ((self.largura - largura_img - 4.5 * margem - offset_x_base) // 7)
            posicoes.append((x, self.altura - 35 - altura_img))

        # 4. ESQUERDA (7 estados - Puxados mais para baixo)
        offset_y_esquerda = 40
        for i in range(7):
            y = self.altura - 130 - altura_img - i * ((self.altura - 160 - altura_img) // 6) + offset_y_esquerda
            posicoes.append((margem, y))

        # Associa os 27 estados às posições
        for (nome_estado, caminho_img), (x, y) in zip(estados.caminhos_mapas.items(), posicoes):
            imagem = pygame.image.load(funcoes.resource_path(caminho_img)).convert_alpha()
            imagem_escalada = pygame.transform.scale(imagem, (largura_img, altura_img))
            rect = imagem_escalada.get_rect(topleft=(x, y))

            self.blocos_estados.append({
                "nome": nome_estado,
                "img": imagem_escalada,
                "rect": rect
            })

    def gerenciar_eventos(self, evento):

        if self.personagem.rect.colliderect(self.botao_skip_rect):
            if not self.clicou_ficar:
                self.confirmacao_fase1 = True #mostra pop se ele subir no botão e não tiver clicado em ficar
        else:
            self.clicou_ficar = False #deixa o botão ficar como não clicado
            self.confirmacao_fase1 = False #o pop-up não aparece se ele sair de cima do botão
            
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = evento.pos
            if self.botao_sair_rect.collidepoint(pos_mouse):
                self.mudar_fase = True
            elif self.botao_continuar_rect.collidepoint(pos_mouse):
                self.clicou_ficar = True #Não mostra o pop-up mesmo o personagem estando em cima do botao
                self.confirmacao_fase1 = False #esconde pop-up

    def atualizar(self):
        teclas = pygame.key.get_pressed()
        self.personagem.mover(teclas)
        self.todas_sprites.update()

        self.estado_atual_colisao = None
        for estado in self.blocos_estados:
            if self.personagem.rect.colliderect(estado["rect"]):
                self.estado_atual_colisao = estado["nome"]
                break

        if self.mudar_fase:
            return "FASE1"

        return "GAME"

    def desenhar(self, tela):
        tela.blit(self.fundo_img, (0,0))

        # Desenha o mapa de estados
        for estado in self.blocos_estados:
            if self.estado_atual_colisao == estado["nome"]:
                pygame.draw.rect(tela, config.amarelo, estado["rect"].inflate(6, 6), width=3, border_radius=4)

            tela.blit(estado["img"], estado["rect"])
            texto = self.fonte_escrita.render(estado["nome"], True, config.preto)
            texto_rect = texto.get_rect(centerx=estado["rect"].centerx, top=estado["rect"].bottom + 2)
            tela.blit(texto, texto_rect)

        tela.blit(self.botao_skip, self.botao_skip_rect)

        self.todas_sprites.draw(tela)
        if self.estado_atual_colisao:
            self.desenhar_popup(tela)

        if self.confirmacao_fase1:
            tela.blit(self.janela_skip, self.janela_skip_rect)
            tela.blit(self.botao_sair, self.botao_sair_rect)
            tela.blit(self.botao_continuar, self.botao_continuar_rect)

        if self.intro_estado != "FIM":
            self.intro_estado, self.tempo_inicio_espera = funcoes.animacao(
                self.intro_estado, self.intro_rect, self.alvo_y, self.duracao_espera, self.tempo_inicio_espera
            )
            tela.blit(self.intro_img, self.intro_rect)

    def desenhar_popup(self, tela):
        popup_rect = pygame.Rect(0, 0, 1020, 600)
        popup_rect.center = (self.largura // 2, self.altura // 2)

        pygame.draw.rect(tela, config.bege, popup_rect, border_radius=15)
        pygame.draw.rect(tela, config.amarelo, popup_rect, width=4, border_radius=15)
        titulo = self.fonte_popup.render(f"Estado: {self.estado_atual_colisao}", True, config.preto)

        tela.blit(titulo, (popup_rect.x + 20, popup_rect.y + 20))
        
        texto_curiosidade = self.curiosidades_estados.get(self.estado_atual_colisao, "Curiosidade não encontrada.")
        largura_maxima = popup_rect.width - 40
        linhas = funcoes.formatar_texto_largura(texto_curiosidade, self.fonte_curiosidades, largura_maxima)

        pos_y_linha = popup_rect.y + 55
        for i in range(len(linhas)):
            linha_renderizada = self.fonte_curiosidades.render(linhas[i], True, config.preto)
            tela.blit(linha_renderizada, (popup_rect.x + 20, pos_y_linha))
            pos_y_linha += 22